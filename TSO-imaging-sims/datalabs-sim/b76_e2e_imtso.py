import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import astropy.io.fits as fits

import jwst
from jwst.pipeline import Detector1Pipeline, Image2Pipeline, Tso3Pipeline, collect_pipeline_cfgs
from jwst.associations.asn_from_list import asn_from_list
from jwst.associations.lib.rules_level2_base import DMSLevel2bBase
from jwst.associations.lib.rules_level3_base import DMS_Level3_Base
import jwst.datamodels as datamodels

import pysiaf


import pdb


# In this script we will run the simulated MIRI TSO imaging data through the pipeline. 
# First step is to performa few header checks and modifications if needed. This is because of some MIRISim limitations.

# This script should be run in a conda environment with the JWST pipeline and package pysiaf installed

def checkheaders(model):
	
	# check that the data have the correct header keywords
	# input is a JWST datamodel
	
	if model.meta.visit.tsovisit != True:
		model.meta.visit.tsovisit = True
		#print('Setting TSOVISIT keyword')
	
	# check that CRPIX1 and CRPIX2 are set to the center of the siaf aperture for the array being used.
	array_cfg = model.meta.subarray.name
	#print('Data uses {0}'.format(array_cfg))
	
	siaf_ap = 'MIRIM_' + array_cfg
	siaf = pysiaf.Siaf('MIRI')
	ap = siaf[siaf_ap]
	# Now set the crpix keywords to the right value we take from the Siaf
	model.meta.wcsinfo.crpix1 = ap.XSciRef
	model.meta.wcsinfo.crpix2 = ap.YSciRef
	#print(model.meta.wcsinfo.crpix1, model.meta.wcsinfo.crpix2)
	
	# also set these coordinates in another attribute of the model
	model.meta.wcsinfo.siaf_xref_sci = ap.XSciRef
	model.meta.wcsinfo.siaf_yref_sci = ap.YSciRef
	
	# we also need to add a couple of attributes for the TSO photometry step.
	nints = model.meta.exposure.nints 
	model.meta.exposure.integration_start = 1
	model.meta.exposure.integration_end = nints
	
	return model
	
	
def load_data(sim_dir=None):
	
	# pass a simulation name and the function will go into that directory
	data_file = glob.glob(sim_dir+'/det_images/*.fits')
	#print(data_file)
	
	assert(len(data_file)==1), "More than 1 datafile found - check"
	
	mod = datamodels.open(data_file[0])
	
	return mod
	
	
#######################################################################################################	


# find the directories and load the data into models and get the data pipeline-ready
sim_dirs = glob.glob('*imtso*mirisim*')
print('found mirisim directories: {0}'.format(sim_dirs))

mods = []
subarr = []
odirs = []

for sd in sim_dirs:
	# note there should only be ONE datafile per folder. the load_data function checks for this.
	mod = load_data(sim_dir=sd)
	sub = mod.meta.subarray.name
	subarr.append(sub)
	
	# check the headers and make changes to make the data pipeline-ready
	modmod = checkheaders(mod)
	mods.append(modmod)
	
	pdb.set_trace()
	
	# create an output directory in each sim directory to hold the pipeline products
	outdir_name = '{0}/pipe_out_{1}/'.format(sd, jwst.__version__)
	if not os.path.exists(outdir_name):
		os.mkdir(outdir_name)
	odirs.append(outdir_name)

# sanity check
print(mods)
print(odirs)
print(subarr)
	

# ensure the configuration files are available
if not os.path.exists('cfg_files/'):
	os.mkdir('cfg_files/')
	cfgs = collect_pipeline_cfgs.collect_pipeline_cfgs(dst='cfg_files/')

# run detector1 pipeline
det1s = []
dimods = []
im2mods = []
im3mods = []

for mm, od, sarr in zip(mods, odirs, subarr):
	det1 = Detector1Pipeline.call(mm, config_file='cfg_files/calwebb_tso1.cfg', save_results=True, output_dir=od, steps={"jump": {"rejection_threshold": 10.}})
	det1s.append(det1)
	# now identify the filename of the rateints file, which is the one we want to continue with. load into a model and add to list.
	di = det1.meta.filename.split('.')[0]+'ints.fits'
	dimod = datamodels.open(od+di)
	dimods.append(dimod)
	
	# run the Image2Pipeline
	im2 = Image2Pipeline.call(dimod, config_file='cfg_files/calwebb_tso-image2.cfg', save_results=True, output_dir=od)
	im2mods.append(im2[0])
	
	pdb.set_trace()
	
	
for ii, od, sarr in zip(im2mods, odirs, subarr):	
	# create an association file for the TSO3 Pipeline
	asn3_files = [od+ii.meta.filename]
	asn_fname = 'tso3_tsoim_{0}_asn.json'.format(sarr)
	asn3 = asn_from_list(asn3_files, rule=DMS_Level3_Base, product_name=asn_fname.split('.')[0])
	with open(asn_fname, 'w') as fp:
	    fp.write(asn3.dump()[1])
	
	im3 = Tso3Pipeline.call(asn_fname, save_results=True, output_dir=od)
	im3mods.append(im3)




	
	
		

