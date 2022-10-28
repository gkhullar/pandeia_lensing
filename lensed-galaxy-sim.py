'''
Running an ETC calculation on a synthetic lensed galaxy.


INFORMATION:
------------
grating waveon waveoff    z1    z2
G140M/F070LP  0.90   1.27 1.414811 1.535942
G140M/F100LP  0.97   1.89 1.602629 2.773962
G235M/F170LP  1.66   3.17 3.453984 5.329872
G395M/F290LP  2.87   5.27 6.700563 9.523163
G140H/F070LP  0.95   1.27 1.548967 1.535942
G140H/F100LP  0.97   1.89 1.602629 2.773962
G235H/F170LP  1.66   3.17 3.453984 5.329872
G395H/F290LP  2.87   5.27 6.700563 9.523163
PRISM/CLEAR   0.60   5.30 0.609874 9.583067

Note from JRR: "above is cut-on and cut-off redshifts to get both 3727 
                and 5007 in one IFU grating setting, for all the gratings."

'''


import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from pandeia.engine.perform_calculation import perform_calculation
import json
from quickcalc_fluxes import *


# loading in json file from the basic run we set up in the online version
with open('plots-data/gsfc-lensed-galaxy-hack.json') as f:
    setup = json.load(f) # this has one point source object w/5 lines definied


# defining galaxy properties, getting predicted line fluxes
# and redshifted lines returned as dictionary
# command:  galaxy(zz=3.,SFR=1.,Av=1.,magnification=10.)
lines = galaxy(zz=2.5) # using defaults for now

# setting up lines for source
lines_list = []
for i in range(len(lines['names'])):
    filler = {'center':lines['zlines'][i], # redshited line, microns
              'emission_or_absorption':'emission',
              'name':lines['names'][i], # line name
              'profile':'gaussian',
              'strength':lines['fluxes'][i], # predicted flux, cgs
              'width':80} # velocity width, km/s
    lines_list.append(filler)

# adding lines to source setup
setup['scene'][0]['spectrum']['lines'] = lines_list




# -------------------- #
# RUNNING CALCULATIONS #
# -------------------- #


# G140M/F100LP
# ------------
setup['configuration']['instrument']['disperser'] = 'g140m'
setup['configuration']['instrument']['filter'] = 'f100lp'

# performing the calculation
results_g140 = perform_calculation(setup)

# saving certain results to add as text to plot
readout_pattern = results_g140['information']['exposure_specification']['readout_pattern']
total_exp = results_g140['information']['exposure_specification']['total_exposure_time']


# plotting results
plt.figure()

plt.step(results_g140['1d']['sn'][0],results_g140['1d']['sn'][1],where='mid')
plt.text(0.027,0.79,f"G140M/F100LP\n" + f"{readout_pattern}\n"+
        f"{round(total_exp,2)} s", transform=plt.gca().transAxes,fontsize=16)
# plt.xlim(1.2,1.5)

plt.xlabel('wavelength [microns]')
plt.ylabel('S/N')

plt.tight_layout()
plt.show()
plt.close('all')






# # G235M/F170LP
# # ------------
# setup['configuration']['instrument']['disperser'] = 'g235m'
# setup['configuration']['instrument']['filter'] = 'f170lp'

# # performing the calculation
# results_g235 = perform_calculation(setup)

# # saving certain results to add as text to plot
# readout_pattern = results_g140['information']['exposure_specification']['readout_pattern']
# total_exp = results_g140['information']['exposure_specification']['total_exposure_time']


# # plotting results
# plt.figure()

# plt.step(results_g235['1d']['sn'][0],results_g235['1d']['sn'][1],where='mid')
# plt.text(0.027,0.79,f"G235M/F170LP\n" + f"{readout_pattern}\n"+
#         f"{round(total_exp,2)} s", transform=plt.gca().transAxes,fontsize=16)

# plt.xlim(1.8,2.7)

# plt.xlabel('wavelength [microns]')
# plt.ylabel('S/N')

# plt.tight_layout()
# plt.show()
# plt.close('all')
