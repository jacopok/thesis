from .lgwa_nested_sampling import run_pe, run_mcmc, make_analysis_functions, from_bilby
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

    
    for n_months in range(1, 13):
        with open(data_path / 'gw150914_lgwa_median.yaml') as f:
            injection_params = yaml.safe_load(f)
    
        folder_name = f'gw150914_median_mbm_{n_months}'
        prior_file = data_path / folder_name / 'priors.txt.prior'
        
        prior_dict = BNSPriorDict()
            
        prior_dict['lambda_1'] = DeltaFunction(injection_params['lambda_1'], name='lambda_1')
        prior_dict['lambda_2'] = DeltaFunction(injection_params['lambda_2'], name='lambda_2')
        prior_dict['chi_1'] = DeltaFunction(injection_params['chi_1'], name='chi_1')
        prior_dict['chi_2'] = DeltaFunction(injection_params['chi_2'], name='chi_2')
        prior_dict['chirp_mass'] = DeltaFunction(injection_params['chirp_mass'], name='chirp_mass')
        prior_dict['mass_ratio'] = DeltaFunction(injection_params['mass_ratio'], name='mass_ratio')
        prior_dict['time_at_center'] = Uniform(injection_params['time_at_center']-1e4, injection_params['time_at_center']+1e4, name='time_at_center', latex_label='$t$', unit='s')
        
        prior_dict['mass_1'] = Constraint(minimum=5, maximum=200, name='mass_1', latex_label='$m_1$', unit=None)
        prior_dict['mass_2'] = Constraint(minimum=5, maximum=200, name='mass_2', latex_label='$m_2$', unit=None)
        # prior_dict['mass_ratio'] = UniformInComponentsMassRatio(minimum=0.125, maximum=1, name='mass_ratio', latex_label='$q$', unit=None, boundary=None, equal_mass=False)
        # prior_dict['chirp_mass'] = UniformInComponentsChirpMass(minimum=4.4, maximum=100, name='chirp_mass', latex_label='$\\mathcal{M}$', unit=None, boundary=None)
        
        prior_dict['luminosity_distance'] = UniformSourceFrame(minimum=0.5, maximum=5000.0, cosmology='Planck15', name='luminosity_distance', latex_label='$d_L$', unit='Mpc', boundary=None)
        
        like = LunarLikelihood()
        f = np.geomspace(1e-2, 3, num=20000)
        amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
        t = time_to_merger(f, phase)

        hx, hy = like.projected_waveform(f, from_bilby(injection_params))
        plt.loglog(f, 2*f*abs(hx))
        plt.loglog(f, 2*f*abs(hy))
        plt.loglog(f, np.sqrt(f*like.psd(f)), lw=.5, c='gray')
        
        t0 = -3600*24*365.25
        month = 3600*24*365.25 / 12
        i0 = np.searchsorted(t, t0)
        i1 = np.searchsorted(t, t0+month*n_months)

        important_times = {
            # 'minute': 60,
            # 'hour': 3600,
            # 'day': 3600*24,
            # 'month': 3600*24*29.5,
            'final freq': -t0-month*n_months,
            'initial_freq': -t0,
        }
        for name, seconds in important_times.items():
            
            idx = np.searchsorted(t, -seconds)
            plt.axvline(f[idx], color='k', linestyle='--', label=name)

        plt.legend()
        
        
        snr = like.optimal_snr(f[i0:i1], from_bilby(injection_params))
        total_snr = like.optimal_snr(f[i0:-1], from_bilby(injection_params))
        injection_params['luminosity_distance'] = float(injection_params['luminosity_distance']*(snr/total_snr))
        
        
        loglike, prior_transform, inverse_prior_transform, log_dir, param_names = make_analysis_functions(injection_parameters=injection_params, folder_name=folder_name, priors=prior_dict, freq=f[i0:i1])
        np.save(log_dir / 'frequency_grid.npy', f[i0:i1])
        with open(log_dir / 'injection_parameters.yaml', 'w') as param_file:
            yaml.dump(
                injection_params, 
                param_file)
        new_snr = like.optimal_snr(f[i0:i1], from_bilby(injection_params))
        plt.title(f'dist: {injection_params["luminosity_distance"]:.1f}Mpc, SNR = {new_snr:.1f}')
        plt.xlim(f[i0]*0.9, f[-1])
        plt.savefig(data_path / folder_name / 'integration_range.png')
        plt.close()
        
        run_mcmc(loglike, prior_transform, inverse_prior_transform, log_dir, param_names, injection_params, n_chain=100_000)