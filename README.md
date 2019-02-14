# TSO-MIRI-simulations
Repository to collect scripts and notebooks for generating MIRISim data for Time Series Observations (TSOs)


## Contents of this repository

This repository will be used to collect scripts to generate simulated data with MIRISim for Time Series Observations with MIRI. These data can be used for DMS or pipeline testing purposes. Currently, the following MIRI  modes are supported for Time Series mode:

* Low Resolution Spectroscopy, slitless mode
* Imaging

Simulations will be grouped in dedicated folders:

* TSO-imaging-sims: Simulations for TSO imaging. 
* 

The output format of MIRISim data is compatible with the JWST calibration pipeline.

## Dependencies

The following packages are called in these scripts:

* numpy
* os
* glob
* importlib

The simulations are designed to be run using MIRISim, the publicly available data simulator developed by the MIRI European Consortium. Instructions for installation and use can be found on [this page](http://miri.ster.kuleuven.be/bin/view/Public/MIRISim_Public). Bugs can be reported to mirisim AT roe.ac.uk.

MIRISim is therefore also called extensively in the scripts and notebooks.

## Authors

Sarah Kendrew, sarah.kendrew AT esa.int