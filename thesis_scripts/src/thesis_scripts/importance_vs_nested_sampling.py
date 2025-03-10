import numpy as np
import emcee
import dynesty
from time import perf_counter
from scipy.stats import norm
from scipy.special import erfinv

import matplotlib.pyplot as plt

from dynesty import DynamicNestedSampler


def compare_methods_old(ndim):
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

def compare_methods():
    
    offset = 5
    
    post = norm(loc=0, scale=1)
    proposal = norm(loc=offset, scale=1)

    def prior_transform(u):
        return offset + np.sqrt(2) * erfinv(2*u-1)

    def log_likelihood(x):
        return np.squeeze(np.log(100) - .5 * (x**2 - (x-offset)**2))
    
    ns_results = {}
    is_results = {}
    
    for nlive in [800, 2000]:
    # for nlive in [200]:
        sampler = DynamicNestedSampler(log_likelihood, prior_transform, ndim=1, nlive=nlive)
        sampler.run_nested()
        ns_results[nlive] = sampler.results
    
    for n in 10_000*2**np.arange(1, 9):
    # for n in [1000]:
        samples = proposal.rvs(size=n, random_state=1)

        weights = 100 * post.pdf(samples) / proposal.pdf(samples)

        neff = np.sum(weights)**2 / np.sum(weights**2)

        evidence_estimate = np.average(weights)
        evidence_error = evidence_estimate * np.sqrt((1 -neff/n) / neff)
        
        is_results[n] = {
            'evidence_estimate': evidence_estimate,
            'evidence_error': evidence_error,
            'neff': neff,
            'weights': weights,
        }
    
    c_is = 'black'
    c_ns = 'orangered'

    for key, val in is_results.items():
        plt.errorbar(key, val['evidence_estimate'], yerr=val['evidence_error'], capsize=5, capthick=2, fmt='o', color=c_is)
    
    for key, val in ns_results.items():
        plt.errorbar(sum(val['ncall']), np.exp(val.logz[-1]), yerr=np.exp(val.logz[-1])*val.logzerr[-1], capsize=5, capthick=2, fmt='o', color=c_ns)
    
    plt.xlabel('Number of likelihood evaluations')
    plt.ylabel('Evidence estimate')
    plt.axhline(y=100, ls='--', color='grey')
    
    # for key, val in is_results.items():
    #     plt.scatter(key, val['neff'], color=c_is)
    
    # for key, val in ns_results.items():
    #     weights = np.exp(val.logwt)
    #     plt.scatter(sum(val['ncall']), np.sum(weights)**2 / np.sum(weights**2), color=c_ns)
    
    # plt.xlabel('Number of likelihood evaluations')
    # plt.ylabel('Number of effective samples')
    
    plt.show()
    
    return ns_results, is_results


if __name__ == '__main__':
    compare_methods()
