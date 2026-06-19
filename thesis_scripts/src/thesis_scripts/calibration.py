from data_sources import all_source_paths, cache_path, figure_path
import numpy as np
import bilby

if __name__ == '__main__':
    lvk_result = bilby.gw.result.CompactBinaryCoalescenceResult.from_hdf5(all_source_paths["lvk_pe_result"])
    
    lvk_result.outdir = '.'
    
    lvk_result.plot_calibration_posterior()