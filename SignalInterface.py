# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import Signals as ss
import SignalProcessing as sp
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SignalsInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.signal_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.btn_generate = GUI_subwidgets.MediumButton('Generate', self, trigger_func=self.btn_generate_trigger)
        self.btn_import = GUI_subwidgets.MediumButton('Import', self, trigger_func=self.btn_import_trigger)
        self.btn_export = GUI_subwidgets.MediumButton('Export', self, trigger_func=self.btn_export_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Close', self, trigger_func=self.btn_clear_trigger)

        self.build_layout()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_import)
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(GUI_subwidgets.HorSeparator())
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def btn_generate_trigger(self):
        signal_interface = SignalInterface()
        wizard = GenerateTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            self.tabs.addTab(signal_interface, '{}'.format(signal_interface.signal.name()))
            self.signal_interfaces.append(signal_interface)
            signal_interface.update_info()
            self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def btn_import_trigger(self):
        signal_interface = SignalInterface()
        wizard = ImportTimeSignal(ui_object=signal_interface)
        if wizard.complete:
            self.tabs.addTab(signal_interface, '{}'.format(signal_interface.signal.name()))
            self.signal_interfaces.append(signal_interface)
            signal_interface.update_info()
            self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def btn_export_trigger(self):
        index = self.tabs.currentIndex()
        interface = self.signal_interfaces[index]
        ExportTimeSignal(ui_object=interface)

    def btn_save_trigger(self):
        index = self.tabs.currentIndex()
        signal_interface = self.signal_interfaces[index]
        if signal_interface.signal:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save signal", '', "")
            if filename[0]:
                signal_interface.signal.save(filename[0])
                self.tabs.setTabText(index, signal_interface.signal.name())

    def btn_load_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            signal_interface = SignalInterface()
            signal_interface.signal = ss.TimeSignal.static_load(filename[0])
            self.signal_interfaces.append(signal_interface)
            self.tabs.addTab(signal_interface, '{}'.format(signal_interface.signal.name()))
            signal_interface.update_info()
            self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def btn_clear_trigger(self):
        index = self.tabs.currentIndex()
        self.signal_interfaces.pop(index)
        self.tabs.removeTab(index)


class SignalInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.signal = None

        self.btn_transform = GUI_subwidgets.MediumButton('Transform', self, trigger_func=self.btn_transform_trigger)
        self.btn_filter = GUI_subwidgets.MediumButton('Filter', self, trigger_func=self.btn_filter_trigger)
        self.btn_crop = GUI_subwidgets.MediumButton('Crop', self, trigger_func=self.btn_crop_trigger)
        self.btn_noise = GUI_subwidgets.MediumButton('Add noise', self, trigger_func=self.btn_noise_trigger)
        self.btn_print = GUI_subwidgets.MediumButton('Print', self, trigger_func=self.btn_print_trigger)

        self.lbl_f_a = QtWidgets.QLabel('')
        self.lbl_bit_depth = QtWidgets.QLabel('')
        self.lbl_bit_rate = QtWidgets.QLabel('')
        self.lbl_codomain = QtWidgets.QLabel('')
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
        self.time_graph.showGrid(x=True, y=True)

        self.frequency_graph = pg.PlotWidget()
        self.frequency_graph.setTitle('Frequency domain magnitude spectrum')
        self.frequency_graph.setLabel('bottom', 'Frequency f, (Hz)')
        self.frequency_graph.setLabel('left', 'Magnitude')
        self.frequency_graph.showGrid(x=True, y=True)

        self.build_layout()
        self.update_info()

    def build_layout(self):

        info_layout = QtWidgets.QGridLayout()
        info_layout.addWidget(QtWidgets.QLabel('Sampling frequency f_a, (Hz): '), 0, 0)
        info_layout.addWidget(QtWidgets.QLabel('Bit depth: '), 1, 0)
        info_layout.addWidget(QtWidgets.QLabel('Bitrate: '), 2, 0)
        info_layout.addWidget(QtWidgets.QLabel('Codomain type: '), 3, 0)
        info_layout.addWidget(QtWidgets.QLabel('Start time t_start, (s): '), 4, 0)
        info_layout.addWidget(QtWidgets.QLabel('End time t_end, (s): '), 5, 0)
        info_layout.addWidget(QtWidgets.QLabel('Sample interval T, (s): '), 0, 2)
        info_layout.addWidget(QtWidgets.QLabel('Angular sampling frequency omega_a, (Hz): '), 1, 2)
        info_layout.addWidget(QtWidgets.QLabel('Number of samples n, (#): '), 2, 2)
        info_layout.addWidget(QtWidgets.QLabel('Signal length (s): '), 3, 2)
        info_layout.addWidget(self.lbl_f_a, 0, 1)
        info_layout.addWidget(self.lbl_bit_depth, 1, 1)
        info_layout.addWidget(self.lbl_bit_rate, 2, 1)
        info_layout.addWidget(self.lbl_codomain, 3, 1)
        info_layout.addWidget(self.lbl_t_start, 4, 1)
        info_layout.addWidget(self.lbl_t_end, 5, 1)
        info_layout.addWidget(self.lbl_T, 0, 3)
        info_layout.addWidget(self.lbl_omega_a, 1, 3)
        info_layout.addWidget(self.lbl_n, 2, 3)
        info_layout.addWidget(self.lbl_length, 3, 3)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_crop)
        btn_layout.addWidget(self.btn_filter)
        btn_layout.addWidget(self.btn_transform)
        btn_layout.addWidget(self.btn_noise)
        btn_layout.addWidget(self.btn_print)
        btn_layout.addStretch()

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addLayout(info_layout)
        panel_layout.addLayout(btn_layout)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.time_graph)
        layout.addWidget(self.frequency_graph)
        layout.addLayout(panel_layout)
        layout.addStretch()
        self.setLayout(layout)

    def btn_transform_trigger(self):
        pass

    def btn_filter_trigger(self):
        pass

    def btn_crop_trigger(self):
        CropSignal(ui_object=self)
        self.update_info()

    def btn_noise_trigger(self):
        AddNoiseSignal(ui_object=self)
        self.update_info()

    def btn_print_trigger(self):
        self.signal.check()
        print(self.signal)

    def plot_signal(self):
        self.time_graph.plotItem.clear()
        plot_line = self.time_graph.plot(self.signal.X, self.signal.Y)
        plot_line.setAlpha(0.65, False)

    def plot_power_spectrum(self):
        self.frequency_graph.plotItem.clear()
        F_signal = sp.MagnitudeFFT(self.signal)
        plot_line = self.frequency_graph.plot(F_signal.X, F_signal.Y)
        plot_line.setAlpha(0.65, False)

    def update_info(self):
        if self.signal:
            self.plot_signal()
            self.plot_power_spectrum()
            self.lbl_f_a.setText('{}'.format(self.signal.f_a))
            self.lbl_bit_depth.setText('{}'.format(self.signal.bit_depth))
            self.lbl_bit_rate.setText('{}'.format(self.signal.bit_rate))
            self.lbl_codomain.setText('{}'.format(self.signal.codomain))
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
            self.lbl_bit_depth.setText('')
            self.lbl_bit_rate.setText('')
            self.lbl_codomain.setText('')
            self.lbl_t_start.setText('')
            self.lbl_t_end.setText('')
            self.lbl_T.setText('')
            self.lbl_omega_a.setText('')
            self.lbl_n.setText('')
            self.lbl_length.setText('')


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
        self.cmb_bits.addItems(['8', '16'])
        self.cmb_bits.setCurrentIndex(1)

        self.box_t_start = QtWidgets.QDoubleSpinBox()
        self.box_t_start.setDecimals(3)

        self.box_t_end = QtWidgets.QDoubleSpinBox()
        self.box_t_end.setDecimals(3)

        if self.ui_obj.signal is not None:
            self.box_f_a.setValue(self.ui_obj.signal.f_a)
            self.box_t_start.setValue(self.ui_obj.signal.t_start)
            self.box_t_end.setValue(self.ui_obj.signal.t_end)
        else:
            self.box_f_a.setValue(44100.0)
            self.box_t_start.setValue(0.0)
            self.box_t_end.setValue(5.0)

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
        self.box_amp.setMaximum(10000.0)
        self.box_amp.setMinimum(0.0)
        self.box_amp.setDecimals(1)
        self.box_amp.setSingleStep(10.0)
        self.box_amp.setValue(420.0)

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
            self.complete = True

    def gen_signal(self):
        self.ui_obj.signal = ss.TimeSignal(
            t_start=self.box_t_start.value(),
            t_end=self.box_t_end.value(),
            sampling_rate=self.box_f_a.value(),
            bit_depth=int(self.cmb_bits.currentText())
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
        self.box_from.setMinimum(self.ui_obj.signal.t_start)
        self.box_from.setMaximum(self.ui_obj.signal.t_end)
        self.box_from.setValue(self.ui_obj.signal.t_start)

        self.box_to = QtWidgets.QDoubleSpinBox()
        self.box_to.setDecimals(3)
        self.box_to.setSingleStep(1.0)
        self.box_to.setMinimum(self.ui_obj.signal.t_start)
        self.box_to.setMaximum(self.ui_obj.signal.t_end)
        self.box_to.setValue(self.ui_obj.signal.t_end)

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
            self.ui_obj.signal = ss.TimeSignal.from_data(new_X, new_Y)
            self.close()


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



