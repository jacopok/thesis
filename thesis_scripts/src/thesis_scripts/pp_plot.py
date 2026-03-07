from scipy import stats

def ks_test(indices, nlive, mode="D+"):
    """
    Compute the two-sided KS test for discrete insertion indices for a given
    number of live points

    Parameters
    ----------
    mode : str
        Method for computing the KS statistic. If D+, the statistic is the
        maximum positive difference between the empirical and assumed CDF.
        If D-, the statistic is the maximum negative difference.

    Returns
    -------
    D : float
        Two-sided KS statistic
    p : float
        p-value
    """

    counts = np.zeros(nlive)
    u, c = np.unique(indices, return_counts=True)
    counts[u] = c
    cdf = np.cumsum(counts) / len(indices)
    if mode == "D+":
        D = np.max(np.arange(1.0, nlive + 1) / nlive - cdf)
    elif mode == "D-":
        D = np.max(cdf - np.arange(0.0, nlive) / nlive)
    else:
        raise RuntimeError(f"{mode} is not a valid mode. Choose D+ or D-")
    p = stats.ksone.sf(D, len(indices))
    return D, p



def pp_plot(uniform_variates, ax):


    D, p_value = ks_test(indices, nlive, mode=ks_test_mode)

    # First bin should have non-zero probability since this is a p.m.f
    x = np.arange(1.0, nlive + 1, 1)
    analytic_cmf = x / x[-1]
    counts = np.bincount(indices, minlength=nlive)
    estimated_cmf = np.cumsum(counts) / len(indices)

    if plot_breakdown:
        n_cols = 3
        figsize = (15, 5)
    else:
        n_cols = 2
        figsize = (10, 5)

    fig, ax = plt.subplots(1, ncols=n_cols, figsize=figsize)
    nbins = min(len(np.histogram_bin_edges(indices, "auto")) - 1, 1000)

    # Plot the analytic p.m.f first
    ax[0].axhline(
        1 / nlive,
        color="black",
        linestyle="-",
        label="pmf",
        alpha=0.5,
    )
    # 1-sigma regions
    ax[0].axhline(
        (1 + (nbins / len(indices)) ** 0.5) / nlive,
        color="black",
        linestyle=":",
        alpha=0.5,
        label="1-sigma",
    )
    ax[0].axhline(
        (1 - (nbins / len(indices)) ** 0.5) / nlive,
        color="black",
        linestyle=":",
        alpha=0.5,
    )

    ax[0].hist(
        indices,
        density=True,
        color="C0",
        histtype="step",
        bins=nbins,
        label="Estimated",
        range=(0, nlive - 1),
    )

    # Subtract 1 since we count indices from 0
    ax[1].plot(
        x - 1,
        analytic_cmf - estimated_cmf,
        c="C0",
        label="Analytic cmf - Estimated cmf",
    )
    n_indices = len(indices)
    for ci in confidence_intervals:
        bound = (1 - ci) / 2
        bound_values = (
            stats.binom.ppf(1 - bound, n_indices, analytic_cmf) / n_indices
        )
        lower = bound_values - analytic_cmf
        upper = analytic_cmf - bound_values

        ax[1].fill_between(x - 1, lower, upper, color="grey", alpha=0.2)

    ax[0].legend(loc="lower right")
    ax[0].set_xlim([0, nlive - 1])
    ax[0].set_xlabel("Insertion index")

    ax[1].legend(loc="lower right")
    ax[1].set_xlim([0, nlive - 1])
    ax[1].set_xlabel("Insertion index")

    return ax