from .lgwa_likelihood import LunarLikelihood
from .lgwa_nested_sampling import from_bilby

from ..plotting import plot_contours, add_time_to_merger_axis
from matplotlib import ticker
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
import pandas as pd
from ..plotting import make_arcmin_grid
from .. import data_path
import yaml
import numpy as np
import matplotlib.pyplot as plt
from .simple_bns_waveforms import time_to_merger_simple_inverse, SUN_MASS_SECONDS


from cmcrameri import cm

cmap_full = cm.devon

if __name__ == '__main__':
    
    run_folder = data_path / 'gw170817_median_1yr_ew_1mo'

    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())

    # post_ew = pd.read_csv(data_path / 'ew_gw170817_run' / 'chains' / 'equal_weighted_post.txt', sep=' ')
    post_full = pd.read_csv(run_folder / 'chains' / 'equal_weighted_post.txt', sep=' ')


    like = LunarLikelihood()
    like.compute_center(injection_params['time_at_center'])

    flo = time_to_merger_simple_inverse(-3600*24*365.25*1.2, injection_params['chirp_mass']*SUN_MASS_SECONDS)
    f1yr = time_to_merger_simple_inverse(-3600*24*365.25, injection_params['chirp_mass']*SUN_MASS_SECONDS)
    f1mo = time_to_merger_simple_inverse(-3600*24*29.5, injection_params['chirp_mass']*SUN_MASS_SECONDS)

    f = np.concatenate((
        np.geomspace(flo, f1yr, num=20000),
        np.geomspace(f1yr, f1mo, num=10000),
        np.geomspace(f1mo, 3, num=1000000),
    ))

    hx_0, hy_0 = like.projected_waveform(f, from_bilby(injection_params))

    ratios_to_plot = 50
    ratios = np.empty((2, ratios_to_plot, len(f)), dtype=complex)

    for i in range(ratios_to_plot):
        params = from_bilby(post_full.iloc[i].to_dict())
        hx, hy = like.projected_waveform(f, params)
        ratios[0, i, :] = hx/hx_0
        ratios[1, i, :] = hy/hy_0

    np.save(run_folder / 'ratios.npy', ratios)
    ratios = np.load(run_folder / 'ratios.npy')

    cmap = plt.get_cmap('Blues')

    phase_diffs = np.sort(
        np.unwrap(
            np.angle(ratios), 
            axis=1), 
        axis=1)

    fig, axs = plt.subplots(2, 1, sharex=True)

    for i in range(2):
    # for percentile in [.5, .9]:
            # i_1 = int(ratios_to_plot*percentile/2.)
            # i_2 = int(ratios_to_plot*(1-percentile/2.))
            # axs[i].fill_between(f, 
            #     phase_diffs[i, i_1],
            #     phase_diffs[i, i_2],
            #     color=cmap(percentile)
            # )
            # axs[i].plot(f,
            #     phase_diffs[i, i_1],
            #     c='black', lw=.5
            # )
            # axs[i].plot(f, 
            #     phase_diffs[i, i_2],
            #     c='black', lw=.5
            # )
        for j in range(phase_diffs.shape[1]):
            axs[i].plot(f, phase_diffs[i, j], lw=.5, c='black', alpha=.2)
        axs[i].set_xscale('log')

    axs[0].set_title('$x$ channel')
    axs[1].set_title('$y$ channel')
    for ax in axs:
        ax.axvline(f1yr, c='black', lw=1, ls='--')
        ax.axvline(f1mo, c='black', lw=1, ls='--')

    add_time_to_merger_axis(axs[0], injection_params['chirp_mass'])
    plt.show()