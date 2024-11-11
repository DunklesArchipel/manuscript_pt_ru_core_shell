## Content

## Core files

* [scripts](./scripts/): additional scripts and modules related to this project.
* Figures to the article and SI are in found in files on pure [electrochemical data](05_figures.ipynb) and [SXRD data](06_SXRD.ipynb). These also help in identifying the CSV files underlying the plots.

## additional files (not part of the manuscript)

* [00_Smearing_CV_DEMS](00_Smearing_CV_DEMS.ipynb) provides information on possible smearing effects (time delay and signal broadening during the DEMS measurements).
* [01_single_file_explorer](01_single_file_explorer.ipynb) introduces approaches to evaluate the DEMS and CV data, and determine charges in various potential regions. A widget allows exploring the impact of varying the K-factor or the timeshift. Various ways to plot the raw data is included.
* [02_multiple_file_integration](02_multiple_file_integration.ipynb) illustrates how multiple CVs can be evaluated simultaneously, and how possible errors for the timeshift of K-factor can be included in such an evaluation.
* [DEMS_EC_evaluation_BL_corr](DEMS_EC_evaluation_BL_corr.ipynb) illustrates how the original EC and DEMS data was merged. It only works with the raw data which is not included in the repository. The raw data is nevertheless still included as columns in the merged output files in the [data folder](../data/).
