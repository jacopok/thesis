from bilby.gw.prior import BNSPriorDict
from scipy.spatial import ConvexHull
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

from thesis_scripts import data_path
from thesis_scripts.postprocess import area_from_samples
import yaml

def compute_area_data():

    folder_base_name = 'gw150914_median_mbm_year_before'
    year = (1*u.yr).si.value
    month = year / 12 # seconds
    omega = (2*np.pi/u.yr).si.value # 2pi / yr in Hz

    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 8), gridspec_kw={'hspace':0.05})

    cmap = plt.get_cmap('magma')
    areas = []
    analysis_durations = []
    avg_freqs = []
    vertical_diffs = []
    posterior_areas = []

    for i in range(1, 13):

        folder = data_path / f'{folder_base_name}_{i}'

        freqs = np.load(folder / 'frequency_grid.npy')

        injection_params = yaml.safe_load((folder / 'injection_parameters.yaml').read_text())

        prior_file = folder / 'priors.txt.prior'
        
        prior_dict = BNSPriorDict({})
        prior_dict.from_file(prior_file)
        prior_dict._resolve_conditions()
        param_names = prior_dict.sorted_keys_without_fixed_parameters

        idx1 = param_names.index('ra')
        idx2 = param_names.index('dec')

        transformed_post = np.load(folder / 'baseline_post_transformed.npy')


        # cov = np.cov(transformed_post[:, [idx1, idx2]].T)
        # dec = injection_params['dec']
        
        # prefactor = abs(np.sin(dec)) * (-2*np.pi) * np.log(1-0.9)

        # posterior_areas.append(prefactor * np.sqrt(cov[0, 0]*cov[1, 1] -cov[0, 1]**2))

        posterior_areas.append(area_from_samples(
            transformed_post[:, idx1],
            transformed_post[:, idx2],
            percentile=90,
        ))

        times = injection_params['time_at_center'] + time_to_merger(
            injection_params['chirp_mass'],
            injection_params['mass_ratio'], 
            freqs
        )
        total_time = times[-1] - times[0]
        detector_motion = project(like.get_detector_position(times))
        vertical_diffs.append(np.linalg.norm(np.linalg.norm(like.get_detector_position(times) - deproject(*detector_motion), axis=0)) / AU)

        hull = ConvexHull(detector_motion.T / AU)
        areas.append(hull.volume)
        analysis_durations.append(total_time)
        avg_freqs.append(np.exp(np.average(np.log(freqs))))

    areas = np.array(areas)
    posterior_areas = np.array(posterior_areas)
    analysis_durations = np.array(analysis_durations)
    avg_freqs = np.array(avg_freqs)
    vertical_diffs = np.array(vertical_diffs)


axs[0].scatter(analysis_durations / month, areas, c=cmap(analysis_durations/month/13), label='Computed from detector motion')

all_times = np.linspace(0, year, num=1000)
axs[0].plot(all_times / month, .5 * (all_times*omega - np.sin(all_times * omega)), ls='--', c='black', label='Analytical prediction')

axs[1].scatter(analysis_durations/month, areas-.5 * (analysis_durations*omega - np.sin(analysis_durations * omega)), c=cmap(analysis_durations/month/13))
axs[2].scatter(analysis_durations/month, vertical_diffs, c=cmap(analysis_durations/month/13))

axs[0].legend()
axs[2].set_xlabel('Time [months]')
axs[0].set_ylabel('Area spanned [square AU]')
axs[1].set_ylabel('Prediction error [square AU]')
axs[2].set_ylabel('Out of plane RMS [AU]')
