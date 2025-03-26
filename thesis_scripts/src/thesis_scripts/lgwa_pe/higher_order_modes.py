from .lgwa_nested_sampling import from_bilby, ensure_float
from .lgwa_likelihood import time_to_merger, LunarLikelihood
from .. import data_path, plotting
import numpy as np
import matplotlib.pyplot as plt
import yaml
import EOBRun_module
from functools import partial

from .simple_bns_waveforms import time_to_merger_simple, time_to_merger_simple_inverse, SUN_MASS_SECONDS
from numdifftools import Derivative

# Msun**2 / Mpc in seconds, i.e. multiplied by G**2 / c**5
TEOB_PREFACTOR = 2.35705224e-25

def modes_to_k(modes: list[tuple[int, int]]) -> list[int]:
    """TEOBResumS-specific function for converting
    a list of modes expressed as (l, m) into a list of single
    integers k.
    """
    return [int(x[0] * (x[0] - 1) / 2 + x[1] - 2) for x in modes]

def from_bilby_to_teob(parameter_dict):
    
    
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

def get_teob_modes(freq, params, modes):
    
    q = params['mass_ratio']
    eta = q / (1+q)**2
    total_mass = params['chirp_mass'] / eta**(3/5)
    dist = ensure_float(params["luminosity_distance"])

    teob_params = {
        "M": ensure_float(total_mass),
        "q": ensure_float(q),
        "chi1": ensure_float(params["chi_1"]),
        "chi2": ensure_float(params["chi_2"]),
        "coalescence_angle": ensure_float(params['phase']),
        "use_geometric_units": "no",
        "distance": dist,
        "inclination": ensure_float(params["theta_jn"]),
        "interp_freqs": "yes",
        "freqs": list(freq),
        "use_mode_lm": modes_to_k(modes),
        # "output_multipoles": "yes",
        # "output_lm": modes_to_k(modes),
        "model": "Giotto",
            # Initial conditions and output time grid
        'initial_frequency'  : float(freq[0]),    # in Hz if use_geometric_units = "no", else in geometric units
        'domain'             : 1,
        'srate_interp'       : float(freq[-1]*2),  # srate at which to interpolate, fixes f_max in 'FD' too
        # 'df': 1./8.,
        'interp_uniform_grid': 'no',
        # Modes
        'use_mode_lm'        : modes_to_k(modes),      # List of modes to use/output through EOBRunPy
        'model'              : "Giotto",
        # Output parameters
        'arg_out'            : "yes",      # Request multipoles and dynamics as output of the function call. Default is "no". Allowed values: ["no","yes"].
        'time_shift_FD': "yes",
        'ode_tmax': 1e11,
        'ode_reltol': 1e-13,
    }

    f, hp_re, hp_im, hc_re, hc_im, hflm, htlm, dyn = EOBRun_module.EOBRunPy(teob_params)
    amp, phase = hflm[str(modes_to_k(modes)[0])]
    pre = eta * total_mass ** 2 / dist * TEOB_PREFACTOR
    # tmax = dyn["t"][-1]
    # tmax = -time_to_merger_simple(freq[0], params['chirp_mass']*SUN_MASS_SECONDS)
    return amp * pre, phase

def make_gw150914_modes_plot(mass_scale = 1):
    with open(data_path / 'gw150914_lgwa_median.yaml') as f:
        injection_params = yaml.safe_load(f)

    injection_params['chirp_mass'] *= mass_scale
    injection_params['luminosity_distance'] *= mass_scale
    like = LunarLikelihood()
    f = np.geomspace(2.5e-2, 3, num=10000)
    
    palette = iter([
        '#882255',
        '#AA4499',
        '#CC6677',
        '#DDCC77',
        '#88CCEE',
    ])
    
    for mode in [
        (2, 2), 
        (2, 1), 
        (3, 3),
        (4, 4),
        (5, 5),
    ]:
        like.amp_phase = partial(get_teob_modes, modes=[mode])

        hx, hy = like.projected_waveform(f, from_bilby(injection_params), parameters_for_amp_phase=injection_params)
        c=next(palette)
        plt.loglog(f, 2*f*abs(hx), lw=3, c=c, label=f'{mode} mode')
        plt.loglog(f, 2*f*abs(hy), lw=1, c=c)

    plt.loglog(f, np.sqrt(f*like.psd(f)), c='grey', lw=3, label='PSD')

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Characteristic strain')
    plt.legend()

    plotting.add_time_to_merger_axis(plt.gca(), injection_params['chirp_mass'])
    
if __name__ == '__main__':
    make_gw150914_modes_plot(200)
    plt.show()