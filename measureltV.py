# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:10:15 2016
Python3 update v0 Tue Mar 27 2018
Python3 update v1 Wed Aug 1 2018
update v2 Thu Apr 2 2020

Example script to run low temperature conductivity experiment.

Controls: 
    Keithley 2000 series DMM
    Oxford Instruments Mercury iTC temperature controller
    Tenma or TTi programmable PSU

Requirements:
    level2labs module  (>=2.1.3): In users site-packages directory on computer
    NI GPIB drivers from National Instruments
    pySerial
    
@author: Aidan Hindmarch
"""
from level2labs.rli.lowtemperature import K2000, MercuryITC, TTiPSU, TenmaPSU
from time import sleep
import matplotlib.pyplot as plt
import numpy


###############################################################################################################################################################

def collect_data(n_pts, next_temp=100.0):
    '''Connect to devices and make an example measurement'''
        
   #itc = MercuryITC('COM4') # Oxford Instruments Mercury ITC temperature controller: PI USB-to-serial connection COM3
   # print(itc.get_identity()) # Prints ITC device identity string to terminal
   # t = itc.temperature_modules[0] # temperature board 
    #h = itc.heater_modules[0] # heater power board
    
    psu = TenmaPSU(port='COM3') # Tenma programmable power supply: USB-to-serial connection COM5
    #psu = TTiPSU('COM3') # TTi programmable power supply: USB-to-serial connection COM3
    print(psu.get_identity()) # Prints PSU device identity string to terminal
    
    #DMMs on National Instruments GPIB-USB-HS GPIB interface
    v_dmm = K2000(address=16, board=0) # GPIB adaptor gpib0, device address 16
    print(v_dmm.get_identity()) # Prints DMM device identity string to terminal
    v_dmm.write(":SENS:FUNC 'VOLT:DC'") # configure to dc voltage
    
    i_dmm = K2000(address=26, board=0) # GPIB adaptor gpib0, device address 26
    print(i_dmm.get_identity()) # Prints DMM device identity string to terminal
    i_dmm.write(":SENS:FUNC 'CURR:DC'") # configure to dc current
    
    # read in the temperature setpoint. t.tset returns a tuple containing the latest 
    # temperature reading(float) as element 0 and unit(string) as element 1
   # temp = t.tset 
   # print('Temperature set to {} {}'.format(temp[0], temp[1])) # print to screen
    
    psu.set_voltage = 0.1
    psu.set_current = 0.002 # A : write the PSU current setpoint (float, in Ampere units)
    #print('PSU voltage output set to {} V'.format(psu.set_voltage))
    #print('PSU current output set to {} A'.format(psu.set_current)) # read back PSU current setpoint value and print to terminal
    
    # initialise data arrays
    temperature = numpy.zeros(n_pts)
    voltage = numpy.zeros(n_pts)
    current = numpy.zeros(n_pts)
    resistance = numpy.zeros(n_pts)
    
    # loop to take repeated readings
    print('Temperature, voltage, current, resistance(from second)')
    for p in range(n_pts):
        #psu.set_current=0.002*p #A - current ramp
    	 #	or
        psu.set_voltage = 0.1*p #V - voltage ramp
        print(psu.set_voltage, psu.set_current)
        sleep(0.5) # pause before taking readings
        
        # t.temp returns a tuple containing the latest temperature reading (float) 
        # as element 0 and unit(string) as element 1
       # temperature[p] = t.temp[0] 
        voltage[p] = v_dmm.reading # *dmm.reading returns latest reading from *dmm (float, in Volt or Ampere units)
        current[p] = i_dmm.reading

        if p == 0:
            print(p, temperature[p], voltage[p], current[p])
        if p > 0:
            resistance[p-1] = (voltage[p]-voltage[p-1])/(current[p]-current[p-1]) # calculate resistance 
            print(p, temperature[p], voltage[p], current[p], resistance[p-1]) # print to screen
     
    psu.output_off	# Turn off PSU output at end
    #t.tset = next_temp # set temperture setpoint on ITC to next required value
    #temp=t.tset # read in the temperature setpoint
    #print('Temperature set to {} {}'.format(temp[0], temp[1])) # print to screen
    
    return temperature, voltage, current, resistance


###############################################################################################################################################################


if __name__== '__main__':
    from os.path import basename
    from sys import argv
    import numpy as np
    # Deal with parameters passed from commandline to control program execution 
    try: # sys.argv are the list of commandline arguments that are given to python (sys.argv[0] is the name of the script file)  
        n_pts = int(argv[1])
        output_filename = argv[2]
    except (IndexError, ValueError): # IndexError raised if arguments not supplied, ValueError raised if cast to integer fails: prompt user for correct usage
        raise SystemExit('Usage:s python {} n_pts output_filename'.format(basename(argv[0]))) 
    
    T, V, I, R = collect_data(n_pts)
    
    # Save the data to file.
    if output_filename:      
        numpy.savetxt(output_filename, numpy.c_[T, V, I]) # numpy.c_ outputs the data as columns, that you can easily import into other software
    
    # plot a graph
    #plt.plot(T, '-k', marker='x',label = 'temperature')
    #plt.plot(V, '-b', marker='x', label = 'voltage')
    #plt.plot(I, '-r', marker='x', label = 'current')
    plt.plot(R, '-r', marker='o', label = 'resistance') 
    plt.legend() 
    sumR = np.sum(R[5:10])/5
    print('average resistance is ', sumR)

    plt.show()
