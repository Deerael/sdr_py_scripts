#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: soapy_tcp
# GNU Radio version: v3.11.0.0git-1096-gc61887f7

from gnuradio import soapy
from gnuradio import zeromq
import threading
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class soapy_tcp(gr.top_block):

    def __init__(self, centre_freq=100e6, cmd_port=2001, data_port=2000, device='fobos', ip='localhost', lna=1, samp_rate=25e6, vga=1):
        gr.top_block.__init__(self, "soapy_tcp", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.centre_freq = centre_freq
        self.cmd_port = cmd_port
        self.data_port = data_port
        self.device = device
        self.ip = ip
        self.lna = lna
        self.samp_rate = samp_rate
        self.vga = vga

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source(f"tcp://{ip}:{cmd_port}", 100, False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, f"tcp://{ip}:{data_port}", 100, False, (-1), '', True, True)
        self.soapy_custom_source_0 = None
        dev = 'driver=' + device
        stream_args = ''
        tune_args = ['']
        settings = ['']
        self.soapy_custom_source_0 = soapy.source(dev, "fc32",
                                  1, '',
                                  stream_args, tune_args, settings)
        self.soapy_custom_source_0.set_sample_rate(0, samp_rate)
        self.soapy_custom_source_0.set_bandwidth(0, 1)
        self.soapy_custom_source_0.set_antenna(0, 'RX')
        self.soapy_custom_source_0.set_frequency(0, centre_freq)
        self.soapy_custom_source_0.set_frequency_correction(0, 0)
        self.soapy_custom_source_0.set_gain_mode(0, False)
        self.soapy_custom_source_0.set_gain(0, (lna + vga))
        self.soapy_custom_source_0.set_dc_offset_mode(0, False)
        self.soapy_custom_source_0.set_dc_offset(0, 0)
        self.soapy_custom_source_0.set_iq_balance(0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.soapy_custom_source_0, 'cmd'))
        self.connect((self.soapy_custom_source_0, 0), (self.zeromq_pub_sink_0, 0))


    def get_centre_freq(self):
        return self.centre_freq

    def set_centre_freq(self, centre_freq):
        self.centre_freq = centre_freq
        self.soapy_custom_source_0.set_frequency(0, self.centre_freq)

    def get_cmd_port(self):
        return self.cmd_port

    def set_cmd_port(self, cmd_port):
        self.cmd_port = cmd_port

    def get_data_port(self):
        return self.data_port

    def set_data_port(self, data_port):
        self.data_port = data_port

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_lna(self):
        return self.lna

    def set_lna(self, lna):
        self.lna = lna
        self.soapy_custom_source_0.set_gain(0, (self.lna + self.vga))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_vga(self):
        return self.vga

    def set_vga(self, vga):
        self.vga = vga
        self.soapy_custom_source_0.set_gain(0, (self.lna + self.vga))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--centre-freq", dest="centre_freq", type=eng_float, default=eng_notation.num_to_str(float(100e6)),
        help="Set centre_freq [default=%(default)r]")
    parser.add_argument(
        "--cmd-port", dest="cmd_port", type=intx, default=2001,
        help="Set cmd port [default=%(default)r]")
    parser.add_argument(
        "--data-port", dest="data_port", type=intx, default=2000,
        help="Set data port [default=%(default)r]")
    parser.add_argument(
        "--device", dest="device", type=str, default='fobos',
        help="Set device driver [default=%(default)r]")
    parser.add_argument(
        "-i", "--ip", dest="ip", type=str, default='localhost',
        help="Set localhost [default=%(default)r]")
    parser.add_argument(
        "-l", "--lna", dest="lna", type=intx, default=1,
        help="Set lna [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(25e6)),
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "-v", "--vga", dest="vga", type=intx, default=1,
        help="Set vga [default=%(default)r]")
    return parser


def main(top_block_cls=soapy_tcp, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(centre_freq=options.centre_freq, cmd_port=options.cmd_port, data_port=options.data_port, device=options.device, ip=options.ip, lna=options.lna, samp_rate=options.samp_rate, vga=options.vga)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
