import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib import ticker

def plot_correlations(cov, symbols):
    n = len(symbols)

    sigmas = np.sqrt(np.diagonal(cov))
    correlations = cov / np.kron(sigmas, sigmas).reshape(n, n)

    cmap = plt.get_cmap('RdBu')
    normalization = Normalize(-1, 1)
    fig, axes = plt.subplots(figsize=(10, 6))
    axes.matshow(correlations, cmap=cmap, norm=normalization)
    for axis in [axes.xaxis, axes.yaxis]:
        axis.set_major_locator(ticker.FixedLocator(np.arange(n)))
        axis.set_major_formatter(ticker.FixedFormatter(symbols))
    plt.colorbar(ScalarMappable(cmap=cmap, norm=normalization), ax=axes)
    plt.show()

