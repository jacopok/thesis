from bilby.gw.prior import BNSPriorDict
import numpy as np

def test_bilby_prior_inversion():
    d = BNSPriorDict()
    
    d['lambda_1'] = 400.
    
    sample = d.sample()
    
    names = list(d.keys())
    names.remove('mass_1')
    names.remove('mass_2')
    
    u_dict = d.cdf(sample)
    u_list = [u_dict[name] for name in names]
    
    # breakpoint()
    
    recovered_sample_list = d.rescale(names, u_list)
    
    recovered_sample_dict = {name: recovered_sample_list[i] for i, name in enumerate(names)}
    
    for name in names:
        assert np.isclose(sample[name], recovered_sample_dict[name])