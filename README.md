
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXX.svg)](https://doi.org/10.5281/zenodo.XXXX)

This project contains the evaluated data files for the article
"Stabilization of Ru-Core, Pt-Shell Model Electrodes by Electronic Effects and Electrooxidation Reactions".

[Figures](./Figures/) contains the final figures found in the submitted manuscript and the supporting information.
Among the final PNG, also the SVG files are included which are based on the raw PNG obtained from the data evaluation.

[data](./data/) contains all CSV for the individual traces in the figures including additional traces not shown. Folders with electrochemical data contain the entire measurement file and the subfolders contain the individual cycles.

[scripts](./scripts/) contains various Jupyter notebooks used for creating the figures of the manuscript and the SI. The notebooks also contain various other figures, that might be of interest. The folder also contains a additional code to evaluate the data. Some of the modules and evaluation procedures are not part of the manuscript ([read more](./scripts/README.md)).

## Installation

To explore the content of this repository locally clone the repository:

```sh
git clone git@github.com:DunklesArchipel/pt_ru_core_shell.git
```

The dependencies can be found in the [environment file](environment.yml).
If you have conda or mamba installed you can execute the notebook locally with jupyter.
Replace `conda` with `mamba`, respectively.

```sh
cd pt_ru_core_shell
conda env create -f environment.yml
conda activate pt_ru_core_shell
jupyter notebook
```

Select the respective file in the jupyter file browser and have fun.
