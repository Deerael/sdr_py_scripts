#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: tcp source wbfm with stereo audio
# GNU Radio version: 3.10.9.2

from gnuradio import analog
import math
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




class wbfm_stereo(gr.top_block):

    def __init__(self, centre_freq=int(100e6), ip_arg='localhost', port_arg=int(2e3), samp_rate=int(10e6), signal_freq=int(102.5e6)):
        gr.top_block.__init__(self, "tcp source wbfm with stereo audio", catch_exceptions=True)

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
        self.wbfm_deviation = wbfm_deviation = 75e3
        self.decim_2 = decim_2 = int((samp_rate / decim) / 0.25e6)
        self.audio_samp_rate = audio_samp_rate = int(48e3)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, f"tcp://{ip_arg}:{port_arg}", 100, False, (-1), '', False)
        self.zeromq_sub_source_0.set_max_output_buffer(2048)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_fff(
                interpolation=(int((audio_samp_rate / 1e3) / 2)),
                decimation=(int((samp_rate / decim / decim_2 / 1e3) / 2)),
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=(int((audio_samp_rate / 1e3) / 2)),
                decimation=(int((samp_rate / decim / decim_2 / 1e3) / 2)),
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim,
                taps=[],
                fractional_bw=0.4)
        self.low_pass_filter_3 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                (samp_rate / decim / decim_2),
                13e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_2 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                (samp_rate / decim / decim_2),
                13e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                (samp_rate / decim / decim_2),
                15e3,
                1e3,
                window.WIN_BLACKMAN,
                6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                (samp_rate / decim / decim_2),
                15e3,
                1e3,
                window.WIN_BLACKMAN,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decim_2,
            firdes.low_pass(
                1,
                (int(samp_rate / decim)),
                100e3,
                15e3,
                window.WIN_BLACKMAN,
                6.76))
        self.dc_blocker_xx_1 = filter.dc_blocker_ff(32, True)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(0.2)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.2)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                (samp_rate / decim / decim_2),
                37.9e3,
                38.1e3,
                500,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                (samp_rate / decim / decim_2),
                23e3,
                53e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_fcc(
            1,
            firdes.complex_band_pass(
                1,
                (samp_rate / decim / decim_2),
                18.8e3,
                19.2e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0 = audio.sink(audio_samp_rate, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (centre_freq - signal_freq), 1, 0, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((0.25e6/(2*math.pi* wbfm_deviation)))
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc((math.pi / 200), (1e-6), (1e-5))
        self.analog_fm_deemph_0_0 = analog.fm_deemph(fs=audio_samp_rate, tau=(50e-6))
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=audio_samp_rate, tau=(50e-6))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_2, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.band_pass_filter_1, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.band_pass_filter_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.dc_blocker_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_3, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.low_pass_filter_1_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.audio_sink_0, 1))
        self.connect((self.dc_blocker_xx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.low_pass_filter_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.low_pass_filter_2, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.low_pass_filter_3, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.low_pass_filter_3, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_fm_deemph_0_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def get_centre_freq(self):
        return self.centre_freq

    def set_centre_freq(self, centre_freq):
        with self._lock:
            self.centre_freq = centre_freq
            self.analog_sig_source_x_0.set_frequency((self.centre_freq - self.signal_freq))

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
            self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
            self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, (self.samp_rate / self.decim / self.decim_2), 18.8e3, 19.2e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 23e3, 53e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_1.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 37.9e3, 38.1e3, 500, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, (int(self.samp_rate / self.decim)), 100e3, 15e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_3.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_2.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        with self._lock:
            self.signal_freq = signal_freq
            self.analog_sig_source_x_0.set_frequency((self.centre_freq - self.signal_freq))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        with self._lock:
            self.decim = decim
            self.set_decim_2(int((self.samp_rate / self.decim) / 0.25e6))
            self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, (self.samp_rate / self.decim / self.decim_2), 18.8e3, 19.2e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 23e3, 53e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_1.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 37.9e3, 38.1e3, 500, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, (int(self.samp_rate / self.decim)), 100e3, 15e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_3.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_2.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))

    def get_wbfm_deviation(self):
        return self.wbfm_deviation

    def set_wbfm_deviation(self, wbfm_deviation):
        with self._lock:
            self.wbfm_deviation = wbfm_deviation
            self.analog_quadrature_demod_cf_0.set_gain((0.25e6/(2*math.pi* self.wbfm_deviation)))

    def get_decim_2(self):
        return self.decim_2

    def set_decim_2(self, decim_2):
        with self._lock:
            self.decim_2 = decim_2
            self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, (self.samp_rate / self.decim / self.decim_2), 18.8e3, 19.2e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 23e3, 53e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_1.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 37.9e3, 38.1e3, 500, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_BLACKMAN, 6.76))
            self.low_pass_filter_3.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_2.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        with self._lock:
            self.audio_samp_rate = audio_samp_rate



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
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(int(10e6))),
        help="Set sample rate [default=%(default)r]")
    parser.add_argument(
        "-f", "--signal-freq", dest="signal_freq", type=eng_float, default=eng_notation.num_to_str(float(int(102.5e6))),
        help="Set frequency of wfm station [default=%(default)r]")
    return parser


def main(top_block_cls=wbfm_stereo, options=None):
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
