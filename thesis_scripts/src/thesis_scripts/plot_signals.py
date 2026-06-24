import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings
from functools import partial
from scipy.interpolate import interp1d


T_20_HZ = 157.86933774
REF_FREQ = 20.
REF_MCHIRP = 1.2187707886145736

def make_time_to_merger_axis_secondary(mchirp, include_month=False):
    """ This function will create a secondary, "detached" axis
    on top of the image.
    """
    ax_time2 = plt.gca().secondary_xaxis('top', functions=(
        partial(time_to_merger, mchirp=mchirp), 
        partial(inverse_time_to_merger, mchirp=mchirp)
    ))
    ax_time2.set_xlabel('Time to merger')
    plt.gcf().subplots_adjust(top=0.75)

    # Offset the right spine of par2.  The ticks and label have already been
    # placed on the right by twinx above.
    ax_time2.spines["top"].set_position(('outward', 35.))
    # Having been created by twinx, par2 has its frame off, so the line of its
    # detached spine is invisible.  First, activate the frame but make the patch
    # and spines invisible.
    make_patch_spines_invisible(ax_time2)
    # Second, show the right spine.
    ax_time2.spines["top"].set_visible(True)
    
    subdivisions = {
        # 1e-3: 'millisecond',
        1.: 'second',
        60.: 'minute',
        3600.: 'hour',
        3600*24.: 'day',
        3600*24*365.24: 'year',
        1e3*3600*24*365.24: '$10^3$ years',
        1e6*3600*24*365.24: '$10^6$ years',
    }
    if include_month:
        subdivisions[3600*24*30.] = 'month'
    
    make_time_axis_fancy(ax_time2, subdivisions)

def make_time_to_merger_axis(mchirp, subdivisions=None):
    ax_time2 = plt.gca().secondary_xaxis('top', functions=(
        partial(time_to_merger, mchirp=mchirp), 
        partial(inverse_time_to_merger, mchirp=mchirp)
    ))
    ax_time2.set_xlabel('Time to merger')
    
    if subdivisions is None:
        subdivisions = {
            1.: 'second',
            60.: 'minute',
            3600.: 'hour',
            3600*24.: 'day',
            3600*24*365.24: 'year',
            1e3*3600*24*365.24: '$10^3$ years',
            1e6*3600*24*365.24: '$10^6$ years',
        }
        
    make_time_axis_fancy(ax_time2, subdivisions)

def time_to_merger(f, mchirp = REF_MCHIRP):
    # time in seconds, frequency in Hz, chirp mass in solar masses
    return T_20_HZ * (f / REF_FREQ)**(-8/3) * (mchirp / REF_MCHIRP)**(-5/3)

def inverse_time_to_merger(t, mchirp = REF_MCHIRP):
    return REF_FREQ * (t / T_20_HZ)**(-3/8) * (mchirp / REF_MCHIRP)**(-5/8)

def chirp_mass(m1, m2):
    return (m1*m2)**(3/5) / (m1 + m2)**(1/5)

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

