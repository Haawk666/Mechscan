# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import random
# 3rd party
from PyQt5 import QtWidgets, QtGui
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import Signals as ss
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SignalsInterface(QtWidgets.QWidget):

    def __init__(self, *args, menu=None, config=None):
        super().__init__(*args)

        self.signal_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.menu = menu.addMenu('Signal')
        self.populate_menu()

        self.config = config

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

        edit = self.menu.addMenu('Edit')
        edit.addAction(GUI_subwidgets.Action('Scale', self, trigger_func=self.menu_scale_trigger))
        edit.addAction(GUI_subwidgets.Action('Shift', self, trigger_func=self.menu_shift_trigger))
        edit.addAction(GUI_subwidgets.Action('Crop', self, trigger_func=self.menu_crop_trigger))
        edit.addAction(GUI_subwidgets.Action('Resample', self, trigger_func=self.menu_resample_trigger))

        self.menu.addAction(GUI_subwidgets.Action('Functions', self, trigger_func=self.menu_combine_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_subwidgets.Action('Settings', self, trigger_func=self.menu_options_trigger))

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
        interface = SignalInterface(config=self.config)
        interface.signal = signal
        interface.update_info()
        self.add_interface(interface)

    def menu_generate_time_trigger(self):
        signal_interface = SignalInterface(config=self.config)
        wizard = NewTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            if signal_interface.signal.codomain == 'int' or signal_interface.signal.codomain == 'float' or signal_interface.signal.codomain == 'bool_':
                func_wiz = GetFunction1DReal(ui_object=signal_interface)
            else:
                func_wiz = GetFunction1DComplex(ui_object=signal_interface)
            if func_wiz.complete:
                signal_interface.update_info()
                self.add_interface(signal_interface)

    def menu_generate_frequency_trigger(self):
        signal_interface = SignalInterface(config=self.config)
        wizard = NewFrequencySignal(ui_object=signal_interface)
        if wizard.complete:
            func_wiz = GetFunction1DComplex(ui_object=signal_interface)
            if func_wiz.complete:
                signal_interface.update_info()
                self.add_interface(signal_interface)

    def menu_new_time_trigger(self):
        signal_interface = SignalInterface(config=self.config)
        wizard = NewTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            signal_interface.update_info()
            self.add_interface(signal_interface)

    def menu_new_frequency_trigger(self):
        signal_interface = SignalInterface(config=self.config)
        wizard = NewFrequencySignal(ui_object=signal_interface)
        if wizard.complete:
            signal_interface.update_info()
            self.add_interface(signal_interface)

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
            signal_interface = SignalInterface(config=self.config)
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
        signal_interface = SignalInterface(config=self.config)
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
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                if signal.signal_type == 'time':
                    wizard = GetAlpha()
                    if wizard.complete:
                        self.add_signal(ss.TimeFrequencySignal.from_time_signal(signal, wizard.alpha))
                elif signal.signal_type == 'time-frequency':
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

    def menu_scale_trigger(self):
        pass

    def menu_shift_trigger(self):
        pass

    def menu_crop_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                interface = SignalInterface(config=self.config)
                interface.signal = signal
                wizard = CropSignal(ui_object=interface)
                interface.update_info()
                self.add_interface(interface)

    def menu_combine_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                interface = SignalInterface(config=self.config)
                interface.signal = signal
                if signal.signal_type == 'time':
                    wizard = GetFunction1DReal(ui_object=interface)
                    if wizard.complete:
                        interface.update_info()
                        self.add_interface(interface)
                elif signal.signal_type == 'frequency':
                    wizard = GetFunction1DComplex(ui_object=interface)
                    if wizard.complete:
                        interface.update_info()
                        self.add_interface(interface)

    def menu_resample_trigger(self):
        pass

    def menu_options_trigger(self):
        wizard = SetOptions(ui_obj=self)
        for interface in self.signal_interfaces:
            interface.config = self.config
            interface.update_info()


class SignalInterface(QtWidgets.QWidget):

    def __init__(self, *args, config=None):
        super().__init__(*args)

        self.config = config

        self.signal = None

        self.lbl_info_keys = QtWidgets.QLabel('')
        self.lbl_info_values = QtWidgets.QLabel('')

        self.graphs = QtWidgets.QTabWidget()
        self.graphs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.build_layout()
        self.update_info()

    def build_layout(self):

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addWidget(self.lbl_info_keys)
        info_layout.addWidget(self.lbl_info_values)
        info_layout.addStretch()

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addLayout(info_layout)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphs)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def plot_signal(self):
        self.graphs.clear()
        if self.signal is not None:
            if self.signal.signal_type == 'time':

                for j in range(self.signal.channels):

                    plot_widget = pg.GraphicsLayoutWidget()
                    self.graphs.addTab(plot_widget, 'Channel {}'.format(j + 1))

                    plot = plot_widget.addPlot(row=0, col=0)
                    if self.signal.codomain == 'complex':
                        legend = plot.addLegend()
                        legend.setBrush('k')
                        plot_type = self.config.get('signals', 'time_plot_type')
                        if 'r' in plot_type:
                            plot.plot(self.signal.X, np.real(self.signal.Y[:, j]), name='Re')
                        if 'i' in plot_type:
                            plot.plot(self.signal.X, np.imag(self.signal.Y[:, j]), pen='r', name='Im')
                        if 'm' in plot_type:
                            plot.plot(self.signal.X, np.absolute(self.signal.Y[:, j]), pen='g', name='Magnitude')
                        if 'p' in plot_type:
                            plot.plot(self.signal.X, np.angle(self.signal.Y[:, j]), pen='y', name='Phase')
                    else:
                        plot.plot(self.signal.X, self.signal.Y[:, j])
                    plot.setTitle('Signal')
                    plot.setLabel('left', 'Amplitude ({})'.format(self.signal.units[1]))
                    plot.setLabel('bottom', 'Time t, ({})'.format(self.signal.units[0]))

            elif self.signal.signal_type == 'frequency':

                for j in range(self.signal.channels):

                    plot_widget = pg.GraphicsLayoutWidget()
                    self.graphs.addTab(plot_widget, 'Channel {}'.format(j + 1))

                    plot = plot_widget.addPlot(row=0, col=0)
                    spectrum_type = self.config.get('signals', 'spectrum_type')
                    if spectrum_type == 'p':
                        plot.plot(self.signal.X[self.signal.n // 2:], np.square(np.absolute(self.signal.Y[self.signal.n // 2:, j])))
                        plot.setTitle('Power spectrum')
                        plot.setLabel('left', 'Magnitude^2')
                    elif spectrum_type == 'm':
                        plot.plot(self.signal.X[self.signal.n // 2:], np.absolute(self.signal.Y[self.signal.n // 2:, j]))
                        plot.setTitle('Magnitude spectrum')
                        plot.setLabel('left', 'Magnitude')
                    else:
                        plot.plot(self.signal.X[self.signal.n // 2:], np.square(np.absolute(self.signal.Y[self.signal.n // 2:, j])))
                        plot.setTitle('Power spectrum')
                        plot.setLabel('left', 'Magnitude^2')
                    plot.setLabel('bottom', 'Frequency f, (Hz)')

                    spectrum_phase = self.config.get('signals', 'spectrum_phase')
                    if spectrum_phase == 'y':
                        plot = plot_widget.addPlot(row=1, col=0)
                        plot.plot(self.signal.X[self.signal.n // 2:], np.angle(self.signal.Y[self.signal.n // 2:, j]))
                        plot.setTitle('Phase spectrum')
                        plot.setLabel('left', 'Angle Theta, (rad)')
                        plot.setLabel('bottom', 'Frequency f, (Hz)')

            elif self.signal.signal_type == 'time-frequency':
                img = pg.ImageItem(image=np.absolute(self.signal.Y))
                self.graph.getPlotItem().addItem(img)
                cm = pg.colormap.get('CET-L9')
                bar = pg.ColorBarItem(values=(np.absolute(self.signal.Y).min(), np.absolute(self.signal.Y).max()), cmap=cm)
                bar.setImageItem(img, insert_in=self.graph.getPlotItem())
                self.graph.setTitle('Spectrogram')
                self.graph.setLabel('bottom', 'Time t, (s)')
                self.graph.setLabel('left', 'Frequency f, (Hz)')
            else:
                self.graph.setTitle('Generic signal')
                self.graph.setLabel('bottom', 'Independent variable')
                self.graph.setLabel('left', 'Signal')

    def update_info(self):
        if self.signal:
            self.plot_signal()
            meta_data = self.signal.info()
            key_string = ''
            value_string = ''
            for key, value in meta_data.items():
                key_string += '{}:    \n'.format(key)
                value_string += '{}\n'.format(value)
            self.lbl_info_keys.setText(key_string)
            self.lbl_info_values.setText(value_string)
        else:
            self.graphs.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')


class GetFunction1DReal(QtWidgets.QDialog):

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
            'Gaussian pulse',
            'Sine',
            'Sign',
            'Delta',
            'Noise',
            'Constant'
        ])
        self.cmb_functions.setCurrentIndex(2)

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

        self.lbl_explain = QtWidgets.QLabel('Enter a function as a string, ie: \'100 * np.exp(0.5 * x)\'.\nIf the signal has multiple dimensions, use \'x_1\', \'x_2\', etc...')

        self.box_function = QtWidgets.QLineEdit()
        self.box_function.setText('5 * np.sin(2 * np.pi * 420 * x)')

        self.box_amp_x = QtWidgets.QDoubleSpinBox()
        self.box_amp_x.setDecimals(1)
        self.box_amp_x.setMinimum(-1000.0)
        self.box_amp_x.setMaximum(1000.0)
        self.box_amp_x.setSingleStep(10.0)
        self.box_amp_x.setValue(1.0)

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

        self.box_amp_delta = QtWidgets.QDoubleSpinBox()
        self.box_amp_delta.setDecimals(1)
        self.box_amp_delta.setMinimum(-100.0)
        self.box_amp_delta.setMaximum(100.0)
        self.box_amp_delta.setSingleStep(1.0)
        self.box_amp_delta.setValue(1.0)

        self.box_delta = QtWidgets.QDoubleSpinBox()
        self.box_delta.setDecimals(1)
        self.box_delta.setMinimum(-10.0)
        self.box_delta.setMaximum(10.0)
        self.box_delta.setSingleStep(1.0)
        self.box_delta.setValue(0.0)

        self.box_amp_noise = QtWidgets.QDoubleSpinBox()
        self.box_amp_noise.setDecimals(1)
        self.box_amp_noise.setMinimum(0.0)
        self.box_amp_noise.setMaximum(100.0)
        self.box_amp_noise.setSingleStep(10.0)
        self.box_amp_noise.setValue(1.0)

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

        self.box_const = QtWidgets.QDoubleSpinBox()
        self.box_const.setDecimals(1)
        self.box_const.setMinimum(-1000.0)
        self.box_const.setMaximum(1000.0)
        self.box_const.setSingleStep(1.0)
        self.box_const.setValue(666.0)

        self.build_layout()

        self.exec_()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Functions: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Operation: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channels: '), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channel: '), 3, 0)
        base_grid.addWidget(QtWidgets.QLabel('From timestamp: '), 4, 0)
        base_grid.addWidget(QtWidgets.QLabel('To timestamp: '), 5, 0)
        base_grid.addWidget(self.cmb_functions, 0, 1)
        base_grid.addWidget(self.cmb_operation, 1, 1)
        base_grid.addWidget(self.chb_all_channels, 2, 1)
        base_grid.addWidget(self.cmb_channels, 3, 1)
        base_grid.addWidget(self.box_from, 4, 1)
        base_grid.addWidget(self.box_to, 5, 1)
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

        sign_grid = QtWidgets.QGridLayout()
        sign_widget = QtWidgets.QWidget()
        sign_widget.setLayout(sign_grid)
        self.stack.addWidget(sign_widget)

        delta_grid = QtWidgets.QGridLayout()
        delta_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        delta_grid.addWidget(QtWidgets.QLabel('Placement: '), 1, 0)
        delta_grid.addWidget(self.box_amp_delta, 0, 1)
        delta_grid.addWidget(self.box_delta, 1, 1)
        delta_widget = QtWidgets.QWidget()
        delta_widget.setLayout(delta_grid)
        self.stack.addWidget(delta_widget)

        noise_grid = QtWidgets.QGridLayout()
        noise_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        noise_grid.addWidget(QtWidgets.QLabel('Mu: '), 1, 0)
        noise_grid.addWidget(QtWidgets.QLabel('Sigma: '), 2, 0)
        noise_grid.addWidget(self.box_amp_noise, 0, 1)
        noise_grid.addWidget(self.box_mu_noise, 1, 1)
        noise_grid.addWidget(self.box_sigma_noise, 2, 1)
        noise_widget = QtWidgets.QWidget()
        noise_widget.setLayout(noise_grid)
        self.stack.addWidget(noise_widget)

        const_grid = QtWidgets.QGridLayout()
        const_grid.addWidget(QtWidgets.QLabel('Constant: '), 0, 0)
        const_grid.addWidget(self.box_const, 0, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(const_grid)
        self.stack.addWidget(const_widget)

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
            start = self.box_from.value()
            end = self.box_to.value()
            if start >= end:
                msg = QtWidgets.QMessageBox()
                msg.setText('Timestamp "to" must be larger than "from"!')
                msg.exec()
            else:
                self.btn_next.setText('Generate')
                self.btn_cancel.setText('Back')

                next_index = 1
                if self.cmb_functions.currentText() == 'Gaussian pulse':
                    next_index = 2
                elif self.cmb_functions.currentText() == 'Sine':
                    next_index = 3
                elif self.cmb_functions.currentText() == 'Sign':
                    next_index = 4
                elif self.cmb_functions.currentText() == 'Delta':
                    next_index = 5
                elif self.cmb_functions.currentText() == 'Noise':
                    next_index = 6
                elif self.cmb_functions.currentText() == 'Constant':
                    next_index = 7

                self.stack.setCurrentIndex(next_index)
                self.stage += 1
        else:
            self.gen_signal()
            self.close()
            self.complete = True

    def gen_signal(self):

        start = self.box_from.value()
        end = self.box_to.value()

        function_string = self.box_function.text()
        operation = self.cmb_operation.currentText()

        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels) - 1]

        if self.cmb_functions.currentText() == 'Gaussian pulse':
            amp = self.box_amp_x.value()
            mu = self.box_mu_x.value()
            sigma = self.box_sigma_x.value()
            function_string = '{} * np.exp(-0.5 * ((x - {}) / {}) ** 2) / ({} * np.sqrt(2 * np.pi))'.format(amp, mu, sigma, sigma)
        elif self.cmb_functions.currentText() == 'Sine':
            amp = self.box_amp_sin.value()
            f = self.box_freq_sin.value()
            theta = self.box_phase_sin.value()
            function_string = '{} * np.sin(2 * np.pi * {} * x - {})'.format(amp, f, theta)
        elif self.cmb_functions.currentText() == 'Sign':
            function_string = 'np.sign(x)'
        elif self.cmb_functions.currentText() == 'Delta':
            amp = self.box_amp_delta.value()
            placement = self.box_delta.value()
            function_string = '{} * (1 if {} == x else 0)'.format(amp, placement)
        elif self.cmb_functions.currentText() == 'Noise':
            amp = self.box_amp_noise.value()
            mu = self.box_mu_noise.value()
            sigma = self.box_sigma_noise.value()
            function_string = '{} * random.gauss({}, {})'.format(amp, mu, sigma)
        elif self.cmb_functions.currentText() == 'Constant':
            const = self.box_const.value()
            function_string = '{}'.format(const)

        if operation == 'Overwrite':
            self.ui_obj.signal.generate_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Add':
            self.ui_obj.signal.add_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Subtract':
            self.ui_obj.signal.subtract_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Multiply':
            self.ui_obj.signal.multiply_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Convolve':
            self.ui_objsignal.convolve_function(lambda x: eval(function_string), channels, a=start, b=end)
        else:
            logger.info('error')
            print('error')


class GetFunction1DComplex(QtWidgets.QDialog):

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
            'Gaussian pulse',
            'Sine',
            'Exponential',
            'Noise',
            'Constant'
        ])
        self.cmb_functions.setCurrentIndex(3)

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

        self.lbl_explain = QtWidgets.QLabel('Enter a function as a string, ie: \'100 * np.exp(0.5 * x)\'.\nIf the signal has multiple dimensions, use \'x_1\', \'x_2\', etc...')

        self.box_function = QtWidgets.QLineEdit()
        self.box_function.setText('np.complex(5 * np.sin(2 * np.pi * 420 * x), x)')

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

        self.box_amp_exp = QtWidgets.QDoubleSpinBox()
        self.box_amp_exp.setDecimals(1)
        self.box_amp_exp.setMinimum(-10000.0)
        self.box_amp_exp.setMaximum(10000.0)
        self.box_amp_exp.setSingleStep(10.0)
        self.box_amp_exp.setValue(100.0)

        self.box_freq_exp = QtWidgets.QDoubleSpinBox()
        self.box_freq_exp.setDecimals(1)
        self.box_freq_exp.setMinimum(0.0)
        self.box_freq_exp.setMaximum(100.0)
        self.box_freq_exp.setSingleStep(1.0)
        self.box_freq_exp.setValue(10.0)

        self.box_phase_exp = QtWidgets.QDoubleSpinBox()
        self.box_phase_exp.setDecimals(1)
        self.box_phase_exp.setMinimum(-2 * np.pi)
        self.box_phase_exp.setMaximum(2 * np.pi)
        self.box_phase_exp.setSingleStep(0.25 * np.pi)
        self.box_phase_exp.setValue(0.0)

        self.box_amp_noise = QtWidgets.QDoubleSpinBox()
        self.box_amp_noise.setDecimals(1)
        self.box_amp_noise.setMinimum(0.0)
        self.box_amp_noise.setMaximum(100.0)
        self.box_amp_noise.setSingleStep(10.0)
        self.box_amp_noise.setValue(1.0)

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

        self.box_const_real = QtWidgets.QDoubleSpinBox()
        self.box_const_real.setDecimals(1)
        self.box_const_real.setMinimum(-1000.0)
        self.box_const_real.setMaximum(1000.0)
        self.box_const_real.setSingleStep(1.0)
        self.box_const_real.setValue(666.0)

        self.box_const_im = QtWidgets.QDoubleSpinBox()
        self.box_const_im.setDecimals(1)
        self.box_const_im.setMinimum(-1000.0)
        self.box_const_im.setMaximum(1000.0)
        self.box_const_im.setSingleStep(1.0)
        self.box_const_im.setValue(666.0)

        self.build_layout()

        self.exec_()

    def build_layout(self):

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

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

        exp_grid = QtWidgets.QGridLayout()
        exp_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        exp_grid.addWidget(QtWidgets.QLabel('Frequency: '), 1, 0)
        exp_grid.addWidget(QtWidgets.QLabel('Phase: '), 2, 0)
        exp_grid.addWidget(self.box_amp_exp, 0, 1)
        exp_grid.addWidget(self.box_freq_exp, 1, 1)
        exp_grid.addWidget(self.box_phase_exp, 2, 1)
        exp_widget = QtWidgets.QWidget()
        exp_widget.setLayout(exp_grid)
        self.stack.addWidget(exp_widget)

        noise_grid = QtWidgets.QGridLayout()
        noise_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        noise_grid.addWidget(QtWidgets.QLabel('Mu: '), 1, 0)
        noise_grid.addWidget(QtWidgets.QLabel('Sigma: '), 2, 0)
        noise_grid.addWidget(self.box_amp_noise, 0, 1)
        noise_grid.addWidget(self.box_mu_noise, 1, 1)
        noise_grid.addWidget(self.box_sigma_noise, 2, 1)
        noise_widget = QtWidgets.QWidget()
        noise_widget.setLayout(noise_grid)
        self.stack.addWidget(noise_widget)

        const_grid = QtWidgets.QGridLayout()
        const_grid.addWidget(QtWidgets.QLabel('Constant (real): '), 0, 0)
        const_grid.addWidget(QtWidgets.QLabel('Constant (imaginary): '), 1, 0)
        const_grid.addWidget(self.box_const_real, 0, 1)
        const_grid.addWidget(self.box_const_im, 1, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(const_grid)
        self.stack.addWidget(const_widget)

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
            start = self.box_from.value()
            end = self.box_to.value()
            if start >= end:
                msg = QtWidgets.QMessageBox()
                msg.setText('Timestamp "to" must be larger than "from"!')
                msg.exec()
            else:
                self.btn_next.setText('Generate')
                self.btn_cancel.setText('Back')
                next_index = 1
                if self.cmb_functions.currentText() == 'Gaussian pulse':
                    next_index = 2
                elif self.cmb_functions.currentText() == 'Sine':
                    next_index = 3
                elif self.cmb_functions.currentText() == 'Exponential':
                    next_index = 4
                elif self.cmb_functions.currentText() == 'Noise':
                    next_index = 5
                elif self.cmb_functions.currentText() == 'Constant':
                    next_index = 6
                self.stack.setCurrentIndex(next_index)
                self.stage += 1
        else:
            self.gen_signal()
            self.close()
            self.complete = True

    def gen_signal(self):

        start = self.box_from.value()
        end = self.box_to.value()

        function_string = self.box_function.text()
        operation = self.cmb_operation.currentText()

        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels) - 1]

        if self.cmb_functions.currentText() == 'Gaussian pulse':
            amp = self.box_amp_x.value()
            mu = self.box_mu_x.value()
            sigma = self.box_sigma_x.value()
            function_string = '{} * np.complex(np.exp(-0.5 * ((x - {}) / {}) ** 2) / ({} * np.sqrt(2 * np.pi), np.exp(-0.5 * ((x - {}) / {}) ** 2) / ({} * np.sqrt(2 * np.pi)))'.format(amp, mu, sigma, sigma, mu, sigma, sigma)
        elif self.cmb_functions.currentText() == 'Sine':
            amp = self.box_amp_sin.value()
            f = self.box_freq_sin.value()
            theta = self.box_phase_sin.value()
            function_string = '{} * np.complex(np.sin(2 * np.pi * {} * x - {}), np.sin(2 * np.pi * {} * x - {}))'.format(amp, f, theta, f, theta)
        elif self.cmb_functions.currentText() == 'Exponential':
            amp = self.box_amp_exp.value()
            f = self.box_freq_exp.value()
            phase = self.box_phase_exp.value()
            function_string = '{} * np.exp(np.complex(0, -{} * (x - {})))'.format(amp, f, phase)
        elif self.cmb_functions.currentText() == 'Noise':
            amp = self.box_amp_noise.value()
            mu = self.box_mu_noise.value()
            sigma = self.box_sigma_noise.value()
            function_string = '{} * np.complex(random.gauss({}, {}), random.gauss({}, {}))'.format(amp, mu, sigma, mu, sigma)
        elif self.cmb_functions.currentText() == 'Constant':
            const = np.complex(self.box_const_real.value(), self.box_const_im.value())
            function_string = '{}'.format(const)

        if operation == 'Overwrite':
            self.ui_obj.signal.generate_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Add':
            self.ui_obj.signal.add_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Subtract':
            self.ui_obj.signal.subtract_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Multiply':
            self.ui_obj.signal.multiply_function(lambda x: eval(function_string), channels, a=start, b=end)
        elif operation == 'Convolve':
            self.ui_objsignal.convolve_function(lambda x: eval(function_string), channels, a=start, b=end)
        else:
            logger.info('error')
            print('error')


class NewTimeSignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('New time signal')

        self.complete = False

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_f_s = QtWidgets.QDoubleSpinBox()
        self.box_f_s.setMaximum(88200.0)
        self.box_f_s.setMinimum(1.0)
        self.box_f_s.setDecimals(1)
        self.box_f_s.setSingleStep(100.0)

        self.cmb_bits = QtWidgets.QComboBox()
        self.cmb_bits.addItems([
            '8 - int',
            '16 - int',
            '32 - int',
            '64 - int',
            '32 - float',
            '64 - float',
            '64 - complex',
            '128 - complex'
        ])
        self.cmb_bits.setCurrentIndex(1)

        self.box_t_start = QtWidgets.QDoubleSpinBox()
        self.box_t_start.setDecimals(3)
        self.box_t_start.setMaximum(100.0)
        self.box_t_start.setMinimum(-100.0)

        self.box_t_end = QtWidgets.QDoubleSpinBox()
        self.box_t_end.setDecimals(3)
        self.box_t_end.setMaximum(100.0)
        self.box_t_end.setMinimum(-100.0)

        self.box_channels = QtWidgets.QSpinBox()
        self.box_channels.setMaximum(10)
        self.box_channels.setMinimum(1)
        self.box_channels.setSingleStep(1)

        self.box_f_s.setValue(44100.0)
        self.box_t_start.setValue(0.0)
        self.box_t_end.setValue(10.0)
        self.box_channels.setValue(1)

        self.box_x_unit = QtWidgets.QLineEdit()
        self.box_x_unit.setText('s')
        self.box_y_unit = QtWidgets.QLineEdit()
        self.box_y_unit.setText('1')

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Sample rate f_s (Hz): '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Bit depth: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Start: '), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('End: '), 3, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channels: '), 4, 0)
        base_grid.addWidget(QtWidgets.QLabel('x unit: '), 5, 0)
        base_grid.addWidget(QtWidgets.QLabel('y unit: '), 6, 0)
        base_grid.addWidget(self.box_f_s, 0, 1)
        base_grid.addWidget(self.cmb_bits, 1, 1)
        base_grid.addWidget(self.box_t_start, 2, 1)
        base_grid.addWidget(self.box_t_end, 3, 1)
        base_grid.addWidget(self.box_channels, 4, 1)
        base_grid.addWidget(self.box_x_unit, 5, 1)
        base_grid.addWidget(self.box_y_unit, 6, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_signal()
        self.close()
        self.complete = True

    def gen_signal(self):
        bit_depth, codomain = self.cmb_bits.currentText().split(' - ')
        self.ui_obj.signal = ss.TimeSignal(
            x_start=self.box_t_start.value(),
            x_end=self.box_t_end.value(),
            delta_x=1.0/self.box_f_s.value(),
            bit_depth=int(bit_depth),
            codomain=codomain,
            channels=int(self.box_channels.value()),
            units=[self.box_x_unit.text(), self.box_y_unit.text()]
        )


class NewFrequencySignal(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('New frequency signal')

        self.complete = False

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_f_s = QtWidgets.QDoubleSpinBox()
        self.box_f_s.setMaximum(88200.0)
        self.box_f_s.setMinimum(1.0)
        self.box_f_s.setDecimals(1)
        self.box_f_s.setSingleStep(100.0)

        self.cmb_bits = QtWidgets.QComboBox()
        self.cmb_bits.addItems(['64', '128'])
        self.cmb_bits.setCurrentIndex(1)

        self.box_t_start = QtWidgets.QDoubleSpinBox()
        self.box_t_start.setDecimals(3)
        self.box_t_start.setMaximum(100.0)
        self.box_t_start.setMinimum(-100.0)

        self.box_t_end = QtWidgets.QDoubleSpinBox()
        self.box_t_end.setDecimals(3)
        self.box_t_end.setMaximum(100.0)
        self.box_t_end.setMinimum(-100.0)

        self.box_channels = QtWidgets.QSpinBox()
        self.box_channels.setMaximum(10)
        self.box_channels.setMinimum(1)
        self.box_channels.setSingleStep(1)

        self.box_f_s.setValue(44100.0)
        self.box_t_start.setValue(0.0)
        self.box_t_end.setValue(10.0)
        self.box_channels.setValue(1)

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Sample rate f_s (Hz)'), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Bit depth'), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Start time (s)'), 2, 0)
        base_grid.addWidget(QtWidgets.QLabel('End time (s)'), 3, 0)
        base_grid.addWidget(QtWidgets.QLabel('Channels'), 4, 0)
        base_grid.addWidget(self.box_f_s, 0, 1)
        base_grid.addWidget(self.cmb_bits, 1, 1)
        base_grid.addWidget(self.box_t_start, 2, 1)
        base_grid.addWidget(self.box_t_end, 3, 1)
        base_grid.addWidget(self.box_channels, 4, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_signal()
        self.close()
        self.complete = True

    def gen_signal(self):
        self.ui_obj.signal = ss.FrequencySignal(
            x_start=-self.box_f_s.value() / 2.0,
            x_end=self.box_f_s.value() / 2.0,
            delta_x=(self.box_f_s.value() / 2.0 + self.box_f_s.value() / 2.0) / (int(np.round(((self.box_t_end.value() - self.box_t_start.value()) / (1.0 / self.box_f_s.value())) + 1.0, decimals=0)) - 1.0),
            bit_depth=int(self.cmb_bits.currentText()),
            codomain='complex',
            channels=int(self.box_channels.value())
        )


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
                if x > new_end:
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


class GetAlpha(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('Set window size')

        self.complete = False
        self.alpha = 0.5

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Transform')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_alpha = QtWidgets.QDoubleSpinBox()
        self.box_alpha.setDecimals(3)
        self.box_alpha.setSingleStep(1.0)
        self.box_alpha.setMinimum(0.0)
        self.box_alpha.setMaximum(10.0)
        self.box_alpha.setValue(0.5)

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('Alpha: '), 0, 0)
        grid.addWidget(self.box_alpha, 0, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.alpha = self.box_alpha.value()
        self.close()
        self.complete = True


class SetOptions(QtWidgets.QDialog):

    def __init__(self, *args, ui_obj=None):
        super().__init__(*args)

        self.setWindowTitle('Options')

        self.ui_obj = ui_obj

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Apply')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        plot_type = self.ui_obj.config.get('signals', 'time_plot_type')
        self.chb_real = QtWidgets.QCheckBox('Re')
        if 'r' in plot_type:
            self.chb_real.setChecked(True)
        else:
            self.chb_real.setChecked(False)
        self.chb_im = QtWidgets.QCheckBox('Im')
        if 'i' in plot_type:
            self.chb_im.setChecked(True)
        else:
            self.chb_im.setChecked(False)
        self.chb_magnitude = QtWidgets.QCheckBox('Magnitude')
        if 'm' in plot_type:
            self.chb_magnitude.setChecked(True)
        else:
            self.chb_magnitude.setChecked(False)
        self.chb_phase = QtWidgets.QCheckBox('Phase')
        if 'p' in plot_type:
            self.chb_phase.setChecked(True)
        else:
            self.chb_phase.setChecked(False)

        spectrum_type = self.ui_obj.config.get('signals', 'spectrum_type')
        self.cmb_spectrum_y = QtWidgets.QComboBox()
        self.cmb_spectrum_y.addItems([
            'Magnitude',
            'Power (Magnitude^2)'
        ])
        if spectrum_type == 'm':
            self.cmb_spectrum_y.setCurrentIndex(0)
        elif spectrum_type == 'p':
            self.cmb_spectrum_y.setCurrentIndex(1)

        spectrum_phase = self.ui_obj.config.get('signals', 'spectrum_phase')
        self.chb_spectrum_phase = QtWidgets.QCheckBox()
        if spectrum_phase == 'y':
            self.chb_spectrum_phase.setChecked(True)
        else:
            self.chb_spectrum_phase.setChecked(False)

        self.build_layout()
        self.exec_()

        if self.ui_obj is None:
            self.close()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        time_group = QtWidgets.QGroupBox('Time signals')
        time_grid = QtWidgets.QGridLayout()
        time_grid.addWidget(QtWidgets.QLabel('Complex plotting: '), 0, 0, 4, 1)
        time_grid.addWidget(self.chb_real, 0, 1)
        time_grid.addWidget(self.chb_im, 1, 1)
        time_grid.addWidget(self.chb_magnitude, 2, 1)
        time_grid.addWidget(self.chb_phase, 3, 1)
        time_group.setLayout(time_grid)

        frequency_group = QtWidgets.QGroupBox('Frequency signals')
        frequency_grid = QtWidgets.QGridLayout()
        frequency_grid.addWidget(QtWidgets.QLabel('Spectrum y-axis: '), 0, 0)
        frequency_grid.addWidget(QtWidgets.QLabel('Show phase spectrum: '), 1, 0)
        frequency_grid.addWidget(self.cmb_spectrum_y, 0, 1)
        frequency_grid.addWidget(self.chb_spectrum_phase, 1, 1)
        frequency_group.setLayout(frequency_grid)

        group_layout = QtWidgets.QHBoxLayout()
        group_layout.addWidget(time_group)
        group_layout.addWidget(frequency_group)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(group_layout)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):

        self.close()

        plot_string = ''
        if self.chb_real.isChecked():
            plot_string += 'r'
        if self.chb_im.isChecked():
            plot_string += 'i'
        if self.chb_magnitude.isChecked():
            plot_string += 'm'
        if self.chb_phase.isChecked():
            plot_string += 'p'

        if self.cmb_spectrum_y.currentText() == 'Magnitude':
            spectrum_type = 'm'
        elif self.cmb_spectrum_y.currentText() == 'Power (Magnitude^2)':
            spectrum_type = 'p'
        else:
            spectrum_type = 'm'

        if self.chb_spectrum_phase.isChecked():
            spectrum_phase = 'y'
        else:
            spectrum_phase = 'n'

        print(plot_string)
        print(spectrum_type)
        print(spectrum_phase)

        self.ui_obj.config.set('signals', 'time_plot_type', plot_string)
        self.ui_obj.config.set('signals', 'spectrum_type', spectrum_type)
        self.ui_obj.config.set('signals', 'spectrum_phase', spectrum_phase)

        with open('config.ini', 'w') as configfile:
            self.ui_obj.config.write(configfile)


