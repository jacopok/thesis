from thesis_scripts.postprocess import area_from_samples, gaussian_area_from_samples
import numpy as np

def test_gaussian_ninety_percent_calculation():
    # the gaussian calculation is:
    # - 2 * pi * sin(dec) * log(1-0.9) * sqrt(cov[00]*cov[11] - cov[01]^2) = 2*pi*log(10)*1e-8 in this case
    
    rng = np.random.default_rng(seed=1)
    samples = rng.normal(size=(1000, 2), loc=[0, np.pi/2], scale=[1e-4, 1e-4])
    
    area = gaussian_area_from_samples(samples[:, 0], samples[:, 1], percentile=90)
    
    assert np.isclose(area, 1.4467568824830927e-7)
    
def test_full_ninety_percent_calculation_gaussian_case():
    rng = np.random.default_rng(seed=1)
    samples = rng.normal(size=(10000, 2), loc=[0, np.pi/2], scale=[1e-4, 1e-4])
    
    area = area_from_samples(samples[:, 0], samples[:, 1], percentile=90)
    
    assert np.isclose(area, 1.4467568824830927e-7)
