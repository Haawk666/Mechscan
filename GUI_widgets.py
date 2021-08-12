# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import TensorFlowAPI as tf
import DataManager
import Signals
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataInterface(QtWidgets.QGroupBox):

    def __init__(self, *args):
        super().__init__(*args)

        self.setTitle('Data interface')

        self.data = None

        self.btn_new = GUI_subwidgets.MediumButton('New', self, trigger_func=self.btn_new_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Clear', self, trigger_func=self.btn_clear_trigger)
        self.lbl_current = QtWidgets.QLabel('Current data: {}'.format(None))

        self.time_graph = pg.PlotWidget()
        self.time_graph.setTitle('Time domain signal')
        self.time_graph.setLabel('bottom', 'Time t, (s)')
        self.time_graph.setLabel('left', 'Amplitude')

        self.frequency_graph = pg.PlotWidget()
        self.frequency_graph.setTitle('Frequency domain signal')
        self.frequency_graph.setLabel('bottom', 'Frequency f, (Hz)')
        self.frequency_graph.setLabel('left', 'Amplitude')

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
        layout.addWidget(self.time_graph)
        layout.addWidget(self.frequency_graph)
        layout.addStretch()
        self.setLayout(layout)

    def btn_new_trigger(self):
        self.data = DataManager.TimeSignal()
        self.data.generate(lambda x: 1.0 * np.sin(2 * np.pi * x) + 1.0 * np.sin(2 * np.pi * 2 * x))
        self.time_graph.plot(self.data.X, self.data.Y)
        Omega, F = Signals.FFT(self.data.Y, self.data.T)
        self.frequency_graph.plot(Omega, F + 10000)

    def btn_save_trigger(self):
        if self.data:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save signal", '', "")
            if filename[0]:
                self.data.save(filename[0])

    def btn_load_trigger(self):
        if not self.data:
            self.data = DataManager.TimeSignal()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            self.data.load(filename[0])
            self.time_graph.plot(self.data.X, self.data.Y)
            Omega, F = Signals.FFT(self.data.Y)
            self.frequency_graph.plot(Omega, F)

    def btn_clear_trigger(self):
        self.data = None
        self.time_graph.plotItem.clear()
        self.frequency_graph.plotItem.clear()


class ModelInterface(QtWidgets.QGroupBox):

    def __init__(self, *args):
        super().__init__(*args)

        self.setTitle('Model interface')

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
















