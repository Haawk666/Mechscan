# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import random
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import GUI_dialogs
import TensorFlowAPI as tf
import DataManager
import Signals
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SignalInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.signal = None

        self.btn_generate = GUI_subwidgets.MediumButton('Generate', self, trigger_func=self.btn_generate_trigger)
        self.btn_import = GUI_subwidgets.MediumButton('Import', self, trigger_func=self.btn_import_trigger)
        self.btn_export = GUI_subwidgets.MediumButton('Export', self, trigger_func=self.btn_export_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Clear', self, trigger_func=self.btn_clear_trigger)
        self.lbl_current = QtWidgets.QLabel('Current signal: {}'.format(None))

        self.lbl_f_a = QtWidgets.QLabel('')
        self.lbl_bits = QtWidgets.QLabel('')
        self.lbl_t_start = QtWidgets.QLabel('')
        self.lbl_t_end = QtWidgets.QLabel('')
        self.lbl_T = QtWidgets.QLabel('')
        self.lbl_omega_a = QtWidgets.QLabel('')
        self.lbl_n = QtWidgets.QLabel('')
        self.lbl_length = QtWidgets.QLabel('')

        self.time_graph = pg.PlotWidget()
        self.time_graph.setTitle('Time domain signal')
        self.time_graph.setLabel('bottom', 'Time t, (s)')
        self.time_graph.setLabel('left', 'Amplitude')

        self.frequency_graph = pg.PlotWidget()
        self.frequency_graph.setTitle('Frequency domain signal')
        self.frequency_graph.setLabel('bottom', 'Frequency f, (Hz)')
        self.frequency_graph.setLabel('left', 'Amplitude')

        self.build_layout()
        self.update_info()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_import)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.lbl_current)
        btn_layout.addStretch()

        info_layout = QtWidgets.QGridLayout()
        info_layout.addWidget(QtWidgets.QLabel('Sampling frequency f_a, (Hz): '), 0, 0)
        info_layout.addWidget(QtWidgets.QLabel('Bits: '), 1, 0)
        info_layout.addWidget(QtWidgets.QLabel('Start time t_start, (s): '), 2, 0)
        info_layout.addWidget(QtWidgets.QLabel('End time t_end, (s): '), 3, 0)
        info_layout.addWidget(QtWidgets.QLabel('Sample interval T, (s): '), 4, 0)
        info_layout.addWidget(QtWidgets.QLabel('Angular sampling frequency omega_a, (Hz): \t'), 5, 0)
        info_layout.addWidget(QtWidgets.QLabel('Number of samples n, (#): '), 6, 0)
        info_layout.addWidget(QtWidgets.QLabel('Signal length (s): '), 7, 0)
        info_layout.addWidget(self.lbl_f_a, 0, 1)
        info_layout.addWidget(self.lbl_bits, 1, 1)
        info_layout.addWidget(self.lbl_t_start, 2, 1)
        info_layout.addWidget(self.lbl_t_end, 3, 1)
        info_layout.addWidget(self.lbl_T, 4, 1)
        info_layout.addWidget(self.lbl_omega_a, 5, 1)
        info_layout.addWidget(self.lbl_n, 6, 1)
        info_layout.addWidget(self.lbl_length, 7, 1)

        outer_info_layout = QtWidgets.QHBoxLayout()
        outer_info_layout.addLayout(info_layout)
        outer_info_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(GUI_subwidgets.HorSeparator())
        layout.addLayout(outer_info_layout)
        layout.addWidget(self.time_graph)
        layout.addWidget(self.frequency_graph)
        layout.addStretch()
        self.setLayout(layout)

    def btn_generate_trigger(self):
        GUI_dialogs.GenerateTimeSignal(ui_object=self)
        self.update_info()

    def btn_import_trigger(self):
        GUI_dialogs.ImportTimeSignal(ui_object=self)
        self.update_info()

    def btn_export_trigger(self):
        GUI_dialogs.ExportTimeSignal(ui_object=self)

    def btn_save_trigger(self):
        if self.signal:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save signal", '', "")
            if filename[0]:
                self.signal.save(filename[0])

    def btn_load_trigger(self):
        if not self.signal:
            self.signal = DataManager.TimeSignal()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            self.signal.load(filename[0])
            self.update_info()

    def btn_clear_trigger(self):
        self.signal = None
        self.update_info()

    def plot_signal(self):
        self.time_graph.plotItem.clear()
        self.time_graph.plot(self.signal.X, self.signal.Y)

    def plot_power_spectrum(self):
        self.frequency_graph.plotItem.clear()
        Y_f = np.absolute(np.fft.fft(self.signal.Y))[:self.signal.n//2]
        X_f = np.fft.fftfreq(n=self.signal.n, d=1/self.signal.f_a)[:self.signal.n//2]
        self.frequency_graph.plot(X_f, Y_f)

    def update_info(self):
        if self.signal:
            self.plot_signal()
            self.plot_power_spectrum()
            self.lbl_f_a.setText('{}'.format(self.signal.f_a))
            self.lbl_bits.setText('{}'.format(self.signal.bits))
            self.lbl_t_start.setText('{}'.format(self.signal.t_start))
            self.lbl_t_end.setText('{}'.format(self.signal.t_end))
            self.lbl_T.setText('{}'.format(self.signal.T))
            self.lbl_omega_a.setText('{}'.format(self.signal.omega_a))
            self.lbl_n.setText('{}'.format(self.signal.n))
            self.lbl_length.setText('{}'.format(self.signal.t_end - self.signal.t_start))
        else:
            self.time_graph.plotItem.clear()
            self.frequency_graph.plotItem.clear()
            self.lbl_f_a.setText('')
            self.lbl_t_start.setText('')
            self.lbl_t_end.setText('')
            self.lbl_T.setText('')
            self.lbl_omega_a.setText('')
            self.lbl_n.setText('')
            self.lbl_length.setText('')


class DataInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.data = None

        self.btn_new = GUI_subwidgets.MediumButton('New', self, trigger_func=self.btn_new_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Clear', self, trigger_func=self.btn_clear_trigger)
        self.lbl_current = QtWidgets.QLabel('Current data: {}'.format(None))

        self.build_layout()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(GUI_subwidgets.HorSeparator())

        layout.addStretch()
        self.setLayout(layout)

    def btn_new_trigger(self):
        pass

    def btn_save_trigger(self):
        pass

    def btn_load_trigger(self):
        pass

    def btn_clear_trigger(self):
        pass


class ModelInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.model = tf.Model('New')

        self.btn_new = GUI_subwidgets.MediumButton('New', self, trigger_func=self.btn_new_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Clear', self, trigger_func=self.btn_clear_trigger)
        self.lbl_current = QtWidgets.QLabel('Current model: {}'.format(self.model.name))

        self.build_layout()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.lbl_current)
        btn_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(GUI_subwidgets.HorSeparator())
        layout.addStretch()
        self.setLayout(layout)

    def btn_new_trigger(self):
        self.model = tf.Model('New')
        self.lbl_current.setText('Current model: {}'.format(self.model.name))

    def btn_load_trigger(self):
        pass

    def btn_save_trigger(self):
        pass

    def btn_clear_trigger(self):
        pass
















