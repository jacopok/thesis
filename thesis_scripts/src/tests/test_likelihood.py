import numpy as np
from thesis_scripts.lgwa_nested_sampling import from_bilby
from thesis_scripts.lgwa_likelihood import LunarLikelihood


def test_likelihood_initialization():
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
    f = np.geomspace(2e-2, 3, num=100)

    like = LunarLikelihood()
    like.make_relbin_data(f, from_bilby(injection_params))