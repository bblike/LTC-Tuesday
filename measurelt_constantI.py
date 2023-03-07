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

def collect_data(current_setting, next_temp, vinit, step):
    """Connect to devices and make an example measurement"""

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


    t.tset = next_temp



    '''setting voltage and current'''

    psu.set_current = 0.1  # A : write the PSU current setpoint (float, in Ampere units)
    # print('PSU voltage output set to {} V'.format(psu.set_voltage))
    print('PSU current output set to {} A'.format(
        psu.set_current))  # read back PSU current setpoint value and print to terminal
    print('######################################################################')
    # initialise data arrays
    psu.set_voltage = 1.4
    temperature = numpy.zeros(10000)
    voltage = numpy.zeros(10000)
    current = numpy.zeros(10000)
    resistance = numpy.zeros(10000)
    voltage_setting = 1.4
    current_setting = 0.5
    p = 0
    #test the voltage value
    while True:
        if (current_setting-i_dmm.reading) > 0.01:
            voltage_setting += 0.01
        elif (i_dmm.reading-current_setting) > 0.01:
            voltage_setting -= 0.01

    while True:
        if (current_setting - i_dmm.reading) > 0.01:
            voltage_setting += 0.01
        elif (i_dmm.reading - set_current) > 0.01:
            voltage_setting -= 0.01

            temperature[p] = t.temp[0]
            voltage[p] = v_dmm.reading  # *dmm.reading returns the latest reading from *dmm (float, in Volt or Ampere units)
            current[p] = i_dmm.reading

            # print out data on the screen
            #automaticly setting voltage
            resistance[p] = voltage[p] / current[p]  # calculate resistance
            print(p, temperature[p], voltage[p], current[p], resistance[p])  # print to screen
            p += 1



    psu.output_off  # Turn off PSU output at end
    return temperature, voltage, current, resistance


###############################################################################################################################################################


if __name__ == '__main__':
    from os.path import basename
    from sys import argv

    # Deal with parameters passed from commandline to control program execution


    # setting the initial voltage and voltage steps
    Vinit = 0.1
    Vstep = 0.01
    set_current = 0.5
    # setting the temperature range
    object_temp = [80]
    # this line is for a fast testing
    # object_temp = [200]
    # data collection
    for t in object_temp:
        T, V, I, R = collect_data(set_current, t, Vinit, Vstep)


        numpy.savetxt('Tset{}K.dat'.format(t), numpy.c_[
                    T, V, I, R])  # numpy.c_ outputs the data as columns, that you can easily import into other software

    ###############################################################################################################################################################
    """email sending part"""
    mail_host = "smtp.gmail.com"
    mail_sender = "lzjgnh2002@gmail.com"
    mail_license = "zbdnlsqoqrlveppn"
    mail_receivers = ["sample_email@gmail.com"]

    mm = MIMEMultipart('related')

    subject_content = """experiment results Low Temperature conductivity"""
    mm["From"] = "Li Zhejun<lzjgnh2002@gmail.com>"
    mm['To'] = "sample<sample_email@gmail.com>"
    mm['Subject'] = Header(subject_content, 'utf-8')

    current_time = datetime.now()
    body_content = """See attachments
    Experiment finish at {}""".format(current_time)
    message_text = MIMEText(body_content, "plain", "utf-8")
    mm.attach(message_text)
    for t in object_temp:
        for i in range(1, 4):
            file = MIMEText(open('T{}V{}.dat'.format(str(t), str(i)), 'rb').read(), 'base64', 'utf-8')
            file["Content-Disposition"] = 'attachment; filename="T{}V{}.dat"'.format(str(t), str(i))
            mm.attach(file)

    stp = smtplib.SMTP_SSL(mail_host)

    stp.set_debuglevel(1)
    stp.login(mail_sender, mail_license)
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("Email sent Successful!")
    stp.quit()
