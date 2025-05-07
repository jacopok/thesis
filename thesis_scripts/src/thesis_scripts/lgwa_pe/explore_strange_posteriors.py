from ..plotting import plot_contours
from matplotlib import ticker
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
import pandas as pd
from ..plotting import make_arcmin_grid
from .. import data_path
import yaml
import numpy as np
import matplotlib.pyplot as plt

from cmcrameri import cm

from .lgwa_likelihood import LunarLikelihood
from .lgwa_nested_sampling import from_bilby
from tqdm import tqdm

def compare_mcmc_guess(run_folder, prior_transform, param_names, injection_parameters):
    # post_full = pd.read_csv(run_folder / 'chains' / 'equal_weighted_post.txt', sep=' ')
    guess = np.load(run_folder / 'baseline_post.npy')
    
    guess_transformed = [prior_transform(np.clip(row, 0, 1)) for row in guess]
    
    np.save(run_folder / 'baseline_post_transformed.npy', np.asarray(guess_transformed))
    
    for idx in range(len(param_names)):
        # plt.hist(post_full[param_names[idx]], alpha=.5, label='posterior', bins=50, density=True)
        plt.hist([row[idx] for row in guess_transformed], alpha=.5, label='initial MCMC run', bins=50, density=True)
        plt.axvline(injection_parameters[param_names[idx]], c='black', ls='--', label='injected value')
        
        plt.legend()
        plt.title(param_names[idx])
        plt.savefig(run_folder / 'plots'/ f'{param_names[idx]}.png')
        plt.close()

def make_2d_scatterplot(run_folder, param_1, param_2, color_param):


    cmap_full = cm.devon
    cmap_ew = cm.lajolla

    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())

    # post_ew = pd.read_csv(data_path / 'ew_gw170817_run' / 'chains' / 'equal_weighted_post.txt', sep=' ')
    post_full = pd.read_csv(run_folder / 'chains' / 'equal_weighted_post.txt', sep=' ')

    norm = Normalize(vmin=min(post_full[color_param]), vmax=max(post_full[color_param]))

    c = plt.scatter(post_full[param_1], post_full[param_2], s=.5, alpha=.5, c=post_full[color_param], cmap=cmap_full, norm=norm)
    plt.scatter(injection_params[param_1], injection_params[param_2], marker='x', c='black')

    plt.colorbar(ScalarMappable(cmap=cmap_full, norm=norm), label=color_param, ax=plt.gca())

    plt.xlabel(param_1)
    plt.ylabel(param_2)

    if param_1 == 'ra' and param_2 == 'dec':
        make_arcmin_grid(plt.gca(), (min(post_full[param_1]), max(post_full[param_1])), (min(post_full[param_2]), max(post_full[param_2])))

    plt.savefig(run_folder / 'plots'/ f'{param_1}_{param_2}_color_{color_param}.png')
    plt.close()

def make_loglike_histogram(run_folder, freq):
    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())

    # post_ew = pd.read_csv(data_path / 'ew_gw170817_run' / 'chains' / 'equal_weighted_post.txt', sep=' ')
    post_full = pd.read_csv(run_folder / 'chains' / 'equal_weighted_post.txt', sep=' ')

    like = LunarLikelihood()
    like.compute_center(injection_params['time_at_center'])
    like.make_relbin_data(freq, from_bilby(injection_params))
    
    lmax = like.relbin_log_likelihood_ratio(from_bilby(injection_params))
    
    likes = np.empty_like(post_full[:1000])
    for i, row in tqdm(post_full.iloc[:1000].iterrows()):
        print(from_bilby(row.to_dict()))
        likes[i] = like.relbin_log_likelihood_ratio(from_bilby(row.to_dict())) - lmax
    
    print(likes.shape)
    plt.hist(likes)
    plt.show()

if __name__ == '__main__':
    run_folder = data_path / 'gw170817_median_1yr_ew_1mo'
    color_param = 'lambda_1'
    param_1 = 'ra'
    param_2 = 'dec'

    # make_2d_scatterplot(run_folder, param_1, param_2, color_param)
    make_loglike_histogram(run_folder, np.geomspace(0.08681618121461131, 3, num=1000))