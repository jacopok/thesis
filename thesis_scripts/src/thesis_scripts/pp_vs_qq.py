from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    rng = np.random.default_rng(seed=1)

    fig, axs = plt.subplots(1, 3)
    
    for _ in range(10):
        variates = rng.normal(loc=0.5, scale=1.5, size=50)
        x = np.linspace(min(variates), max(variates), num=1000)
        u = np.linspace(0, 1, num=1000)
        analytical_cdf = stats.norm().cdf(x)
        analytical_icdf = stats.norm().ppf(u)
    
        ecdf = stats.ecdf(variates).cdf.evaluate(x)
        eicdf = np.interp(u, ecdf, x)

        axs[0].plot(analytical_cdf, ecdf, c='#1E88E5', alpha=.5)
        axs[1].plot(analytical_icdf, eicdf, c='#1E88E5', alpha=.5)
        
        correct_variates = np.sort(rng.normal(size=50))
        
        axs[2].plot(correct_variates, np.sort(variates), alpha=.5, c='#1E88E5')

    axs[0].plot(u, u, lw=1, c='k', ls='--')
    axs[1].plot(x, x, lw=1, c='k', ls='--')
    axs[2].plot(x, x, lw=1, c='k', ls='--')
    
    axs[0].set_xlabel('Analytical CDF')
    axs[0].set_ylabel('Empirical CDF')

    axs[1].set_xlabel('Analytical inverse CDF')
    axs[1].set_ylabel('Empirical inverse CDF')

    axs[2].set_xlabel('Sorted variates from the correct distribution')
    axs[2].set_ylabel('Sorted variates from the empirical distribution')


    axs[0].set_title('pp plot')
    axs[1].set_title('qq plot')
    axs[2].set_title('Variates approach')
    plt.show()