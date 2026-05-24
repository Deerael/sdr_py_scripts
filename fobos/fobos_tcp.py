#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from gnuradio import RigExpert
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq




class fobos_tcp(gr.top_block):

    def __init__(self, center_freq_arg=100e6, ip_arg='localhost', lna_arg=0, port_arg=2000, sample_rate_arg=25e6, vga_arg=0):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.center_freq_arg = center_freq_arg
        self.ip_arg = ip_arg
        self.lna_arg = lna_arg
        self.port_arg = port_arg
        self.sample_rate_arg = sample_rate_arg
        self.vga_arg = vga_arg

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, f"tcp://{ip_arg}:{port_arg}", 100, False, (-1), '', True, True)
        self.RigExpert_fobos_sdr_0 = RigExpert.fobos_sdr(0, center_freq_arg, sample_rate_arg, lna_arg, vga_arg, 0, 0)
        self.RigExpert_fobos_sdr_0.set_max_output_buffer(2048)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.RigExpert_fobos_sdr_0, 0), (self.zeromq_pub_sink_0, 0))


    def get_center_freq_arg(self):
        return self.center_freq_arg

    def set_center_freq_arg(self, center_freq_arg):
        self.center_freq_arg = center_freq_arg
        self.RigExpert_fobos_sdr_0.set_frequency(self.center_freq_arg)

    def get_ip_arg(self):
        return self.ip_arg

    def set_ip_arg(self, ip_arg):
        self.ip_arg = ip_arg

    def get_lna_arg(self):
        return self.lna_arg

    def set_lna_arg(self, lna_arg):
        self.lna_arg = lna_arg
        self.RigExpert_fobos_sdr_0.set_lna_gain(self.lna_arg)

    def get_port_arg(self):
        return self.port_arg

    def set_port_arg(self, port_arg):
        self.port_arg = port_arg

    def get_sample_rate_arg(self):
        return self.sample_rate_arg

    def set_sample_rate_arg(self, sample_rate_arg):
        self.sample_rate_arg = sample_rate_arg
        self.RigExpert_fobos_sdr_0.set_samplerate(self.sample_rate_arg);

    def get_vga_arg(self):
        return self.vga_arg

    def set_vga_arg(self, vga_arg):
        self.vga_arg = vga_arg
        self.RigExpert_fobos_sdr_0.set_vga_gain(self.vga_arg)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--center-freq-arg", dest="center_freq_arg", type=eng_float, default=eng_notation.num_to_str(float(100e6)),
        help="Set center_freq [default=%(default)r]")
    parser.add_argument(
        "-i", "--ip-arg", dest="ip_arg", type=str, default='localhost',
        help="Set ip [default=%(default)r]")
    parser.add_argument(
        "-l", "--lna-arg", dest="lna_arg", type=intx, default=0,
        help="Set lna [default=%(default)r]")
    parser.add_argument(
        "-p", "--port-arg", dest="port_arg", type=intx, default=2000,
        help="Set port [default=%(default)r]")
    parser.add_argument(
        "-s", "--sample-rate-arg", dest="sample_rate_arg", type=eng_float, default=eng_notation.num_to_str(float(25e6)),
        help="Set sample_rate [default=%(default)r]")
    parser.add_argument(
        "-v", "--vga-arg", dest="vga_arg", type=intx, default=0,
        help="Set vga [default=%(default)r]")
    return parser


def main(top_block_cls=fobos_tcp, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(center_freq_arg=options.center_freq_arg, ip_arg=options.ip_arg, lna_arg=options.lna_arg, port_arg=options.port_arg, sample_rate_arg=options.sample_rate_arg, vga_arg=options.vga_arg)

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
