import numpy as np
import matplotlib.pyplot as plt
import os
import pdb

from mirisim.skysim import Background, sed, Point, Skycube
from mirisim.skysim import wrap_pysynphot as wS

from mirisim.config_parser import SimConfig, SimulatorConfig, SceneConfig
from mirisim import MiriSimulation

# this script will create a scene for simulations of LRS time series observations with MIRI. 
# the setup of the simulation will be captured in a function; the scene is the same for all cases. 
# simulations to perform:
# Array config: SLITLESSPRISM
# Length of exposure: Short, Medium and Long

# the target is WASP-62 a F7 star, Kmag = 8.994 (or 20e3 microJy at 2 um, BBT = 6230 K (from the exoplanet catalog))

def wasp62_scene(scene_file=None, write_cube=False):
	# place a star object in the centre of the field
	
	if scene_file is not None:
		print('Creating scene. Scene will be written to file {0}'.format(scene_file))
	else:
		print('No filename provided. Scene will be written out to file scene.ini')
		scene_file = 'scene.ini'
	
	star = Point(Cen=(0,0))
	
	# enter the BB parameters into a dictionary. flux should be given in uJy. read this off from the ETC curve; BB source with T6250  normalised to K=8.944. reference flux should be given in MICRO-Jy.
	bbparams = {'Temp':6230., 'wref': 2.0, 'flux': 20e3}
	bb = sed.BBSed(**bbparams)

	# set the star's SED to this blackbody SED
	star.set_SED(bb)

	# now write out to a FITS file
	fov = np.array([[-5, 5], [-5,5]])
	spat_samp = 0.05

	# now we can add a background if requested:
	bg = Background(level='low', gradient=0., pa=0.)
	scene = star + bg    

	if write_cube:
		scene.writecube(cubefits='wasp62_scene.fits', FOV=fov, spatsampling=spat_samp, wrange=[5., 15.], wsampling=0.05,  clobber=True, time=0.0)

	# now we also want to create the ini file
	targetlist = [star]

	## export to ini file -- THIS DOESN'T WORK AS DESCRIBED IN THE JUPYTER NOTEBOOK
	scene_config = SceneConfig.makeScene(loglevel=0,
	                                    background=bg,
	                                    targets = targetlist)
	
	if os.path.exists(scene_file):
		print('File {0} already exists. Will be overwritten.'.format(scene_file))
	
	scene_config.write(scene_file)
		
	return scene_file


def wasp62_sim_config(mode='lrs', arr='SLITLESSPRISM', ngrp=None, nint=None, nexp=1, scene_file=None, out=True):
	
	'''
	Function to set up the imaging TSO simulation. Arguments:
	- mode: the MIRI mode to use (default='lrs') [string]
	- arr: array configureation (default='SLITLESSPRISM') [string]
	- ngrp: the number of groups (minimum of 2 required; minimum of 5 is recommended) [integer]
	- nint: number of integrations [integer]
	- nexp: number of exposures (default = 1, as recommended for TSOs) [integer]
	- scene_file: scene filename, as returned by the scene generation function [string]
	- out: set to True if you want to write the sim configuration out to file (default=True)[boolean]
	
	
	Notes on other simulation parameters, as we are only using this function for imaging simulations:
	- POP: always 'IMA'
	- parameters disperser, detector and mrs_* are included in teh list but NOT ACCESSED
	- ima_mode: always use FAST mode for TSOs
	
	'''
	
	if (mode == 'lrs') & (arr == 'SLITLESSPRISM'):
		op_path = 'IMA'
		cfg = 'LRS_SLITLESS'
		filt = 'P750L'
		
	else:
		raise ValueError("This mode is not supported in this function.")
		
	if arr not in ['SLITLESSPRISM']:
		raise ValueError("Array configuration not supported for LRS slitless TSOs.")
		
	if os.path.exists(scene_file):
		print("Found scene file {0}".format(scene_file))
	else:
		raise ValueError('Scene file not found.')
	
	if ngrp < 2:
		raise ValueError("Number of groups must be 2 or larger.")
		
	fbase = scene_file.split('_')[0]
	simname = '{3}_{4}_{0}G{1}I{2}E'.format(ngrp, nint, nexp, fbase, arr)
	
	sim_config = SimConfig.makeSim(
	    name = simname,    # name given to simulation
	    scene = scene_file, # name of scene file to input
	    rel_obsdate = 1.0,          # relative observation date (0 = launch, 1 = end of 5 yrs)
	    POP = op_path,                # Component on which to center (Imager or MRS)
	    ConfigPath = cfg,  # Configure the Optical path (MRS sub-band)
	    Dither = False,             # Don't Dither
	    StartInd = 1,               # start index for dither pattern [NOT USED HERE]
	    NDither = 2,                # number of dither positions [NOT USED HERE]
	    DitherPat = 'ima_recommended_dither.dat', # dither pattern to use [NOT USED HERE]
	    disperser = 'SHORT',        # [NOT USED HERE]
	    detector = 'SW',            # [NOT USED HERE]
	    mrs_mode = 'SLOW',          # [NOT USED HERE]
	    mrs_exposures = 10,          # [NOT USED HERE]
	    mrs_integrations = 3,       # [NOT USED HERE]
	    mrs_frames = 5,             # [NOT USED HERE]
	    ima_exposures = nexp,          # number of exposures
	    ima_integrations = nint,       # number of integrations
	    ima_frames = ngrp,             # number of groups (for MIRI, # Groups = # Frames)
	    ima_mode = 'FAST',          # Imager read mode (default is FAST ~ 2.3 s)
	    filter = filt,          # Imager Filter to use
	    readDetect = arr         # Portion of detector to read out,
	)	
	
	
	# write the simulation config out to file, if out was set to True. the output filename is the simname, followed b the number of groups, ints and exp, for easy reference.
	simout = '{0}_simconfig.ini'.format(simname)
	if out:
		sim_config.write(simout)
	
	# set up the simulator "under the hood". deafult values can be accepted here.
	simulator_config = SimulatorConfig.from_default()
	
	return simout
	
