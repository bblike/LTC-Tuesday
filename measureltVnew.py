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
from datetime import datetime
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header


###############################################################################################################################################################

def collect_data(n_pts, next_temp, vinit, step):
    """Connect to devices and make an example measurement"""

    try:
        itc = MercuryITC('COM4')  # Oxford Instruments Mercury ITC temperature controller: PI USB-to-serial connection COM3
        print(itc.get_identity())  # Prints ITC device identity string to terminal
        t = itc.temperature_modules[0]  # temperature board
        h = itc.heater_modules[0]  # heater power board

        psu = TenmaPSU(port='COM3')  # Tenma programmable power supply: USB-to-serial connection COM5
        # psu = TTiPSU('COM3') # TTi programmable power supply: USB-to-serial connection COM3
        print(psu.get_identity())  # Prints PSU device identity string to terminal

        # DMMs on National Instruments GPIB-USB-HS GPIB interface
        v_dmm = K2000(address=16, board=0)  # GPIB adaptor gpib0, device address 16
        print(v_dmm.get_identity())  # Prints DMM device identity string to terminal
        v_dmm.write(":SENS:FUNC 'VOLT:DC'")  # configure to dc voltage

        i_dmm = K2000(address=26, board=0)  # GPIB adaptor gpib0, device address 26
        print(i_dmm.get_identity())  # Prints DMM device identity string to terminal
        i_dmm.write(":SENS:FUNC 'CURR:DC'")  # configure to dc current
    except:
        print('Connecting error, data failure')

    try:
        '''Part for testing if the temperature close to set temperature'''
        t.tset = next_temp
        print('Temperature setting to {} {}'.format(t.temp[0], t.temp[1]))
        # set temperature to objective temperature and wait for enough time
        # until it reach close to objective temperature for enough time
        flag = 0
        while True:
            # read in the temperature setpoint. t.tset returns a tuple containing the latest
            # temperature reading(float) as element 0 and unit(string) as element 1
            temp = t.temp[0]

            # loop until stable
            if (temp - next_temp) < 0.5 and (next_temp - temp) < 0.5:
                flag += 1
            else:
                flag = 0
            sleep(1)
            if flag > 30:
                break
    except:
        print("Temperature setting error at T={}K".format(next_temp))
        # print to screen
    try:
        '''setting voltage and current'''
        # psu.set_voltage = 0.1
        psu.set_current = 0.1  # A : write the PSU current setpoint (float, in Ampere units)
        # print('PSU voltage output set to {} V'.format(psu.set_voltage))
        # print('PSU current output set to {} A'.format(psu.set_current)) # read back PSU current setpoint value and print to terminal

        # initialise data arrays
        temperature = numpy.zeros(n_pts)
        voltage = numpy.zeros(n_pts)
        current = numpy.zeros(n_pts)
        resistance = numpy.zeros(n_pts)

        limiter = 0
        counter = 0
        # loop to take repeated readings
        print('Temperature, voltage, current, resistance(from second time)')
        for p in range(n_pts):
            counter = p
            # psu.set_current=0.002*p #A - current ramp
            #	or
            psu.set_voltage = step * p + vinit  # V - voltage ramp
            print(psu.set_voltage, psu.set_current)
            sleep(0.1)  # pause before taking readings

            '''Take reading'''

            # t.temp returns a tuple containing the latest temperature reading (float)
            # as element 0 and unit(string) as element 1
            temperature[p] = t.temp[0]
            voltage[p] = v_dmm.reading  # *dmm.reading returns the latest reading from *dmm (float, in Volt or Ampere units)
            current[p] = i_dmm.reading

            # print out data on the screen
            if p == 0:
                print(p, temperature[p], voltage[p], current[p])
            if p > 0:
                resistance[p - 1] = (voltage[p] - voltage[p - 1]) / (current[p] - current[p - 1])  # calculate resistance
                print(p, temperature[p], voltage[p], current[p], resistance[p - 1])  # print to screen

            # break when current hit top edge
            if limiter > 3:
                break
            if (1 - current[p]) < 0.05:
                limiter += 1

    except:
        print("Loop went wrong at T = {}".format(next_temp))
        T[counter] = 'NaN'
        V[counter] = 'NaN'
        I[counter] = 'NaN'
        R[counter] = 'NaN'
    finally:

        psu.output_off  # Turn off PSU output at end
        return temperature, voltage, current, resistance


###############################################################################################################################################################


if __name__ == '__main__':
    from os.path import basename
    from sys import argv

    # Deal with parameters passed from commandline to control program execution 
    try:  # sys.argv are the list of commandline arguments that are given to python (sys.argv[0] is the name of the script file)
        n_pts = int(argv[1])
        # output_filename = argv[2]
    except (IndexError,
            ValueError):  # IndexError raised if arguments not supplied, ValueError raised if cast to integer fails: prompt user for correct usage
        raise SystemExit('Usage:s python {} n_pts'.format(basename(argv[0])))

    # setting the initial voltage and voltage steps
    Vinit = 0.1
    Vstep = 0.01

    # setting the temperature range
    object_temp = [80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    # this line is for a fast testing
    # object_temp = [120, 110, 100]
    # data collection
    for t in object_temp:
        for i in range(1, 3):
            T, V, I, R = collect_data(n_pts, t, Vinit, Vstep)
            if len(R) == n_pts:
                print("Data collection complete.")
                failure = ""
            else:
                print("error occurs, file will be marked.")
                failure = "F"
            # Save the data to file.
            if t:
                numpy.savetxt('T{}V{}{}.dat'.format(str(t), str(i), failure), numpy.c_[
                    T, V, I, R])  # numpy.c_ outputs the data as columns, that you can easily import into other software

    ###############################################################################################################################################################
    """email sending part"""
    mail_host = "smtp.gmail.com"
    mail_sender = "lzjgnh2002@gmail.com"
    mail_license = "zbdnlsqoqrlveppn"
    mail_receivers = ["1220047112@qq.com", "lzjgnh2002@gmail.com"]

    mm = MIMEMultipart('related')

    subject_content = """experiment results Low Temperature conductivity"""
    mm["From"] = "Li Zhejun<lzjgnh2002@gmail.com>"
    mm['To'] = "Backup_account<1220047112@qq.com>,Myself<lzjgnh2002@gmail.com>"
    mm['Subject'] = Header(subject_content, 'utf-8')

    current_time = datetime.now()
    body_content = """See attachments
    Experiment finish at {}""".format(current_time)
    message_text = MIMEText(body_content, "plain", "utf-8")
    mm.attach(message_text)
    for t in object_temp:
        for i in range(1, 3):
            file = MIMEText(open('T{}V{}.dat'.format(str(t), str(i)), 'rb').read(), 'base64', 'utf-8')
            file["Content-Disposition"] = 'attachment; filename="T{}V{}.dat"'.format(str(t), str(i))
            mm.attach(file)

    stp = smtplib.SMTP_SSL(mail_host)

    stp.set_debuglevel(1)
    stp.login(mail_sender, mail_license)
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("Email sent Successful!")
    stp.quit()
