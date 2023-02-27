# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 10:26:36 2016
Python3 update v0 Tue Mar 27 2018
Python3 update v0.1 Thu Mar 19 2020
Python3 update v0.2 Wed Sept 14 2022

Data acquisition script for Skills session 3: Introducing automated data acquisition

Requirements:
    level2labs module: in users site-packages directory on computer
    National Instruments NIDAQmx drivers

@author: Aidan Hindmarch
"""

from level2labs.skills import ReadAI, WriteDO
from os.path import basename
from sys import argv
import matplotlib.pyplot as plt
import numpy


#################################################################################
#
# Modify CHANNELs to correct Device number and Channel number 
#                                                             
# e.g.                                                        
#	AICHANNEL = "Dev2/ai1"                                     

AICHANNEL="Dev1/ai0"
DOCHANNEL="Dev1/port0/line0,Dev1/port0/line7"

SAMPLE_RATE = 512 # samples per second
VOLTAGE_RANGE = 10 # V amplitude
#                                   
#################################################################################

                        
def collect_data(duration_s, ai_channels, n_ai_channels, sample_rate, voltage_range=10.0, do_channels=None):
    '''function to collect data - do not modify'''
    print('Collecting data...')
    if do_channels:
        WriteDO(chanlist=do_channels, nchans=2, vals_ndarray=numpy.array([1,0], dtype=numpy.uint8))	# Light up red LED to indicate measurement in progress
    data = ReadAI(duration_s, chanlist=ai_channels, nchans=n_ai_channels, samplerate=sample_rate, vrange=voltage_range)	# Collect and return data
    if do_channels:
        WriteDO(chanlist=DOCHANNEL, nchans=2, vals_ndarray=numpy.array([0,1], dtype=numpy.uint8))	# Light up green LED to indicate measurement complete
    return data


if __name__ == '__main__':  
    
    try:
        duration_seconds = float(argv[1])
        output_filename = argv[2]; print('Saving {} seconds of data to {}\n'.format(duration_seconds, output_filename))
    except (IndexError, TypeError): # IndexError raised if arguments not supplied, TypeError raised if cast to float fails: prompt user for correct usage
        raise SystemExit('Usage: python {} duration_seconds output_filename'.format(basename(argv[0])))
    
    data = collect_data(duration_seconds, AICHANNEL, 1, SAMPLE_RATE, voltage_range=VOLTAGE_RANGE, do_channels=DOCHANNEL)
    
    if output_filename:
        numpy.savetxt(output_filename, data)	
        
    #############################################################################
    #
    # Can comment from here if you like; just prints to console and plots a simple graph. 
    #            
    print(data)
    plt.plot(data, marker='x')
    plt.show()
