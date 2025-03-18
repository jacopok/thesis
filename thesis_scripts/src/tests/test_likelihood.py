import numpy as np
from thesis_scripts.lgwa_nested_sampling import from_bilby
from thesis_scripts.lgwa_likelihood import LunarLikelihood
import pytest


@pytest.fixture
def injection():
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
    return from_bilby(injection_params)

def test_grid_refine_grid(injection):
    like = LunarLikelihood()
    f = np.linspace(1e-1, 2e-1, num=101)
    like.make_relbin_data(f, injection)
    
    new_f = np.sqrt(f[51]*f[50])
    f2 = np.insert(f, 51, new_f)
    
    like.add_relbin_frequency(50)
    
    data_after_insertion = like.relbin_summary_data.copy()
    
    like2 = LunarLikelihood()
    like2.make_relbin_data(f2, injection)
    
    # breakpoint()
    # it seems like the whole array is modified - weird!
    
    assert np.allclose(like.relbin_summary_data, like2.relbin_summary_data)
    assert np.allclose(like.relbin_frequencies, like2.relbin_frequencies)
    assert np.allclose(like.h0_bin, like2.h0_bin)
