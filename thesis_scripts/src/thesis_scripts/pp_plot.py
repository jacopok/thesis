"""KS test and pp plot for uniform random variates.

Adapted from nessai, specifically 
https://github.com/mj-will/nessai/blob/main/src/nessai/plot.py
and
https://github.com/mj-will/nessai/blob/main/src/nessai/utils/indices.py.
"""

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import patheffects

white_stroke = [patheffects.withStroke(linewidth=4, foreground="w")]


def ks_test(u, mode="D+"):
    """
    Compute the two-sided KS test for random variates u in [0, 1].

    Parameters
    ----------
    mode : str
        Method for computing the KS statistic. If D+, the statistic is the
        maximum positive difference between the empirical and assumed CDF.
        If D-, the statistic is the maximum negative difference.

    Returns
    -------
    D : float
        One or two-sided KS statistic
    p : float
        p-value
    """

    N = len(u)
    x = np.arange(1.0, N + 1) / N
    theoretical_cdf = x
    cdf = stats.ecdf(u).cdf.evaluate(x)
    
    if mode == "D+":
        idx = np.argmax(cdf - theoretical_cdf)
        D = (cdf - theoretical_cdf)[idx]
        p = stats.ksone.sf(D, N)
        return D, p, idx
    elif mode == "D-":
        idx = np.argmax(theoretical_cdf - cdf)
        D = (theoretical_cdf - cdf)[idx]
        p = stats.ksone.sf(D, N)
        return -D, p, idx
    elif mode == "D":
        idx = np.argmax(abs(cdf - theoretical_cdf))
        D = abs(cdf - theoretical_cdf)[idx]
        p = stats.kstwo.sf(D, N)
        return D, p, idx

    else:
        raise RuntimeError(f"{mode} is not a valid mode. Choose D, D+ or D-")



def pp_plot(u, confidence_intervals = (.68, .95, .997), ks_test_labels='floating'):

    N = len(u)
    x = np.arange(1.0, N + 1) / N
    theoretical_cdf = x
    estimated_cdf = stats.ecdf(u).cdf.evaluate(x)

    fig, ax = plt.subplots(1, ncols=3, figsize=(8, 8/3))
    nbins = min(len(np.histogram_bin_edges(u, "auto")) - 1, 1000)

    # Plot the analytic p.m.f first
    ax[0].axhline(
        1,
        color="black",
        linestyle="-",
        label="Uniform distribution",
        alpha=0.5,
    )
    
    sigma = (nbins / N) ** 0.5
    for ci in confidence_intervals:
        bound = (1 - ci) / 2
        z_score = stats.norm.isf(bound)
        lower = np.ones_like(x) * (1-z_score*sigma)
        upper = np.ones_like(x) * (1+z_score*sigma)
        ax[0].fill_between(
            x, lower, upper, color="grey", alpha=0.2)

    ax[0].hist(
        u,
        density=True,
        color="C0",
        histtype="step",
        bins=nbins,
        label="Histogram of random variates",
        range=(0, 1),
    )
    
    ax[1].plot(
        x,
        theoretical_cdf ,
        c="C0",
        ls='--',
        label="Analytic cdf",
    )
    ax[1].plot(
        x,
        estimated_cdf,
        c="C0",
        label="Estimated cdf",
    )

    for ci in confidence_intervals:
        bound = (1 - ci) / 2
        bound_values = (
            stats.binom.ppf(1 - bound, N, theoretical_cdf) / N
        )
        lower = bound_values - theoretical_cdf
        upper = theoretical_cdf - bound_values

        ax[2].fill_between(x, lower, upper, color="grey", alpha=0.2)


    ax[2].plot(
        x,
        estimated_cdf - theoretical_cdf,
        c="C0",
        label="Analytic cdf - Estimated cdf",
    )

    for ci in confidence_intervals:
        bound = (1 - ci) / 2
        lower = (
            stats.binom.ppf(1 - bound, N, theoretical_cdf) / N
        )
        upper = (
            stats.binom.ppf(bound, N, theoretical_cdf) / N
        )

        ax[1].fill_between(x, lower, upper, color="grey", alpha=0.2)

    for mode in ['D+', 'D-']:
        D, p_value, idx = ks_test(u, mode=mode)

        ax[2].annotate(
            "",
            xytext=(x[idx], D), 
            xy=(x[idx], 0),
            arrowprops=dict(arrowstyle="->"),
        )
        
        if p_value < 0.0001:
            p_string = f'$p<10^{{-4}}$'
        elif p_value > 0.9999:
            p_string = f'$p>1-10^{{-4}}$'
        else:
            p_string = f'$p={p_value:.4f}$'

        label = f'K-S test, {mode} mode\n$D={abs(D):.3f}$\n{p_string}'

        if ks_test_labels == 'on_arrow':
            if x[idx] < 0.2:
                horizontalalignment = 'left'
            elif x[idx] > 0.8:
                horizontalalignment ='right'
            else:
                horizontalalignment = 'center'
            
            if mode == 'D+':
                verticalalignment = 'bottom'
            else:
                verticalalignment = 'top'
            
                
            ax[2].text(
                x[idx], D*1.1,
                label, 
                horizontalalignment=horizontalalignment,
                verticalalignment=verticalalignment,
            )
        elif ks_test_labels == 'floating':
            
            if mode == 'D+':
                y = 0.75
            else:
                y = 0.25
            
            ax[2].text(
                0.5, y,
                label, 
                transform=ax[2].transAxes,
                path_effects=white_stroke,
                horizontalalignment='center',
                verticalalignment='center',
            )
        

    for a in ax:
        # a.legend(loc="lower right")
        a.set_xlim([0, 1])
        a.set_xlabel("Uniform variates")

    return fig, ax