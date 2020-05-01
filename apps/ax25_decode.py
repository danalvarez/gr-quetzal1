#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Quetzal-1 Receiver
# Author: Dan Álvarez, based on code by Daniel Estévez
# Description: An AX.25 + HDLC decoder for the NanoCom AX100 transceiver. Default baud rate is set to 4800. Includes parser for beacons and images.
# GNU Radio version: 3.7.14.0
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import quetzal1_parse
import satellites


class ax25_decode(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Quetzal-1 Receiver")

        ##################################################
        # Variables
        ##################################################
        self.symb_rate = symb_rate = 4800
        self.samp_rate = samp_rate = 48000
        self.samp_per_sym = samp_per_sym = int(samp_rate/symb_rate)
        self.log = log = 0
        self.homedir = homedir = ""
        self.hhmmss = hhmmss = ""
        self.gain_mu = gain_mu = 0.175*3
        self.filename_raw_beacon = filename_raw_beacon = ""
        self.filename_parsed_beacon = filename_parsed_beacon = ""
        self.filename_image_metadata = filename_image_metadata = ""
        self.filename_image = filename_image = ""
        self.do_once = do_once = 0
        self.data_rate = data_rate = 4800
        self.count = count = 0
        self.center_freq = center_freq = 437.2e6

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:1502', 100, False, -1)
        self.satellites_strip_ax25_header_0 = satellites.strip_ax25_header()
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.quetzal1_parse = quetzal1_parse.quetzal1_parse(filename_parsed_beacon='', filename_raw_beacon='')
        self.low_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, 48000, 2400, 2000, firdes.WIN_HAMMING, 6.76))
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0, 16)
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(10, 0.25*gain_mu*gain_mu, 0.5, gain_mu, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(1024, True)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/dan/Documents/repos/gr-quetzal1/recordings/example_beacon_quetzal1.wav', False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((5, ))



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.satellites_strip_ax25_header_0, 'in'))
        self.msg_connect((self.satellites_strip_ax25_header_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.satellites_strip_ax25_header_0, 'out'), (self.quetzal1_parse, 'in'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.satellites_hdlc_deframer_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.digital_descrambler_bb_0, 0))

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_samp_per_sym(int(self.samp_rate/self.symb_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_sym(int(self.samp_rate/self.symb_rate))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym

    def get_log(self):
        return self.log

    def set_log(self, log):
        self.log = log

    def get_homedir(self):
        return self.homedir

    def set_homedir(self, homedir):
        self.homedir = homedir

    def get_hhmmss(self):
        return self.hhmmss

    def set_hhmmss(self, hhmmss):
        self.hhmmss = hhmmss

    def get_gain_mu(self):
        return self.gain_mu

    def set_gain_mu(self, gain_mu):
        self.gain_mu = gain_mu
        self.digital_clock_recovery_mm_xx_0_0.set_gain_omega(0.25*self.gain_mu*self.gain_mu)
        self.digital_clock_recovery_mm_xx_0_0.set_gain_mu(self.gain_mu)

    def get_filename_raw_beacon(self):
        return self.filename_raw_beacon

    def set_filename_raw_beacon(self, filename_raw_beacon):
        self.filename_raw_beacon = filename_raw_beacon

    def get_filename_parsed_beacon(self):
        return self.filename_parsed_beacon

    def set_filename_parsed_beacon(self, filename_parsed_beacon):
        self.filename_parsed_beacon = filename_parsed_beacon

    def get_filename_image_metadata(self):
        return self.filename_image_metadata

    def set_filename_image_metadata(self, filename_image_metadata):
        self.filename_image_metadata = filename_image_metadata

    def get_filename_image(self):
        return self.filename_image

    def set_filename_image(self, filename_image):
        self.filename_image = filename_image

    def get_do_once(self):
        return self.do_once

    def set_do_once(self, do_once):
        self.do_once = do_once

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq


def main(top_block_cls=ax25_decode, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
