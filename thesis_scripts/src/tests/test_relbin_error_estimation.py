from thesis_scripts.lgwa_nested_sampling import from_bilby
from thesis_scripts.lgwa_likelihood import LunarLikelihood
from thesis_scripts import data_path
from tqdm import tqdm

import pandas as pd
import numpy as np
from bilby.gw.prior import BNSPriorDict

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.cm import ScalarMappable
from cmcrameri import cm

import yaml

def make_accurate_ll_data():
    run_folder = data_path / 'bns_test'

    fname = run_folder / 'chains' /'weighted_post.txt'
    assert fname.exists()
    
    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())
    post_equal = pd.read_csv(fname.parent / 'equal_weighted_post.txt', sep = ' ')
    prior = BNSPriorDict({})
    prior.from_file(run_folder / 'priors.txt.prior')

    rng = np.random.default_rng(seed=1)

    n_p, n_f = 20, 5
    random_indices = rng.choice(post_equal.index, size=n_p, replace=False)

    accurate_ll_values = np.zeros((n_p, n_f))

    n_freqs = np.geomspace(1e6, 4e7, num=n_f, dtype=int)
    like = LunarLikelihood()
    like.compute_center(injection_params['time_at_center'])
    for j, n_freq in enumerate(n_freqs):
        f = np.geomspace(1e-3, 3, num=n_freq)
        like.data = like.projected_waveform(f, from_bilby(injection_params))
        for i, idx in tqdm(enumerate(random_indices)):
            accurate_ll_values[i, j] = like.log_likelihood_ratio(f, from_bilby(
                post_equal.iloc[idx].to_dict() | {
                    key: prior[key].peak for key in prior.fixed_keys
                }
                ))
            print(accurate_ll_values)

    np.save(run_folder / 'accurate_ll_values.npy', accurate_ll_values)

def plot_relbin_error_estimation():

    rng = np.random.default_rng(seed=1)
    run_folder = data_path / 'bns_test'

    fname = run_folder / 'chains' /'weighted_post.txt'
    assert fname.exists()
    
    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())
    post_equal = pd.read_csv(fname.parent / 'equal_weighted_post.txt', sep = ' ')
    prior = BNSPriorDict({})
    prior.from_file(run_folder / 'priors.txt.prior')


    n_p, n_f = 20, 5
    random_indices = rng.choice(post_equal.index, size=n_p, replace=False)
    n_freqs = np.geomspace(1e6, 4e7, num=n_f, dtype=int)
    accurate_ll_values = np.load(run_folder / 'accurate_ll_values.npy')

    # this plot shows that the "accurate ll values" are accurate to within roughly 1e-5
    # plt.loglog(n_freqs, abs(accurate_ll_values.T-accurate_ll_values[:, -1]))
    # plt.show()
    # plt.close()
    
    n_f_relbin = 5
    n_freqs_relbin = np.geomspace(1e2, 1e4, num=n_f_relbin, dtype=int)
    like = LunarLikelihood()
    like.compute_center(injection_params['time_at_center'])

    likes_relbin = np.empty((n_p, n_f_relbin))
    estimated_errors_relbin = np.empty((n_p, n_f_relbin))
    errors_relbin = np.empty((n_p, n_f_relbin))
    
    for j, n_freq in enumerate(n_freqs_relbin):
        f = np.geomspace(1e-3, 3, num=n_freq)
        like.make_relbin_data(f, from_bilby(injection_params), n_local_grid=max(2**10, int(2**20/n_freq)))
        for i, idx in tqdm(enumerate(random_indices)):
            params = from_bilby(
            post_equal.iloc[idx].to_dict() | {
                key: prior[key].peak for key in prior.fixed_keys
                })
            likes_relbin[i, j] = like.relbin_log_likelihood_ratio(params)
            estimated_errors_relbin[i, j] = like.relbin_log_likelihood_error(params, n_midpoints=1)
            errors_relbin[i, j] = abs(likes_relbin[i, j] - accurate_ll_values[i, -1])
    
    norm_freq = LogNorm(min(n_freqs_relbin), max(n_freqs_relbin))
    
    errors_full_integration = abs(accurate_ll_values[:, -2] - accurate_ll_values[:, -1])

    plt.scatter(
        x=errors_relbin.flatten(), 
        y=estimated_errors_relbin.flatten(), 
        c=cm.imola(
            norm_freq(
                np.repeat(n_freqs_relbin, n_p).reshape(
                    (n_f_relbin, n_p)
                    ).T.flatten()
                )
            ),
        )
    plt.errorbar(
        x=errors_relbin.flatten(), 
        y=estimated_errors_relbin.flatten(), 
        yerr=np.repeat(errors_full_integration, n_f_relbin),
        c='black',
        fmt='none',
    )
    plt.xscale('log')
    plt.yscale('log')
    
    plt.xlabel('Loglikelihood error: comparison with proper likelihood')
    plt.ylabel('Loglikelihood error: rough estimate with 1 midpoint per bin')
    plt.colorbar(ScalarMappable(cmap=cm.imola, norm=norm_freq), label='Frequency nodes used', ax=plt.gca())
    
    r = np.geomspace(1e-6, 1)
    plt.plot(r, r, c='black', ls='--')
    plt.show()
    
def plot_all_ll_estimated_errors():
    run_folder = data_path / 'bns_test'

    fname = run_folder / 'chains' /'weighted_post.txt'
    assert fname.exists()
    
    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())
    post_equal = pd.read_csv(fname.parent / 'equal_weighted_post.txt', sep = ' ')
    prior = BNSPriorDict({})
    prior.from_file(run_folder / 'priors.txt.prior')
    
    
    like = LunarLikelihood()
    like.compute_center(injection_params['time_at_center'])
    fixed_dict = {
        key: prior[key].peak for key in prior.fixed_keys
    }
    
    numbers_of_f = 5
    n_plot = 10
    estimated_errors = np.zeros((numbers_of_f, n_plot))
    estimated_likes = np.zeros((numbers_of_f, n_plot))
    
    freq_nums = np.geomspace(500, 10000, num=numbers_of_f, dtype=int)
    
    for i, n_f in enumerate(freq_nums):
    
        freq = np.geomspace(1e-3, 3, num=n_f)
        like.make_relbin_data(freq, from_bilby(injection_params))
        
        # n_plot = len(post_equal) // 100

        for idx in tqdm(range(n_plot)):
            params = from_bilby(
                post_equal.iloc[idx].to_dict() | fixed_dict)
            estimated_likes[i, idx] = like.relbin_log_likelihood_ratio(params)
            estimated_errors[i, idx] = like.relbin_log_likelihood_error(params, n_midpoints=10)
    
    for idx in range(n_plot):
        plt.errorbar(freq_nums+idx/100., estimated_likes[:, idx]-estimated_likes[-1, idx], estimated_errors[:, idx], capsize=1)
    plt.xscale('log')
    plt.show()
    
if __name__ == '__main__':
    # plot_relbin_error_estimation()
    plot_all_ll_estimated_errors()