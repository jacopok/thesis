import numpy as np
import bilby
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import LogLocator, LogFormatter # For formatting plot axes
from matplotlib.lines import Line2D # For making custom legends
from matplotlib import rcParams
from scipy.interpolate import interp1d # For interpolating data

# PESummary is useful for dealing with posterior samples and making plots
# Documentation https://pesummary.readthedocs.io/en/stable/
from pesummary.io import read
from pesummary.utils.samples_dict import MultiAnalysisSamplesDict # For dealing with sets of analysis results
from pesummary.utils.bounded_1d_kde import bounded_1d_kde # For making 1-dimensional kernel density estimates for bounded data
from pesummary.utils.bounded_2d_kde import Bounded_2d_kde # For making 2-dimensional kernel density estimates for bounded data


# Helper function to plot spline model used for calibration in inference
def plot_spline_pos(log_freqs, samples, nfreqs=100, level=0.9, color='k', label=None, xform=None, plot_type='fill'):
    """
    Plot calibration posterior estimates for a spline model in log space.
    Adapted from the same function in lalinference.bayespputils

    Parameters
    ==========
    log_freqs: array-like
        The (log) location of spline control points.
    samples: array-like
        List of posterior draws of function at control points ``log_freqs``
    nfreqs: int
        Number of points to evaluate spline at for plotting.
    level: float
        Credible level to fill in (default 0.9 for the 90% credible interval).
    color: str
        Color to plot with.
    label: str
        Legend label for the posterior envelope.
    xform: callable
        Function to transform the spline into plotted values.
    plot_type : {'fill', 'lines'}
        Draw a filled credible region or boundary lines.

    Returns
    -------
    matplotlib.collections.PolyCollection or list
        The plotted object (either filled or plotted with lines).
    """

    # Define frequency array
    freq_points = np.exp(log_freqs)
    freqs = np.logspace(min(log_freqs), max(log_freqs), nfreqs, base=np.exp(1))

    data = np.zeros((samples.shape[0], nfreqs))

    if xform is None:
        scaled_samples = samples
    else:
        scaled_samples = xform(samples)

    scaled_samples_summary = bilby.core.utils.SamplesSummary(scaled_samples, average='mean', confidence_level=level)
    data_summary = bilby.core.utils.SamplesSummary(data, average='mean', confidence_level=level)

    # Reconstruct cubic spline models for calibration envelopes
    for i, sample in enumerate(samples):
        temp = interp1d(
            log_freqs, sample, kind="cubic", fill_value=0,
            bounds_error=False)(np.log(freqs))
        if xform is None:
            data[i] = temp
        else:
            data[i] = xform(temp)

    # Boundaries of symmetric credible interval
    lower = data_summary.lower_absolute_credible_interval
    upper = data_summary.upper_absolute_credible_interval

    # Either plot lines or shaded region
    if plot_type=='lines':
        post_plot = plt.plot(freqs, lower, color=color, label=label, lw=3)
        plt.plot(freqs, upper, color=color, lw=3)
    elif plot_type=='fill':
        post_plot = plt.fill_between(freqs, lower,
                    upper,
                    color=color, alpha=0.5, linewidth=0.1, label=label) # alpha here controls fill of the posterior regions
    plt.xlim(freq_points.min() - 0.5, freq_points.max() + 50)
    
    return post_plot

# Helper function to make plots
def plot_cal(posterior, ax_amp, ax_phase, color, plot_type, label=None):
    """
    Plot calibration posterior credible intervals for amplitude and phase

    Parameters
    ----------
    posterior : dict-like
        Posterior sample dictionary containing calibration spline parameters
    ax_amp : matplotlib.axes.Axes
        Axis on which to plot the amplitude calibration uncertainty
    ax_phase : matplotlib.axes.Axes
        Axis on which to plot the phase calibration uncertainty
    color : str
        Color used for the plotted posterior interval
    plot_type : {'fill', 'lines'}
        Plot style for the posterior credible region
    label : str, optional
        Legend label for the posterior envelope

    Returns
    -------
    matplotlib.collections.PolyCollection or list
        The plotting object returned by `plot_spline_pos`.
    """

    # Amplitude error
    plt.sca(ax_amp)
    parameters = posterior.keys()
    
    # Collect frequencies of the spline nodes
    freq_params = np.sort([param for param in parameters if
                        'recalib_H1_frequency_' in param])
    logfreqs = np.log([posterior[param][0] for param in freq_params])
    # Collect inferred amplitude errors delta A'
    amp_params = np.sort([param for param in parameters if
                        'recalib_H1_amplitude_' in param])

    # Transform amplitude from inference to calibration convention and scale to become a percentage
    amplitude = 100 * (1/(np.column_stack([posterior[param] for param in amp_params]) + 1) - 1)
    
    post_plot = plot_spline_pos(logfreqs, amplitude, color=color, label=label, plot_type=plot_type, level=0.68)

    # Phase error
    plt.sca(ax_phase)

    # Collect inferred phase errors delta phi'
    phase_params = np.sort([param for param in parameters if
                        'recalib_H1_phase_' in param])
    
    # Transform phase from inference to calibration convention and from radians to degrees
    phase = -np.column_stack([posterior[param] for param in phase_params])*180/np.pi

    # 68% credible level is plotted here (roughly one sigma for a Gaussian) as the convention when dealing with calibration measurements
    plot_spline_pos(logfreqs, phase, color=color, plot_type=plot_type, level=0.68)

    return post_plot


# Helper functions to calculate the peak frequency
def Get22PeakAngFreq(eta, chi):
    """
    Compute the peak angular frequency of the dominant (2,2) multipole moment.

    This is a Python port of the function in LAL:
    https://git.ligo.org/lscsoft/lalsuite/-/blob/master/lalsimulation/lib/LALSimInspiralTestingGRCorrections.c

    Parameters
    ----------
    eta : float or ndarray
        Symmetric mass ratio of the binary, m1*m2/(m1+m2)^2.
    chi : float or ndarray
        Spin parameter used in the peak-frequency fit.

    Returns
    -------
    float or ndarray
        Peak angular frequency of the (2,2) multipole moment in natural units based upon the total mass of the binary.
    """
    
    res = 0.5626787200433265 + (-0.08706198756945482 + 0.0017434519312586804*chi) * \
        np.log(10.26207326082448 - chi * (7.629921628648589 - 72.75949266353584 * (-0.25 + eta)) - 62.353217004599784 * (-0.25 + eta))
    return res

def get_fpeak(m1, m2, chi1z, chi2z):
    """
    Estimate the detector-frame peak frequency of the (2,2) mode.

    Parameters
    ----------
    m1 : array-like
        Detector-frame primary mass values.
    m2 : array-like
        Detector-frame secondary mass values.
    chi1z : array-like
        Aligned spin component of the primary object.
    chi2z : array-like
        Aligned spin component of the secondary object.

    Returns
    -------
    float or ndarray
        Estimated peak frequency of the dominant (2,2) multipole moment in Hz.
    """

    MTSUN_SI = 4.925490947641267e-06 # One solar mass * G / c^3 to give units of seconds
    Mt = m1 + m2              # Total mass
    eta = m1 * m2 / Mt**2     # Symmetric mass ratio
    chi = 0.5*(chi1z + chi2z) + 0.5*(chi1z - chi2z)*(m1 - m2)/(m1 + m2)/(1.0 - 2.0*eta) # A spin parameter

    # Find the peak frequency for a binary of the given total mass
    f22Peak = Get22PeakAngFreq(eta, chi) / (2*np.pi * Mt * MTSUN_SI) # (2,2) multipole moment peak frequency
    return f22Peak



def figure_2_lvk_calib_paper():


    # Set up some plotting style
    rcParams['font.family'] = 'serif'
    rcParams['text.usetex'] = True
    contour=[90] # Default contours at 90% credible level

    # Define analysis-specific colors for consistency across plots
    paper_colors = {}
    # paper_colors['NoUncert'] = '#ee9502'
    # paper_colors['C00Env'] = '#d95f02'
    paper_colors['C00Wide'] = '#332288'
    # paper_colors['C01Env'] = '#7570b3'
    paper_colors['H1'] = '#88CCEE'
    
    # Define location of data. You can download this data from the Zenodo data release. Add the path here.
    # The subdirectory for specific inputs to the analysis
    
    data_path = pathlib.Path(__file__).parent.parent.parent.parent / 'data'

    configPath = data_path / 'cal_env/'
    # The subdirectory for the samples output from the analysis
    samplePath = data_path / 'combined_samples/'

    # Define location to save figures. Change this as preferred
    figPath = (data_path.parent / 'chapters' / 'anatomy'/ 'figures').resolve()
    
    # Read in files

    # Hanford calibration uncertainty envelopes
    # Wide envelope used for both GW250114 and GW250207
    env_wide = np.genfromtxt(configPath/'calibration_uncertainty_H1_tmp_20.txt').T
    # C00 in-situ envelope for GW250114
    # env_jan_C00 = np.genfromtxt(configPath/'S250114n/C00/calibration_uncertainty_H1_1411261218.txt').T
    # C01 in-situ envelope for GW250114
    # env_jan_C01 = np.genfromtxt(configPath/'S250114n/C01/calibration_uncertainty_H1_1411261218.txt').T
    # The calibration files can also be obtained from the results files, like the posterior samples
    # For example,
    # read(samplePath/'S250114n/combinedPHM_envcalC00_metafile.hdf5').priors['calibration_raw']['C00:IMRPhenomXPNR']['H1'].T
    # would return the env_jan_C00 calibration file.
    # You can also read in the calibration files for the other detectors, but we focus on Hanford here as it has the most significant calibration uncertainty.

    # GW250925 posterior samples
    # We use samples from a mix of waveforms, but the results files also contain results with individual waveform models
    # Results using miscalibrated C00 data with a calbiration prior based upon in-situ measurements
    # result_jan_C00 = read(samplePath/'S250114n/combinedPHM_envcalC00_metafile.hdf5').samples_dict['C00:Mixed']
    # Results using miscalibrated C00 data with a wide calbiration prior (to test astrophysical calibration)
    # result_jan_wide = read(samplePath/'S250114n/combinedPHM_flatcalC00_metafile.hdf5').samples_dict['C00:Mixed'] 
    # Results using recalibrated C01 data with a calbiration prior based upon in-situ measurements (our headline results)
    # result_jan_C01 = read(samplePath/'S250114n/combinedPHM_envcalC01_metafile.hdf5').samples_dict['C01:Mixed'] 
    # Results using miscalibrated C00 data without accounting for calibration uncertainty (we expect biased results)
    # result_jan_nocal = read(samplePath/'S250114n/combinedPHM_nocalC00_metafile.hdf5').samples_dict['C00:Mixed'] 
    result_jan_wide = read(samplePath/'S250114/posterior_samples_NRSur7dq4.h5').samples_dict['bilby-NRSur7dq4_prod-reweighted']
    result_jan_nocal = read(samplePath/'S250114/posterior_samples_NRSur7dq4_no_calibration.h5').samples_dict['bilby-NRSur7dq4_prod_nocal-reweighted']

    # GW250207 posterior samples
    # We use samples from a mix of waveforms, but the results files also contain results with individual waveform models
    # Results using a wide calibration prior
    result_feb_wide = read(samplePath/'S250207bg/combinedPHM_cal_metafile.hdf5').samples_dict['C00:NRSur7dq4']
    # Results only using Hanford data (instead of from all three detectors) with a wide calibration prior
    result_feb_H1 = read(samplePath/'S250207bg/combinedPHM_H1cal_metafile.hdf5').samples_dict['C00:NRSur7dq4']
    # Results without accounting for calibration uncertainty (we expect biased results)
    results_feb_nocal = read(samplePath/'S250207bg/combinedPHM_nocal_metafile.hdf5').samples_dict['C00:NRSur7dq4']
    # Calculate estimates of the peak frequencies
    # Here we use the redshifted detector-frame masses, not the source masses, as we want the frequency observed by our detectors
    # The median for GW250114
    jan_peak = np.median(get_fpeak(result_jan_wide['mass_1'], result_jan_wide['mass_2'], result_jan_wide['spin_1z'], result_jan_wide['spin_2z']))

    # The median for GW250207
    feb_peak = np.median(get_fpeak(result_feb_wide['mass_1'], result_feb_wide['mass_2'], result_feb_wide['spin_1z'], result_feb_wide['spin_2z']))

    # Make plot
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(30, 15), dpi=500, sharey=True, sharex=True)

    # Plot GW250114 posteriors
    post_plot_jan_wide = plot_cal(result_jan_wide, ax1, ax3, color=paper_colors['C00Wide'], label='Calibrated', plot_type='fill')
    # post_plot_jan_C00 = plot_cal(result_jan_nocal, ax1, ax3, color=paper_colors['C00Env'], label='Not calibrated', plot_type='fill')

    # Plot GW250207 posteriors
    post_plot_feb_wide = plot_cal(result_feb_wide, ax2, ax4, color=paper_colors['C00Wide'], label='C00 Wide Posterior', plot_type='fill')
    post_plot_feb_H1 = plot_cal(result_feb_H1, ax2, ax4, color=paper_colors['H1'], label='Hanford Only Posterior', plot_type='fill')

    colors = [paper_colors['C00Wide']]
    labels = ['C00 Wide Prior']

    ax1.axvline(x=jan_peak, linestyle=':', color='k')
    ax3.axvline(x=jan_peak, linestyle=':', color='k')
    ax2.axvline(x=feb_peak, linestyle=':', color='k')
    ax4.axvline(x=feb_peak, linestyle=':', color='k')

    # Loop over results sets
    prior_plots_jan = []
    prior_plots_feb = []
    for i, env in enumerate([env_wide]):
        
        freqs = env[0]
        
        # The magnitude uncertainty is 1 + delta A, so we subtract 1 to get delta A
        amplitude_median = env[1] - 1 
        amplitude_upper = env[5] - 1 
        amplitude_lower = env[3] - 1 
        
        phase_median = env[2] 
        phase_upper = env[6] 
        phase_lower = env[4] 

        # Plot as a percentage
        temp, = ax1.plot(freqs, 100*(amplitude_upper), ls = '-', color=colors[i], lw=4, label=labels[i]) 
        prior_plots_jan.append(temp)

        ax1.plot(freqs, 100*(amplitude_lower), ls = '-', color=colors[i], lw=4)

        # Plot in degrees
        ax3.plot(freqs, (phase_upper)*180/np.pi, ls = '-', color=colors[i], lw=4)
        ax3.plot(freqs, (phase_lower)*180/np.pi, ls = '-', color=colors[i], lw=4)

        # GW250207 only has the wide prior, which is used for both analyses
        if i==0:
            # Since the priors are the same, we will plot with a dashed line, so we can see both
            
            # First set up for the legend
            temp, = ax2.plot(freqs, 100*(amplitude_upper), ls = '-', color=paper_colors['H1'], lw=4, label=labels[i])
            prior_plots_feb.append(temp)

            # Plot solid line underneath
            # Plot as a percentage
            temp, = ax2.plot(freqs, 100*(amplitude_upper), ls = '-', color=colors[i], lw=4, label=labels[i])
            prior_plots_feb.append(temp)
            ax2.plot(freqs, 100*(amplitude_lower), ls = '-', color=colors[i], lw=4)

            # Plot in degrees
            ax4.plot(freqs, (phase_upper)*180/np.pi, ls = '-', color=colors[i], lw=4)
            ax4.plot(freqs, (phase_lower)*180/np.pi, ls = '-', color=colors[i], lw=4)

            # Plot dashed line on top
            linestyle=(0,(5,5))
            # Plot as a percentage
            ax2.plot(freqs, 100*(amplitude_upper), ls = linestyle, color=paper_colors['H1'], lw=4, label=labels[i])
            ax2.plot(freqs, 100*(amplitude_lower), ls = linestyle, color=paper_colors['H1'], lw=4)

            # Plot in degrees
            ax4.plot(freqs, (phase_upper)*180/np.pi, ls = linestyle, color=paper_colors['H1'], lw=4)
            ax4.plot(freqs, (phase_lower)*180/np.pi, ls = linestyle, color=paper_colors['H1'], lw=4)

    # Label axes
    font_size = 42
    ax1.tick_params(labelsize=0.85 * font_size)
    ax2.tick_params(labelsize=0.85 * font_size)
    ax3.tick_params(labelsize=0.85 * font_size)
    ax4.tick_params(labelsize=0.85 * font_size)
    ax1.tick_params(which='major',length=8)
    ax1.tick_params(which='minor',length=6)
    ax2.tick_params(which='major',length=8)
    ax2.tick_params(which='minor',length=6)
    ax3.tick_params(which='major',length=8)
    ax3.tick_params(which='minor',length=6)
    ax4.tick_params(which='major',length=8)
    ax4.tick_params(which='minor',length=6)
    ax1.grid(visible=False)
    ax2.grid(visible=False)
    ax3.grid(visible=False)
    ax4.grid(visible=False)

    # Add legends
    leg_jan = [
        (post_plot_jan_wide,prior_plots_jan[0]),
    ]
    
    labels_jan = ["Hanford and Livingston",]
    leg_feb = [(post_plot_feb_wide,prior_plots_feb[1]),(post_plot_feb_H1,prior_plots_feb[0])]
    labels_feb = ["Hanford, Livingston, Virgo","Hanford Only"]
    ax1.legend(leg_jan,labels_jan,loc='upper left', prop={'size': 0.75 * font_size}, framealpha=0.7) 
    ax2.legend(leg_feb,labels_feb,loc='upper left', prop={'size': 0.75 * font_size}, framealpha=0.7) 

    # Set different limits for the two plots as the signals from different frequency ranges
    ax1.set_xscale('log')
    ax2.set_xscale('log')
    ax3.set_xscale('log')
    ax4.set_xscale('log')
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlim(21, 448)
        ax.set_ylim(-30, 30)
        ax.axhline(0, c='black', ls='--')

    # Finish formatting axes
    ax2.set_xticks([30, 100, 300], minor=False, labels=[30, 100, 300])
    ax4.set_xticks([30, 100, 300], minor=False, labels=[30, 100, 300])

    ax3.set_xlabel('Frequency [Hz]', fontsize=font_size)
    ax4.set_xlabel('Frequency [Hz]', fontsize=font_size)
    ax1.set_ylabel(r'Amplitude [$\%$]', fontsize=font_size)
    ax3.set_ylabel('Phase [deg]', fontsize=font_size)
    ax1.set_title('GW250114 at Hanford', fontsize= 1.1 * font_size)
    ax2.set_title('GW250207 at Hanford', fontsize = 1.1 * font_size)

    filename = figPath/'H1_calibration_comp.pdf'
    fig.tight_layout()
    fig.savefig(filename, dpi=600, bbox_inches='tight')

def plot_calibration_posterior(result, ax, which='amplitude', level=0.9):
    
    parameters = result.posterior.keys()

    # ifos = np.unique([param.split('_')[1] for param in parameters if 'recalib_' in param])
    ifos = ['H1']

    for ifo in ifos:
        freq_params = np.sort([param for param in parameters if
                            'recalib_{0}_frequency_'.format(ifo) in param])

        logfreqs = np.log([posterior[param].iloc[0] for param in freq_params])

        plt.sca(ax)
        if which == 'amplitude':
            # Amplitude calibration model
            amp_params = np.sort([param for param in parameters if
                                'recalib_{0}_amplitude_'.format(ifo) in param])
            if len(amp_params) > 0:
                amplitude = 100 * np.column_stack([posterior[param] for param in amp_params])
                bilby.gw.utils.plot_spline_pos(logfreqs, amplitude, color=color, level=level,
                                label=r"{0} (mean, {1}$\%$)".format(ifo.upper(), int(level * 100)))

        elif which == 'phase':
            # Phase calibration model
            phase_params = np.sort([param for param in parameters if
                                    'recalib_{0}_phase_'.format(ifo) in param])
            if len(phase_params) > 0:
                phase = np.column_stack([posterior[param] for param in phase_params])
                bilby.gw.utils.plot_spline_pos(logfreqs, phase, color=color, level=level,
                                label=r"{0} (mean, {1}$\%$)".format(ifo.upper(), int(level * 100)),
                                xform=bilby.gw.utils.spline_angle_xform)

        
    # data_path = pathlib.Path(__file__).parent.parent.parent.parent / 'data'
    
    # lvk_result = bilby.gw.result.CompactBinaryCoalescenceResult.from_hdf5(data_path / 'bilby-NRSur7dq4_prod_data0_1420878141-222656_analysis_H1L1_merge_result.hdf5')
    
    # lvk_result.outdir = (data_path.parent / 'chapters' / 'anatomy'/ 'figures' / 'lvk_250114').resolve().as_posix()
    
    # lvk_result.plot_calibration_posterior()
    
    # figure_2_lvk_calib_paper()


def posterior_cal_nocal_comparison(res, res_nocal, ax, label):
    data_path = pathlib.Path(__file__).parent.parent.parent.parent / 'data'

    configPath = data_path / 'cal_env/'

    from scipy import stats
    
    params = [
        'a_1', 
        'a_2', 
        'chirp_mass', 
        'tilt_1', 
        'tilt_2', 
        'dec', 
        'geocent_time', 
        'luminosity_distance', 
        'mass_ratio', 
        'phase', 
        'phi_12', 
        'phi_jl', 
        'psi', 
        'ra', 
        'theta_jn', 
    ]
    
    params_nice = {
        'a_1': '$a_1$', 
        'a_2': '$a_2$', 
        'chirp_mass': '$\\mathcal{{M}}$', 
        'tilt_1': '$\\mathrm{{tilt}}_1$', 
        'tilt_2': '$\\mathrm{{tilt}}_2$', 
        'dec': 'dec', 
        'geocent_time': '$t_{{\\mathrm{{geo}}}}$', 
        'luminosity_distance': '$d_L$', 
        'mass_ratio': '$q$', 
        'phase': '$\\phi_0$', 
        'phi_12': '$\\phi_{12}$', 
        'phi_jl': '$\\phi_{{\\mathrm{{JL}}}}$', 
        'psi': '$\\psi$', 
        'ra': 'ra', 
        'theta_jn': '$\\theta_{{\\mathrm{{JN}}}}$', 
    }
    
    cdfs1 = {}
    cdfs2 = {}
    cdfs_at_ref = []

    for key in params:
        
        x = np.linspace(np.min(res[key]), np.max(res[key]))

        cdfs1[key] = stats.ecdf(res[key]).cdf.evaluate(x)
        cdfs2[key] = stats.ecdf(res_nocal[key]).cdf.evaluate(x)
    
        idx = np.searchsorted(cdfs1[key], 0.5)
        cdfs_at_ref.append(cdfs2[key][idx])
    
    
    norm = mpl.colors.Normalize(0, len(params))
    cmap = plt.get_cmap('coolwarm')
    for i, key in enumerate(np.array(params)[np.argsort(cdfs_at_ref)[::-1]]):
        ax.plot(cdfs1[key], cdfs2[key], label=params_nice[key], c=cmap(norm(i)))

    ax.set_xlabel('CDF with calibration')
    ax.set_ylabel('CDF without calibration')
        
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    ax.set_title(label)
    
    ax.legend()
    
if __name__ == '__main__':
    
    rcParams['font.family'] = 'serif'
    rcParams['text.usetex'] = True

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    data_path = pathlib.Path(__file__).parent.parent.parent.parent / 'data'

    configPath = data_path / 'cal_env/'
    # The subdirectory for the samples output from the analysis
    samplePath = data_path / 'combined_samples/'
    
    res = read(samplePath/'S250114/posterior_samples_NRSur7dq4.h5').samples_dict['bilby-NRSur7dq4_prod-reweighted']
    res_nocal = read(samplePath/'S250114/posterior_samples_NRSur7dq4_no_calibration.h5').samples_dict['bilby-NRSur7dq4_prod_nocal-reweighted']
    
    posterior_cal_nocal_comparison(res, res_nocal, axs[0], 'GW250114')
    
    result_feb_wide = read(samplePath/'S250207bg/combinedPHM_cal_metafile.hdf5').samples_dict['C00:NRSur7dq4']
    results_feb_nocal = read(samplePath/'S250207bg/combinedPHM_nocal_metafile.hdf5').samples_dict['C00:NRSur7dq4']

    posterior_cal_nocal_comparison(result_feb_wide, results_feb_nocal, axs[1], 'GW2502027')
    
    figPath = (data_path.parent / 'chapters' / 'anatomy'/ 'figures').resolve()
    
    plt.savefig(figPath / f'posterior_nocal_compared.pdf')
    plt.close()

    figure_2_lvk_calib_paper()