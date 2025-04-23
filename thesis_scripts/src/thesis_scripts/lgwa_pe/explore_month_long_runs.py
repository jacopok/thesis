from .lgwa_nested_sampling import run_pe, run_mcmc, make_analysis_functions, from_bilby
from .lgwa_likelihood import LunarLikelihood, time_to_merger
from bilby.gw.prior import (
    BNSPriorDict, 
    DeltaFunction, 
    Uniform, 
    UniformSourceFrame,
    Constraint,
    UniformInComponentsChirpMass,
    UniformInComponentsMassRatio
)
import numpy as np
import matplotlib.pyplot as plt
import yaml
from .. import data_path
from .explore_strange_posteriors import compare_mcmc_guess

if __name__ == '__main__':

    
    for n_months in range(1, 2):
    
        folder_name = f'gw150914_median_mbm_{n_months}'
        prior_file = data_path / folder_name / 'priors.txt.prior'
        f = np.load(data_path / folder_name / 'frequency_grid.npy')
        with open(data_path / folder_name / 'injection_parameters.yaml') as fi:
            injection_params = yaml.safe_load(fi)
        
        prior_dict = BNSPriorDict({})
        prior_dict.from_file(prior_file)
        prior_dict._resolve_conditions()
        
        like = LunarLikelihood()
        amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
        t = time_to_merger(f, phase)
        
        t0 = -3600*24*365.25
        month = 3600*24*365.25 / 12
        i0 = np.searchsorted(t, t0)
        i1 = np.searchsorted(t, t0+month*n_months)
        
        loglike, prior_transform, inverse_prior_transform, log_dir, param_names = make_analysis_functions(injection_parameters=injection_params, folder_name=folder_name, priors=prior_dict, freq=f[i0:i1])

        (data_path / folder_name / 'plots').mkdir(exist_ok=True)
        
        compare_mcmc_guess(data_path / folder_name, prior_transform, param_names, injection_params)