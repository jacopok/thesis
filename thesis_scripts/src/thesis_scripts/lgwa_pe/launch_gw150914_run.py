from .lgwa_nested_sampling import run_pe, make_analysis_functions, from_bilby
from .lgwa_likelihood import LunarLikelihood, time_to_merger
from bilby.gw.prior import (
    BNSPriorDict, 
    DeltaFunction, 
    Uniform, 
    UniformSourceFrame,
    Constraint,
    UniformInComponentsChirpMass,
    UniformInComponentsMassRatio
)
import numpy as np
import matplotlib.pyplot as plt
import yaml
from .. import data_path

if __name__ == '__main__':

    with open(data_path / 'gw150914_lgwa_median.yaml') as f:
        injection_params = yaml.safe_load(f)
    
    folder_name = 'gw150914_median_1yr'
    prior_file = data_path / folder_name / 'priors.txt.prior'
    
    prior_dict = BNSPriorDict()
        
    prior_dict['lambda_1'] = DeltaFunction(injection_params['lambda_1'], name='lambda_1')
    prior_dict['lambda_2'] = DeltaFunction(injection_params['lambda_2'], name='lambda_2')
    # prior_dict['chi_1'] = DeltaFunction(injection_params['chi_1'], name='chi_1')
    # prior_dict['chi_2'] = DeltaFunction(injection_params['chi_2'], name='chi_2')
    prior_dict['time_at_center'] = Uniform(injection_params['time_at_center']-1e4, injection_params['time_at_center']+1e4, name='time_at_center', latex_label='$t$', unit='s')
    
    prior_dict['mass_1'] = Constraint(minimum=5, maximum=200, name='mass_1', latex_label='$m_1$', unit=None)
    prior_dict['mass_2'] = Constraint(minimum=5, maximum=200, name='mass_2', latex_label='$m_2$', unit=None)
    prior_dict['mass_ratio'] = UniformInComponentsMassRatio(minimum=0.125, maximum=1, name='mass_ratio', latex_label='$q$', unit=None, boundary=None, equal_mass=False)
    prior_dict['chirp_mass'] = UniformInComponentsChirpMass(minimum=4.4, maximum=100, name='chirp_mass', latex_label='$\\mathcal{M}$', unit=None, boundary=None)
    
    prior_dict['luminosity_distance'] = UniformSourceFrame(minimum=10.0, maximum=5000.0, cosmology='Planck15', name='luminosity_distance', latex_label='$d_L$', unit='Mpc', boundary=None)
    
    like = LunarLikelihood()
    # like.compute_center(t0)
    f = np.geomspace(1e-2, 3, num=10000)
    amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
    time_to_merger = time_to_merger(f, phase)

    hx, hy = like.projected_waveform(f, from_bilby(injection_params))
    plt.loglog(f, abs(hx))
    plt.loglog(f, abs(hy))
    
    important_times = {
        # 'minute': 60,
        # 'hour': 3600,
        'day': 3600*24,
        'month': 3600*24*29.5,
        'year': 3600*24*365.25,
    }
    for name, seconds in important_times.items():
        
        idx = np.searchsorted(time_to_merger, -seconds)
        plt.axvline(f[idx], color='k', linestyle='--', label=name)

    plt.legend()
    plt.show()
    plt.close()
    f0 = f[np.searchsorted(time_to_merger, -important_times['year'])]
    freq = np.geomspace(f0, 3, num=5000)

    loglike, prior_transform, inverse_prior_transform, log_dir, param_names = make_analysis_functions(injection_parameters=injection_params, folder_name=folder_name, priors=prior_dict, freq=freq)

    print(param_names)
    
    # run_pe(loglike, prior_transform, inverse_prior_transform, log_dir, param_names, injection_params, n_live=500)
    
    # baseline_post_transformed = np.load(data_path / 'gw150914_median_1yr' / 'baseline_post.npy')
    # for i in range(11):
    #     plt.hist(baseline_post_transformed[:, i])
    #     plt.show()
    #     plt.close()
    from .explore_strange_posteriors import compare_mcmc_guess
    
    compare_mcmc_guess(data_path / folder_name, prior_transform, param_names, injection_params)