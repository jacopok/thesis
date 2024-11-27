import numpy as np
import emcee
import dynesty
from time import perf_counter

def compare_methods(ndim):
    prior_width = 10
    def prior_transform(u):
        return prior_width * (u - .5)
    
    lnorm = -0.5 * (
        np.log(2 * np.pi) * ndim +
        np.log(ndim))
    
    def log_like(x):
        -0.5 * np.sum(x ** 2) + lnorm
        
    def log_post_unnormalized(x):
        return log_like(x) - np.log(prior_width)

    nwalkers = 100
    ivar = 1. / np.random.rand(ndim)
    p0 = np.random.randn(nwalkers, ndim)

    sampler_emcee = emcee.EnsembleSampler(nwalkers, ndim, log_post_unnormalized)
    t0 = perf_counter()
    sampler_emcee.run_mcmc(p0, ndim*5000, progress=True)
    tau = int(np.average(sampler_emcee.get_autocorr_time()))
    chain = sampler_emcee.get_chain(discard = 5*tau, thin=tau//2, flat=True)
    
    t1 = perf_counter()
    
if __name__ == '__main__':
    compare_methods(2)