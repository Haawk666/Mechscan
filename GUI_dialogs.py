# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
# Internals
import DataManager
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GenerateTimeSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Generate signal')

        self.ui_obj = ui_object
        self.stage = 0

        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_f_a = QtWidgets.QDoubleSpinBox()
        self.box_f_a.setMaximum(88000.0)
        self.box_f_a.setMinimum(1.0)
        self.box_f_a.setDecimals(1)

        self.cmb_bits = QtWidgets.QComboBox()
        self.cmb_bits.addItems(['8', '16'])

        self.box_t_start = QtWidgets.QDoubleSpinBox()
        self.box_t_start.setDecimals(3)

        self.box_t_end = QtWidgets.QDoubleSpinBox()
        self.box_t_end.setDecimals(3)

        if self.ui_obj.signal is not None:
            self.box_f_a.setValue(self.ui_obj.signal.f_a)
            self.box_t_start.setValue(self.ui_obj.signal.t_start)
            self.box_t_end.setValue(self.ui_obj.signal.t_end)
        else:
            self.box_f_a.setValue(44000.0)
            self.box_t_start.setValue(0.0)
            self.box_t_end.setValue(1.0)

        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems([
            'Constant',
            'Sine',
            'Cosine',
            'Pulse',
            'Gaussian noise'
        ])

        self.box_const = QtWidgets.QDoubleSpinBox()
        self.box_const.setDecimals(3)
        self.box_const.setValue(1.0)

        self.box_amp = QtWidgets.QDoubleSpinBox()
        self.box_amp.setDecimals(3)
        self.box_amp.setValue(1.0)

        self.box_freq = QtWidgets.QDoubleSpinBox()
        self.box_freq.setDecimals(1)
        self.box_freq.setValue(2.0)

        self.box_phase = QtWidgets.QDoubleSpinBox()
        self.box_phase.setDecimals(1)
        self.box_phase.setValue(0.0)

        self.box_mu = QtWidgets.QDoubleSpinBox()
        self.box_mu.setDecimals(3)
        self.box_mu.setValue(0.5)

        self.box_sigma = QtWidgets.QDoubleSpinBox()
        self.box_sigma.setDecimals(3)
        self.box_sigma.setValue(0.1)

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Sample rate f_a (Hz)'), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Bits'), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Start time (s)'), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('End time (s)'), 3, 0)
        base_grid.addWidget(QtWidgets.QLabel('Type'), 4, 0)
        base_grid.addWidget(self.box_f_a, 0, 1)
        base_grid.addWidget(self.cmb_bits, 1, 1)
        base_grid.addWidget(self.box_t_start, 2, 1)
        base_grid.addWidget(self.box_t_end, 3, 1)
        base_grid.addWidget(self.cmb_type, 4, 1)
        base_widget = QtWidgets.QWidget()
        base_widget.setLayout(base_grid)
        self.stack.addWidget(base_widget)

        const_grid = QtWidgets.QGridLayout()
        const_grid.addWidget(QtWidgets.QLabel('Value'), 0, 0)
        const_grid.addWidget(self.box_const, 0, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(const_grid)
        self.stack.addWidget(const_widget)

        sine_grid = QtWidgets.QGridLayout()
        sine_grid.addWidget(QtWidgets.QLabel('Amplitude'), 0, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Frequency'), 1, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Phase'), 2, 0)
        sine_grid.addWidget(self.box_amp, 0, 1)
        sine_grid.addWidget(self.box_freq, 1, 1)
        sine_grid.addWidget(self.box_phase, 2, 1)
        sine_widget = QtWidgets.QWidget()
        sine_widget.setLayout(sine_grid)
        self.stack.addWidget(sine_widget)

        gauss_grid = QtWidgets.QGridLayout()
        gauss_grid.addWidget(QtWidgets.QLabel('mu'), 0, 0)
        gauss_grid.addWidget(QtWidgets.QLabel('sigma'), 1, 0)
        gauss_grid.addWidget(self.box_mu, 0, 1)
        gauss_grid.addWidget(self.box_sigma, 1, 1)
        gauss_widget = QtWidgets.QWidget()
        gauss_widget.setLayout(gauss_grid)
        self.stack.addWidget(gauss_widget)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.stack)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        if self.stage == 0:
            self.close()
        else:
            self.btn_next.setText('Next')
            self.btn_cancel.setText('Cancel')
            self.stack.setCurrentIndex(0)
            self.stage = 0

    def btn_next_trigger(self):
        if self.stage == 0:
            next_index = 0
            type_text = self.cmb_type.currentText()
            if type_text == 'Constant':
                next_index = 1
            elif type_text == 'Sine' or type_text == 'Cosine':
                next_index = 2
            elif type_text == 'Pulse' or type_text == 'Gaussian noise':
                next_index = 3
            else:
                self.close()
            self.btn_next.setText('Generate')
            self.btn_cancel.setText('Back')
            self.stack.setCurrentIndex(next_index)
            self.stage += 1
        else:
            self.gen_signal()
            self.close()

    def gen_signal(self):
        self.ui_obj.signal = DataManager.TimeSignal(
            t_start=self.box_t_start.value(),
            t_end=self.box_t_end.value(),
            sampling_rate=self.box_f_a.value(),
            bits=int(self.cmb_bits.currentText())
        )

        type_text = self.cmb_type.currentText()
        if type_text == 'Constant':
            const = self.box_const.value()
            for k, y in enumerate(self.ui_obj.signal.X):
                self.ui_obj.signal.Y[k] = int(const)
        elif type_text == 'Sine':
            amp = self.box_amp.value()
            freq = self.box_freq.value()
            phase = self.box_phase.value()
            self.ui_obj.signal.generate(lambda x: amp * np.sin(2 * np.pi * freq * x - phase))
        elif type_text == 'Cosine':
            amp = self.box_amp.value()
            freq = self.box_freq.value()
            phase = self.box_phase.value()
            self.ui_obj.signal.generate(lambda x: amp * np.cos(2 * np.pi * freq * x - phase))
        elif type_text == 'Pulse':
            mu = self.box_mu.value()
            sigma = self.box_sigma.value()
            self.ui_obj.signal.generate(lambda x: (1 / np.sqrt(2 * np.pi * sigma)) * np.exp(-(x - mu)**2/(2 * sigma)))
        elif type_text == 'Gaussian noise':
            mu = self.box_mu.value()
            sigma = self.box_sigma.value()
            self.ui_obj.signal.add_noise_gauss(mu, sigma)


class ImportTimeSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Import signal')

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Import')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems([
            'Wav'
        ])

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.addStretch()
        content_layout.addWidget(self.cmb_type)
        content_layout.addStretch()

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(content_layout)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_signal()
        self.close()

    def gen_signal(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal from wav", '', "")
        if filename[0]:
            if self.cmb_type.currentText() == 'Wav':
                self.ui_obj.signal = DataManager.TimeSignal.import_wav_signal(filename[0])


class ExportTimeSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Export signal')

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Export')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems([
            'Wav'
        ])

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.addStretch()
        content_layout.addWidget(self.cmb_type)
        content_layout.addStretch()

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(content_layout)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        if self.ui_obj.signal is not None:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Export signal", '', "")
            if filename[0]:
                if self.cmb_type.currentText() == 'Wav':
                    self.ui_obj.signal.export_wav_signal(filename[0])
        self.close()



