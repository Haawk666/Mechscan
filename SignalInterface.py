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

        menu_generate_time = QtWidgets.QAction('Time domain', self)
        menu_generate_time.triggered.connect(self.menu_generate_time_trigger)
        generate.addAction(menu_generate_time)

        menu_generate_frequency = QtWidgets.QAction('Frequency domain', self)
        menu_generate_frequency.triggered.connect(self.menu_generate_frequency_trigger)
        generate.addAction(menu_generate_frequency)

        new = self.menu.addMenu('New')

        menu_new_time = QtWidgets.QAction('Time domain', self)
        menu_new_time.triggered.connect(self.menu_new_time_trigger)
        new.addAction(menu_new_time)

        menu_new_frequency = QtWidgets.QAction('Frequency domain', self)
        menu_new_frequency.triggered.connect(self.menu_new_frequency_trigger)
        new.addAction(menu_new_frequency)

        menu_save = QtWidgets.QAction('Save', self)
        menu_save.triggered.connect(self.menu_save_trigger)
        self.menu.addAction(menu_save)

        menu_load = QtWidgets.QAction('Load', self)
        menu_load.triggered.connect(self.menu_load_trigger)
        self.menu.addAction(menu_load)

        menu_close = QtWidgets.QAction('Close', self)
        menu_close.triggered.connect(self.menu_close_trigger)
        self.menu.addAction(menu_close)

        self.menu.addSeparator()

        menu_import = QtWidgets.QAction('Import', self)
        menu_import.triggered.connect(self.menu_import_trigger)
        self.menu.addAction(menu_import)

        menu_export = QtWidgets.QAction('Export', self)
        menu_export.triggered.connect(self.menu_export_trigger)
        self.menu.addAction(menu_export)

        self.menu.addSeparator()

        transforms = self.menu.addMenu('Transforms')

        menu_FFT = QtWidgets.QAction('FFT/IFFT', self)
        menu_FFT.triggered.connect(self.menu_FFT_trigger)
        transforms.addAction(menu_FFT)

        filters = self.menu.addMenu('Filters')

        menu_compression = QtWidgets.QAction('Compression', self)
        menu_compression.triggered.connect(self.menu_compression_trigger)
        filters.addAction(menu_compression)

        edit = self.menu.addMenu('Edit')

        menu_scale = QtWidgets.QAction('Scale', self)
        menu_scale.triggered.connect(self.menu_scale_trigger)
        edit.addAction(menu_scale)

        menu_shift = QtWidgets.QAction('Shift', self)
        menu_shift.triggered.connect(self.menu_shift_trigger)
        edit.addAction(menu_shift)

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
                    pass

    def menu_scale_trigger(self):
        pass

    def menu_shift_trigger(self):
        pass

    def menu_compression_trigger(self):
        pass


class SignalInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.signal = None

        self.btn_transform = GUI_subwidgets.MediumButton('Transform', self, trigger_func=self.btn_transform_trigger)
        self.btn_filter = GUI_subwidgets.MediumButton('Filter', self, trigger_func=self.btn_filter_trigger)
        self.btn_crop = GUI_subwidgets.MediumButton('Crop', self, trigger_func=self.btn_crop_trigger)
        self.btn_noise = GUI_subwidgets.MediumButton('Add noise', self, trigger_func=self.btn_noise_trigger)
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
        btn_layout.addWidget(self.btn_crop)
        btn_layout.addWidget(self.btn_filter)
        btn_layout.addWidget(self.btn_transform)
        btn_layout.addWidget(self.btn_noise)
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



