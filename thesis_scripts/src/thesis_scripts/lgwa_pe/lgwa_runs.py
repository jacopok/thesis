from .lgwa_nested_sampling import run_pe, make_analysis_functions, LunarLikelihood, from_bilby
from bilby.gw.prior import BNSPriorDict, DeltaFunction, Uniform, UniformSourceFrame
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    total_mass = 36+29
    distance = 420.
    t0_moon = 1_126_224_017.4
    q = 36/29

    injection_params = {
        'chirp_mass': total_mass * q**(3/5) * (1 + q)**(-6/5), 
        'mass_ratio': 1/q,
        'luminosity_distance': distance,
        'theta_jn': 1.,
        'psi': 0.,
        'phase': 0.,
        'ra': np.deg2rad(-30),
        'dec': np.deg2rad(-75),
        'time_at_center': t0_moon,
        'chi_1': 0.,
        'chi_2': 0.,
        'lambda_1': 0.,
        'lambda_2': 0.
    }

    prior_dict = BNSPriorDict()
    prior_dict['lambda_1'] = DeltaFunction(injection_params['lambda_1'], name='lambda_1')
    prior_dict['lambda_2'] = DeltaFunction(injection_params['lambda_2'], name='lambda_2')
    # prior_dict['chi_1'] = DeltaFunction(injection_params['chi_1'], name='chi_1')
    # prior_dict['chi_2'] = DeltaFunction(injection_params['chi_2'], name='chi_2')
    prior_dict['time_at_center'] = Uniform(t0_moon-1e4, t0_moon+1e4, name='time_at_center', latex_label='$t$', unit='s')
    prior_dict['luminosity_distance'] = UniformSourceFrame(minimum=10.0, maximum=5000.0, cosmology='Planck15', name='luminosity_distance', latex_label='$d_L$', unit='Mpc', boundary=None)
    
    loglike, prior_transform, inverse_prior_transform, log_dir, param_names = make_analysis_functions(injection_parameters=injection_params, folder_name='bbh_test', priors=prior_dict, n_freqs=1000)

    # like = LunarLikelihood()
    # like.compute_center(t0_moon)
    # f = np.geomspace(1e-3, 3, num=1000)
    # hx, hy = like.projected_waveform(f, from_bilby(injection_params))
    # plt.loglog(f, abs(hx))
    # plt.loglog(f, abs(hy))
    # plt.show()

    run_pe(loglike, prior_transform, inverse_prior_transform, log_dir, param_names, injection_params)
