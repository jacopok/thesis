from scipy.integrate import trapezoid
from tqdm import tqdm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

from .lgwa_pe.lgwa_likelihood import LunarLikelihood
from .lgwa_pe.lgwa_nested_sampling import from_bilby
from .lgwa_pe.simple_bns_waveforms import time_to_merger_simple_inverse, SUN_MASS_SECONDS

import cartopy.crs as ccrs

from . import data_path



def mismatch_plot(params, freq, ra_lims, dec_lims, n_grid=80, mollweide=False, shift_center=True, n_f=2000, cache_name=None, rad=False, **fig_kwargs):

    like = LunarLikelihood()
    
    if shift_center:
        like.compute_center(params['time_at_center'])

    like.make_relbin_data(freq, from_bilby(params))

    ra_range = np.deg2rad(np.linspace(*ra_lims, num=n_grid))
    dec_range = np.deg2rad(np.linspace(*dec_lims, num=n_grid))

    RA, DEC = np.meshgrid(ra_range, dec_range)
    
    results = []
    if cache_name is not None:
        file_path = (data_path / cache_name).with_suffix('.npy')
        if file_path.exists():
            results = np.load(file_path)
            if results.shape[0] != n_grid:
                results = []
    
    if len(results) == 0:
        for ra, dec in tqdm(zip(RA.flatten(), DEC.flatten()), total=n_grid**2):
            new_params = params.copy()
            new_params['ra'] = ra
            new_params['dec'] = dec
            results.append(like.relbin_log_likelihood_ratio(from_bilby(new_params)))
        results = np.reshape(results, (n_grid, n_grid))
        if cache_name is not None:
            np.save(file_path, results)

    fig = plt.figure(**fig_kwargs)
    # fig = plt.figure(figsize=(16*.8, 9*.8))
    if mollweide:
        ax = fig.add_subplot(111, projection=ccrs.Mollweide())
        contour_kwargs = {'transform': ccrs.PlateCarree()}
    else:
        ax = fig.add_subplot(111)
        contour_kwargs = {}

    lmax = max(results.flatten())
    norm = Normalize(vmin=-lmax, vmax=lmax)
    cmap = plt.get_cmap('bwr')

    if rad:
        ax.contourf(RA, DEC, results, levels=100, cmap=cmap, norm=norm, **contour_kwargs)
        ax.scatter(params['ra'], params['dec'], c='black', marker='x', label='True value', **contour_kwargs)

    else:
        ax.contourf(np.rad2deg(RA), np.rad2deg(DEC), results, levels=100, cmap=cmap, norm=norm, **contour_kwargs)
        ax.scatter(np.rad2deg(params['ra']), np.rad2deg(params['dec']), c='black', marker='x', label='True value', **contour_kwargs)
        
        ax.set_xlabel('RA [deg]')
        ax.set_ylabel('DEC [deg]')
    
    if mollweide:
        ax.set_global()
    
    plt.colorbar(ScalarMappable(cmap=cmap, norm=norm), ax=ax, label='$\\log \\mathcal{L} - \\log \\mathcal{L}_{\\mathrm{noise}}$')
    
    plt.tight_layout()
    return ax

def make_all_plots():
    
    with open(data_path / 'gw170817_lgwa_median.yaml') as f:
        injection_params = yaml.safe_load(f)

    for i, total_mass in enumerate(np.geomspace(2, 10, num=50)):
        
        # if total_mass < 2.5: 
        #     radius = np.deg2rad(1.5)
        #     fig_args = {
        #         'ra_lims': (
        #             np.rad2deg(params['ra']-radius*16/9), 
        #             np.rad2deg(params['ra']+radius*16/9)
        #         ),
        #         'dec_lims': (
        #             np.rad2deg(params['dec']-radius), 
        #             np.rad2deg(params['dec']+radius)
        #         ),
        #         'mollweide': False
        #     }
        # elif total_mass < 10:
        #     radius = np.deg2rad(5)
        #     fig_args = {
        #         'ra_lims': (
        #             np.rad2deg(params['ra']-radius*16/9), 
        #             np.rad2deg(params['ra']+radius*16/9)
        #         ),
        #         'dec_lims': (
        #             np.rad2deg(params['dec']-radius), 
        #             np.rad2deg(params['dec']+radius)
        #         ),
        #         'mollweide': False
        #     }        
        # else:
        #     fig_args = {
        #         'ra_lims': (0, 360),
        #         'dec_lims': (-85, 85),
        #         'mollweide': True
        #     }
        radius = np.deg2rad(6)
        fig_args = {
            'ra_lims': (
                np.rad2deg(params['ra']-radius*16/9), 
                np.rad2deg(params['ra']+radius*16/9)
            ),
            'dec_lims': (
                np.rad2deg(params['dec']-radius), 
                np.rad2deg(params['dec']+radius)
            ),
            'mollweide': False
        }
    
        mismatch_plot(
            params|{'chirp_mass': total_mass / 2**(6/5)}, 
            Network(['LGWA']), 
            n_grid=300,
            **fig_args
        )
        plt.title(f'Total mass = {total_mass:.1f}')
        plt.savefig(f'Match_sky_plot_{i:03d}.png', dpi=200)
        plt.close()

    plt.show()
    

if __name__ == '__main__':
    # make_all_plots()
    import yaml
    
    with open(data_path / 'gw170817_lgwa_median.yaml') as f:
        params = yaml.safe_load(f)

    def fig_args(radius, params):
        return {
            'ra_lims': (
                np.rad2deg(params['ra']-radius), 
                np.rad2deg(params['ra']+radius)
            ),
            'dec_lims': (
                np.rad2deg(params['dec']-radius), 
                np.rad2deg(params['dec']+radius)
            ),
            'mollweide': False
        }
    fmin = time_to_merger_simple_inverse(-3600*24*365.25, params['chirp_mass']*SUN_MASS_SECONDS)
    
    mismatch_plot(
        params, 
        np.geomspace(fmin, 3, num=500), 
        n_grid=100, 
        # cache_name='cache/bns_recentered', 
        cache_name=None, 
        **fig_args(np.deg2rad(2), params))
    plt.show()
