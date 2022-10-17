#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Adapted from: Copyright 2018 Daniel Estevez <daniel@destevez.net>
# 
# Modification 2019, Dan Álvarez
# Image parser for QUETZAL-1 Beacon
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

import numpy as np
from gnuradio import gr
import pmt
import os

class msg_block(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
	"""This block concatenates image packets into a single photo

	If it is an image, then it writes to imageXXX.dat and writes the metadata of the image into image_metadataXXX.txt. 

	XXX represents the date and time at the moment of creating the file.

	Everything is stored in the home directory, in a folder named "Received Data"

	Inputs:
	- filename_image: the name of the file that saves the received image
	- filaname_image_metadata: the name of the file that saves the metadata of the received image
	- rtc: the datetime of the current photo being sent (part of the RTC of the satellite, in the format hh-mm-ss-dd-mm-yy)
	- homedir: the home directory of the current PC
	- log: each photo packet contains a packet number, this variable saves the packet number of the packet that was just received
	- do_once: used to perform an action only once
	"""

	def __init__(self, filename_image = "", filename_image_metadata = "", rtc = [], homedir = "", log = -1, do_once = 0):  # only default arguments here
		"""arguments to this function show up as parameters in GRC"""
		gr.basic_block.__init__(
		self,
		name='Write Photo',   # will show up in GRC
		in_sig=None,
		out_sig=None
		)

		# generate filenames and necessary directories
		self.homedir = os.environ['HOME']
		if not os.path.exists(self.homedir + "/Received Data"):
			os.mkdir(self.homedir + "/Received Data")
		self.filename_image = filename_image										# saves the image data
		self.filename_image_metadata = filename_image_metadata						# saves the metadata of each image
		
		# declare other variables
		self.log = log 																# saves the packet number of the last packet
		self.do_once = do_once														# aids in doing a task only once
		self.rtc = rtc																# saves the rtc of the satellite

		self.message_port_register_in(pmt.intern('msg_in'))
		self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

	def handle_msg(self, msg):
		_in = pmt.to_python(msg) #the PMT message that comes in is a tuple, the actual packet is in _in[1]

		data = _in[1]

		if len(data) == 236:
			# write to imageXXX.dat if image
			# bytes 0 through 4 are CSP header, rest is image data

			# verify current rtc to past rtc (if they are different, it's a new photo, so create new file names)
			currRTC = [str(val) for val in data[-6:]] 
			if currRTC != self.rtc:
				self.filename_image = self.homedir + "/Received Data/image_" + "-".join(currRTC) + ".dat"
				self.filename_image_metadata = self.homedir + "/Received Data/image_metadata_" + "-".join(currRTC) + ".txt"
				self.do_once = 0

			# open files
			f = open(self.filename_image, "a")
			f2 = open(self.filename_image_metadata, "a")

			# add blocks of zeros as placeholders for missing packets
			if data[-7] > self.log+1:
				diff = data[-7] - self.log - 1				# calculate the amount of packets that were lost
				f.write(np.zeros(224*diff,dtype=np.uint8))	# image packet is 224 bytes

			# compares the packet number of the current and last packets.
			# only write the packet if it is not duplicated (because images are sent with redundancy)
			# also writes the metadata of the image into a readable text file
			if self.log != data[-7]:	
				f.write(data[4:-8])	# image data starts right after CSP header, last 8 bytes are image metadata

				if self.do_once == 0:	# only do this once for every image
					f2.write("Image Number: " + str(data[-8]) + "\n")
					f2.write("RTC (hh-mm-ss-dd-mm-yy): " + "-".join(currRTC) + "\n\n")
					f2.write("Received packets:\n\n")

					self.do_once += 1
				
				f2.write(str(data[-7]) + "\n")	# write the packet number into the metadata text file
				self.log = data[-7]				# save the current packet number
				self.rtc = currRTC				# save current rtc value

			f.close()
			f2.close()

		return

	def work(self, input_items, output_items):
		pass