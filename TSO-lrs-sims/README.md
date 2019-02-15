# Simulations of MIRI LRS Time Series Observations

This folder contains the following files:

* tso_lrs_sims_setup.py: a script containing functions to set up the simulation
* MIRI-lrs-TSO-simulations.ipynb: a jupyter notebook that calls the above functions with added background information, runs the simulations and cleans up the output.
* wasp62_(x)_(x)_simconfig.ini: simulation configuration files. these files are created and written out by the sim setup functions, if not already present.
* wasp62_scene.ini: the scene file. this is also created by the sim setup functions, if not already present. the file is called in the simconfig.ini files.
* wasp-62_proposal.aptx: the APT file describing the observations

### Target of the simulated observations

The target used for these simulations is the exoplanet host star WASP-62. Further details are given in the jupyter notebook.

### Instructions

The jupyter notebook contains relevant information to run the simulations. 

### Author

S. Kendrew, sarah.kendrew@esa.int