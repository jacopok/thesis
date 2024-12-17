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

from . import data_path

def fix_angles(angles):
    return (angles + np.pi)%(2 * np.pi) - np.pi

def phase_diffs(params, network, f, post, n_samples=100):

    param_names = ['chirp_mass', 'mass_ratio', 'luminosity_distance', 'theta_jn', 'psi', 'phase', 'ra', 'dec', 'geocent_time']
    true_params_array = [params[name] for name in param_names]

    detector = network.detectors[0]

    detector.frequencyvector = f
    data_params = {
        'frequencyvector': f,
        'f_ref': 50.
    }
    center = network.coordinate_center(params)

    base_waveform_obj = LALFD_Waveform('IMRPhenomD_NRTidalv2', params, data_params)
    base_wave = base_waveform_obj()
    t = base_waveform_obj.t_of_f
    def waveform_differences(param_vector):
        these_params = {name: param_vector[i] for i, name in enumerate(param_names)}
        waveform_obj = LALFD_Waveform('IMRPhenomD_NRTidalv2', these_params, data_params)
        wave = waveform_obj()
        t_of_f = waveform_obj.t_of_f
        
        proj = projection(these_params, detector, wave, t_of_f, center)

        return abs(proj[:, 0]) / abs(base_wave[:, 0]), np.unwrap(np.angle(proj[:, 0]) - np.angle(base_wave[:, 0]))
    
    _, baseline_differences_phase = waveform_differences(true_params_array)

    diffs = np.empty((n_samples, len(t)))

    for i in tqdm(range(n_samples)):
        amp_diff, phase_diff = waveform_differences(post.iloc[i])
        diffs[i] = fix_angles(phase_diff-baseline_differences_phase)

    diffs = np.sort(diffs, axis=0)
    return t, diffs, baseline_differences_phase
    
def phase_ppd(params, diffs, t, baseline_differences_phase):
    fig, axs = plt.subplots(2, 1, sharex=True, gridspec_kw={'hspace': 0}, figsize=(16, 9))

    cmap = plt.get_cmap('Blues')

    # diffs = fix_angles(diffs)
    n_samples = diffs.shape[0]
    n_t = len(t)
    days_to_seconds = 24*60*60

    for percentile in [.5, .9]:
        axs[0].fill_between(
            -(t-params['geocent_time']) / days_to_seconds, 
            diffs[int(n_samples*percentile/2)],
            diffs[int(n_samples*(1-percentile/2))],
            color=cmap(percentile),
        )
        axs[0].plot(
            -(t-params['geocent_time']) / days_to_seconds, 
            diffs[int(n_samples*percentile/2)],
            c='black',
            lw=.5
        )
        axs[0].plot(
            -(t-params['geocent_time']) / days_to_seconds, 
            diffs[int(n_samples*(1-percentile/2))],
            c='black',
            lw=.5
        )


    for ax in axs:
        for i in range(13):
            ax.axvline(i*30, c='black', ls='--', lw=.5)
        for i in range(11):
            ax.axvline(i*365.25, c='black', ls='--', lw=.5)

        ax.set_xscale('log')
    ax.set_xlim(*reversed(ax.get_xlim()))

    axs[1].plot(
        -(t-params['geocent_time']) / days_to_seconds, 
        baseline_differences_phase
    )
    axs[0].set_ylim(-0.5, 0.5)

    axs[0].axhline(0, c='white')

    # for ax in axs:
    #     ax.axvline(t_to_merger_days[np.searchsorted(f, 0.3)], c='red')

    axs[1].set_xlabel('Time to merger [days]')
    axs[0].set_ylabel('Phase error [rad]')
    axs[1].set_ylabel('Phase modulation [rad]')