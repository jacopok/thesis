import numpy as np
from scipy.stats import gaussian_kde

def area_from_samples(ra_samples, dec_samples, n_grid=200, percentile=90):
    ra_grid = np.linspace(min(ra_samples), max(ra_samples), n_grid)
    dec_grid = np.linspace(min(dec_samples), max(dec_samples), n_grid)
    
    RA, DEC = np.meshgrid(ra_grid, dec_grid)
    
    ra_spacing = ra_grid[1] - ra_grid[0]
    dec_spacing = dec_grid[1] - dec_grid[0]
    
    kernel = gaussian_kde((ra_samples, dec_samples))
    probdensity = kernel(np.vstack([RA.ravel(), DEC.ravel()])) / np.sin(DEC.ravel())
    
    areas = np.sin(DEC.ravel()) * ra_spacing * dec_spacing
    
    idx = np.argsort(probdensity)[::-1]
    idx_percentile = np.searchsorted(
        np.cumsum(probdensity[idx] * areas[idx]) 
        / np.sum(areas*probdensity), 
        percentile/100)
    # normalize total probability to 1
    # if the sample size is not large enough, numerical inaccuracy will make it slightly different
    
    return np.sum(areas[idx[:idx_percentile]])

def gaussian_area_from_samples(ra_samples, dec_samples, percentile=90):

    cov = np.cov(np.vstack((ra_samples, dec_samples)))
    
    prefactor = abs(np.sin(np.average(dec_samples))) * (-2*np.pi) * np.log(1-percentile/100)
    
    # breakpoint()
    return prefactor * np.sqrt(cov[0, 0]*cov[1, 1] -cov[0, 1]**2)