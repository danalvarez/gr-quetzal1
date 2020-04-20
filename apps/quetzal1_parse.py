#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Adapted from: Copyright 2018 Daniel Estevez <daniel@destevez.net>
# 
# Modification 2019, Dan Álvarez
# Parser for QUETZAL-1 Beacon
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
import pmt
import os
import datetime
import struct

def csp():
	# CSP Header is 4 bytes long

	_format = "L"

	return _format

def identifier():
	# Satellite identifier

    _format = "8s"

    return _format

def cdhs():
	_format = ""

	rtc_hour 			= "B"
	rtc_min				= "B"
	rtc_sec				= "B"
	rtc_day				= "B"
	rtc_month			= "B"
	rtc_year			= "B"
	adm_status			= "B"
	eps_status			= "B"
	htr_status			= "B"
	adcs_status			= "B"
	pld_status			= "B"
	adm_reset_counter 	= "B"
	eps_reset_counter 	= "B"
	adcs_reset_counter1 = "B"			# software reset counter
	adcs_reset_counter2 = "B"			# hardware reset counter
	comm_reset_counter 	= "B"
	reset_counter 		= "H"

	_format = rtc_hour + rtc_min + rtc_sec + rtc_day + rtc_month + rtc_year + adm_status + eps_status + htr_status + adcs_status + pld_status \
	+ adm_reset_counter + eps_reset_counter + adcs_reset_counter1 + adcs_reset_counter2 + comm_reset_counter + reset_counter

	return _format

def eps():
	_format = ""

	# TMP100
	tmp 				= "B"

	# BQ27441 No. 1
	SoC					= "B"
	bat_voltage			= "B"
	ave_current			= "H"
	remaining_capacity	= "H"
	ave_power			= "H"
	SoH 				= "B"

	# INA260 No. 1
	ch1_voltage			= "B"
	ch1_current 		= "H"

	# INA260 No. 2
	ch2_voltage			= "B"
	ch2_current 		= "H"

	# INA260 No. 3
	ch3_voltage			= "B"
	ch3_current 		= "H"

	# Subsystem Currents
	ADCS_current		= "H"
	COMM_current		= "H"
	PLD_current			= "H"
	HTR_current			= "H"
	
	# Overcurrent and Short Circuit Flags
	fault_flags			= "B" 	#bits 0, 1, 2, 3  = overcurrent flags; bits 4, 5, 6, 7 =  short circuit flags.

								# bits 0,4 = ADCS
								# bits 1,5 = COMMS
								# bits 2,6 = PLD
								# bits 3,7 = HEATER

	# Communication and Transmission Flags
	comm_flag			= "B"	# bit0 = INA260 1, bit1 = INA260 2, bit2 = INA260 3, bit3 = BQ27441, bit4 = TMP100
	trans_flag			= "B"	# bit0 = INA260 1, bit1 = INA260 2, bit2 = INA260 3, bit3 = BQ27441, bit4 = TMP100

	_format = tmp + SoC + bat_voltage + ave_current + remaining_capacity + ave_power + SoH + ch1_voltage + ch1_current + ch2_voltage \
	+ ch2_current + ch3_voltage + ch3_current + ADCS_current + COMM_current + PLD_current + HTR_current + fault_flags + comm_flag + trans_flag

	return _format

def adcs():
	_format = ""

	# BNO055 Gyroscope
	gyr_x				= "B"
	gyr_y				= "B"
	gyr_z				= "B"

	# BNO055 Magnetometer
	mag_x 				= "H"
	mag_y 				= "H"
	mag_z 				= "H"

	# ADC No. 1
	ch1_adc1			= "B"
	ch2_adc1			= "B"
	ch3_adc1			= "B"
	ch4_adc1			= "B"
	ch5_adc1			= "B"
	ch6_adc1			= "B"

	# ADC No. 2
	ch1_adc2			= "B"
	ch2_adc2			= "B"
	ch3_adc2			= "B"
	ch4_adc2			= "B"
	ch5_adc2			= "B"
	ch6_adc2			= "B"

	# Temperature Sensors
	bno_temp			= "b"
	tmp100				= "h"

	# Communication and Transmission Flags
	flags    			= "B"	# bit0 = BNO055, bit1 = ADC1, bit2 = ADC2, bit3 = TMP100

	_format = gyr_x + gyr_y + gyr_z + mag_x + mag_y + mag_z + ch1_adc1 + ch2_adc1 + ch3_adc1 + ch4_adc1 + ch5_adc1 + ch6_adc1 \
	+ ch1_adc2 + ch2_adc2 + ch3_adc2 + ch4_adc2 + ch5_adc2 + ch6_adc2 + bno_temp + tmp100 + flags

	return _format

def comm():
	# COMM only returns the package counter, which is in 4 bytes

	_format = "L"

	return _format

def pld():
	_format = ""

	operation 			= "B"
	picture_counter		= "H"

	_format = operation + picture_counter

	return _format

def uvg_message():
	# 27-byte string containing message

	_format	 = "27s"

	return _format

def ram_params():
	# 22 RAM parameters

	cdhs_cycle_time 	= "B"
	cdhs_wdt_time		= "B"
	adm_soc_lim			= "B"
	adcs_soc_lim		= "B"
	comm_soc_lim		= "B"
	pld_soc_lim			= "B"
	htr_cycle_time		= "B"
	htr_on_time			= "B"
	htr_off_time		= "B"
	adm_cycle_time		= "B"
	adm_burn_time		= "B"
	adm_max_cycles		= "B"
	adm_wait_time_1		= "B"
	adm_wait_time_2		= "B"
	adm_enable			= "B"
	comm_cycle_time		= "B"
	pld_cycle_time		= "B"
	pld_op_mode			= "B"
	cam_res				= "B"
	cam_expo			= "B"
	cam_pic_save_time	= "B"
	pay_enable			= "B"

	_format = cdhs_cycle_time + cdhs_wdt_time + adm_soc_lim + adcs_soc_lim + comm_soc_lim + pld_soc_lim + htr_cycle_time \
	+ htr_on_time + htr_off_time + adm_cycle_time + adm_burn_time + adm_max_cycles + adm_wait_time_1 + adm_wait_time_2 \
	+ adm_enable + comm_cycle_time + pld_cycle_time + pld_op_mode + cam_res + cam_expo + cam_pic_save_time + pay_enable

	return _format

def ack():
	# every ack returns 2 bytes, which corresponds to the command that was sent

	byte1 				= "B"
	byte2				= "B"

	_format = byte1 + byte2

	return _format

def format_telemetry(data):
	# parse the data of the whole beacon
	# use ">" for big-endian interpretation of incoming bytes, which is necessary because of how struct.unpack reads and unpacks bytes

	_format = ">" + identifier() + cdhs() + eps() + adcs() + comm() + pld() + ram_params() + uvg_message()

	return struct.unpack(_format,data)

def format_ram_flash_params(data):
	# parse the data of the ram and flash parameters
	# use ">" for big-endian interpretation of incoming bytes, which is necessary because of how struct.unpack reads and unpacks bytes
	
	_format = ">" + ram_params() + ram_params()

	# ram_params() is called twice because the satellite first sends the RAM parameters and then the FLASH parameters, since these are
	# equal (in the order of data), no need to create a function flash_params() that is exactly the same to ram_params().

	return struct.unpack(_format,data)

def format_ack(data):
	# parse the data of an acknowledge
 	# use ">" for big-endian interpretation of incoming bytes, which is necessary because of how struct.unpack reads and unpacks bytes

	_format = ">" + ack()

	return struct.unpack(_format,data)

def parse_telemetry(data):
	# place telemetry into a human readable string
	filedata = ""

	filedata += "\n\n\n\n"
	filedata += "---------------------------\n"
	filedata += "|   QUETZAL-1 TELEMETRY   |\n"
	filedata += "---------------------------\n"
	filedata += "Identifier:                  "+ str(data[0]) + "\n"

	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|          CDHS           |\n"
	filedata += "---------------------------\n"
	filedata += "RTC (hh-mm-ss dd-mm-yy):     "+ str(data[1])+ " "+ str(data[2])+ " "+ str(data[3])+ " "+ str(data[4])+ " "+ str(data[5])+ " "+ str(data[6]) + "\n"
	filedata += "ADM Status (a1 a2 a3 a4):    "+ str(data[7] & 0x01) + " " + str((data[7] & 0x02) >> 1) + " " + str((data[7] & 0x04) >> 2) + " " + str((data[7] & 0x08) >> 3) + "\n"
	filedata += "EPS Status:                  "+ str(hex(data[8])) + "\n"
	filedata += "HEATER Status (A/M, On/Off): "+ str((data[9] & 0xF0) >> 4) + " , " + str(data[9] & 0x0F) + "\n"
	filedata += "ADCS Status:                 "+ str(hex(data[10])) + "\n"
	filedata += "PLD Status:                  "+ str(hex(data[11])) + "\n"
	filedata += "ADM Software Reset Counter:  "+ str(data[12]) + "\n"
	filedata += "EPS Software Reset Counter:  "+ str(data[13]) + "\n"
	filedata += "ADCS Software Reset Counter: "+ str(data[14]) + "\n"
	filedata += "ADCS Hardware Reset Counter: "+ str(data[15]) + "\n"
	filedata += "COMM Hardware Reset Counter: "+ str(data[16]) + "\n"
	filedata += "Reset Counter:               "+ str(data[17]) + "\n"

	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|           EPS           |\n"
	filedata += "---------------------------\n"
	filedata += "-----------Temps-----------\n"
	if(data[18] == 253 or data[18] == 255):
		filedata += "TMP100 (degC):               "+ str(data[18]) + "\n"
	else:
		filedata += "TMP100 (degC):               "+ str(0.377*data[18]-25) + "\n"

	filedata += "----------BQ27441----------\n"
	filedata += "State of Charge (%):         "+ str(data[19]) + "\n"
	
	if(data[20] == 253 or data[20] == 254 or data[20] == 255):
		filedata += "Battery Voltage (mV):        "+ str(data[20]) + "\n"
	else:	
		filedata += "Battery Voltage (mV):        "+ str(7.9681*data[20]+2492.0319) + "\n"

	if(data[21] == 4093 or data[21] == 4095):
		filedata += "Average Current (mA):        "+ str(data[21]) + "\n"
	else:
		filedata += "Average Current (mA):        "+ str(1.2219*data[21]-2500) + "\n"

	if(data[22] == 4093 or data[22] == 4094 or data[22] == 4095):
		filedata += "Remaining Capacity (mAh):    "+ str(data[22]) + "\n"
	else:
		filedata += "Remaining Capacity (mAh):    "+ str(0.97752*data[22]) + "\n"

	if(data[23] == 4093 or data[23] == 4095):
		filedata += "Average Power (mW):          "+ str(data[23]) + "\n"
	else:
		filedata += "Average Power (mW):          "+ str(4.1544*data[23]-8500) + "\n"

	if data[24] == 253:
		filedata += "State of Health (%):         "+ str(data[24]) + "\n"
	else:	
		filedata += "State of Health (%):         "+ str(data[24]) + "\n"

	filedata += "---------INA260 1----------\n"
	if(data[25] == 253 or data[25] == 255):
		filedata += "Channel 1 Voltage (V):       "+ str(data[25]) + "\n" 
	else:
		filedata += "Channel 1 Voltage (V):       "+ str(0.01785*data[25]) + "\n"

	if(data[26] == 4093 or data[26] == 4094 or data[26] == 4095):
		filedata += "Channel 1 Current (mA):      "+ str(data[26]) + "\n"
	else:	
		filedata += "Channel 1 Current (mA):      "+ str(0.6109*data[26]) + "\n"

	filedata += "---------INA260 2----------\n"
	if(data[27] == 253 or data[27] == 255):
		filedata += "Channel 2 Voltage (V):       "+ str(data[27]) + "\n"	
	else:
		filedata += "Channel 2 Voltage (V):       "+ str(0.01785*data[27]) + "\n"

	if(data[28] == 4093 or data[28] == 4094 or data[28] == 4095):
		filedata += "Channel 2 Current (mA):      "+ str(data[28]) + "\n"
	else:
		filedata += "Channel 2 Current (mA):      "+ str(0.6109*data[28]) + "\n"

	filedata += "---------INA260 3----------\n"
	if(data[29] == 253 or data[29] == 255):
		filedata += "Channel 3 Voltage (V):       "+ str(data[29]) + "\n"	
	else:
		filedata += "Channel 3 Voltage (V):       "+ str(0.01785*data[29]) + "\n"

	if(data[30] == 4093 or data[30] == 4094 or data[30] == 4095):
		filedata += "Channel 3 Current (mA):      "+ str(data[30]) + "\n"
	else:
		filedata += "Channel 3 Current (mA):      "+ str(0.6109*data[30]) + "\n"

	filedata += "----Subsystem Currents-----\n"
	filedata += "ADCS Current (mA):           "+ str(data[31]) + "\n"
	filedata += "COMM Current (mA):           "+ str(data[32]) + "\n"
	filedata += "PLD Current (mA):            "+ str(data[33]) + "\n"
	filedata += "HTR Current (mA):            "+ str(data[34]) + "\n"
	filedata += "-----Overcurrent Flags-----\n"
	filedata += "ADCS Overcurrent:            "+ str(data[35] & 0x01) + "\n"
	filedata += "COMM Overcurrent:            "+ str((data[35] & 0x02) >> 1) + "\n"
	filedata += "PLD Overcurrent:             "+ str((data[35] & 0x04) >> 2) + "\n"
	filedata += "Heater Overcurrent:          "+ str((data[35] & 0x08) >> 3) + "\n"
	filedata += "----Short Circuit Flags----\n"
	filedata += "ADCS Short Circuit:          "+ str((data[35] & 0x10) >> 4) + "\n"
	filedata += "COMM Short Circuit:          "+ str((data[35] & 0x20) >> 5) + "\n"
	filedata += "PLD Short Circuit:           "+ str((data[35] & 0x40) >> 6) + "\n"
	filedata += "Heater Short Circuit:        "+ str((data[35] & 0x80) >> 7) + "\n"
	filedata += "----Communication Flags----\n"
	filedata += "INA260 No. 1:                "+ str(data[36] & 0x01) + "\n"
	filedata += "INA260 No. 2:                "+ str((data[36] & 0x02) >> 1) + "\n"
	filedata += "INA260 No. 3:                "+ str((data[36] & 0x04) >> 2) + "\n"
	filedata += "BQ27441:                     "+ str((data[36] & 0x08) >> 3) + "\n"
	filedata += "TMP100:                      "+ str((data[36] & 0x10) >> 4) + "\n"
	filedata += "----Transmission Flags-----\n"
	filedata += "INA260 No. 1:                "+ str(data[37] & 0x01) + "\n"
	filedata += "INA260 No. 2:                "+ str((data[37] & 0x02) >> 1) + "\n"
	filedata += "INA260 No. 3:                "+ str((data[37] & 0x04) >> 2) + "\n"
	filedata += "BQ27441:                     "+ str((data[37] & 0x08) >> 3) + "\n"
	filedata += "TMP100:                      "+ str((data[37] & 0x10) >> 4) + "\n"
	
	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|          ADCS           |\n"
	filedata += "---------------------------\n"
	filedata += "------------Gyro-----------\n"
	filedata += "Gyro X (deg/s):              "+ str((data[38]-127.5)/1.275) + "\n"
	filedata += "Gyro Y (deg/s):              "+ str((data[39]-127.5)/1.275) + "\n"
	filedata += "Gyro Z (deg/s):              "+ str((data[40]-127.5)/1.275) + "\n"
	filedata += "--------Magnetometer-------\n"
	filedata += "Mag X (uT):                  "+ str((data[41]-65536.0/2)/(8192.0/325)) + "\n"
	filedata += "Mag Y (uT):                  "+ str((data[42]-65536.0/2)/(8192.0/325)) + "\n"
	filedata += "Mag Z (uT):                  "+ str((data[43]-65536.0/2)/(8192.0/625)) + "\n"
	filedata += "------------ADC1-----------\n"
	filedata += "ADC1 Ch.1 (V):               "+ str(data[44]/77.27) + "\n"
	filedata += "ADC1 Ch.2 (V):               "+ str(data[45]/77.27) + "\n"
	filedata += "ADC1 Ch.3 (V):               "+ str(data[46]/77.27) + "\n"
	filedata += "ADC1 Ch.4 (V):               "+ str(data[47]/77.27) + "\n"
	filedata += "ADC1 Ch.5 (V):               "+ str(data[48]/77.27) + "\n"
	filedata += "ADC1 Ch.6 (V):               "+ str(data[49]/77.27) + "\n"
	filedata += "------------ADC2-----------\n"
	filedata += "ADC2 Ch.1 (V):               "+ str(data[50]/77.27) + "\n"
	filedata += "ADC2 Ch.2 (V):               "+ str(data[51]/77.27) + "\n"
	filedata += "ADC2 Ch.3 (V):               "+ str(data[52]/77.27) + "\n"
	filedata += "ADC2 Ch.4 (V):               "+ str(data[53]/77.27) + "\n"
	filedata += "ADC2 Ch.5 (V):               "+ str(data[54]/77.27) + "\n"
	filedata += "ADC2 Ch.6 (V):               "+ str(data[55]/77.27) + "\n"
	filedata += "-----------Temps-----------\n"
	filedata += "BNO055 Temperature (degC):   "+ str(data[56]) + "\n"
	filedata += "TMP100 Temperature (degC):   "+ str(data[57]) + "\n"
	filedata += "----Transmission Flags-----\n"	
	filedata += "BNO055:                      "+ str(data[58] & 0x01) + "\n"
	filedata += "ADC1:                        "+ str((data[58] & 0x02) >> 1) + "\n"
	filedata += "ADC2:                        "+ str((data[58] & 0x04) >> 2) + "\n"
	filedata += "TMP100:                      "+ str((data[58] & 0x08) >> 3) + "\n"


	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|          COMM           |\n"
	filedata += "---------------------------\n"
	filedata += "Package Counter:             "+ str(data[59]) + "\n"

	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|           PLD           |\n"
	filedata += "---------------------------\n"
	filedata += "Operation Mode:              "+ str(hex(data[60])) + "\n"
	filedata += "Picture Counter:             "+ str(data[61]) + "\n"

	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|       RAM PARAMS        |\n"
	filedata += "---------------------------\n"
	filedata += "CDHS Cycle Time:             "+ str(data[62]) + "\n"
	filedata += "CDHS WDT Time:               "+ str(data[63]) + "\n"
	filedata += "ADM SOC Limit:               "+ str(data[64]) + "\n"
	filedata += "ADCS SOC Limit:              "+ str(data[65]) + "\n"
	filedata += "COMMS SOC Limit:             "+ str(data[66]) + "\n"
	filedata += "PLD SOC Limit:               "+ str(data[67]) + "\n"
	filedata += "HTR Cycle Time:              "+ str(data[68]) + "\n"
	filedata += "Heater Emergency On Time:    "+ str(data[69]) + "\n"
	filedata += "Heater Emergency Off Time:   "+ str(data[70]) + "\n"
	filedata += "ADM Cycle Time:              "+ str(data[71]) + "\n"
	filedata += "ADM Burn Time:               "+ str(data[72]) + "\n"
	filedata += "ADM Max Cycles:              "+ str(data[73]) + "\n"
	filedata += "ADM Wait Time 1:             "+ str(data[74]) + "\n"
	filedata += "ADM Wait Time 2:             "+ str(data[75]) + "\n"
	filedata += "ADM Enable:                  "+ str(data[76]) + "\n"
	filedata += "COMM Cycle Time:             "+ str(data[77]) + "\n"
	filedata += "PLD Cycle Time:              "+ str(data[78]) + "\n"
	filedata += "PLD Operation Mode:          "+ str(data[79]) + "\n"
	filedata += "Camera Resolution:           "+ str(data[80]) + "\n"
	filedata += "Camera Exposure:             "+ str(data[81]) + "\n"
	filedata += "Camera Picture Save Time:    "+ str(data[82]) + "\n"
	filedata += "Payload Enable:              "+ str(data[83]) + "\n"

	filedata += "\n"
	filedata += "UVG Message:                 "+ str(data[84]) + "\n"

	return filedata

def parse_ram_flash_params(data):
	# place ram/flash parameters into human-readable string

	filedata = ""

	filedata += "\n"
	filedata += "---------------------------\n"
	filedata += "|     RAM/FLASH PARAMS     |\n"
	filedata += "---------------------------\n"
	filedata += "CDHS Cycle Time:             "+ str(data[0]) + " / " + str(data[22]) + "\n"
	filedata += "CDHS WDT Time:               "+ str(data[1]) + " / " + str(data[23]) + "\n"
	filedata += "ADM SOC Limit:               "+ str(data[2]) + " / " + str(data[24]) + "\n"
	filedata += "ADCS SOC Limit:              "+ str(data[3]) + " / " + str(data[25]) + "\n"
	filedata += "COMMS SOC Limit:             "+ str(data[4]) + " / " + str(data[26]) + "\n"
	filedata += "PLD SOC Limit:               "+ str(data[5]) + " / " + str(data[27]) + "\n"
	filedata += "HTR Cycle Time:              "+ str(data[6]) + " / " + str(data[28]) + "\n"
	filedata += "Heater Emergency On Time:    "+ str(data[7]) + " / " + str(data[29]) + "\n"
	filedata += "Heater Emergency Off Time:   "+ str(data[8]) + " / " + str(data[30]) + "\n"
	filedata += "ADM Cycle Time:              "+ str(data[9]) + " / " + str(data[31]) + "\n"
	filedata += "ADM Burn Time:               "+ str(data[10]) + " / " + str(data[32]) + "\n"
	filedata += "ADM Max Cycles:              "+ str(data[11]) + " / " + str(data[33]) + "\n"
	filedata += "ADM Wait Time 1:             "+ str(data[12]) + " / " + str(data[34]) + "\n"
	filedata += "ADM Wait Time 2:             "+ str(data[13]) + " / " + str(data[35]) + "\n"
	filedata += "ADM Enable:                  "+ str(data[14]) + " / " + str(data[36]) + "\n"
	filedata += "COMM Cycle Time:             "+ str(data[15]) + " / " + str(data[37]) + "\n"
	filedata += "PLD Cycle Time:              "+ str(data[16]) + " / " + str(data[38]) + "\n"
	filedata += "PLD Operation Mode:          "+ str(data[17]) + " / " + str(data[39]) + "\n"
	filedata += "Camera Resolution:           "+ str(data[18]) + " / " + str(data[40]) + "\n"
	filedata += "Camera Exposure:             "+ str(data[19]) + " / " + str(data[41]) + "\n"
	filedata += "Camera Picture Save Time:    "+ str(data[20]) + " / " + str(data[42]) + "\n"
	filedata += "Payload Enable:              "+ str(data[21]) + " / " + str(data[43]) + "\n"

	return filedata

def parse_ack(data):
	# parse the acknolwedge bytes

	filedata = ""

	filedata += "Acknowledge Detected: " + str(hex(data[0])) + " " + str(hex(data[1]))

	return filedata

class quetzal1_parse(gr.basic_block):
    """
    Parse Quetzal-1 packets from the incoming data. 

    If beacon, the parsed data will be written into parsed_beaconXXX.txt and printed into terminal. The raw data will be written into raw_beaconXXX.dat

    If acknowledge, the received data will just be printed into terminal.

    If an image packet, only a notice of "image packet detected" will be printed into terminal.

    XXX represents the current date and time. 

    Inputs:
    - filaname_parsed_beacon: the name of the file that saves the parsed beacon data
    - filename_raw_beacon: the name of the file that saves the raw beacon data
    """

    def __init__(self, filename_parsed_beacon = "", filename_raw_beacon = ""):
        gr.basic_block.__init__(self,
            name="Quetzal-1 Packet Parser",
            in_sig=[],
            out_sig=[])

        # generate file name and necessary directories
        # in which all received data will be saved
        homedir = os.environ['HOME']

        if not os.path.exists(homedir + "/Received Data"):
        	os.mkdir(homedir + "/Received Data")

        self.filename_parsed_beacon = homedir + "/Received Data/parsed_beacon_" + str(datetime.datetime.now()) + ".txt"		# saves the beacon parsed data
        self.filename_raw_beacon = homedir + "/Received Data/raw_beacon_" + str(datetime.datetime.now()) + ".dat"			# saves the beacon raw data


        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
		msg = pmt.cdr(msg_pmt)
		if not pmt.is_u8vector(msg):
			print "[ERROR] Received invalid message type. Expected u8vector"
			return
		packet = bytearray(pmt.u8vector_elements(msg))

		try:
			if len(packet) == 141:
				# BEACON
				# bytes 0 through 4 are CSP header, rest is beacon data

				# write raw data into .dat file
				f = open(self.filename_raw_beacon, "a")
				f.write(packet[4:])
				f.close()

				# parse data
				data = format_telemetry(packet[4:])
				parsedData = parse_telemetry(data)                

				# write parsed data into text file
				f = open(self.filename_parsed_beacon, "a")
				f.write(parsedData)
				f.close()

				# print parsed data into terminal
				print parsedData
			elif len(packet) == 236:
				# IMAGE PACKET
				# bytes 0 through 4 are CSP header, rest is image data

				print "Image packet detected"
			elif len(packet) == 6:
				# Acknowledge from satellite
				# bytes 0 through 4 are CSP header, rest is ack data

				# parse ack data
				data = format_ack(packet[4:])
				parsedData = parse_ack(data)

				# print parsed ack into readable text
				print parsedData
			elif len(packet) == 48:
				# RAM/FLASH PARAMS
				# bytes 0 through 4 are CSP header, rest is RAM/FLASH params

				# parse ram/flash parameters into readable text
				data = format_ram_flash_params(packet[4:])
				parsedData = parse_ram_flash_params(data)

				# print parsed ram/flash parameters into terminal
				print parsedData
			else:
				print "GCS Command or Incorrect beacon length"
		except Exception as e:
			print "Could not decode telemetry beacon"
			print(e)
		return