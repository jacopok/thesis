from .lgwa_nested_sampling import from_bilby, LunarLikelihood
import numpy as np

import cProfile
import pstats

def profile(func, *args, **kwargs):
    
    with cProfile.Profile() as pr:
        func(*args, **kwargs)
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    return stats

if __name__ == '__main__':

    total_mass = 2.8
    distance = 40
    t0_moon = 1187008882.4
    q = 0.9

    injection_params = {
        'chirp_mass': total_mass * q**(3/5) * (1 + q)**(-6/5), 
        'mass_ratio': q,
        'luminosity_distance': distance,
        'theta_jn': 2.545065595974997,
        'psi': np.pi/2,
        'phase': np.pi,
        'ra': 3.4461599999999994,
        'dec': -0.4080839999999999,
        'time_at_center': t0_moon,
        'chi_1': 0.,
        'chi_2': 0.,
        'lambda_1': 400.,
        'lambda_2': 400.
    }

    like = LunarLikelihood()
    like.compute_center(t0_moon)
    
    freq = np.geomspace(1e-1, 3, num=2048)
    
    like.make_relbin_data(freq, from_bilby(injection_params))
    
    par = from_bilby(injection_params)
    
    like.relbin_log_likelihood_ratio(par)
    stats = profile(like.relbin_log_likelihood_ratio, par)
    stats.dump_stats('likelihood_512.prof')

    