import numpy as np
import matplotlib.pyplot as plt
import pdb

from mirisim.skysim import Background, sed, Point, Skycube
from mirisim.skysim import wrap_pysynphot as wS

from mirisim.config_parser import SimConfig, SimulatorConfig, SceneConfig
from mirisim import MiriSimulation


# this script will create a scene file for WASP-62, which is my test case for simulated TSO data. this is a simple point source, 
# and can approximate with a BB source of T=6250, normalised to K=8.944 (abmag in bessel K)

# initialise the point source:
star = Point(Cen=(0,0), vel=0.)

# enter the BB parameters into a dictionary. flux should be given in uJy. read this off from the ETC curve; BB source with T6250  normalised to K=8.944
bbparams = {'Temp':6250., 'wref': 10, 'flux': 73e3}
bb = sed.BBSed(**bbparams)

# set the star's SED to this blackbody SED
star.set_SED(bb)

# now write out to a FITS file
fov = np.array([[-5, 5], [-5,5]])
spat_samp = 0.05

# now we can add a background if requested:
bg = Background(level='low', gradient=0., pa=0.)
scene = star + bg    

# write some output
#print(scene)
    
#scene.writecube(cubefits='wasp-62/wasp62_scene.fits', FOV=fov, spatsampling=spat_samp, wrange=[5., 15.], wsampling=0.05,  clobber=True, time=0.0)

# now we also want to create the ini file
targetlist = [star]

## export to ini file -- THIS DOESN'T WORK AS DESCRIBED IN THE JUPYTER NOTEBOOK
scene_config = SceneConfig.makeScene(loglevel=0,
                                    background=bg,
                                    targets = targetlist)
scene_config.write('wasp-62/wasp62_scene.ini')
pdb.set_trace()

#Set up the simulation
sim_config = SimConfig.makeSim(
    name = 'wasp62_slitless_simulation',    # name given to simulation
    scene = 'wasp62_scene.ini', # name of scene file to input
    rel_obsdate = 1.0,          # relative observation date (0 = launch, 1 = end of 5 yrs)
    POP = 'IMA',                # Component on which to center (Imager or MRS)
    ConfigPath = 'LRS_SLITLESS',  # Configure the Optical path (MRS sub-band)
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
    ima_exposures = 1,          # number of exposures
    ima_integrations = 1,       # number of integrations
    ima_frames = 100,             # number of groups (for MIRI, # Groups = # Frames)
    ima_mode = 'FAST',          # Imager read mode (default is FAST ~ 2.3 s)
    filter = 'P750L',          # Imager Filter to use
    readDetect = 'SLITLESSPRISM'         # Portion of detector to read out
)

sim_config.write('wasp-62/wasp62_simulation_G100I1E10.ini')
