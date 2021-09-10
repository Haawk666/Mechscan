# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import time
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import Signals as ss
import SignalProcessing as sp
import SignalDialogs
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
        generate.addAction(GUI_subwidgets.Action('Time-frequency domain', self, trigger_func=self.menu_generate_time_frequency_trigger))

        self.menu.addAction(GUI_subwidgets.Action('New', self, trigger_func=self.menu_new_trigger))

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
            tab = self.tabs.addTab(interface, '{}'.format(interface.signal.name()))
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
        wizard = SignalDialogs.NewTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            if signal_interface.signal.codomain == 'int' or signal_interface.signal.codomain == 'float' or signal_interface.signal.codomain == 'bool_':
                func_wiz = SignalDialogs.GetFunction1D(ui_object=signal_interface)
            else:
                func_wiz = SignalDialogs.GetFunction1DComplex(ui_object=signal_interface)
            if func_wiz.complete:
                params = func_wiz.params
                iterations = signal_interface.signal.n - 1
                progress_window = GUI_subwidgets.ProgressDialog('Generating signal...', 'Cancel', 0, iterations, self)
                signal_interface.signal = sp.evaluate(
                    signal_interface.signal,
                    lambda x: eval(params['function_string']),
                    method=params['method'],
                    update=progress_window
                )
                signal_interface.update_info()
                self.add_interface(signal_interface)

    def menu_generate_frequency_trigger(self):
        signal_interface = SignalInterface(config=self.config)
        wizard = SignalDialogs.NewTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            signal_interface.signal = sp.fft(signal_interface.signal)
            func_wiz = SignalDialogs.GetFunction1DComplex(ui_object=signal_interface)
            if func_wiz.complete:
                signal_interface.update_info()
                self.add_interface(signal_interface)

    def menu_generate_time_frequency_trigger(self):
        X_1 = np.zeros((4, ), dtype=np.float64)
        X_2 = np.zeros((4, ), dtype=np.float64)
        X_1[0] = 0.0
        X_1[1] = 1.0
        X_1[2] = 2.0
        X_1[3] = 3.0
        X_2[0] = 0.0
        X_2[1] = 1.0
        X_2[2] = 2.0
        X_2[3] = 3.0
        X = [X_1, X_2]
        Y = np.zeros((4, 4, 1), dtype=np.complex64)
        for i in range(4):
            for j in range(4):
                Y[i, j] = np.complex(50 * (X_1[i] + X_2[j]), 0)
        time_frequency_signal = ss.TimeFrequencySignal.from_data(X, Y)
        self.add_signal(time_frequency_signal)

    def menu_new_trigger(self):
        signal_interface = SignalInterface(config=self.config)
        wizard = SignalDialogs.NewTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            signal_interface.update_info()
            self.add_interface(signal_interface)

    def menu_save_trigger(self):
        if len(self.signal_interfaces) > 0:
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
        wizard = SignalDialogs.ImportTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            self.tabs.addTab(signal_interface, '{}'.format(signal_interface.signal.name()))
            self.signal_interfaces.append(signal_interface)
            signal_interface.update_info()
            self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def menu_export_trigger(self):
        index = self.tabs.currentIndex()
        interface = self.signal_interfaces[index]
        SignalDialogs.ExportTimeSignal(ui_object=interface)

    def menu_FFT_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                if signal.signal_type == 'time':
                    self.add_signal(sp.fft(signal))
                elif signal.signal_type == 'frequency':
                    self.add_signal(sp.ifft(signal))

    def menu_gabor_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                if signal.signal_type == 'time':
                    wizard = SignalDialogs.GetGaborParams()
                    if wizard.complete:
                        params = wizard.params
                        delta_tau_n = int(np.round(params['delta_tau'] / signal.delta_x, decimals=0))
                        N = int(np.round(signal.N / delta_tau_n - 1, decimals=0))
                        iterations = signal.channels * N
                        progress_window = GUI_subwidgets.ProgressDialog('Transforming...', 'Cancel', 0, iterations, self)
                        self.add_signal(sp.gabor_transform(
                            signal,
                            window_size=params['window_length'],
                            window_function=params['window_function'],
                            delta_tau=params['delta_tau'],
                            delta_freq=params['delta_freq'],
                            update=progress_window
                        ))
                elif signal.signal_type == 'time-frequency':
                    pass

    def menu_wavelet_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                if signal.signal_type == 'time':
                    wizard = SignalDialogs.GetWaveletParams()
                    if wizard.complete:
                        params = wizard.params
                        self.add_signal(sp.wavelet_transform(
                            signal,
                            window_size=params['window_length'],
                            window_function=params['window_function'],
                            delta_tau=params['delta_tau'],
                            delta_freq=params['delta_freq']
                        ))
                elif signal.signal_type == 'time-frequency':
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
                wizard = SignalDialogs.CropSignal(ui_object=interface)
                interface.update_info()
                self.add_interface(interface)

    def menu_combine_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            signal = self.signal_interfaces[index].signal
            if signal is not None:
                if signal.codomain == 'int' or signal.codomain == 'float' or signal.codomain == 'bool_':
                    func_wiz = SignalDialogs.GetFunction1D(ui_object=self.signal_interfaces[index])
                else:
                    func_wiz = SignalDialogs.GetFunction1DComplex(ui_object=self.signal_interfaces[index])
                if func_wiz.complete:
                    params = func_wiz.params
                    iterations = signal.n - 1
                    progress_window = GUI_subwidgets.ProgressDialog('{}ing signals...'.format(params['method']), 'Cancel', 0, iterations, self)
                    self.signal_interfaces[index].signal = sp.evaluate(
                        signal,
                        lambda x: eval(params['function_string']),
                        method=params['method'],
                        update=progress_window
                    )
                    self.signal_interfaces[index].update_info()

    def menu_resample_trigger(self):
        pass

    def menu_options_trigger(self):
        wizard = SignalDialogs.SetOptions(ui_obj=self)
        if wizard.complete:
            for interface in self.signal_interfaces:
                interface.config = self.config
                interface.update_info()


class SignalInterface(QtWidgets.QWidget):

    def __init__(self, *args, config=None):
        super().__init__(*args)

        self.config = config

        self.signal = None

        self.btn_play = GUI_subwidgets.MediumButton('Play', self, trigger_func=self.play_trigger)

        self.lbl_info_keys = QtWidgets.QLabel('')
        self.lbl_info_values = QtWidgets.QLabel('')

        self.graphs = QtWidgets.QTabWidget()
        self.graphs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.build_layout()
        self.update_info()

    def build_layout(self):

        btn_layout = QtWidgets.QVBoxLayout()
        btn_layout.addWidget(self.btn_play)
        btn_layout.addStretch()

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addLayout(btn_layout)
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

                for j in range(self.signal.channels):

                    plot_widget = pg.GraphicsLayoutWidget()
                    self.graphs.addTab(plot_widget, 'Channel {}'.format(j + 1))

                    plot = plot_widget.addPlot(row=0, col=0)
                    cm = pg.colormap.get('CET-L9')

                    if self.signal.codomain == 'complex':
                        img = pg.ImageItem(image=np.absolute(self.signal.Y[:, self.signal.n[1] // 2:, j]))
                        bar = pg.ColorBarItem(values=(np.absolute(self.signal.Y).min(), np.absolute(self.signal.Y).max()), cmap=cm)
                    else:
                        img = pg.ImageItem(image=self.signal.Y[:, self.signal.n[1] // 2:, j])
                        bar = pg.ColorBarItem(values=(self.signal.Y.min(), self.signal.Y.max()), cmap=cm)

                    plot.addItem(img)
                    bar.setImageItem(img, insert_in=plot)
                    plot.setTitle('Spectrogram')
                    plot.setLabel('bottom', 'Time t, (s)')
                    plot.setLabel('left', 'Frequency f, (Hz)')

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

    def play_trigger(self):

        if self.signal is not None:

            if self.signal.signal_type == 'time':

                channel = self.graphs.currentIndex()

                self.signal.play(channel=channel)

            else:

                if self.signal.time_signal is not None:

                    channel = self.graphs.currentIndex()

                    self.signal.time_signal.play(channel=channel)




