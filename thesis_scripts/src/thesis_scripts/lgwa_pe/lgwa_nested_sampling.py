from .. import data_path
from .lgwa_likelihood import LunarLikelihood, time_to_merger
from .simple_bns_waveforms import compute_delta_lambda, compute_lambda_tilde
import numpy as np
import matplotlib.pyplot as plt

from bilby.gw.prior import BNSPriorDict, Uniform, UniformSourceFrame, PriorDict, DeltaFunction
import yaml

import emcee
from ultranest.hotstart import get_auxiliary_contbox_parameterization
import ultranest
import ultranest.stepsampler

def ensure_float(x):
    if isinstance(x, float):
        return x
    if isinstance(x, np.float64):
        return float(x)
    if x.shape == ():
        return x[()]
    if x.shape == (1,):
        return x[0]
    breakpoint()


def from_bilby(parameter_dict):
    
    res = {}
    
    res['chirp_mass'] = parameter_dict['chirp_mass']
    res['mass_ratio'] = parameter_dict['mass_ratio']
    
    q = res['mass_ratio']
    eta = q / (1+q)**2
    total_mass = res['chirp_mass'] / eta**(3/5)
    m1 = total_mass * q / (1+q)
    m2 = total_mass / (1+q)
    
    res['phase'] = parameter_dict['phase']
    res['luminosity_distance'] = parameter_dict['luminosity_distance']
    res['time_at_center'] = parameter_dict['time_at_center']
    
    res['right_ascension'] = float(parameter_dict['ra'])
    res['declination'] = float(parameter_dict['dec'])
    res['inclination'] = parameter_dict['theta_jn'] # this is not exactly true but it'll do for now
    res['polarization'] = parameter_dict['psi']
    res['spin_1z'] = parameter_dict['chi_1']
    res['spin_2z'] = parameter_dict['chi_2']
    res['lambda_eff'] = compute_lambda_tilde(m1, m2, parameter_dict['lambda_1'], parameter_dict['lambda_2'])
    res['d_lambda'] = compute_delta_lambda(m1, m2, parameter_dict['lambda_1'], parameter_dict['lambda_2'])
    
    return res

def make_analysis_functions(
    injection_parameters: dict, 
    folder_name: str, 
    priors: PriorDict,
    freq: np.ndarray,
    ):
    
    log_dir = data_path / folder_name
    log_dir.mkdir(parents=True, exist_ok=True)
    
    like = LunarLikelihood()
    like.compute_center(injection_parameters['time_at_center'])
    
    like.make_relbin_data(freq, from_bilby(injection_parameters))
    
    with open(log_dir / 'injection_parameters.yaml', 'w') as f:
        yaml.dump(
            injection_parameters, 
            f)
    
    priors.to_file(outdir=log_dir.as_posix(), label='priors.txt')

    prior_keys = set(priors.keys())
    prior_keys.remove('mass_1')
    prior_keys.remove('mass_2')
    
    if prior_keys != set(injection_parameters.keys()):
        print('Priors and injection parameters keys differ!')
        print(set(priors.keys()).difference(set(injection_parameters.keys())))
    
    param_names = priors.sorted_keys_without_fixed_parameters
    
    fixed_keys = priors.fixed_keys
    fixed_params = {key: injection_parameters[key] for key in fixed_keys}
    
    def loglike(par):
        param_dict = {
            name: par[i] for i, name in enumerate(param_names)
            } | fixed_params
        return like.relbin_log_likelihood_ratio(from_bilby(param_dict))
    
    def prior_transform(u):
        # list to list
        return priors.rescale(param_names, u)
    
    def inverse_prior_transform(par):
        # list to list
        
        param_dict = {name: par[i] for i, name in enumerate(param_names)}
        u_dict = priors.cdf(param_dict)
        return [ensure_float(u_dict[name]) for name in param_names]
    
    return loglike, prior_transform, inverse_prior_transform, log_dir, param_names

def run_pe(loglike, prior_transform, inverse_prior_transform, log_dir, param_names, injection_params, n_live=400, baseline_post_fname=None):
    
    baseline_post_fname = log_dir / 'baseline_post.npy'
        
    if baseline_post_fname.exists():
        baseline_post_transformed = np.load(baseline_post_fname)
    else:
        def log_prob(par):
            if np.any(par < 0) or np.any(par > 1):
                return -np.inf
            return loglike(prior_transform(par))
        
        mc_sampler = emcee.EnsembleSampler(50, len(param_names), log_prob)
        
        rng = np.random.default_rng(seed=1)
        u0 = np.asarray(inverse_prior_transform([injection_params[name] for name in param_names]))
        p0 = rng.normal(loc=0, scale=2e-9, size=(50, len(param_names))) + u0[np.newaxis, :]
        
        mc_sampler.run_mcmc(
            p0,
            10000,
            progress=True,
            skip_initial_state_check=True,
        )
        baseline_post_transformed = mc_sampler.get_chain(flat=True, thin=1, discard=1000)
        np.save(baseline_post_fname, baseline_post_transformed)

    nsamples = baseline_post_transformed.shape[0]
    weights = np.ones(nsamples) / nsamples
    
    aux_param_names, aux_loglike, aux_transform, vectorized = get_auxiliary_contbox_parameterization(
        param_names, 
        loglike, 
        prior_transform, 
        baseline_post_transformed, 
        uweights=weights,
        beta=1.
    )

    sampler = ultranest.ReactiveNestedSampler(
        aux_param_names,
        aux_loglike,
        aux_transform,
        # log_dir='ultranest_fast_run',
        log_dir=log_dir,
        resume='resume',
        # resume='overwrite',
        # warmstart_max_tau=0.1,
    )
    sampler.stepsampler = ultranest.stepsampler.SliceSampler(
        nsteps=128,
        generate_direction=ultranest.stepsampler.generate_mixture_random_direction,
    )
    
    for result in sampler.run_iter(min_num_live_points=n_live, frac_remain=1e-2):
        sampler.plot_run()
        sampler.plot_trace()

    return sampler, result


if __name__ == '__main__':
    import yaml

    with open(data_path / 'gw170817_lgwa_median.yaml') as f:
        injection_params = yaml.safe_load(f)

    prior_dict = BNSPriorDict()
    # prior_dict['lambda_1'] = DeltaFunction(injection_params['lambda_1'], name='lambda_1')
    # prior_dict['lambda_2'] = DeltaFunction(injection_params['lambda_2'], name='lambda_2')
    # prior_dict['chi_1'] = DeltaFunction(injection_params['chi_1'], name='chi_1')
    # prior_dict['chi_2'] = DeltaFunction(injection_params['chi_2'], name='chi_2')
    prior_dict['time_at_center'] = Uniform(injection_params['time_at_center']-1e4, injection_params['time_at_center']+1e4, name='time_at_center', latex_label='$t$', unit='s')
    prior_dict['luminosity_distance'] = UniformSourceFrame(minimum=10.0, maximum=5000.0, cosmology='Planck15', name='luminosity_distance', latex_label='$d_L$', unit='Mpc', boundary=None)
    sample = prior_dict.sample()
    
    like = LunarLikelihood()
    # like.compute_center(t0)
    f = np.geomspace(1e-1, 3, num=10000)
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

    loglike, prior_transform, inverse_prior_transform, log_dir, param_names = make_analysis_functions(injection_parameters=injection_params, folder_name='gw170817_median_1yr', priors=prior_dict, freq=freq)

    run_pe(loglike, prior_transform, inverse_prior_transform, log_dir, param_names, injection_params, n_live=500)

