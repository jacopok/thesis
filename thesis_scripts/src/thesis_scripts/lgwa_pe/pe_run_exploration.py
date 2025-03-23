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

# plt.hist2d(
#     np.rad2deg(post_equal['ra']-injection_params['ra']), 
#     np.rad2deg(post_equal['dec']-injection_params['dec']), 
#     bins=40, density=True)

rng = np.random.default_rng(seed=1)

n_p, n_f = 20, 5
random_indices = rng.choice(post_equal.index, size=n_p, replace=False)

print(random_indices)

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


# plt.show()

