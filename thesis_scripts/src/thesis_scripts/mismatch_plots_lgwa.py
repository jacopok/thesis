from GWFish.modules.detection import projection, Network
from GWFish.modules.waveforms import LALFD_Waveform
from scipy.integrate import trapezoid
from tqdm import tqdm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

import cartopy.crs as ccrs

from . import data_path

def mismatch(proj_1, proj_2, psd, f):
    
    norm_1 = trapezoid(abs(proj_1)**2 / psd, x=f)
    norm_2 = trapezoid(abs(proj_2)**2 / psd, x=f)
    return trapezoid(proj_1 * np.conj(proj_2) / psd, x=f).real / np.sqrt(norm_1 * norm_2)

norm = Normalize(vmin=-1, vmax=1)
cmap = plt.get_cmap('bwr')


def mismatch_plot(params, network, ra_lims, dec_lims, n_grid=80, mollweide=False, shift_center=True, n_f=2000, cache_name=None, rad=False):

    detector = network.detectors[0]
    detector.frequencyvector = np.geomspace(
        detector.frequencyvector[0, 0], 
        detector.frequencyvector[-1, 0], 
        num=n_f)[:, np.newaxis]
    f = np.squeeze(detector.frequencyvector)
    data_params = {
        'frequencyvector': f,
        'f_ref': 50.
    }
    waveform_obj = LALFD_Waveform('IMRPhenomD_NRTidalv2', params, data_params)
    wave = waveform_obj()
    t_of_f = waveform_obj.t_of_f
    if shift_center:
        center = network.coordinate_center(params)
    else:
        center = np.array([0, 0, 0])

    proj_baseline = projection(params, detector, wave, t_of_f, center)
    psd = detector.components[0].Sn(f)

    ra_range = np.deg2rad(np.linspace(*ra_lims, num=n_grid))
    dec_range = np.deg2rad(np.linspace(*dec_lims, num=n_grid))

    RA, DEC = np.meshgrid(ra_range, dec_range)
    
    results = []
    if cache_name is not None:
        file_path = (data_path / cache_name).with_suffix('.npy')
        if file_path.exists():
            results = np.load(file_path)
    
    if len(results) == 0:
        for ra, dec in tqdm(zip(RA.flatten(), DEC.flatten()), total=n_grid**2):
            new_params = params.copy()
            new_params['ra'] = ra
            new_params['dec'] = dec
            proj_new = projection(new_params, detector, wave, t_of_f, center)
            results.append(mismatch(proj_new[:, 0], proj_baseline[:, 0], psd=psd, f=f))
        results = np.reshape(results, (n_grid, n_grid))
        if cache_name is not None:
            np.save(file_path, results)

    fig = plt.figure(figsize=(16*.8, 9*.8))
    if mollweide:
        ax = fig.add_subplot(111, projection=ccrs.Mollweide())
        contour_kwargs = {'transform': ccrs.PlateCarree()}
    else:
        ax = fig.add_subplot(111)
        contour_kwargs = {}

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
    
    plt.colorbar(ScalarMappable(cmap=cmap, norm=norm), ax=ax, label='$h_+$ overlap')
    
    # ax.set_title(f'GW170817 with LGWA')
    plt.tight_layout()


def make_all_plots():
    
    total_mass = 2.8
    distance = 20
    t0_moon = 1187008882.4

    params = {
        'chirp_mass': total_mass / 2**(6/5), 
        'mass_ratio': 0.9,
        'luminosity_distance': distance,
        'theta_jn': 2.545065595974997,
        'psi': np.pi/2,
        'phase': np.pi,
        'ra': 3.4461599999999994,
        'dec': -0.4080839999999999,
        'geocent_time': t0_moon,
    }
    
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
    
    total_mass = 10
    distance = 200
    t0_moon = 1187008882.4

    params = {
        'chirp_mass': total_mass / 2**(6/5), 
        'mass_ratio': 0.9,
        'luminosity_distance': distance,
        'theta_jn': 2.545065595974997,
        'psi': np.pi/2,
        'phase': np.pi,
        'ra': 3.4461599999999994,
        'dec': -0.4080839999999999,
        'geocent_time': t0_moon,
    }
    
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
        n_grid=50,
        **fig_args
    )
    post_bbh  = pd.read_csv(Path(__file__).parent / 'bbh' / 'chains' / 'equal_weighted_post.txt', sep=' ')
    plt.scatter(np.rad2deg(post_bbh['ra']), np.rad2deg(post_bbh['dec']), s=1, alpha=.5)
    plt.show()