import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    rng = np.random.default_rng(seed=1)
    
    # total_time = 3600. * 24. * 365.25
    total_time = 3600. * 24. * 7
    quake_rate = 1/(3600. * 24.)
    n_quakes = rng.poisson(total_time * quake_rate)
    
    quake_times = rng.uniform(0, total_time, n_quakes)
    
    quake_durations = rng.exponential(scale = 3600., size = n_quakes)
    
    for t, d in zip(quake_times, quake_durations):
        plt.plot([t, t + d], [0, 0], 'k-')
    plt.show()