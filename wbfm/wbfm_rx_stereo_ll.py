#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
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
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import sip
import threading



class wbfm_rx_stereo_ll(gr.top_block, Qt.QWidget):

    def __init__(self, centre_freq=int(100e6), ip_arg='localhost', port_arg=int(2e3), samp_rate=int(10e6), signal_freq=int(99.6e6)):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "wbfm_rx_stereo_ll")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

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
        self.wbfm_deviation = wbfm_deviation = 75e3
        self.audio_decim = audio_decim = int(samp_rate / decim / decim_2 / audio_samp_rate)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, f"tcp://{ip_arg}:{port_arg}", 100, False, (-1), '', False)
        self.zeromq_sub_source_0.set_max_output_buffer(2048)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim,
                taps=[],
                fractional_bw=0.45)
        self.qtgui_freq_sink_x_3_0_2 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            0.25e6, #bw
            "high pass pll before mult", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_3_0_2.set_update_time(0.10)
        self.qtgui_freq_sink_x_3_0_2.set_y_axis(0, 150)
        self.qtgui_freq_sink_x_3_0_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_3_0_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_3_0_2.enable_autoscale(True)
        self.qtgui_freq_sink_x_3_0_2.enable_grid(True)
        self.qtgui_freq_sink_x_3_0_2.set_fft_average(0.2)
        self.qtgui_freq_sink_x_3_0_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_3_0_2.enable_control_panel(False)
        self.qtgui_freq_sink_x_3_0_2.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_3_0_2.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_3_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_3_0_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_3_0_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_3_0_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_3_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_3_0_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_3_0_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_3_0_2_win)
        self.qtgui_freq_sink_x_3_0_1_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            0.25e6, #bw
            "deemph", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_3_0_1_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_3_0_1_1.set_y_axis(0, 150)
        self.qtgui_freq_sink_x_3_0_1_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_3_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_3_0_1_1.enable_autoscale(True)
        self.qtgui_freq_sink_x_3_0_1_1.enable_grid(True)
        self.qtgui_freq_sink_x_3_0_1_1.set_fft_average(0.2)
        self.qtgui_freq_sink_x_3_0_1_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_3_0_1_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_3_0_1_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_3_0_1_1.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_3_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_3_0_1_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_3_0_1_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_3_0_1_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_3_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_3_0_1_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_3_0_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_3_0_1_1_win)
        self.qtgui_freq_sink_x_3_0_1_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            0.25e6, #bw
            "deemph", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_3_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_3_0_1_0.set_y_axis(0, 150)
        self.qtgui_freq_sink_x_3_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_3_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_3_0_1_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_3_0_1_0.enable_grid(True)
        self.qtgui_freq_sink_x_3_0_1_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_3_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_3_0_1_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_3_0_1_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_3_0_1_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_3_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_3_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_3_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_3_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_3_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_3_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_3_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_3_0_1_0_win)
        self.qtgui_freq_sink_x_3_0_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            0.25e6, #bw
            "high pass L-R", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_3_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_3_0_0.set_y_axis(0, 150)
        self.qtgui_freq_sink_x_3_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_3_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_3_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_3_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_3_0_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_3_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_3_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_3_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_3_0_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_3_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_3_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_3_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_3_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_3_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_3_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_3_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_3_0_0_win)
        self.qtgui_freq_sink_x_3_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            0.25e6, #bw
            "high pass pll", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_3_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_3_0.set_y_axis(0, 150)
        self.qtgui_freq_sink_x_3_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_3_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_3_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_3_0.enable_grid(True)
        self.qtgui_freq_sink_x_3_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_3_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_3_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_3_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_3_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_3_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_3_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_3_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_3_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_3_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_3_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_3_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_3_0_win)
        self.qtgui_freq_sink_x_3 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            0.25e6, #bw
            "deemph", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_3.set_update_time(0.10)
        self.qtgui_freq_sink_x_3.set_y_axis(0, 150)
        self.qtgui_freq_sink_x_3.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_3.enable_autoscale(True)
        self.qtgui_freq_sink_x_3.enable_grid(True)
        self.qtgui_freq_sink_x_3.set_fft_average(0.2)
        self.qtgui_freq_sink_x_3.enable_axis_labels(True)
        self.qtgui_freq_sink_x_3.enable_control_panel(False)
        self.qtgui_freq_sink_x_3.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_3.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_3.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_3_win = sip.wrapinstance(self.qtgui_freq_sink_x_3.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_3_win)
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
            audio_decim,
            firdes.low_pass(
                1,
                (samp_rate / decim / decim_2),
                15e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(
            audio_decim,
            firdes.low_pass(
                1,
                (samp_rate / decim / decim_2),
                15e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decim_2,
            firdes.low_pass(
                1,
                (int(samp_rate / decim)),
                100e3,
                15e3,
                window.WIN_HAMMING,
                6.76))
        self.dc_blocker_xx_1 = filter.dc_blocker_ff(32, True)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(0.5)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.5)
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
        self.analog_agc_xx_0 = analog.agc_cc((1e-2), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_fm_deemph_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_2, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_freq_sink_x_3, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_3_0_0, 0))
        self.connect((self.band_pass_filter_1, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.band_pass_filter_1, 0), (self.qtgui_freq_sink_x_3_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_3_0_1_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.band_pass_filter_1, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.qtgui_freq_sink_x_3_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.dc_blocker_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_3, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.low_pass_filter_1_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_freq_sink_x_3_0_1_1, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.dc_blocker_xx_1, 0), (self.audio_sink_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_fm_deemph_0_0, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.low_pass_filter_2, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.low_pass_filter_2, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.low_pass_filter_3, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.low_pass_filter_3, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wbfm_rx_stereo_ll")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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
            self.set_audio_decim(int(self.samp_rate / self.decim / self.decim_2 / self.audio_samp_rate))
            self.set_decim(int(self.samp_rate / 1e6))
            self.set_decim_2(int((self.samp_rate / self.decim) / 0.25e6))
            self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
            self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, (self.samp_rate / self.decim / self.decim_2), 18.8e3, 19.2e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 23e3, 53e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_1.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 37.9e3, 38.1e3, 500, window.WIN_HAMMING, 6.76))
            self.high_pass_filter_2_0.set_taps(firdes.high_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, (int(self.samp_rate / self.decim)), 100e3, 15e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_2.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_3.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))

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
            self.set_audio_decim(int(self.samp_rate / self.decim / self.decim_2 / self.audio_samp_rate))
            self.set_decim_2(int((self.samp_rate / self.decim) / 0.25e6))
            self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, (self.samp_rate / self.decim / self.decim_2), 18.8e3, 19.2e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 23e3, 53e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_1.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 37.9e3, 38.1e3, 500, window.WIN_HAMMING, 6.76))
            self.high_pass_filter_2_0.set_taps(firdes.high_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, (int(self.samp_rate / self.decim)), 100e3, 15e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_2.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_3.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))

    def get_decim_2(self):
        return self.decim_2

    def set_decim_2(self, decim_2):
        with self._lock:
            self.decim_2 = decim_2
            self.set_audio_decim(int(self.samp_rate / self.decim / self.decim_2 / self.audio_samp_rate))
            self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, (self.samp_rate / self.decim / self.decim_2), 18.8e3, 19.2e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 23e3, 53e3, 1e3, window.WIN_HAMMING, 6.76))
            self.band_pass_filter_1.set_taps(firdes.band_pass(1, (self.samp_rate / self.decim / self.decim_2), 37.9e3, 38.1e3, 500, window.WIN_HAMMING, 6.76))
            self.high_pass_filter_2_0.set_taps(firdes.high_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 15e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_2.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))
            self.low_pass_filter_3.set_taps(firdes.low_pass(1, (self.samp_rate / self.decim / self.decim_2), 13e3, 1e3, window.WIN_HAMMING, 6.76))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        with self._lock:
            self.audio_samp_rate = audio_samp_rate
            self.set_audio_decim(int(self.samp_rate / self.decim / self.decim_2 / self.audio_samp_rate))

    def get_wbfm_deviation(self):
        return self.wbfm_deviation

    def set_wbfm_deviation(self, wbfm_deviation):
        with self._lock:
            self.wbfm_deviation = wbfm_deviation
            self.analog_quadrature_demod_cf_0.set_gain((0.25e6/(2*math.pi* self.wbfm_deviation)))

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        with self._lock:
            self.audio_decim = audio_decim



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
        "-f", "--signal-freq", dest="signal_freq", type=eng_float, default=eng_notation.num_to_str(float(int(99.6e6))),
        help="Set frequency of wfm station [default=%(default)r]")
    return parser


def main(top_block_cls=wbfm_rx_stereo_ll, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(centre_freq=options.centre_freq, ip_arg=options.ip_arg, port_arg=options.port_arg, samp_rate=options.samp_rate, signal_freq=options.signal_freq)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
