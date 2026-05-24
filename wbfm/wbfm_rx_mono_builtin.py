#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import threading




class wbfm_rx_mono_builtin(gr.top_block):

    def __init__(self, centre_freq=int(100e6), ip_arg='localhost', port_arg=int(2e3), samp_rate=int(50e6), signal_freq=int(99.6e6)):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        self._lock = threading.RLock()

        ##################################################
        # Parameters
        ##################################################
        self.centre_freq = centre_freq
        self.ip_arg = ip_arg
        self.port_arg = port_arg
        self.samp_rate = samp_rate
        self.signal_freq = signal_freq

        ##################################################
        # Variables
        ##################################################
        self.decim = decim = int(samp_rate / 1e6)
        self.decim_2 = decim_2 = int((samp_rate / decim) / 0.25e6)
        self.audio_samp_rate = audio_samp_rate = int(50e3)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, f"tcp://{ip_arg}:{port_arg}", 100, False, (-1), '', False)
        self.zeromq_sub_source_0.set_max_output_buffer(2048)
        self.low_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                audio_samp_rate,
                15e3,
                500,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decim_2,
            firdes.low_pass(
                1,
                (int(samp_rate / decim)),
                100e3,
                20e3,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, firdes.low_pass(1,samp_rate, samp_rate/decim, 0.4e6), (int(signal_freq - centre_freq)), int(samp_rate))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.75)
        self.audio_sink_0 = audio.sink(audio_samp_rate, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=0.25e6,
        	audio_decimation=5,
        )
        self.analog_agc_xx_0 = analog.agc_cc((1e-4), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.analog_agc_xx_0, 0))


    def get_centre_freq(self):
        return self.centre_freq

    def set_centre_freq(self, centre_freq):
        with self._lock:
            self.centre_freq = centre_freq
            self.freq_xlating_fir_filter_xxx_0.set_center_freq((int(self.signal_freq - self.centre_freq)))

    def get_ip_arg(self):
        return self.ip_arg

    def set_ip_arg(self, ip_arg):
        with self._lock:
            self.ip_arg = ip_arg

    def get_port_arg(self):
        return self.port_arg

    def set_port_arg(self, port_arg):
        with self._lock:
            self.port_arg = port_arg

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        with self._lock:
            self.samp_rate = samp_rate
            self.set_decim(int(self.samp_rate / 1e6))
            self.set_decim_2(int((self.samp_rate / self.decim) / 0.25e6))
            self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate, self.samp_rate/self.decim, 0.4e6))
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, (int(self.samp_rate / self.decim)), 100e3, 20e3, window.WIN_HAMMING, 6.76))

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        with self._lock:
            self.signal_freq = signal_freq
            self.freq_xlating_fir_filter_xxx_0.set_center_freq((int(self.signal_freq - self.centre_freq)))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        with self._lock:
            self.decim = decim
            self.set_decim_2(int((self.samp_rate / self.decim) / 0.25e6))
            self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate, self.samp_rate/self.decim, 0.4e6))
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, (int(self.samp_rate / self.decim)), 100e3, 20e3, window.WIN_HAMMING, 6.76))

    def get_decim_2(self):
        return self.decim_2

    def set_decim_2(self, decim_2):
        with self._lock:
            self.decim_2 = decim_2

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        with self._lock:
            self.audio_samp_rate = audio_samp_rate
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_samp_rate, 15e3, 500, window.WIN_HAMMING, 6.76))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--centre-freq", dest="centre_freq", type=eng_float, default=eng_notation.num_to_str(float(int(100e6))),
        help="Set centre_freq [default=%(default)r]")
    parser.add_argument(
        "-i", "--ip-arg", dest="ip_arg", type=str, default='localhost',
        help="Set ip [default=%(default)r]")
    parser.add_argument(
        "-p", "--port-arg", dest="port_arg", type=intx, default=int(2e3),
        help="Set port [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(int(50e6))),
        help="Set sample rate [default=%(default)r]")
    parser.add_argument(
        "-f", "--signal-freq", dest="signal_freq", type=eng_float, default=eng_notation.num_to_str(float(int(99.6e6))),
        help="Set frequency of wfm station [default=%(default)r]")
    return parser


def main(top_block_cls=wbfm_rx_mono_builtin, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(centre_freq=options.centre_freq, ip_arg=options.ip_arg, port_arg=options.port_arg, samp_rate=options.samp_rate, signal_freq=options.signal_freq)

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
