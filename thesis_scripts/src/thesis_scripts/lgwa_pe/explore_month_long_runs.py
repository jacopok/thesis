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

GENERIC_FNAME = 'gw150914_median_mbm_year_before'

def run_postprocessing():
    
    for n_months in range(1, 13):
    
        folder_name = f'{GENERIC_FNAME}_{n_months}'
        prior_file = data_path / folder_name / 'priors.txt.prior'
        f = np.load(data_path / folder_name / 'frequency_grid.npy')

        with open(data_path / folder_name / 'injection_parameters.yaml') as fi:
            injection_params = yaml.safe_load(fi)
        
        prior_dict = BNSPriorDict({})
        prior_dict.from_file(prior_file)
        prior_dict._resolve_conditions()
        
        # like = LunarLikelihood()
        # amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
        # t = time_to_merger(f, phase)
        
        # t0 = -3600*24*365.25
        # month = 3600*24*365.25 / 12
        # i0 = np.searchsorted(t, t0)
        # i1 = np.searchsorted(t, t0+month*n_months)
        
        loglike, prior_transform, inverse_prior_transform, log_dir, param_names = make_analysis_functions(injection_parameters=injection_params, folder_name=folder_name, priors=prior_dict, freq=f)

        (data_path / folder_name / 'plots').mkdir(exist_ok=True)
        
        compare_mcmc_guess(data_path / folder_name, prior_transform, param_names, injection_params)

def plot_trajectories():
    
    cmap = plt.get_cmap('magma')
    for n_months in range(1, 12):
    
        folder_name = f'{GENERIC_FNAME}_{n_months}'
        prior_file = data_path / folder_name / 'priors.txt.prior'
        f = np.load(data_path / folder_name / 'frequency_grid.npy')
        with open(data_path / folder_name / 'injection_parameters.yaml') as fi:
            injection_params = yaml.safe_load(fi)
        
        like = LunarLikelihood()
        amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
        t = time_to_merger(f, phase)
        AU = 1.49597871e+11
        pos = like.get_detector_position_vector(t+injection_params['time_at_center']) / AU
        # breakpoint()
        plt.scatter(2.1*n_months, 0, color=cmap(n_months/13), label=f'{n_months} months')
        plt.plot(pos[:, 0]+2.1*n_months, pos[:, 1], c=cmap(n_months/13))
        plt.fill(pos[:, 0]+2.1*n_months, pos[:, 1], c=cmap(n_months/13), alpha=.2)
        
    plt.xlabel('Shifted ICRS $x$ coordinate [AU]')
    plt.ylabel('ICRS $y$ coordinate [AU]')
    plt.show()

def plot_timing_posteriors():
    
    cmap = plt.get_cmap('magma')
    for n_months in range(1, 12):
    
        folder_name = f'{GENERIC_FNAME}_{n_months}'
        prior_file = data_path / folder_name / 'priors.txt.prior'
        
        prior_dict = BNSPriorDict({})
        prior_dict.from_file(prior_file)
        prior_dict._resolve_conditions()
        param_names = prior_dict.sorted_keys_without_fixed_parameters

        f = np.load(data_path / folder_name / 'frequency_grid.npy')
        with open(data_path / folder_name / 'injection_parameters.yaml') as fi:
            injection_params = yaml.safe_load(fi)
        
        # like = LunarLikelihood()
        # amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
        # t = time_to_merger(f, phase)
        transformed_post = np.load(data_path / folder_name / 'baseline_post_transformed.npy')
        
        idx = param_names.index('time_at_center')
        plt.hist(transformed_post[:, idx], density=True, color=cmap(n_months/13), alpha=.5, bins=100, histtype='step', label=f'{n_months} months')
    
    plt.legend()
    plt.xlabel('Time at center [s]')
    plt.show()

def plot_sky_position_posteriors():
    
    cmap = plt.get_cmap('magma')
    
    fig, axs = plt.subplots(1, 2)
    
    for n_months in range(1, 13):
    
        folder_name = f'{GENERIC_FNAME}_{n_months}'
        prior_file = data_path / folder_name / 'priors.txt.prior'
        
        prior_dict = BNSPriorDict({})
        prior_dict.from_file(prior_file)
        prior_dict._resolve_conditions()
        param_names = prior_dict.sorted_keys_without_fixed_parameters

        f = np.load(data_path / folder_name / 'frequency_grid.npy')
        with open(data_path / folder_name / 'injection_parameters.yaml') as fi:
            injection_params = yaml.safe_load(fi)
        
        # like = LunarLikelihood()
        # amplitude, phase = like.amp_phase(f, from_bilby(injection_params))
        # t = time_to_merger(f, phase)
        transformed_post = np.load(data_path / folder_name / 'baseline_post_transformed.npy')
        
        idx1 = param_names.index('ra')
        idx2 = param_names.index('dec')
        axs[0].hist(np.rad2deg(transformed_post[:, idx1]), density=True, color=cmap(n_months/13), alpha=.5, bins=100, histtype='step', label=f'{n_months} months')
        axs[1].hist(np.rad2deg(transformed_post[:, idx2]), density=True, color=cmap(n_months/13), alpha=.5, bins=100, histtype='step', label=f'{n_months} months')
    axs[0].axvline(np.rad2deg(injection_params['ra']), c='black', ls='--')
    axs[1].axvline(np.rad2deg(injection_params['dec']), c='black', ls='--')
    
    plt.legend()
    axs[0].set_xlabel('right ascension [deg]')
    axs[1].set_xlabel('declination [deg]')
    plt.show()


if __name__ == '__main__':

    # run_postprocessing()
    
    # plot_trajectories()
    # plot_timing_posteriors()
    plot_sky_position_posteriors()