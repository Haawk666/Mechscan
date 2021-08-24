# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
import random
# Internals
import GUI_subwidgets
import Signals as ss
import SignalProcessing as sp
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SignalsInterface(QtWidgets.QWidget):

    def __init__(self, *args, menu=None):
        super().__init__(*args)

        self.signal_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.menu = menu.addMenu('Signal')
        self.populate_menu()

        self.build_layout()

    def populate_menu(self):

        generate = self.menu.addMenu('Generate')
        generate.addAction(GUI_subwidgets.Action('Time domain', self, trigger_func=self.menu_generate_time_trigger))
        generate.addAction(GUI_subwidgets.Action('Frequency domain', self, trigger_func=self.menu_generate_frequency_trigger))

        new = self.menu.addMenu('New')
        new.addAction(GUI_subwidgets.Action('Time domain', self, trigger_func=self.menu_new_time_trigger))
        new.addAction(GUI_subwidgets.Action('Frequency domain', self, trigger_func=self.menu_new_frequency_trigger))

        self.menu.addAction(GUI_subwidgets.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_subwidgets.Action('Import', self, trigger_func=self.menu_import_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Export', self, trigger_func=self.menu_export_trigger))

        self.menu.addSeparator()

        transforms = self.menu.addMenu('Transforms')
        transforms.addAction(GUI_subwidgets.Action('Fast Fourier Transform', self, trigger_func=self.menu_FFT_trigger))
        transforms.addAction(GUI_subwidgets.Action('Gabor transform', self, trigger_func=self.menu_gabor_trigger))
        transforms.addAction(GUI_subwidgets.Action('Wavelet transform', self, trigger_func=self.menu_wavelet_trigger))
        transforms.addAction(GUI_subwidgets.Action('Z-transform', self, trigger_func=self.menu_z_trigger))
        transforms.addAction(GUI_subwidgets.Action('Laplace transform', self, trigger_func=self.menu_laplace_trigger))

        filters = self.menu.addMenu('Filters/effects')
        filters.addAction(GUI_subwidgets.Action('Low pass', self, trigger_func=self.menu_low_pass_trigger))
        filters.addAction(GUI_subwidgets.Action('High pass', self, trigger_func=self.menu_high_pass_trigger))
        filters.addAction(GUI_subwidgets.Action('Band pass', self, trigger_func=self.menu_band_pass_trigger))
        filters.addAction(GUI_subwidgets.Action('Cut-off', self, trigger_func=self.menu_cut_trigger))
        filters.addAction(GUI_subwidgets.Action('Compression', self, trigger_func=self.menu_compression_trigger))
        filters.addAction(GUI_subwidgets.Action('Noise', self, trigger_func=self.menu_noise_trigger))

        edit = self.menu.addMenu('Edit')
        edit.addAction(GUI_subwidgets.Action('Scale', self, trigger_func=self.menu_scale_trigger))
        edit.addAction(GUI_subwidgets.Action('Shift', self, trigger_func=self.menu_shift_trigger))
        edit.addAction(GUI_subwidgets.Action('Crop', self, trigger_func=self.menu_crop_trigger))
        edit.addAction(GUI_subwidgets.Action('Functions', self, trigger_func=self.menu_combine_trigger))
        edit.addAction(GUI_subwidgets.Action('Resample', self, trigger_func=self.menu_resample_trigger))

    def build_layout(self):

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def add_interface(self, interface):
        if interface.signal:
            self.tabs.addTab(interface, '{}'.format(interface.signal.name()))
        else:
            self.tabs.addTab(interface, 'Empty')
        self.signal_interfaces.append(interface)
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def add_signal(self, signal):
        interface = SignalInterface()
        interface.signal = signal
        interface.update_info()
        self.add_interface(interface)

    def menu_generate_time_trigger(self):
        signal_interface = SignalInterface()
        wizard = GenerateTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            signal_interface.update_info()
            self.add_interface(signal_interface)

    def menu_generate_frequency_trigger(self):
        pass

    def menu_new_time_trigger(self):
        self.add_signal(ss.TimeSignal())

    def menu_new_frequency_trigger(self):
        self.add_signal(ss.FrequencySignal())

    def menu_save_trigger(self):
        index = self.tabs.currentIndex()
        signal_interface = self.signal_interfaces[index]
        if signal_interface.signal:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save signal", '', "")
            if filename[0]:
                signal_interface.signal.save(filename[0])
                self.tabs.setTabText(index, signal_interface.signal.name())

    def menu_load_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            signal_interface = SignalInterface()
            signal_interface.signal = ss.TimeSignal.static_load(filename[0])
            signal_interface.update_info()
            self.add_interface(signal_interface)

    def menu_close_trigger(self):
        if len(self.tabs) > 0:
            index = self.tabs.currentIndex()
            self.signal_interfaces.pop(index)
            self.tabs.removeTab(index)

    def menu_close_all_trigger(self):
        self.signal_interfaces = []
        self.tabs.clear()

    def menu_import_trigger(self):
        signal_interface = SignalInterface()
        wizard = ImportTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            self.tabs.addTab(signal_interface, '{}'.format(signal_interface.signal.name()))
            self.signal_interfaces.append(signal_interface)
            signal_interface.update_info()
            self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def menu_export_trigger(self):
        index = self.tabs.currentIndex()
        interface = self.signal_interfaces[index]
        ExportTimeSignal(ui_object=interface)

    def menu_FFT_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                if signal.signal_type == 'time':
                    self.add_signal(ss.FrequencySignal.from_time_signal(signal))
                elif signal.signal_type == 'frequency':
                    self.add_signal(ss.TimeSignal.from_frequency(signal))

    def menu_gabor_trigger(self):
        pass

    def menu_wavelet_trigger(self):
        pass

    def menu_z_trigger(self):
        pass

    def menu_laplace_trigger(self):
        pass

    def menu_low_pass_trigger(self):
        pass

    def menu_high_pass_trigger(self):
        pass

    def menu_band_pass_trigger(self):
        pass

    def menu_cut_trigger(self):
        pass

    def menu_compression_trigger(self):
        pass

    def menu_noise_trigger(self):
        pass

    def menu_scale_trigger(self):
        pass

    def menu_shift_trigger(self):
        pass

    def menu_crop_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                interface = SignalInterface()
                interface.signal = signal
                wizard = CropSignal(ui_object=interface)
                interface.update_info()
                self.add_interface(interface)

    def menu_combine_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                interface = SignalInterface()
                interface.signal = signal
                wizard = Functions(ui_object=interface)
                if wizard.complete:
                    interface.update_info()
                    self.add_interface(interface)

    def menu_resample_trigger(self):
        pass


class SignalInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.signal = None

        self.btn_print = GUI_subwidgets.MediumButton('Print', self, trigger_func=self.btn_print_trigger)

        self.lbl_info_1 = QtWidgets.QLabel('')
        self.lbl_info_2 = QtWidgets.QLabel('')

        self.graph = pg.PlotWidget()
        self.graph.showGrid(x=True, y=True)

        self.build_layout()
        self.update_info()

    def build_layout(self):

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addWidget(self.lbl_info_1)
        info_layout.addWidget(self.lbl_info_2)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_print)
        btn_layout.addStretch()

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addLayout(info_layout)
        panel_layout.addStretch()
        panel_layout.addLayout(btn_layout)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graph)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def btn_print_trigger(self):
        self.update_info()
        print(self.signal)

    def plot_signal(self):
        self.graph.plotItem.clear()
        if self.signal is not None:
            if self.signal.signal_type == 'time':
                self.graph.setTitle('Time domain signal')
                self.graph.setLabel('bottom', 'Time t, (s)')
                self.graph.setLabel('left', 'Amplitude')
                for j in range(self.signal.channels):
                    plot_line = self.graph.plot(self.signal.X, self.signal.Y[:, j])
                    plot_line.setAlpha(0.65, False)
            elif self.signal.signal_type == 'frequency':
                self.graph.setTitle('Power density spectrum')
                self.graph.setLabel('bottom', 'Frequency f, (Hz)')
                self.graph.setLabel('left', 'Magnitude')
                for j in range(self.signal.channels):
                    plot_line = self.graph.plot(self.signal.X, np.absolute(self.signal.Y[:, j]))
                    plot_line.setAlpha(0.65, False)
            else:
                self.graph.setTitle('Generic signal')
                self.graph.setLabel('bottom', 'Independent variable')
                self.graph.setLabel('left', 'Signal')

    def update_info(self):
        if self.signal:
            self.plot_signal()
            info_1, info_2 = self.signal.info()
            self.lbl_info_1.setText(info_1)
            self.lbl_info_2.setText(info_2)
        else:
            self.graph.plotItem.clear()
            self.lbl_info_1.setText('')
            self.lbl_info_2.setText('')


class Functions(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Functions')

        self.ui_obj = ui_object

        self.complete = False

        self.stage = 0
        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_functions = QtWidgets.QComboBox()
        self.cmb_functions.addItems([
            'Custom',
        ])

        self.cmb_operation = QtWidgets.QComboBox()
        self.cmb_operation.addItems([
            'Overwrite',
            'Add',
            'Subtract',
            'Multiply',
            'Convolve'
        ])

        self.chb_all_channels = QtWidgets.QCheckBox('All channels')
        self.chb_all_channels.setChecked(True)
        self.chb_all_channels.toggled.connect(self.chb_all_channels_trigger)

        self.cmb_channels = QtWidgets.QComboBox()
        if self.ui_obj.signal is not None:
            for nchan in range(self.ui_obj.signal.channels):
                self.cmb_channels.addItem('Channel {}'.format(nchan + 1))
        self.cmb_channels.setDisabled(True)

        self.lbl_explain = QtWidgets.QLabel('Enter a function as a string, ie: \'100 * np.exp(0.5 * x)\'.\nIf the signal has multiple dimensions, use \'x_1\', \'x_2\', etc...')

        self.box_function = QtWidgets.QLineEdit()

        self.box_amp_x = QtWidgets.QDoubleSpinBox()
        self.box_amp_x.setDecimals(1)
        self.box_amp_x.setMinimum(-1000.0)
        self.box_amp_x.setMaximum(1000.0)
        self.box_amp_x.setSingleStep(10.0)
        self.box_amp_x.setValue(0.0)

        self.box_mu_x = QtWidgets.QDoubleSpinBox()
        self.box_mu_x.setDecimals(1)
        self.box_mu_x.setMinimum(0.0)
        self.box_mu_x.setMaximum(100.0)
        self.box_mu_x.setSingleStep(1.0)
        self.box_mu_x.setValue(0.0)

        self.box_sigma_x = QtWidgets.QDoubleSpinBox()
        self.box_sigma_x.setDecimals(1)
        self.box_sigma_x.setMinimum(0.0)
        self.box_sigma_x.setMaximum(1000.0)
        self.box_sigma_x.setSingleStep(1.0)
        self.box_sigma_x.setValue(10.0)

        self.box_amp_sin = QtWidgets.QDoubleSpinBox()
        self.box_amp_sin.setDecimals(1)
        self.box_amp_sin.setMinimum(0.0)
        self.box_amp_sin.setMaximum(1000.0)
        self.box_amp_sin.setSingleStep(10.0)
        self.box_amp_sin.setValue(666.0)

        self.box_freq_sin = QtWidgets.QDoubleSpinBox()
        self.box_freq_sin.setDecimals(1)
        self.box_freq_sin.setMinimum(0.0)
        self.box_freq_sin.setMaximum(10000.0)
        self.box_freq_sin.setSingleStep(10.0)
        self.box_freq_sin.setValue(666.0)

        self.box_phase_sin = QtWidgets.QDoubleSpinBox()
        self.box_phase_sin.setDecimals(1)
        self.box_phase_sin.setMinimum(-2.0 * np.pi)
        self.box_phase_sin.setMaximum(2.0 * np.pi)
        self.box_phase_sin.setSingleStep(1.0)
        self.box_phase_sin.setValue(0.0)

        self.box_step = QtWidgets.QDoubleSpinBox()
        self.box_step.setDecimals(1)
        self.box_step.setMinimum(-10.0)
        self.box_step.setMaximum(10.0)
        self.box_step.setSingleStep(1.0)
        self.box_step.setValue(0.0)

        self.box_delta = QtWidgets.QDoubleSpinBox()
        self.box_delta.setDecimals(1)
        self.box_delta.setMinimum(-10.0)
        self.box_delta.setMaximum(10.0)
        self.box_delta.setSingleStep(1.0)
        self.box_delta.setValue(0.0)

        self.box_mu_noise = QtWidgets.QDoubleSpinBox()
        self.box_mu_noise.setDecimals(1)
        self.box_mu_noise.setMinimum(-10.0)
        self.box_mu_noise.setMaximum(10.0)
        self.box_mu_noise.setSingleStep(1.0)
        self.box_mu_noise.setValue(0.0)

        self.box_sigma_noise = QtWidgets.QDoubleSpinBox()
        self.box_sigma_noise.setDecimals(1)
        self.box_sigma_noise.setMinimum(0.0)
        self.box_sigma_noise.setMaximum(100.0)
        self.box_sigma_noise.setSingleStep(1.0)
        self.box_sigma_noise.setValue(10.0)

        self.build_layout()

        self.exec_()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        if self.ui_obj.signal.signal_type == 'time':
            self.cmb_functions.addItems([
                'Gaussian pulse',
                'Sine',
                'Step',
                'Delta',
                'Noise'
            ])
        elif self.ui_obj.signal.signal_type == 'frequency':
            self.cmb_functions.addItems([
                'Gaussian pulse',
                'Hyperbolic',
                'Delta',
                'Noise'
            ])

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Functions: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Operation: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channels: '), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channel: '), 3, 0)
        base_grid.addWidget(self.cmb_functions, 0, 1)
        base_grid.addWidget(self.cmb_operation, 1, 1)
        base_grid.addWidget(self.chb_all_channels, 2, 1)
        base_grid.addWidget(self.cmb_channels, 3, 1)
        base_widget = QtWidgets.QWidget()
        base_widget.setLayout(base_grid)
        self.stack.addWidget(base_widget)

        custom_function_grid = QtWidgets.QGridLayout()
        custom_function_grid.addWidget(self.lbl_explain, 0, 0, 0, 2)
        custom_function_grid.addWidget(QtWidgets.QLabel('Function string: '), 1, 0)
        custom_function_grid.addWidget(self.box_function, 1, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(custom_function_grid)
        self.stack.addWidget(const_widget)

        pulse_grid = QtWidgets.QGridLayout()
        pulse_grid.addWidget(QtWidgets.QLabel('Scale by: '), 0, 0)
        pulse_grid.addWidget(QtWidgets.QLabel('Mu: '), 1, 0)
        pulse_grid.addWidget(QtWidgets.QLabel('Sigma: '), 2, 0)
        pulse_grid.addWidget(self.box_amp_x, 0, 1)
        pulse_grid.addWidget(self.box_mu_x, 1, 1)
        pulse_grid.addWidget(self.box_sigma_x, 2, 1)
        pulse_widget = QtWidgets.QWidget()
        pulse_widget.setLayout(pulse_grid)
        self.stack.addWidget(pulse_widget)

        sine_grid = QtWidgets.QGridLayout()
        sine_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Frequency: '), 1, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Phase: '), 2, 0)
        sine_grid.addWidget(self.box_amp_sin, 0, 1)
        sine_grid.addWidget(self.box_freq_sin, 1, 1)
        sine_grid.addWidget(self.box_phase_sin, 2, 1)
        sine_widget = QtWidgets.QWidget()
        sine_widget.setLayout(sine_grid)
        self.stack.addWidget(sine_widget)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.stack)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def chb_all_channels_trigger(self, state):
        if state:
            self.cmb_channels.setDisabled(True)
        else:
            self.cmb_channels.setDisabled(False)

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
            self.btn_next.setText('Generate')
            self.btn_cancel.setText('Back')
            next_index = 1
            if self.cmb_functions.currentText() == 'Gaussian pulse':
                next_index = 2
            elif self.cmb_functions.currentText() == 'Sine':
                next_index = 3
            elif self.cmb_functions.currentText() == 'Step':
                next_index = 4
            elif self.cmb_functions.currentText() == 'Delta':
                next_index = 5
            elif self.cmb_functions.currentText() == 'Noise':
                next_index = 6
            self.stack.setCurrentIndex(next_index)
            self.stage += 1
        else:
            self.gen_signal()
            self.close()
            self.complete = True

    def gen_signal(self):

        function_string = self.box_function.text()
        operation = self.cmb_operation.currentText()
        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels)]

        if self.cmb_functions.currentText() == 'Gaussian pulse':
            amp = self.box_amp_x.value()
            mu = self.box_mu_x.value()
            sigma = self.box_sigma_x.value()
            function_string = '{} * np.exp(-0.5 * ((x - {}) / {}) ** 2) / ({} * np.sqrt(2 * np.pi))'.format(amp, mu, sigma, sigma)
        elif self.cmb_functions.currentText() == 'Sine':
            amp = self.box_amp_sin.value()
            f = self.box_freq_sin.value()
            theta = self.box_phase_sin.value()
            function_string = '{} * np.sin(2 * np.pi * {} - {})'.format(amp, f, theta)

        if operation == 'Overwrite':
            self.ui_obj.signal.generate_function(lambda x: eval(function_string), channels)
        elif operation == 'Add':
            self.ui_obj.signal.add_function(lambda x: eval(function_string), channels)
        elif operation == 'Subtract':
            self.ui_obj.signal.subtract_function(lambda x: eval(function_string), channels)
        elif operation == 'Multiply':
            self.ui_obj.signal.multiply_function(lambda x: eval(function_string), channels)
        elif operation == 'Convolve':
            self.ui_objsignal.convolve_function(lambda x: eval(function_string), channels)
        else:
            logger.info('error')
            print('error')


class GenerateTimeSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Generate signal')

        self.complete = False

        self.ui_obj = ui_object
        self.stage = 0

        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_f_a = QtWidgets.QDoubleSpinBox()
        self.box_f_a.setMaximum(88200.0)
        self.box_f_a.setMinimum(1.0)
        self.box_f_a.setDecimals(1)
        self.box_f_a.setSingleStep(100.0)

        self.cmb_bits = QtWidgets.QComboBox()
        self.cmb_bits.addItems(['8', '16', '32', '64'])
        self.cmb_bits.setCurrentIndex(1)

        self.box_t_start = QtWidgets.QDoubleSpinBox()
        self.box_t_start.setDecimals(3)

        self.box_t_end = QtWidgets.QDoubleSpinBox()
        self.box_t_end.setDecimals(3)

        self.box_channels = QtWidgets.QSpinBox()
        self.box_channels.setMaximum(10)
        self.box_channels.setMinimum(1)
        self.box_channels.setSingleStep(1)

        if self.ui_obj.signal is not None:
            self.box_f_a.setValue(self.ui_obj.signal.f_a)
            self.box_t_start.setValue(self.ui_obj.signal.t_start)
            self.box_t_end.setValue(self.ui_obj.signal.t_end)
            self.box_channels.setValue(self.ui_obj.signal.channels)
        else:
            self.box_f_a.setValue(44100.0)
            self.box_t_start.setValue(0.0)
            self.box_t_end.setValue(5.0)
            self.box_channels.setValue(1)

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
        self.box_const.setValue(10.0)
        self.box_const.setMaximum(10000.0)
        self.box_const.setMinimum(-10000.0)
        self.box_const.setSingleStep(10.0)

        self.box_amp = QtWidgets.QDoubleSpinBox()
        self.box_amp.setMaximum(10000.0)
        self.box_amp.setMinimum(0.0)
        self.box_amp.setDecimals(1)
        self.box_amp.setSingleStep(10.0)
        self.box_amp.setValue(1000.0)

        self.box_freq = QtWidgets.QDoubleSpinBox()
        self.box_freq.setMaximum(44100.0)
        self.box_freq.setMinimum(0.0)
        self.box_freq.setDecimals(1)
        self.box_freq.setSingleStep(10.0)
        self.box_freq.setValue(420.0)

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
        base_grid.addWidget(QtWidgets.QLabel('Channels'), 5, 0)
        base_grid.addWidget(self.box_f_a, 0, 1)
        base_grid.addWidget(self.cmb_bits, 1, 1)
        base_grid.addWidget(self.box_t_start, 2, 1)
        base_grid.addWidget(self.box_t_end, 3, 1)
        base_grid.addWidget(self.cmb_type, 4, 1)
        base_grid.addWidget(self.box_channels, 5, 1)
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
            self.complete = True

    def gen_signal(self):
        self.ui_obj.signal = ss.TimeSignal(
            x_start=self.box_t_start.value(),
            x_end=self.box_t_end.value(),
            delta_x=1/self.box_f_a.value(),
            bit_depth=int(self.cmb_bits.currentText()),
            channels=int(self.box_channels.value())
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
            self.ui_obj.signal.generate_function(lambda x: amp * np.sin(2 * np.pi * freq * x - phase))
        elif type_text == 'Cosine':
            amp = self.box_amp.value()
            freq = self.box_freq.value()
            phase = self.box_phase.value()
            self.ui_obj.signal.generate_function(lambda x: amp * np.cos(2 * np.pi * freq * x - phase))
        elif type_text == 'Pulse':
            mu = self.box_mu.value()
            sigma = self.box_sigma.value()
            self.ui_obj.signal.generate_function(lambda x: (1 / np.sqrt(2 * np.pi * sigma)) * np.exp(-(x - mu) ** 2 / (2 * sigma)))
        elif type_text == 'Gaussian noise':
            mu = self.box_mu.value()
            sigma = self.box_sigma.value()
            sp.add_gaussian_noise(self.ui_obj.signal, mu, sigma)


class ImportTimeSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Import signal')

        self.complete = False

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
        self.complete = True

    def gen_signal(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal from wav", '', "")
        if filename[0]:
            if self.cmb_type.currentText() == 'Wav':
                self.ui_obj.signal = ss.TimeSignal.from_wav(filename[0])


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


class CropSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Crop signal')

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Crop')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_from = QtWidgets.QDoubleSpinBox()
        self.box_from.setDecimals(3)
        self.box_from.setSingleStep(1.0)
        self.box_from.setMinimum(self.ui_obj.signal.x_start)
        self.box_from.setMaximum(self.ui_obj.signal.x_end)
        self.box_from.setValue(self.ui_obj.signal.x_start)

        self.box_to = QtWidgets.QDoubleSpinBox()
        self.box_to.setDecimals(3)
        self.box_to.setSingleStep(1.0)
        self.box_to.setMinimum(self.ui_obj.signal.x_start)
        self.box_to.setMaximum(self.ui_obj.signal.x_end)
        self.box_to.setValue(self.ui_obj.signal.x_end)

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('From: '), 0, 0)
        grid.addWidget(QtWidgets.QLabel('To: '), 1, 0)
        grid.addWidget(self.box_from, 0, 1)
        grid.addWidget(self.box_to, 1, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        new_start = self.box_from.value()
        new_end = self.box_to.value()
        if new_start >= new_end:
            msg = QtWidgets.QMessageBox()
            msg.setText('Timestamp "to" must be larger than "from"!')
            msg.exec()
        else:
            start_index = 0
            end_index = self.ui_obj.signal.n - 1
            for i, x in enumerate(self.ui_obj.signal.X):
                if x >= new_start:
                    start_index = i
                    break
            for i, x in enumerate(self.ui_obj.signal.X):
                if x >= new_end:
                    end_index = i
                    break
            new_X = self.ui_obj.signal.X[start_index:end_index]
            new_Y = self.ui_obj.signal.Y[start_index:end_index]

            if self.ui_obj.signal.signal_type == 'time':
                self.ui_obj.signal = ss.TimeSignal.from_data(new_X, new_Y)
            elif self.ui_obj.signal.signal_type == 'frequency':
                self.ui_obj.signal = ss.FrequencySignal.from_data(new_X, new_Y)
            else:
                logger.info('error')
                print('error')
            self.close()


class FunctionSignal1DReal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Functions')

        self.ui_obj = ui_object

        self.complete = False

        self.stage = 0
        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_function = QtWidgets.QComboBox()
        self.cmb_function.addItems([
            'Constant',
            'Sine',
            'Cosine',
            'Pulse',
            'Noise'
        ])
        self.cmb_function.setCurrentIndex(0)

        self.cmb_operation = QtWidgets.QComboBox()
        self.cmb_operation.addItems([
            'Overwrite',
            'Add',
            'Subtract',
            'Multiply',
            'Convolve'
        ])

        self.chb_all_channels = QtWidgets.QCheckBox('All channels')
        self.chb_all_channels.setChecked(True)
        self.chb_all_channels.toggled.connect(self.chb_all_channels_trigger)

        self.cmb_channels = QtWidgets.QComboBox()
        if self.ui_obj.signal is not None:
            for nchan in range(self.ui_obj.signal.channels):
                self.cmb_channels.addItem('Channel {}'.format(nchan + 1))
        self.cmb_channels.setDisabled(True)

        self.box_const = QtWidgets.QDoubleSpinBox()
        self.box_const.setDecimals(3)
        self.box_const.setValue(10.0)
        self.box_const.setMaximum(10000.0)
        self.box_const.setMinimum(-10000.0)
        self.box_const.setSingleStep(10.0)

        self.box_amp = QtWidgets.QDoubleSpinBox()
        self.box_amp.setMaximum(10000.0)
        self.box_amp.setMinimum(-10000.0)
        self.box_amp.setDecimals(1)
        self.box_amp.setSingleStep(10.0)
        self.box_amp.setValue(1000.0)

        self.box_freq = QtWidgets.QDoubleSpinBox()
        if self.ui_obj.signal is not None:
            self.box_freq.setMaximum(self.ui_obj.signal.f_s / 2)
        else:
            self.box_freq.setMaximum(44100.0)
        self.box_freq.setMinimum(0.0)
        self.box_freq.setDecimals(1)
        self.box_freq.setSingleStep(10.0)
        self.box_freq.setValue(420.0)

        self.box_phase = QtWidgets.QDoubleSpinBox()
        self.box_phase.setDecimals(2)
        self.box_phase.setValue(0.0)
        self.box_phase.setMaximum(8 * np.pi)
        self.box_phase.setMinimum(0.0)
        self.box_phase.setSingleStep(np.pi / 4)

        self.box_mu_x = QtWidgets.QDoubleSpinBox()
        self.box_mu_x.setDecimals(2)
        if self.ui_obj.signal is not None:
            self.box_mu_x.setMaximum(2 * self.ui_obj.signal.x_end)
            self.box_mu_x.setMinimum(-self.ui_obj.signal.x_start)
            self.box_mu_x.setValue((self.ui_obj.signal.x_start + self.ui_obj.signal.x_end) / 2)
        else:
            self.box_mu_x.setMaximum(2 * 10.0)
            self.box_mu_x.setMinimum(-10.0)
            self.box_mu_x.setValue(5.0)
        self.box_mu_x.setSingleStep(1.0)

        self.box_sigma_x = QtWidgets.QDoubleSpinBox()
        self.box_sigma_x.setDecimals(2)
        if self.ui_obj.signal is not None:
            self.box_sigma_x.setMaximum(self.ui_obj.signal.length())
            self.box_sigma_x.setMinimum(0.0)
        else:
            self.box_sigma_x.setMaximum(10.0)
            self.box_sigma_x.setMinimum(0.0)
        self.box_sigma_x.setSingleStep(0.1)
        self.box_sigma_x.setValue(1.0)

        self.box_mu_y = QtWidgets.QDoubleSpinBox()
        self.box_mu_y.setDecimals(2)
        if self.ui_obj.signal is not None:
            self.box_mu_y.setMaximum(np.absolute(self.ui_obj.signal.Y).max())
            self.box_mu_y.setMinimum(-np.absolute(self.ui_obj.signal.Y).max())
        else:
            self.box_mu_y.setMaximum(10000.0)
            self.box_mu_y.setMinimum(-10000.0)
        self.box_mu_y.setValue(0.0)
        self.box_mu_y.setSingleStep(1.0)

        self.box_sigma_y = QtWidgets.QDoubleSpinBox()
        self.box_sigma_y.setDecimals(2)
        if self.ui_obj.signal is not None:
            self.box_sigma_y.setMaximum(np.absolute(self.ui_obj.signal.Y).max())
            self.box_sigma_y.setMinimum(0.0)
        else:
            self.box_sigma_y.setMaximum(10000.0)
            self.box_sigma_y.setMinimum(0.0)
        self.box_sigma_y.setSingleStep(1.0)
        self.box_sigma_y.setValue(1.0)

        self.build_layout()

        self.exec_()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Function: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Operation: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channels: '), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channel: '), 3, 0)
        base_grid.addWidget(self.cmb_function, 0, 1)
        base_grid.addWidget(self.cmb_operation, 1, 1)
        base_grid.addWidget(self.chb_all_channels, 2, 1)
        base_grid.addWidget(self.cmb_channels, 3, 1)
        base_widget = QtWidgets.QWidget()
        base_widget.setLayout(base_grid)
        self.stack.addWidget(base_widget)

        const_grid = QtWidgets.QGridLayout()
        const_grid.addWidget(QtWidgets.QLabel('Value: '), 0, 0)
        const_grid.addWidget(self.box_const, 0, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(const_grid)
        self.stack.addWidget(const_widget)

        sine_grid = QtWidgets.QGridLayout()
        sine_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Frequency: '), 1, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Phase: '), 2, 0)
        sine_grid.addWidget(self.box_amp, 0, 1)
        sine_grid.addWidget(self.box_freq, 1, 1)
        sine_grid.addWidget(self.box_phase, 2, 1)
        sine_widget = QtWidgets.QWidget()
        sine_widget.setLayout(sine_grid)
        self.stack.addWidget(sine_widget)

        gauss_grid_x = QtWidgets.QGridLayout()
        gauss_grid_x.addWidget(QtWidgets.QLabel('mu'), 0, 0)
        gauss_grid_x.addWidget(QtWidgets.QLabel('sigma'), 1, 0)
        gauss_grid_x.addWidget(self.box_mu_x, 0, 1)
        gauss_grid_x.addWidget(self.box_sigma_x, 1, 1)
        gauss_widget_x = QtWidgets.QWidget()
        gauss_widget_x.setLayout(gauss_grid_x)
        self.stack.addWidget(gauss_widget_x)

        gauss_grid_y = QtWidgets.QGridLayout()
        gauss_grid_y.addWidget(QtWidgets.QLabel('mu'), 0, 0)
        gauss_grid_y.addWidget(QtWidgets.QLabel('sigma'), 1, 0)
        gauss_grid_y.addWidget(self.box_mu_y, 0, 1)
        gauss_grid_y.addWidget(self.box_sigma_y, 1, 1)
        gauss_widget_y = QtWidgets.QWidget()
        gauss_widget_y.setLayout(gauss_grid_y)
        self.stack.addWidget(gauss_widget_y)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.stack)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def chb_all_channels_trigger(self, state):
        if state:
            self.cmb_channels.setDisabled(True)
        else:
            self.cmb_channels.setDisabled(False)

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
            type_text = self.cmb_function.currentText()
            if type_text == 'Constant':
                next_index = 1
            elif type_text == 'Sine' or type_text == 'Cosine':
                next_index = 2
            elif type_text == 'Pulse':
                next_index = 3
            elif type_text == 'Noise':
                next_index = 4
            else:
                self.close()
            self.btn_next.setText('Generate')
            self.btn_cancel.setText('Back')
            self.stack.setCurrentIndex(next_index)
            self.stage += 1
        else:
            self.gen_signal()
            self.close()
            self.complete = True

    def gen_signal(self):

        function = self.cmb_function.currentText()
        operation = self.cmb_operation.currentText()
        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels)]
        if function == 'Constant':
            const = self.box_const.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: const, channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: const, channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: const, channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: const, channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: const, channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Sine':
            amp = self.box_amp.value()
            freq = self.box_freq.value()
            phase = self.box_phase.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: amp * np.sin(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: amp * np.sin(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: amp * np.sin(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: amp * np.sin(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: amp * np.sin(2 * np.pi * freq * x - phase), channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Cosine':
            amp = self.box_amp.value()
            freq = self.box_freq.value()
            phase = self.box_phase.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: amp * np.cos(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: amp * np.cos(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: amp * np.cos(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: amp * np.cos(2 * np.pi * freq * x - phase), channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: amp * np.cos(2 * np.pi * freq * x - phase), channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Pulse':
            mu_x = self.box_mu_x.value()
            sigma_x = self.box_sigma_x.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: (1 / np.sqrt(2 * np.pi * sigma_x)) * np.exp(-(x - mu_x) ** 2 / (2 * sigma_x)), channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: (1 / np.sqrt(2 * np.pi * sigma_x)) * np.exp(-(x - mu_x) ** 2 / (2 * sigma_x)), channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: (1 / np.sqrt(2 * np.pi * sigma_x)) * np.exp(-(x - mu_x) ** 2 / (2 * sigma_x)), channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: (1 / np.sqrt(2 * np.pi * sigma_x)) * np.exp(-(x - mu_x) ** 2 / (2 * sigma_x)), channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: (1 / np.sqrt(2 * np.pi * sigma_x)) * np.exp(-(x - mu_x) ** 2 / (2 * sigma_x)), channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Gaussian noise':
            mu_y = self.box_mu_y.value()
            sigma_y = self.box_sigma_y.value()
            self.ui_obj.signal.noise(mu_y, sigma_y, channels=channels, operation=operation.lower())


class FunctionSignal1DComplex(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Functions')

        self.ui_obj = ui_object

        self.complete = False

        self.stage = 0
        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_function = QtWidgets.QComboBox()
        self.cmb_function.addItems([
            'Constant',
            'Hyperbolic',
            'Pulse',
            'Noise'
        ])
        self.cmb_function.setCurrentIndex(0)

        self.cmb_operation = QtWidgets.QComboBox()
        self.cmb_operation.addItems([
            'Overwrite',
            'Add',
            'Subtract',
            'Multiply',
            'Convolve'
        ])

        self.chb_all_channels = QtWidgets.QCheckBox('All channels')
        self.chb_all_channels.setChecked(True)
        self.chb_all_channels.toggled.connect(self.chb_all_channels_trigger)

        self.cmb_channels = QtWidgets.QComboBox()
        if self.ui_obj.signal is not None:
            for nchan in range(self.ui_obj.signal.channels):
                self.cmb_channels.addItem('Channel {}'.format(nchan + 1))
        self.cmb_channels.setDisabled(True)

        self.box_const_1 = QtWidgets.QDoubleSpinBox()
        self.box_const_1.setDecimals(3)
        self.box_const_1.setValue(10.0)
        self.box_const_1.setMaximum(10000.0)
        self.box_const_1.setMinimum(-10000.0)
        self.box_const_1.setSingleStep(10.0)

        self.box_const_2 = QtWidgets.QDoubleSpinBox()
        self.box_const_2.setDecimals(3)
        self.box_const_2.setValue(10.0)
        self.box_const_2.setMaximum(10000.0)
        self.box_const_2.setMinimum(-10000.0)
        self.box_const_2.setSingleStep(10.0)

        self.box_amp_1 = QtWidgets.QDoubleSpinBox()
        self.box_amp_1.setMaximum(10000.0)
        self.box_amp_1.setMinimum(-10000.0)
        self.box_amp_1.setDecimals(1)
        self.box_amp_1.setSingleStep(10.0)
        self.box_amp_1.setValue(1000.0)

        self.box_freq_1 = QtWidgets.QDoubleSpinBox()
        if self.ui_obj.signal is not None:
            self.box_freq_1.setMaximum(self.ui_obj.signal.f_s / 2)
        else:
            self.box_freq_1.setMaximum(44100.0)
        self.box_freq_1.setMinimum(0.0)
        self.box_freq_1.setDecimals(1)
        self.box_freq_1.setSingleStep(10.0)
        self.box_freq_1.setValue(420.0)

        self.box_phase_1 = QtWidgets.QDoubleSpinBox()
        self.box_phase_1.setDecimals(2)
        self.box_phase_1.setValue(0.0)
        self.box_phase_1.setMaximum(8 * np.pi)
        self.box_phase_1.setMinimum(0.0)
        self.box_phase_1.setSingleStep(np.pi / 4)

        self.box_amp_2 = QtWidgets.QDoubleSpinBox()
        self.box_amp_2.setMaximum(10000.0)
        self.box_amp_2.setMinimum(-10000.0)
        self.box_amp_2.setDecimals(1)
        self.box_amp_2.setSingleStep(10.0)
        self.box_amp_2.setValue(1000.0)

        self.box_freq_2 = QtWidgets.QDoubleSpinBox()
        if self.ui_obj.signal is not None:
            self.box_freq_2.setMaximum(self.ui_obj.signal.f_s / 2)
        else:
            self.box_freq_2.setMaximum(44100.0)
        self.box_freq_2.setMinimum(0.0)
        self.box_freq_2.setDecimals(1)
        self.box_freq_2.setSingleStep(10.0)
        self.box_freq_2.setValue(420.0)

        self.box_phase_2 = QtWidgets.QDoubleSpinBox()
        self.box_phase_2.setDecimals(2)
        self.box_phase_2.setValue(0.0)
        self.box_phase_2.setMaximum(8 * np.pi)
        self.box_phase_2.setMinimum(0.0)
        self.box_phase_2.setSingleStep(np.pi / 4)

        self.box_mu_x = QtWidgets.QDoubleSpinBox()
        self.box_mu_x.setDecimals(1)
        if self.ui_obj.signal is not None:
            self.box_mu_x.setMaximum(self.ui_obj.signal.X[-1])
            self.box_mu_x.setMinimum(self.ui_obj.signal.X[0])
        else:
            self.box_mu_x.setMaximum(2 * 10.0)
            self.box_mu_x.setMinimum(-10.0)
        self.box_mu_x.setValue(0.0)
        self.box_mu_x.setSingleStep(1.0)

        self.box_sigma_x = QtWidgets.QDoubleSpinBox()
        self.box_sigma_x.setDecimals(1)
        if self.ui_obj.signal is not None:
            self.box_sigma_x.setMaximum(self.ui_obj.signal.length())
            self.box_sigma_x.setMinimum(0.0)
        else:
            self.box_sigma_x.setMaximum(10.0)
            self.box_sigma_x.setMinimum(0.0)
        self.box_sigma_x.setSingleStep(0.1)
        self.box_sigma_x.setValue(1.0)

        self.box_mu_y = QtWidgets.QDoubleSpinBox()
        self.box_mu_y.setDecimals(2)
        if self.ui_obj.signal is not None:
            self.box_mu_y.setMaximum(np.absolute(self.ui_obj.signal.Y).max())
            self.box_mu_y.setMinimum(-np.absolute(self.ui_obj.signal.Y).max())
        else:
            self.box_mu_y.setMaximum(10000.0)
            self.box_mu_y.setMinimum(-10000.0)
        self.box_mu_y.setValue(0.0)
        self.box_mu_y.setSingleStep(1.0)

        self.box_sigma_y = QtWidgets.QDoubleSpinBox()
        self.box_sigma_y.setDecimals(2)
        if self.ui_obj.signal is not None:
            self.box_sigma_y.setMaximum(np.absolute(self.ui_obj.signal.Y).max())
            self.box_sigma_y.setMinimum(0.0)
        else:
            self.box_sigma_y.setMaximum(10000.0)
            self.box_sigma_y.setMinimum(0.0)
        self.box_sigma_y.setSingleStep(1.0)
        self.box_sigma_y.setValue(1.0)

        self.build_layout()

        self.exec_()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Function: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Operation: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channels: '), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channel: '), 3, 0)
        base_grid.addWidget(self.cmb_function, 0, 1)
        base_grid.addWidget(self.cmb_operation, 1, 1)
        base_grid.addWidget(self.chb_all_channels, 2, 1)
        base_grid.addWidget(self.cmb_channels, 3, 1)
        base_widget = QtWidgets.QWidget()
        base_widget.setLayout(base_grid)
        self.stack.addWidget(base_widget)

        const_grid = QtWidgets.QGridLayout()
        const_grid.addWidget(QtWidgets.QLabel('Real value: '), 0, 0)
        const_grid.addWidget(QtWidgets.QLabel('Imaginary value: '), 1, 0)
        const_grid.addWidget(self.box_const_1, 0, 1)
        const_grid.addWidget(self.box_const_2, 1, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(const_grid)
        self.stack.addWidget(const_widget)

        sine_grid = QtWidgets.QGridLayout()
        sine_grid.addWidget(QtWidgets.QLabel('Real amplitude: '), 0, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Real frequency: '), 1, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Real phase: '), 2, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Imaginary amplitude: '), 3, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Imaginary frequency: '), 4, 0)
        sine_grid.addWidget(QtWidgets.QLabel('Imaginary phase: '), 5, 0)
        sine_grid.addWidget(self.box_amp_1, 0, 1)
        sine_grid.addWidget(self.box_freq_1, 1, 1)
        sine_grid.addWidget(self.box_phase_1, 2, 1)
        sine_grid.addWidget(self.box_amp_2, 3, 1)
        sine_grid.addWidget(self.box_freq_2, 4, 1)
        sine_grid.addWidget(self.box_phase_2, 5, 1)
        sine_widget = QtWidgets.QWidget()
        sine_widget.setLayout(sine_grid)
        self.stack.addWidget(sine_widget)

        gauss_grid_x = QtWidgets.QGridLayout()
        gauss_grid_x.addWidget(QtWidgets.QLabel('mu'), 0, 0)
        gauss_grid_x.addWidget(QtWidgets.QLabel('sigma'), 1, 0)
        gauss_grid_x.addWidget(self.box_mu_x, 0, 1)
        gauss_grid_x.addWidget(self.box_sigma_x, 1, 1)
        gauss_widget_x = QtWidgets.QWidget()
        gauss_widget_x.setLayout(gauss_grid_x)
        self.stack.addWidget(gauss_widget_x)

        gauss_grid_y = QtWidgets.QGridLayout()
        gauss_grid_y.addWidget(QtWidgets.QLabel('mu'), 0, 0)
        gauss_grid_y.addWidget(QtWidgets.QLabel('sigma'), 1, 0)
        gauss_grid_y.addWidget(self.box_mu_y, 0, 1)
        gauss_grid_y.addWidget(self.box_sigma_y, 1, 1)
        gauss_widget_y = QtWidgets.QWidget()
        gauss_widget_y.setLayout(gauss_grid_y)
        self.stack.addWidget(gauss_widget_y)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.stack)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def chb_all_channels_trigger(self, state):
        if state:
            self.cmb_channels.setDisabled(True)
        else:
            self.cmb_channels.setDisabled(False)

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
            type_text = self.cmb_function.currentText()
            if type_text == 'Constant':
                next_index = 1
            elif type_text == 'Hyperbolic':
                next_index = 2
            elif type_text == 'Pulse':
                next_index = 3
            elif type_text == 'Noise':
                next_index = 4
            else:
                self.close()
            self.btn_next.setText('Generate')
            self.btn_cancel.setText('Back')
            self.stack.setCurrentIndex(next_index)
            self.stage += 1
        else:
            self.gen_signal()
            self.close()
            self.complete = True

    def gen_signal(self):

        function = self.cmb_function.currentText()
        operation = self.cmb_operation.currentText()
        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels)]
        if function == 'Constant':
            const_real = self.box_const_1.value()
            const_im = self.box_const_2.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: np.complex(const_real, const_im), channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: np.complex(const_real, const_im), channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: np.complex(const_real, const_im), channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: np.complex(const_real, const_im), channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: np.complex(const_real, const_im), channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Hyperbolic':
            amp_re = self.box_amp_1.value()
            freq_re = self.box_freq_1.value()
            phase_re = self.box_phase_1.value()
            amp_im = self.box_amp_2.value()
            freq_im = self.box_freq_2.value()
            phase_im = self.box_phase_2.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: np.complex(amp_re * np.sin(2 * np.pi *freq_re * x - phase_re), amp_im * np.cos(2 * np.pi * freq_im * x - phase_im)), channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: np.complex(amp_re * np.sin(2 * np.pi *freq_re * x - phase_re), amp_im * np.cos(2 * np.pi * freq_im * x - phase_im)), channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: np.complex(amp_re * np.sin(2 * np.pi *freq_re * x - phase_re), amp_im * np.cos(2 * np.pi * freq_im * x - phase_im)), channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: np.complex(amp_re * np.sin(2 * np.pi *freq_re * x - phase_re), amp_im * np.cos(2 * np.pi * freq_im * x - phase_im)), channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: np.complex(amp_re * np.sin(2 * np.pi *freq_re * x - phase_re), amp_im * np.cos(2 * np.pi * freq_im * x - phase_im)), channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Pulse':
            mu_x = self.box_mu_x.value()
            sigma_x = self.box_sigma_x.value()
            if operation == 'Overwrite':
                self.ui_obj.signal.generate_function(lambda x: np.complex(np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi)), np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi))), channels)
            elif operation == 'Add':
                self.ui_obj.signal.add_function(lambda x: np.complex(np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi)), np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi))), channels)
            elif operation == 'Subtract':
                self.ui_obj.signal.subtract_function(lambda x: np.complex(np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi)), np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi))), channels)
            elif operation == 'Multiply':
                self.ui_obj.signal.multiply_function(lambda x: np.complex(np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi)), np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi))), channels)
            elif operation == 'Convolve':
                self.ui_objsignal.convolve_function(lambda x: np.complex(np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi)), np.exp(-0.5 * ((x - mu_x) / sigma_x) ** 2) / (sigma_x * np.sqrt(2 * np.pi))), channels)
            else:
                logger.info('error')
                print('error')
        elif function == 'Gaussian noise':
            mu_y = self.box_mu_y.value()
            sigma_y = self.box_sigma_y.value()
            if operation == 'Overwrite':
                for k, x in enumerate(self.ui_obj.signal.X):
                    self.ui_obj.signal.Y[k, 0] = random.gauss(mu_y, sigma_y)
            elif operation == 'Add':
                for k, x in enumerate(self.ui_obj.signal.X):
                    self.ui_obj.signal.Y[k, 0] += random.gauss(mu_y, sigma_y)
            elif operation == 'Subtract':
                for k, x in enumerate(self.ui_obj.signal.X):
                    self.ui_obj.signal.Y[k, 0] -= random.gauss(mu_y, sigma_y)
            elif operation == 'Multiply':
                for k, x in enumerate(self.ui_obj.signal.X):
                    self.ui_obj.signal.Y[k, 0] *= random.gauss(mu_y, sigma_y)
            elif operation == 'Convolve':
                pass
            else:
                logger.info('error')
                print('error')


class AddNoiseSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Add gaussian noise signal')

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Add noise')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_mu = QtWidgets.QDoubleSpinBox()
        self.box_mu.setDecimals(1)
        self.box_mu.setSingleStep(1.0)
        self.box_mu.setMinimum(-10000.0)
        self.box_mu.setMaximum(10000.0)
        self.box_mu.setValue(0.0)

        self.box_sigma = QtWidgets.QDoubleSpinBox()
        self.box_sigma.setDecimals(1)
        self.box_sigma.setSingleStep(1.0)
        self.box_sigma.setMinimum(-10000.0)
        self.box_sigma.setMaximum(10000.0)
        self.box_sigma.setValue(0.0)

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('Mu: '), 0, 0)
        grid.addWidget(QtWidgets.QLabel('Sigma: '), 1, 0)
        grid.addWidget(self.box_mu, 0, 1)
        grid.addWidget(self.box_sigma, 1, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        mu = self.box_mu.value()
        sigma = self.box_sigma.value()
        sp.add_gaussian_noise(self.ui_obj.signal, mu, sigma)
        self.close()

