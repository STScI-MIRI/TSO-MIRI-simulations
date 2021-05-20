#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '')


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from mirisim.config_parser import SimulatorConfig
from mirisim import MiriSimulation
import tso_img_datalabs_sim
from tso_img_datalabs_sim import wasp103_scene, wasp103_sim_config

from importlib import reload


# In this notebook I'm going to generate simulated MIRI time series imaging data, to provide as test set for ESA Datalabs. To install Mirisim, see the [the public release webpage](http://miri.ster.kuleuven.be/bin/view/Public/MIRISim_Public). The target for the mock observations is WASP-103, an exoplanet host star with the following properties from [the exoplanet encyclopaedia](http://exoplanet.eu/catalog/wasp-103_b/):
# 
# * spectral type F8V
# * T_bb = 6110 K
# * V = 12.0, K = 10.7
# 
# K magnitude of 10.7 corresponds to a flux of 32.5 mJy or 32.5e3 microJy.
# 
# Using the ETC, I calculated the following number of groups for a high-SNR but unsaturated image:
# * FULL array: NGROUPS = 5
# * SUB64 subarray: NGROUPS = 60
# 
# We want to simulate a medium length exposure in both FULL and SUB64 subarras. In total that's 2 simulations.
# 
# 
# | Sim no | Array   | NGroups  | NInt   | NExp   | Exp time |
# | -------|---------| ---------|--------|--------|----------|
# |1       |FULL     |  5       | 200    | 1      | 0.77 hr  |
# |2       |SUB64    |  60      | 600    | 1      | 0.85 hr  |
# 
# ### Steps in setting up the simulation
# 
# This notebook will go through the following steps:
# 
# * Create the scene
# * Set up the simulation
# * Run the simulation
# 
# Each step has its own function. Steps 1 and 2 will each write out a .ini file, which will be used as input for the final step.

# In[3]:


arr = ['FULL', 'SUB64']
ngrp = [5, 60]
nints = [50, 600]
#nints = [1, 1]


# ## Step 1: Creating the input scene (WASP-103)
# 
# Here we'll create the input scene for the simulations using the function wasp103_scene(). Arguments:
# 
# * scene_file: the filename for the .ini file
# * write_cube: write the scene image out to a FITS file (optional; default=False)
# 
# The function returns a mirisim.skysim.scenes.CompositeSkyScene object.
# 

# In[4]:


scene_ini = wasp103_scene(scene_file='wasp103_scene.ini', write_cube=False)


# In[5]:


print(scene_ini)


# ## Step 2: Configuring the simulation
# 
# Now I'll set up the simulations and prepare to run them. I'll set it up to loop through the 2 simulations. For this I wrote the function wasp103_sim_config. Check the docstring for descriptions and default values of the arguments. 
# 
# The function will write out another .ini file containing the simulation configuration, and it returns the output filename for further use.

# In[6]:


#reload(tso_img_sims_setup)
#from tso_img_sims_setup import wasp103_sim_config

for (a, g, i) in zip(arr, ngrp, nints):
    sim_ini = wasp103_sim_config(mode='imaging', arr=a, ngrp=g, nint=i, nexp=1, filt='F770W', 
                   scene_file=scene_ini, out=True)
    print(sim_ini)


# ### Step 3: Run the simulation
# 
# In the following step we'll run the simulations for the 6 different cases. For each run, we need 3 input files: the scene, the simulation configuration, and the simulator setup file. The first and last of these remain the same for each run, and we loop through the list of 6 simulation config files.
# 
# After the simulation has run, the code renames the output directory to include the simulation settings to the directory.
# 

# In[10]:


cfg_files = glob.glob('*_simconfig.ini')
print(cfg_files)


# In[11]:


# configure the simulator engine - this requires no editing from the default
simulator_config = SimulatorConfig.from_default()

for f in cfg_files[:1]:
    tmp = f.split('.')
    fcomps = tmp[0].split('_')
    sim = MiriSimulation.from_configfiles(f)
    sim.run()
    outdir = sorted(glob.glob('*_*_mirisim'), key=os.path.getmtime )[-1]
    new_outdir = 'wasp103_imtso_{0}_{1}_{2}'.format(fcomps[1], fcomps[2], outdir)
    os.rename(outdir, new_outdir)
    print(outdir, new_outdir)


# ### Step 3: Minor housekeeping to make the sim pipeline-ready
# 
# To make the MIRISim data ready for the TSO-specific pipeline, we have to make a couple of small changes to the data:
# 
# * add the TSOVISIT = TRUE to the primary header
# * make sure the 
