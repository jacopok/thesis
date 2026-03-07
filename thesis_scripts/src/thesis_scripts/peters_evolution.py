from __future__ import annotations
from abc import ABC, abstractmethod
import warnings
from typing import Tuple, Union, Type, Optional
import numpy as np
import matplotlib.pyplot as plt  # type: ignore
from dataclasses import dataclass
from copy import deepcopy
import logging
import pandas as pd
from tqdm import tqdm

from . import data_path

# from numba import njit  # type: ignore

from scipy.integrate import solve_ivp

# for demo of what removing njit does
# replace it with the identity decorator
# def njit(func):
#     return func
import numpy as np

parsec = 3.08568e18
msun = 1.98892e33  # msun/g
G = 6.6743015e-8  # gravity constant cgs
c = 2.99792458e10  # speed of light cgs
c5 = c * c * c * c * c
G3 = G * G * G
yr = 3.1557600e7  # yr/seconds
Myr = 1e6 * yr
day = 86400.0



# @njit
def evolution_derivatives_gw(
    a: float, e: float, m1: float, m2: float, 
) -> Tuple[float, float]:
    """Contribution to binary evolution
    from energy loss due to GW emission

    Args:
        m1 (float): primary mass (cgs units)
        m2 (float): secondary mass (cgs units)
        a (float): semimajor axis (cgs units)
        e (float): eccentricity (cgs units)

    Returns:
        (a_dot, e_dot) (Tuple[float, float]): semimajor axis and eccentricity derivatives
    """
    return (
        -64.0
        / 5.0
        * G3
        * m1
        * m2
        * (m1 + m2)
        / (c5 * a**3 * (1 - e**2) ** 3.5)
        * (1.0 + 73.0 / 24.0 * e**2 + 37.0 / 96.0 * e**4),
        -304.0
        / 15.0
        * e
        * G3
        * m1
        * m2
        * (m1 + m2)
        / (c5 * a**4 * (1 - e**2) ** 2.5)
        * (1.0 + 121.0 / 304.0 * e**2),
    )

def get_semimajor_axis(m1, m2, f):
    return (G * (m1+m2)*msun / 4 / np.pi**2 / f**2)**(1/3)

def get_frequency(m1, m2, a):
    return (G * (m1+m2)*msun / 4 / np.pi**2 / a**3)**(1/2)

def evolve_eccentricity_backward(m1, m2, f0, e0, max_t=12*30*24*3600):
    a0 = get_semimajor_axis(m1, m2, f0)
    
    def func(t, y, m1, m2):
        a, e = y
        return evolution_derivatives_gw(a, e, m1*msun, m2*msun)

    sol = solve_ivp(
        fun=func,
        t_span=(0, -max_t),
        t_eval=-np.geomspace(.001, max_t, num=10000),
        y0=[a0, e0],
        args=(m1, m2),
    )
    
    freq = get_frequency(m1, m2, sol.y[0])
    ecc = sol.y[1]
    time = sol.t
    
    return time, freq, ecc

def get_gw250114_samples():

    param_names = 'm1 m2 a1x a1y a1z a2x a2y a2z mc eta ra dec time phiorb incl psi distance Npts lnL p ps neff mtotal q chi_eff chi_p m1_source m2_source mc_source mtotal_source redshift eccentricity meanPerAno'.split(' ')

    gw250114_samples = pd.read_csv(data_path / 'TEOB-RIFT_extrinsic_posterior_samples_TEOB.dat', 
                                skiprows=1, 
                                sep=' ',
                                names = param_names)
    
    return gw250114_samples

def get_gw250114_eccentricity_extrapolation():
    
    fname = data_path / 'cache' / 'gw250114_eccentricity_extrapolation.npy'

    if fname.exists():
        freqs, lo, med, hi = np.load(fname)
    else:
        gw250114_samples = get_gw250114_samples()

        n_freq = 250
        freqs = np.geomspace(2e-2, 13.33, num=n_freq)
        eccentricities = np.empty((len(gw250114_samples), n_freq))
        for index, row in tqdm(gw250114_samples.iterrows()):

            time, f, e = evolve_eccentricity_backward(row['m1'], row['m2'], 13.33, row['eccentricity'])
            eccentricities[index] = np.interp(freqs, f[::-1], e[::-1])

        lo, med, hi = np.quantile(eccentricities, [.05, .5, .95], axis=0)
        
        save_data = np.vstack((freqs, lo, med, hi))
        np.save(fname.as_posix(), save_data)

    return freqs, lo, med, hi
