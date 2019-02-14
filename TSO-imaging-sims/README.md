# Simulations of MIRI Imaging Time Series Observations

This folder contains the following files:

* tso_img_sims_setup.py: a script containing functions to set up the simulation
* MIRI Imaging Time Series Observations simulations.ipynb: a jupyter notebook that calls the above functions with added background information, runs the simulations and cleans up the output.
* wasp103_(*)_(*)_simconfig.ini: simulation configuration files. these files are created and written out by the sim setup functions, if not already present.
* wasp103_scene.ini: the scene file. this is also created by the sim setup functions, if not already present. the file is called in the simconfig.ini files.

### Target of the simulated observations

The target used for these simualtions is the exoplanet host star WASP-103. This target has a brightness suitbale for observations with both FULL array and the smallest imaging subarray, SUB64. Furtehr details are given in the jupyter notebook.

### Instructions

The jupyter notebook contains relevant information to run the simulations. 

### Author

S. Kendrew, sarah.kendrew@esa.int