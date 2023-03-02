###############################################################################
Run measureltVnew.py by:
>>> python measureltVnew.py n-pts
where n-pts is the suitable number that holds:
Voltage = 0.01 * n_pts + 0.1
and it will automaticly generate results of measurements.
Files are saved on 3 side, 1 SSD, 1 computer and 1 github program.

##############################################################################
Notes for Shay:
1.Line 1 to 56: connecting devices and pre setting
2.Line 60 to 80: temperature setting, it will pause the experiment until the temperature change to objective temperature
3.Line 81 to 130: setting current and voltage and take reading. Some reference used:
	limiter: reference to break the experiment it current hit the limit of power supply.
	vinit: beginning voltage, value set in line 147
	vstep: voltage step, value set in line 148
4.Line 132 to 168: main part, control the program. Some reference used:
	Vinit: initial voltage
	Vstep: voltage steps
	Object_temp: temperature to be measured at
	n_pts: numbers of data to be tested, need input(The program can automaticly stop running when the current across 0.1A so this number can be as large as possible)
	*Line 156 and line 189 sets the number of experiment to go, range(1,4) means it will repeat 3 times at each temperature.
	*change of these two lines should run together or error would occur. 
5.Line 170 to end: email sending part
	for this part, I use my own email as sender and you only need to change line 174:
		mail_receivers = ["sample_email@gmail.com"]
	and line 180:
		mm['To'] = "sample<sample_email@gmail.com>"
	to replace the email to your own email and replace "sample" to your name. It will generate a email and send to your email account with all data collected.
	If you do not want this function, just delete all after line 170 and it will have no influence to data collection.
6.Code to run this file:
	use command line to go to the path, using following code:
		python measureltVnew.py n_pts
	(you do not need to name the file name, as it will automaticly generate name in form "TxxxVx.dat", with xxx reprecent the Kelvin temperature and x represent the sequence of experiment)


Open for read and communication.

