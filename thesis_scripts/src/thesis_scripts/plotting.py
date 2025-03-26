from matplotlib import ticker

from matplotlib.projections.polar import ThetaFormatter
from matplotlib import ticker
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, gaussian_kde
from .lgwa_pe.simple_bns_waveforms import time_to_merger_simple, time_to_merger_simple_inverse, SUN_MASS_SECONDS

class MinuteFormatter(ThetaFormatter):
    """
    Used to format the *theta* tick labels.  
    """
    def __call__(self, x, pos=None):
        vmin, vmax = self.axis.get_view_interval()
        d = np.rad2deg(abs(vmax - vmin))

        angle_deg = np.rad2deg(x)
        angle_deg_int = np.floor(angle_deg)
        minutes = (angle_deg - angle_deg_int + 1e-6)*60
        
        return f"${angle_deg_int:.0f}^\circ${int(minutes)}'"


def make_arcmin_grid(ax, ra_lims, dec_lims):

    ax.set_xlim(*ra_lims)
    ax.set_ylim(*dec_lims)

    ax.xaxis.set_major_formatter(MinuteFormatter())
    ax.yaxis.set_major_formatter(MinuteFormatter())

    ax.xaxis.set_major_locator(ticker.FixedLocator(np.arange(int(np.rad2deg(ra_lims[0])*12), int(np.rad2deg(ra_lims[1])*12)+1) / (12*180/np.pi)))
    ax.yaxis.set_major_locator(ticker.FixedLocator(np.arange(int(np.rad2deg(dec_lims[0])*12), int(np.rad2deg(dec_lims[1])*12)+1)/ (12*180/np.pi)))

    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(int(np.rad2deg(ra_lims[0])*60), int(np.rad2deg(ra_lims[1])*60)+1) / (60*180/np.pi)))
    ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(int(np.rad2deg(dec_lims[0])*60), int(np.rad2deg(dec_lims[1])*60)+1)/ (60*180/np.pi)))


def plot_contours(x_points, y_points, ax, cmap='Blues', levels=[.5, .9], N=100, **kwargs):
    
    # good cmaps: sequentials (https://matplotlib.org/stable/_images/sphx_glr_colormaps_002_2_00x.png)
    
    points = np.vstack((x_points, y_points)).T
    
    if 'x' in kwargs:
        x = kwargs['x']
        assert len(x) == N
    else:
        x = np.linspace(min(x_points), max(x_points), num=N)

    if 'y' in kwargs:
        y = kwargs['y']
        assert len(y) == N
    else:
        y = np.linspace(min(y_points), max(y_points), num=N)
        
    X, Y = np.meshgrid(x, y)
    
    z = gaussian_kde(points.T)(np.vstack([X.ravel(), Y.ravel()])).reshape((N, N))
    z = z/z.max()
    
    sorted_probs = np.sort(z.flatten())[::-1]
    cumulative = np.cumsum(sorted_probs)
    cumulative /= cumulative[-1]
    
    contour_probs = np.zeros_like(levels)
    for i, level in enumerate(levels):
        try:
            contour_probs[i] = sorted_probs[cumulative <= level][-1]
        except IndexError:
            contour_probs[i] = sorted_probs[0]
    
    contour_probs = np.concatenate((contour_probs[::-1], [1]))
    assert np.all(np.diff(contour_probs) >= 0)
    
    ax.contourf(X, Y, z, cmap=cmap, levels=contour_probs, **kwargs)
    ax.contour(X, Y, z, levels=contour_probs, colors='black')
    
def add_time_to_merger_axis(ax, mchirp):
    DAY = 3600*24.
    def forward(x):
        return -time_to_merger_simple(x, injection_params['chirp_mass']*SUN_MASS_SECONDS) / DAY

    def inverse(x):
        return time_to_merger_simple_inverse(-x*DAY, injection_params['chirp_mass']*SUN_MASS_SECONDS)

    secax = ax.secondary_xaxis('top',
        functions=(forward, inverse),
    )
    secax.set_xlabel('Time to merger [days]')
    return secax