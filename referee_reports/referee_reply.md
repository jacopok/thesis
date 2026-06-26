---
# compile with:
# pandoc -f markdown-implicit_figures --citeproc referee_reply.md -o referee_reply.pdf

title: "Referee reply"
author: Jacopo Tissino
date: 2026-06-26
geometry: "left=3.5cm,right=3.5cm,top=2.5cm,bottom=2.5cm"
output: pdf_document
colorlinks: true
linkcolor: blue
link-citations: true

hyperrefoptions:
- linktoc=all
- linkcolor=blue

---

I would like to thank the referees for their helpful reports.
I made several improvements to the thesis based on them.

The major changes are as follows:

- I updated the figures in chapters 7 and 8 to those we ultimately used in the [Geometry of Lunar Gravitational Wave Detection paper](https://arxiv.org/abs/2606.04918); while finishing the preparation we found a small issue in the calculations, which did not affect the conclusions. Also, in that paper we presented results for an injection with the Einstein Telescope, more details on which are now in the Einstein Telescope chapter. 
-  I added more details to the Introduction, as well as to the start of all chapters, regarding my personal contributions.
- I added a new discussion on the impact of non-zero Gaussian noise on LGWA analyses. This is in two new sections: in chapter 3,  a description of how a such an injection can cheaply be generated, as outlined in the original relative binning paper (Zackay et al. 2018). The other is in chapter 8, where I describe the results of a campaign of noisy injections and compare them to the noise-free case.
- I added a more detailed discussion of the impact of calibration and astrophysical calibration, showing the envelopes for GW250114 and GW250207. 
- I added priors tables in chapters 7 and 8, and made sure to mention which parameters were sampled in each analysis.
- I added an "acknowledgements" section to the introduction.

More minor changes are listed in the detailed responses to each referee.

# Reply to Prof. Barausse

Dear Prof. Barausse,

I thank you for your kind words and useful comments.
Here, I will provide a brief response to the points you raise.

1. First, the
boundary between established background and the candidate's own contributions is not
always evident. This is set out clearly once, in the introductory section on personal
contributions, but the reader would benefit from having it briefly restated at the start of each
chapter or section. Related to this, the introductory chapters, while pedagogically very well
written and genuinely useful as a reference, are somewhat long; a more concise treatment of
the standard material, with more emphasis on the candidate's own results, would have
improved the balance of the thesis. 

I added notes about results being my own work in several places in the thesis,
as well as more detail to the introductory section.

As far as the introductory chapters are concerned, I agree that they are 
quite long. This was a deliberate choice, made for two reasons: 
as you note, it allowed me to create a reference which will hopefully
be useful to others.
Furthermore, many of thse chapters include novel results from recent papers
which I was involved in:

- in chapter 3, the results from the "[window strikes back](https://doi.org/10.1088/1361-6382/ae1ac7)" paper --- I coauthored the figures shown in the thesis from that work;
- in chapter 4, the results from the [GW250114 detection paper](https://doi.org/10.1103/kw5g-d732), which I was part of the writing team for --- specifically, all the figures shown in that chapter were either authored or coauthored by me;
- in chapter 5, the results from the [GW150914 reanalysis](https://doi.org/10.1088/1361-6382/adfe50) paper and the [machine learning BNS surrogate](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.107.084037) paper.

I felt that weaving these results into the discussion of 
standard results would lead to an overall better reading experience.

2. Second, in some of the parameter-estimation
exercises it is not always clear which parameters are held fixed and which are marginalized,
and the choice of priors, although discussed in several places, is not consistently stated;
making the inference setup explicit in each case would further strengthen the results and
their reproducibility, especially because – as the thesis itself rightly emphasizes for
eccentricity, for instance – conclusions can strongly depend on the priors. 

I added three tables, clearly outlining the prior choices and injected parameters
for the main injections performed with the Einstein Telescope and Lunar Gravitational Wave Antenna.
These should also clarify which parameters were varied and which were not.

Furthermore, the paper on these results is now out as a preprint, 
and with it I published a [Zenodo data release](https://zenodo.org/records/20510354).
This will ensure full reproducibility.

3. Third, the thesis
contains a large number of figures, several of which would have warranted somewhat more
interpretation in the text.

I added more discussion to the captions of several figures, as well as 
to the surrounding text, especially in chapters 7 and 8.
In the process of addressing the other referee's concerns
I did add more figures, but I ensured these were all well described
in their captions as well in the text.

Finally, I noticed that in the evaluation criteria you selected a poor rating
regarding conference presentations.
Indeed, it was an oversight on my part to not include them
in the CV you received; you should receive an updated version along with
this response.

# Reply to Dr. Romero-Shaw

Dear Dr. Romero-Shaw,

I would like to thank you for your thorough and thoughtful review of my thesis.
I wanted to do it justice, which will require adding some extra analyses and figures;
for example, performing some noisy injections with the LGWA. 
They had been on my to-do list for a while and I'm happy your review gave me
motivation to add them.

You should also have received an updated CV, which includes a mention of the main 
conference talks I gave (another referee raised the point that they were missing).

## Sec 1: Introduction

- Please provide a link here to the mentioned static website version of the thesis – a reader of the PDF would probably like to be able to easily navigate to this. The link to the source code gives me a 404 error, please fix this.

The repository containing the source code and the website are not public yet; 
the plan I discussed with my supervisor is to release both upon graduation.
I am, however, happy to share it before, especially if there are any specific points you would like to check.

As I am glad you noticed, I wrote large parts of the thesis with the intention of making a 
useful reference; with this in mind, I think it is wise to only publish it after
as many mistakes as possible are corrected. When doing so, I will be sure to also
include a link to the website, as you suggest; I already set up everything so that 
upon a push to the repository the website can be automatically deployed.

In any case, I added a note to the current version of the thesis saying that the 
404 error is expected.

- Although Section 1.1 purports to explicitly outline the contributions made by the author, I do not find it clear exactly what the personal contributions to some mentioned publications were. [...]

Here is a detailed description of my contribution to all the papers mentioned;
I weaved a slightly less detailed version of it into the introduction text.

In the GW250114 discovery paper, my primary task was figure-making. 
I authored all figures in the main text except for figure 2, 
and co-authored figures 2 and 3 in the Supplement.
I was also responsible for the data release, as well as coordinating with the 
outreach team for the creation of various items, such as the infographic and image shown 
[here](https://ligo.org/detections/gw250114-10-years-of-gravitational-wave-astronomy/).
Furthermore, I performed some parameter estimation runs, 
and drafted and edited parts of the text, though I am not sure about how much of what 
I wrote survived the many rounds of revision.

I became involved with the windowing paper by raising 
the window factor correction as a potential systematic for GW250114 
and all previous analyses, though at the time I was reassured it was not a problem.
As far as the paper itself is concerned, my contribution was a review which 
led to improvements in the visual presentation of figure 4, the correction
of some errors and inaccuracies as well as other minor changes to the text.

In the papers with Filippo Santoliquido, my main role was in the interpretation
of results. He performed the injections and drafted the 
text. Furthermore, it is tricky to identify any conceptual contributions as mine alone, 
since the understanding we got for many of the aspects at hand came though 
discussion between the two of us.
I developed the theoretical Bayesian framework for the classification of 
binaries in our "Classifying binary black holes" 2024 paper.
I drafted parts of the text (_e.g._ section IV.B 
of the "Fast and accurate PE" 2025 paper, sections 2.5 and 4.2 of the 
"Classifying binary black holes" 2024 paper) and edited all of it.
Similarly, though the figures were all drafted by Filippo, 
I provided feedback on all of them, though I did not practically edit them
as we were not working on a shared repository.
To be sure, I consulted with him and he agrees on this description.

Regarding the recent work (Iacovelli et al 2025) on parameter estimation with LGWA for a
GW231123-like system, my main contribution consisted in providing 
cross-checks on the validity of the geocentric approximation; 
this was practically reflected in me writing the last paragraphs of section II.B.
Furthermore, I helped tighten the text, make minor modifications to the figures,
and check the data release.

Futhermore, though you did not specifically ask for it, I can add information 
about what I did for some other papers mentioned.
In Cozzumbo et al (2023), the "Opportunities ans limits" paper, I helped develop
a more accurate model for lunar dust, and authored section V as well as figures 9 through 12.
For the GWFish paper (Dupletsa et al 2023) and the "Validating Prior-informed Fisher-matrix Analyses" 
paper (Dupletsa et al 2025), my primary contribution was in the development of 
the GWFish code.
I did also edit the text and help in the interpretation of results.
In the "Revisiting GW150914" paper (Gamba et al 2025), besides writing the waveform interface,
I coauthored figures 5 and 6 and edited the text.

## Sec 2: Statistical Methods: 


- Figure 2.1: There are no axis labels on this plot – it would be useful to an unfamiliar reader if these could be added.

I added axis label here.

- 2.1.1.2: in the equation for wi it might be helpful to explain why the evidence can be neglected.

I added a comment on why we can avoid including the evidence in the equation, 
and also how the weights provide us with an estimate for it.

- 2.1.2-3: I really enjoyed these sections! I would appreciate a little more clarity around how the plots were generated though. Were posteriors obtained through some injection study? Or were simple draws from different distributions used? (I would assume the latter, but it is not clear.) This section also has inconsistent notation for the likelihood and prior than the surrounding sections – unless there is a good reason for this, please make the notation consistent.

I added more details on how the pp plots were generated - this was helpful, since it allowed me to simplify and clarify the setup, I believe it now reads much better.

Also, I made the notation on likelihoods and priors consistent in section 2.1.4, and add a clarification on the meaning of $Z(d)$, which appears in the derivation of the Bayes Factor.

- The last paragraph in Sec 2.1 took me a little while to parse. I think it should be made clearer that here the “baseline model” corresponds to model 1 in Eq 2.4.

I clarified what "baseline" and "deviation" mean here.

- Fig 2.12: It might be nice to include a horizontal line on this plot before $-log X = 4$ to guide the reader’s eye in assessing whether horizontal slices of the ensemble are thinner when we have more live points.

Very good idea! I added errorbars based on the one sigma interval as computed from the distribution of curves.
Furthermore, I changed the comparison from 50 vs 100 live points to 25 vs 100: this way, there is a factor 2 between the standard deviation, which is clearer.
I also took the occasion to make the plot slightly more colorful and appealing.

- 2.2.3.1: The statements “this seems restrictive at first glance, but does not actually constrain the class of models we can consider” and “this restricts the  space of useable priors” seem contradictory. Please clarify.

Indeed, the discussion was incomplete and unclear. 
"The class of models we can consider" in theory is larger than "the space of useable priors" we can sample from in practice with existing computational methods. 
I rephrased a large fraction of this section, making the distinction clearer, and introducing some detail on how one might work with a non-separable prior.

- 2.2.7.1: “depending on what is the quantity we are more interested in evaluating” sounds a bit clunky, perhaps rephrase as “depending on the quantity  we are most interested in evaluating”. 

Agreed, I changed it.

- The Pareto front has not been introduced or defined, please include a footnote or similar for more information on this.

I added a footnote with a brief definition of the Pareto front.

- The placement of the reference in the final sentence in this section is also awkward, please move it to the end of the sentence.

Done.

- 2.3.1: I believe “distribution” should be “distributions” in the first sentence. The $\mathcal{L}$ used in the loss function in e.g., Eq 2.6, Eq 2.7 could be confused with the likelihood defined in earlier sections, please use a different notation for the loss function. 

I corrected the first typo, and switched to the full term "loss" for the equations. 

- The Dax et al. [51] reference should be \citep rather than \citet.

Fixed (though the syntax for me is slightly different, I'm not directly writing in LaTeX).

- 2.3.3.2: “2.5 an 0.3”  “2.5 and 0.3”. The last sentence in this section ends should end with a full stop rather than with a comma.

Fixed.

- 2.4.1.2: “an year”  “a year” or “one year”

Fixed.

##  Sec 3: Gravitational wave parameter estimation

- Note 4: It would be helpful to include a brief description of aliasing at the end of this note.

Done.

- Fig 3.3: Contrary to naïve expectations, the amplitude of the maximum likelihood and reconstructed signals in the middle panel do not drop to 0 after the ringdown of GW250114. It would be helpful to an unfamiliar reader to explain why this happens.

I added a note on how this is an artefact of the filtering procedure.

- 3.2: “…reached a value higher than 75…” – why not quote the exact measured SNR?

I wanted to stick to information explicitly given in the detection paper, and "77 to 80" somehow did not sound right to me when I wrote that.
I have switched to this, though, since it more closely matches what we reported in the paper.

- 3.2.1: “This is useful information in the context of forecasting, i.e., estimating the number of detected signals by some detector that is not yet operational”. This is not the only time that forecasting would be employed: it is also used when, e.g., designing detector upgrades that change noise sensitivity curves of existing detectors; seeing how detection rates change if new detectors are added to the existing network; estimating how many detectable mergers a given compact binary merger formation channel might produce in existing detectors; and so on. Please change the “i.e.” to an “e.g.” or expand the given statement into a list of all cases where forecasting might be useful.

I'm not sure where the "i.e." came from, I simply meant "forecasting the number of detected signals". Sorry about that. Fixed now.

- With an SNR threshold of 8, the FAR for BBHs is found to be 5500 per year in  O1. This is very high. The author then says that “values in the range of roughly 8 to 12 will be sufficient”. It would be helpful to explain a bit more when a threshold of 8 is appropriate and when it is not, perhaps also describing the thresholds that were used in the first detection.

This is the first comment in this review where I would like to stand by what I wrote. 
This paragraph is dedicated to forecasting the detection statistics of future instruments. 
Determining when a given threshold is appropriate or not is ultimately 
something that depends on the actual detector data, which we 
do not have access to for a future detector.

5500 per year is very high, 1 per 100 years is very small. 
The argument here is that we can get these FAR values with SNR thresholds that are within tens of percent
of each other, meaning that something like a horizon distance or a BNS range can be
forecasted without a large uncertainty contribution from the choice of this threshold.

In any case, I added a paragraph here with some further discussion 
of FAR thresholds, including examples from O4, which hopefully clarifies my point.

- 3.3.1: “The formulation given here works well in the absence of orbital  precession” – I assume this means spin-induced precession? I think it will also break down for eccentric waveforms – please add a note about this too.

Indeed, noted. To my knowledge this is fairly unexplored territory. 

- 3.3.2: When introducing reduced order quadrature, please cite Canizares et al: https://ui.adsabs.harvard.edu/abs/2015PhRvL.114g1104C/abstract

Done.

##  Sec 4: Tests of General Relativity with GW250114


- I am once again confused as to why the author states “the signal to noise ratio was higher than 75” rather than stating the measured value?

As mentioned before, changed to the range we reported in the paper.

- “what can be gleamed” -> “what can be gleaned”

Corrected.

- “signal’s amplitude” -> “signal amplitude”

Corrected.

- Fig 4.7: Some elements of this figure are not explained in the text or the caption. What is the orange vertical band in the tope panel representing (the cutoff time for the inspiral analysis)? What does the dotted line in the bottom panel show? I am assuming the lighter grey vertical region in the bottom panel is excluded by energy conservation, is that correct? How is the “full signal measurement” band obtained and why is that not the main result being presented here?

I added more detail on these aspects, as well as a brief argument for the energy conservation limit.

##  Sec 5: Intrinsic parameters and waveform modelling

- 5.1: The Blanchet citation should be a \citep rather than a \citet.

Corrected.

- 5.1.2: SPA and FD are not defined, please expand and define them at their first  use.

I expanded both, didn't really need to abbreviate them here.

- 5.1.3: “importanto” -> “important”

Corrected.

- 5.2: “Qualitatively, Xeff was slightly negative while Xp was small”. I think the figure (Fig 5.3) shows that Xeff gets more negative with higher Xp. Initially I thought this statement was contradictory to this trend, but I think I understand the intention behind the statement: the figure is showing a restricted range of Xp and Xeff, and in qualitative terms, Xeff was constrained to be slightly negative, while Xp was constrained to be small. It might be worth clarifying this statement and the fact that the range of the plot is restricted. It might also be interesting to comment on why the trend of more negative Xeff for higher values of Xp arises.

I think my usage of "while" was confusing here. I used it to mean "and", essentially just referring to the two marginals and not to the correlation, but I can see 
how that might not come have across. 
I switched to "and", and added a note about the restricted range.

- 5.3: As we enter the eccentricity section I am reminded to encourage the author to clarify “spin-precessing” instead of “precessing” whenever spin-induced precession is mentioned. This is particularly important when talking about eccentric systems, which also experience orbital precession of a different kind. This is a comment that should be addressed throughout the whole thesis, not just this section.

I went through the whole thesis and clarified every instance of this imprecise language.
Interestingly, this section contained the one instance where I was actually referring to perihelion precession for eccentric systems and not spin precession.

- “semilatus rectus” -> “semilatus rectum”

Corrected.

- “peaks and trophs” -> “peaks and troughs”

Corrected.

- 5.3.1: When evolving the eccentricity posterior backwards in time, were variations in the spin of the binary included? Please also cite here Fumagalli et al https://ui.adsabs.harvard.edu/abs/2024PhRvD.110f3012F/abstract, where the issue of unmeasurable eccentricity as a systematic uncertainty on the earlier properties of the black hole binary, and therefore their formation channel, is explored in detail.

They were not included, and I think that's implicitly mentioned already 
(I write that the backward evolution is performed through Peter's equations,
and spin is not accounted for in those).
However, I added a comment after that sentence, explicitly mentioning 
the possibility of evolving spin-precession backward and citing Giulia's paper.

- When discussing the meaning of the prior on eccentricity, please cite Clarke et al. https://ui.adsabs.harvard.edu/abs/2026arXiv260518742C/abstract, which explores the sometimes surprising implications of different commonly-used priors in eccentricity in detail.

Agreed - I really liked that paper, and I also discussed it with Teagan 
when it was circulated (I'm in the acnowledgements!).
It wasn't out when I was writing that section, but I am adding it now.

- Please describe why a reference frequency of 13.33 Hz was chosen.

This was actually already in the thesis, as footnote 6 on page 88.

- There is some inconsistency in this section between eccentricity written as “e” and written as “e_13.33Hz”. For example, in the definition of the prior (“uniform in e”, “log-uniform prior p(e)”…) e is used while in the final paragraph e_13.33Hz is used. I think e_13.33Hz should be used in all of these cases, but please make them consistent.

I made these consistent. 
The one mention of $e$ which should not have the 13.33Hz label is the one discussing the value in the decihertz band.

- 5.4: “This deformation enhances the gravitational attraction between the two objects, but it is only effective at relatively short separations: the net effect, therefore, is to leave the early inspiral almost unchanged, while accelerating its late stages”. Since the previous section talked about eccentricity, the question naturally arises as to how tidal deformability would affect the inspiral in an eccentric system, where shorter separations can be reached earlier in the inspiral. Could a short comment on this be added here? The tidal field in the static case is described, but nothing is mentioned about the dynamical case. It might benefit the thesis to add just a short commentary on dynamical tides.

I added a discussion on dynamical and high-order tides.

- 5.5: References should be added for Numerical Relativity surrogate and phenomenological waveform models.

I was not referring to any specific waveform model here, only to the broad approaches.
I added references for examples of an NR surrogate, a phenomenological model, and a self-force model.

- Throughout the various subsections here, it would be worth clarifying which waveform models discussed are inspiral-only (e.g, TaylorF2) vs full inspiral- merger-ringdown. Other differences in physics contained could also be higher- order modes.

A description of how the EOB approach can provide IMR waveforms was already present; 
I added a specification of the fact that TF2 is not. 
Also, I added a note on HOM content - PN waveforms with HOM content do exist, so 
this is not a fundamental difference between the approaches considered here.

- 5.5.1: “Post-Newtonian templates”: I think this should be “Post-Newtonian waveform models”? Typically “templates” refer to specific instances of generated waveforms (for example, in a matched-filter search you will find the best-matching template as the waveform instance with the highest SNR).

Good point, I fixed this.

- 5.5.2: “Post-Netwonian” -> “Post-Newtonian”

Fixed.

- There seems to be an error formatting a reference: I see “`@gambaRevisitingGW150914Nonplanar2025`” after “their waveforms need to be computed in the time domain” and reference 108.

Fixed.

- Fig 5.11: In the legend I see some names that clearly refer to waveform models, but it is not clear what the labels with various numbers x N refer to, please clarify this.

These are linear fits to the waveform evaluation time.
I clarified it in the caption.

##  Sec 6: Extrinsic parameters and signal projection 

- Note 7: There is an unfinished sentence: “The formulas given here are again from”. Also, “GW” has not actually been defined and “gravitational waves” is used throughout the majority of the thesis, so I suggest expanding it here.

Done for both. I removed that sentence - I don't quite remember what I was trying to say and it does not seem necessary.

- 6.1.1.3: I have mentioned this already, but just as a reminder, please wherever “precession” or “precessing” is mentioned, clarify that this refers to spin- induced precession.

Done.

- Fig 6.1: This is slightly small for ease of interpretation, please make this figure about twice as large as it is currently.

Done.

- 6.3: The description of calibration here is quite limited. It would improve the thesis to expand this description (perhaps with an illustrative plot), and also make reference to the recent astrophysical calibrations enabled by GW observations: https://arxiv.org/pdf/2605.11703.

I added some more discussion on this, as well as plots showing
the calibration envelopes for GW250114 and GW250207,
and the PE bias resulting from neglecting 
calibration uncertainty for these two events.

- 6.4.1: Here e is used as a unit vector, but e was also used earlier as eccentricity. I appreciate that this is a problem with conventions using the same letter, but the fact that a previously defined notation is now changing should be explicitly noted.

I changed the letter for the unit vector to l.

Furthermore, in this section I made some improvements to the figure showing the options for luminosity distance priors.

## Sec 7: Einstein Telescope

- “current ground-based detectors”: ground-based does not need to be specified, since all current detectors are ground-based.

Corrected.

- “two main proposed designs for it”: the last two words can be removed from this sentence for a smoother read.

Modified.

- Cosmic Explorer is mentioned once on p68, but never in the section on Einstein Telescope, which is surprising since they are very comparable instruments that may be concurrent. Many of the challenges faced for ET data analysis will be relevant for CE data analysis, for example. Please add a sentence or two in the introduction to Sec 7 on Cosmic Explorer, its similarities and differences from ET, and why the focus here is on ET only.

I added a paragraph on Cosmic Explorer.
The honest answer to "why the focus is on the ET" is that I did my PhD in Italy; 
still, only some of the results shown generalize to Cosmic Explorer, since 
many of them are specifically dependent on the geometry of the Einstein Telescope.

- 7.1: “that of only one signal being present in the data”: specifically, the assumption is that there is only one signal in the data segment being analysed. We hope, and know, that there are many more signals in the data overall!

Clarified.

- Fig 7.2: The text on this figure is too small to read comfortably, please either increase the text size or increase the figure size. 

I removed the figure.

- Fig 7.2, 7.3, 7.4: These are all produced by Filippo Santoliquido. Is it possible to replace these with figures produced by the author? Other figures not produced by the author are taken from publications, but it seems unusual to have figures produced specifically for the thesis that are not produced by the author.

Done (actually only for figures 7.3 and 7.4, I removed figure 7.2).

- Figs 7.6 and 7.7: Text is a bit too small to read comfortably in the figure legends here, please make this text larger. The meanings of the different detector combinations described in the figure legends are not defined, please defined these (e.g., “2L A”, “2L MisA”, “LHI”, “CE”….)

I do not have easy access to the data required to reproduce these figures,
so I did not modify them. While they were produced with a different page format 
in mind, I believe that (after making them larger) they are sufficiently clear.

I did define the detector combinations in the text.

- 7.2: “misaligned 2L configuration is more in constraining sky position”: there is a word missing in this sentence. More what?

I rephrased the sentence.

- 7.2.1: “For the many of the expected CBC sources” -> “For many of the CBC sources”

Rephrased.

- Fig 7.1.2: This figure is too small to read the results comfortably, please make it larger.

I assume this refers to figure 7.12. I made it larger.

## Sec 8: Lunar Gravitational Wave Antenna

- What does being included in the “Reserve Pool of Activities” mean for the Soundcheck mission? Will it go ahead? It sounds exciting!

As far as I know, it means that the European Space Agency has recognized the scientific 
validity of the mission, but without a guarantee that it will be possible for it to fly.

So, unfortunately it is not yet known whether it will go ahead, though I definitely hope so!

- “LROC Norther Polar Mosaic” -> “LROC Northern Polar Mosaic”

Fixed.

- Fig 8.5: The space between the figure captions (a) and (b) is not adequate to clearly distinguish which is which, please increase this spacing.

I increased the spacing.

- 8.1.2.1: “For the purposes of the LGWA, these may simply lead to a fraction of the data, as opposed to making the entirety of the data too noisy.” This sentence is unclear to me. Should it be: “For the purposes of the LGWA, these may simply lead to a fraction of the data, as opposed to the entirety of the data, being too noisy”?

There was a missing "being unusable" after "a fraction of the data". I corrected it.

- “ALSEP” has not been defined, please expand the acronym.

Expanded.

- “GWs” has not been defined and “gravitational waves” is used throughout the majority of the thesis, so I suggest expanding it here.

Expanded.

- Fig 8.7 has no vertical axis labels, please add these.

I did not produce this figure, it comes from a textbook.
I added a description of the vertical axis in the caption.

- 8.1.3: Again “GWs” is not defined, please expand.

Expanded.

- Fig 8.13: The text in this figure is too small to read comfortably, please make the text larger.

I updated this figure to the version I used for the paper: it has a larger font and a new panel.

- 8.2.1: “The formation mechanism of the Moon could also be investigated, as is not a settled debate” -> “The formation mechanism of the Moon could also be investigated, as this is not a settled debate”

Fixed.

- The explanation of the isotopic crisis is limited. Why is it hard to explain under the giant impact scenario?

I agree that my phrasing was not clear, I expanded it now.

The idea is that most of the Moon's mass would come from the impactor,
while most of the Earth's mass would be from the original proto-Earth,
so we should expect the isotopic compositions of Earth and Moon
to approximately reflect those of proto-Earth and impactor respectively.

Since these were two independent objects, which presumably formed 
in different regions of the Solar System, they ought to have
different isotopic compositions --- for example, if we look 
at the composition of Mars, it's different from the Earth's. 
Instead, it seems like the impactor and Earth somehow had the 
same composition. That's unlikely!

- 8.2.2.1: GW190521 is described as one of “the edges” of the mass range observed by ground-based detectors, but this is not true since GW231123. Please replace GW190521 in this discussion and in Fig 8.15 with GW231123.

Fair, that figure was made before november 2023, I replaced GW190521 and also added GW250114
so that all the events analyzed in this chapter of the thesis are included.

- It is described that GW231123 would be detectable by LGWA and would accumulate the majority of its SNR on the last day before merger, but the latter point is not explained or illustrated in Fig 8.16. Please describe or include a plot of the SNR accumulation over time.

I included such a subpanel when updating the characteristic strain plot for GW250114.
I would argue that, while the SNR accumulation is not quantitatively shown in fig 8.16, 
its qualitative behaviour can be approximately understood based on that figure, 
as described in the "Noise plotting and characteristic strain" section of chapter 3, 
and as briefly recollected below that figure.

I agree that there are some steps required to go from that figure to a
plot of SNR against time, but all that's being said here is that, visually,
the waveform is significantly above the noise curve (only) in the region between
the labels "1 day" and "1 minute".
I think that the way this corresponds to SNR accumulation over time
under the approximations at hand is adequately explained in the text near the figure.

- The final sentence in this section indicates that IMRIs would be a source for LGWA and observing them would shed light on the formation of IMBHs. Please add additional explanation of how observations with LGWA would shed light on the formation of IMBHs.

I added a paragraph describing how this would work.

- 8.2.2.2: “Mergers of white dwarfs (WDs) are an interesting event” -> “Mergers of white dwarfs (WDs) are interesting events”

Fixed.

- “accurate 3D simulations of this scenario becoming available only recently”: please add a reference to these newly available simulations.

I added the reference.

- “The main limitation in the study of their systems” -> The main limitation in the study of these systems”

Fixed.

- This section is lacking a few references, for example, for WD tidal disruptions creating a signal in the deciHertz band, CCSn exhibiting emission in this band, and detection of the stochastic background requiring seismometers at both poles.

I added references to this section.

- 8.2.3: I am not sure “notorious” is the right work to use for GW170817 and GW250114. “Notorious” typically implies something or someone that is well- known for negative reasons. Perhaps change this to “well-known”.

I wasn't aware of the connotations of that word, thanks.

- “GW170871” -> “GW170817”

Fixed.

- 8.2.3.1: Would a lack of noise realisation not increase the uncertainty on measured parameters? I suggest at least one additional analysis showing the difference in recovery between the zero-noise and realistically noisy case, or at least a stronger argument as to why realistic noise would not impact the posterior width.

I repeated the analysis several times to verify the intuition that the zero-noise case is representative of 
the distribution of cases we could obtain with a realization of Gaussian noise.

The results are in a new section titled "Impact of non-zero Gaussian noise".
In short: Gaussian noise can indeed impact posterior width, but the fluctuations
induced by this effect can go in either direction, both increasing and decreasing
the uncertainty on measured parameters.

I am specifically using the expression "Gaussian noise" and not "realistic noise":
assuming that the LGWA will be simply 
affected by colored Gaussian noise is not realistic.

- 8.2.3.2: The LVK posterior shown in Fig 8.20 is the true posterior, obtained with real noisy data. As mentioned above, since this contains real noise, I think this is quite a different scenario than the zero-noise LGWA simulation. Therefore the posteriors are not directly comparable. Please clarify this, or repeat the simulated analysis on realistically noisy data.

Based on the new results, I would argue that, among the various limitations making my injections 
unrealistic and different from the LVK one, the lack of a noise realization
is a fairly minor one.

Indeed, for several systematic reasons the posteriors we could obtain with the LGWA 
might differ from those in these simulations, as described in the "limitations" section.
Even something as simple as the sky position of the source could be considered such a systematic:
using a different sample from the posterior distribution as opposed to the maximum likelihood one 
could have led to a better or worse localization.

The fluctuations Gaussian noise induces in parameter uncertainties are on the order of 
a few tens or percentage points at most; other systematics could have a much greater effect.
For one, the uncertainty on the effective PSD of the LGWA is already greater than this.

What qualifies as "directly comparable"? 
They definitely represent very different scenarios, and while the LVK results
describe our best estimate of the properties of a real, astrophysical source,
the LGWA and ET results I show represent an estimate of the constraints we _might_ 
obtain on the properties of a similar source, with detectors that may be built in the future.

I would argue that the results _are_ comparable,
as long as we interpret the LVK posteriors as telling us 
how well the two LIGO detectors can currently constrain the properties of a 
GW250114-like source.

In principle I could have repeated the GW250114 analysis by injecting that same maximum-likelihood
point and using Gaussian noise generated with the locally-estimated PSDs for LIGO Hanford and LIGO Livingston.
I do not believe my results would have been significantly different than the real analysis.

- Fig 8.20, 8.21: I believe the delta in “ET-delta” should be the triangle used in earlier notation.

Fixed.

- Fig 8.23 figure caption: two instances of “time 0” -> “time 0 s”

I fixed it.

- Figs 8.24, 8.25: Text is too small to read comfortably, please increase text size in these figures

I increased the font and figure size.

- Fig 8.25: The colours used for the lines are hard to distinguish from the heat map. Please make them clearer by using different colours. Also please explain what they mean in the figure caption.

I was not able to find better colors which would stand out both against a dark and a light 
background. Instead, I gave the orbital tracks and the best localization curve a white outline.
I hope that makes them clear enough.

- 8.3.2: Overall this was one of my favourite sections, very clearly presented with interesting results.

I am making some changes to it: when finishing up the paper I recently
submitted about this we found a (small) issue in the calculations. 
The discussion still holds up qualitatively, but the figures and text have been updated
(and, I hope, clarified).

- The list of injection setups is broken by two pages that each contain one figure. Is it possible to bring this whole list onto the same page for ease of readability?

By adding more material before this section, it happens to now be on one page.

- Fig 8.30: I really like this figure, it shows the difference between the different scenarios explored very effectively! To save the reader having to scroll back to the list that describes these scenarios, could they be recapped in the figure caption?

Added.

- 8.3.3: “doing so for the complete injection, which requires a good amount of resources even with a close-to-optimal frame would be wasteful and lengthy” -> “doing so for the complete injection, which requires a good amount of resources even with a close-to-optimal frame, would be wasteful and lengthy” 

Rephrased as suggested.

- Normally dynesty is in low caps but once it is written as DYNESTY. Please make the stylisation consistent.

Fixed.

## Sec 9: Conclusions

- “grond-based” -> “ground based”

Changed.

