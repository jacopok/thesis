from .lgwa_nested_sampling import from_bilby
from .lgwa_likelihood import time_to_merger, LunarLikelihood
from .. import data_path
import numpy as np
import matplotlib.pyplot as plt
import yaml
import EOBRun_module

from .simple_bns_waveforms import time_to_merger_simple, time_to_merger_simple_inverse, SUN_MASS_SECONDS
from numdifftools import Derivative

def modes_to_k(modes: list[tuple[int, int]]) -> list[int]:
    """TEOBResumS-specific function for converting
    a list of modes expressed as (l, m) into a list of single
    integers k.
    """
    return [int(x[0] * (x[0] - 1) / 2 + x[1] - 2) for x in modes]

def from_bilby_to_teob(parameter_dict):
    
    res = {}
    
    # res['chirp_mass'] = parameter_dict['chirp_mass']
    res['q'] = parameter_dict['mass_ratio']
    
    q = res['q']
    eta = q / (1+q)**2
    total_mass = parameter_dict['chirp_mass'] / eta**(3/5)
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
    
    return res

def get_teob_modes(modes, freq, params):
    
    new_params = {
        "interp_freqs": "yes",
        "freqs": freq,
        "use_mode_lm": modes_to_k(modes),
        "output_multipoles": "yes",
        "output_lm": modes_to_k(modes),
    }
    
    t, hpfr, hpfi, hcfr, hcfi, hflm, dyn = EOBRun_module.EOBRunPy(params)



if __name__ == '__main__':
    with open(data_path / 'gw150914_lgwa_median.yaml') as f:
        injection_params = yaml.safe_load(f)

    like = LunarLikelihood()
    f = np.geomspace(1e-2, 3, num=2000)

    hx, hy = like.projected_waveform(f, from_bilby(injection_params))
    plt.loglog(f, 2*f*abs(hx))
    plt.loglog(f, 2*f*abs(hy))
    plt.loglog(f, np.sqrt(f*like.psd(f)))

    DAY = 3600*24.
    def forward(x):
        return -time_to_merger_simple(x, injection_params['chirp_mass']*SUN_MASS_SECONDS) / DAY

    def inverse(x):
        return time_to_merger_simple_inverse(-x*DAY, injection_params['chirp_mass']*SUN_MASS_SECONDS)

    secax = plt.gca().secondary_xaxis('top',
        functions=(forward, inverse),
        label='Time to merger [days]',
    )
    
    plt.show()
