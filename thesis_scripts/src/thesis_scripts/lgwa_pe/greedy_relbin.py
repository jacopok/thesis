from .plotting import plot_contours, make_arcmin_grid
from .lgwa_nested_sampling import from_bilby
from .lgwa_likelihood import LunarLikelihood
from . import data_path
from tqdm import tqdm

import pandas as pd
import numpy as np
from bilby.gw.prior import BNSPriorDict

import matplotlib.pyplot as plt

import yaml


if __name__ == '__main__':

    run_folder = data_path / 'bns_test'

    fname = run_folder / 'chains' /'weighted_post.txt'
    assert fname.exists()

    injection_params = yaml.safe_load((run_folder / 'injection_parameters.yaml').read_text())
    prior = BNSPriorDict({})
    prior.from_file(run_folder / 'priors.txt.prior')

    # weighted posterior
    post_pandas = pd.read_csv(fname, sep=' ')
    weights = post_pandas['weight']

    # equal_weighted posterior
    post_equal = pd.read_csv(fname.parent / 'equal_weighted_post.txt', sep = ' ')

    rng = np.random.default_rng(seed=1)

    like = LunarLikelihood()
    like.compute_center(injection_params['time_at_center'])
    
    f0 = 0.08681618121461131
    
    f_big = np.geomspace(f0, 3, num=int(4e6))
    like.data = like.projected_waveform(f_big, from_bilby(injection_params))
    ll_max = like.log_likelihood_ratio(f_big, from_bilby(injection_params))
    f_initial = np.geomspace(f0, 3, num=5)
    like.make_relbin_data(f_initial, from_bilby(injection_params))
    
    exp_tapered_error = 1e2
    decay = 0.01
    points_per_iteration = 5
    while exp_tapered_error > 1e-3:
        random_idx = rng.choice(post_equal.index, size=1)[0]
        params = from_bilby(post_equal.iloc[random_idx].to_dict())
        ll = like.relbin_log_likelihood_ratio(params)
        err, indices = like.relbin_log_likelihood_error(params, n_midpoints=1, n_to_return=points_per_iteration)
        err_balanced = err / (ll_max - ll)
        exp_tapered_error = np.average([err_balanced, exp_tapered_error], weights=[decay, 1-decay])
        print(f'Local: {err_balanced:.3f}, like diff: {ll_max - ll:.2f}, tapered: {exp_tapered_error:.3f}, {len(like.relbin_frequencies)} frequencies, adding at indices {indices}')
        # print(like.relbin_frequencies)
        for idx in indices:
            like.add_relbin_frequency(idx)
        if len(like.relbin_frequencies) % 1000 < points_per_iteration:
            f = like.relbin_frequencies
            
            t = like.t_of_f(f, params)
            hx, hy = like.projected_waveform(f, params)
            hx0, hy0 = like.projected_waveform(f, from_bilby(injection_params))
            for key in params:
                print(f'{key}: {params[key]} vs {from_bilby(injection_params)[key]}, difference {params[key]-from_bilby(injection_params)[key]}')
            psd = like.psd(f)
            alpha = np.sqrt(max(psd)/psd)
            fig, axs = plt.subplots(2, 2)
            axs[0, 0].semilogx(f, abs(hx/hx0))
            axs[0, 0].semilogx(f, abs(hy/hy0))
            axs[1, 0].semilogx(f, np.angle(hx/hx0))
            axs[1, 0].semilogx(f, np.angle(hy/hy0))
            
            i0, i1 = np.searchsorted(t, [1e9, 1.01e9])
            axs[0, 1].plot(t[i0:i1], abs(hx/hx0)[i0:i1])
            axs[0, 1].plot(t[i0:i1], abs(hy/hy0)[i0:i1])
            axs[1, 1].plot(t[i0:i1], np.angle(hx/hx0)[i0:i1])
            axs[1, 1].plot(t[i0:i1], np.angle(hy/hy0)[i0:i1])
            # axs[0, 1].set_xlim(1e9, 1.01e9)
            # axs[1, 1].set_xlim(1e9, 1.01e9)

            fig_path = run_folder / 'plots_greedy'
            plt.savefig(fig_path / f'waveforms_{len(like.relbin_frequencies)/1000:.0f}.png', dpi=600)
            plt.close()
            
            # test the summary data is correctly computed
            # like2 = LunarLikelihood()
            # like2.compute_center(injection_params['time_at_center'])
            # like2.make_relbin_data(f, from_bilby(injection_params))
            # assert np.allclose(like2.relbin_summary_data, like.relbin_summary_data)

            fig, axs = plt.subplots(1, 2)
            axs[0].hist(t, bins=120)
            axs[0].set_yscale('log')
            axs[1].hist(np.log10(f), bins=60)
            plt.savefig(fig_path / f'histograms_{len(like.relbin_frequencies)/1000:.0f}.png', dpi=600)
            plt.close()
    
    np.save(run_folder / 'greedy_freqs.npy', like.relbin_frequencies)