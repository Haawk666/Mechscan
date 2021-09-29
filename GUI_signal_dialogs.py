# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
# Internals
import GUI_subwidgets
import Signal as ss
import functions
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetFunction(QtWidgets.QDialog):

    def __init__(self, *args, signal=None):
        super().__init__(*args)

        self.setWindowTitle('Functions')

        self.signal = signal
        self.functions = functions.get_function_map(self.signal)
        self.params = dict()

        self.complete = False

        self.stage = 0
        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_functions = QtWidgets.QComboBox()
        for key in self.functions:
            self.cmb_functions.addItem(key)

        self.cmb_operation = QtWidgets.QComboBox()
        self.cmb_operation.addItems([
            'overwrite',
            'add',
            'multiply',
            'convolve'
        ])

        self.chb_all_channels = QtWidgets.QCheckBox('All channels')
        self.chb_all_channels.setChecked(True)
        self.chb_all_channels.toggled.connect(self.chb_all_channels_trigger)

        self.cmb_channels = QtWidgets.QComboBox()
        for nchan in range(self.signal.channels):
            self.cmb_channels.addItem('Channel {}'.format(nchan + 1))
        self.cmb_channels.setDisabled(True)

        self.range_widgets = []
        for d in range(self.signal.dimensions):
            self.range_widgets.append(dict())
            if self.signal.dimensions == 1:
                self.range_widgets[-1]['from'] = GUI_subwidgets.DoubleSpinBox(
                    minimum=self.signal.x_start,
                    maximum=self.signal.x_end,
                    step=1.0,
                    decimals=3,
                    value=self.signal.x_start
                )
                self.range_widgets[-1]['to'] = GUI_subwidgets.DoubleSpinBox(
                    minimum=self.signal.x_start,
                    maximum=self.signal.x_end,
                    step=1.0,
                    decimals=3,
                    value=self.signal.x_end
                )
            else:
                self.range_widgets[-1]['from'] = GUI_subwidgets.DoubleSpinBox(
                    minimum=self.signal.x_start[d],
                    maximum=self.signal.x_end[d],
                    step=1.0,
                    decimals=3,
                    value=self.signal.x_start[d]
                )
                self.range_widgets[-1]['to'] = GUI_subwidgets.DoubleSpinBox(
                    minimum=self.signal.x_start[d],
                    maximum=self.signal.x_end[d],
                    step=1.0,
                    decimals=3,
                    value=self.signal.x_end[d]
                )

        self.lbl_explain = QtWidgets.QLabel('Enter a function as a string, ie: \'100 * np.exp(0.5 * x)\'.')

        self.box_custom = QtWidgets.QLineEdit('')

        # Functions:
        # - Custom:
        self.param_boxes = dict()
        for function, details in self.functions.items():
            if not function == 'custom':
                self.param_boxes[function] = dict()
                for key, parameter in self.functions[function]['kwargs'].items():
                    self.param_boxes[function][key] = GUI_subwidgets.DoubleSpinBox(
                        minimum=parameter.min,
                        maximum=parameter.max,
                        step=parameter.step,
                        decimals=parameter.dec,
                        value=parameter.default
                    )

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

        range_grid = QtWidgets.QGridLayout()
        range_grid.addWidget(QtWidgets.QLabel('From: '), 0, 1)
        range_grid.addWidget(QtWidgets.QLabel('To: '), 0, 2)
        row = 1
        for d, dimension in enumerate(self.range_widgets):
            range_grid.addWidget(QtWidgets.QLabel('dimension {}: '.format(d)), row, 0)
            range_grid.addWidget(dimension['from'], row, 1)
            range_grid.addWidget(dimension['to'], row, 2)
            row += 1
        range_widget = QtWidgets.QWidget()
        range_widget.setLayout(range_grid)
        self.stack.addWidget(range_widget)

        custom_function_grid = QtWidgets.QGridLayout()
        custom_function_grid.addWidget(self.lbl_explain, 0, 0, 0, 2)
        custom_function_grid.addWidget(QtWidgets.QLabel('Function string: '), 1, 0)
        custom_function_grid.addWidget(self.box_custom, 1, 1)
        const_widget = QtWidgets.QWidget()
        const_widget.setLayout(custom_function_grid)
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
        elif self.stage == 1:
            self.btn_next.setText('Next')
            self.btn_cancel.setText('Cancel')
            self.stack.setCurrentIndex(0)
            self.stage = 0
        elif self.stage == 2:
            self.btn_next.setText('Next')
            self.btn_cancel.setText('Back')
            self.stack.setCurrentIndex(1)
            self.stage = 1
        else:
            self.btn_next.setText('Next')
            self.btn_cancel.setText('Back')
            self.stack.setCurrentIndex(12)
            self.stage = 2

    def btn_next_trigger(self):
        if self.stage == 0:
            self.stack.setCurrentIndex(1)
            self.stage = 1
            self.btn_next.setText('Next')
            self.btn_cancel.setText('Back')
        elif self.stage == 1:
            function = self.cmb_functions.currentText()
            if function == 'custom':
                self.stack.setCurrentIndex(2)
            else:
                if self.stack.count() == 4:
                    self.stack.removeWidget(self.stack.widget(3))
                param_grid = QtWidgets.QGridLayout()
                row = 0
                for key, parameter in self.functions[function]['kwargs'].items():
                    param_grid.addWidget(QtWidgets.QLabel('{}: '.format(key)), row, 0)
                    param_grid.addWidget(self.param_boxes[function][key], row, 1)
                    row += 1
                param_widget = QtWidgets.QWidget()
                param_widget.setLayout(param_grid)
                self.stack.addWidget(param_widget)
                self.stack.setCurrentIndex(3)
            self.stage = 2
            self.btn_next.setText('Generate')
            self.btn_cancel.setText('Back')
        else:
            self.gen_params()
            self.complete = True
            self.close()

    def gen_params(self):

        self.params['a'] = []
        self.params['b'] = []
        for d in range(self.signal.dimensions):
            self.params['a'].append(self.range_widgets[0]['from'].value())
            self.params['b'].append(self.range_widgets[0]['to'].value())

        self.params['method'] = self.cmb_operation.currentText()

        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels) - 1]
        self.params['channels'] = channels

        function_key = self.cmb_functions.currentText()

        self.params['vector'] = self.functions[function_key]['vector']
        self.params['kwargs'] = dict()
        for key, value in self.functions[function_key]['kwargs'].items():
            self.params['kwargs'][key] = self.param_boxes[function_key][key].value()
        if function_key == 'custom':
            self.params['kwargs']['string'] = self.box_custom.text()
        self.params['function'] = self.functions[function_key]['function']
        self.params['args'] = self.functions[function_key]['args']


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
            'wav',
            'mp3'
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
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Import signal", '', "")
        if filename[0]:
            if self.cmb_type.currentText() == 'wav':
                self.ui_obj.signal = ss.TimeSignal.from_wav(filename[0])
            elif self.cmb_type.currentText() == 'mp3':
                self.ui_obj.signal = ss.TimeSignal.from_mp3(filename[0])


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


class GetGaborParams(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('Gabor transform parameters')

        self.complete = False
        self.params = self.params = {
            'window_length': 0.1,
            'window_function': 'Hann',
            'delta_tau': 0.5,
            'delta_freq': 0.1
        }

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Transform')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_alpha = QtWidgets.QDoubleSpinBox()
        self.box_alpha.setDecimals(3)
        self.box_alpha.setSingleStep(1.0)
        self.box_alpha.setMinimum(0.0)
        self.box_alpha.setMaximum(10.0)
        self.box_alpha.setValue(0.2)

        self.cmb_window_function = QtWidgets.QComboBox()
        self.cmb_window_function.addItems([
            'Hann'
        ])

        self.box_delta_tau = QtWidgets.QDoubleSpinBox()
        self.box_delta_tau.setDecimals(3)
        self.box_delta_tau.setSingleStep(1.0)
        self.box_delta_tau.setMinimum(0.001)
        self.box_delta_tau.setMaximum(10.000)
        self.box_delta_tau.setValue(0.2)

        self.box_delta_f = QtWidgets.QDoubleSpinBox()
        self.box_delta_f.setDecimals(1)
        self.box_delta_f.setSingleStep(1.0)
        self.box_delta_f.setMinimum(0.1)
        self.box_delta_f.setMaximum(10.0)
        self.box_delta_f.setValue(1.0)

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('Window length: '), 0, 0)
        grid.addWidget(QtWidgets.QLabel('Window function: '), 1, 0)
        grid.addWidget(QtWidgets.QLabel('Delta tau: '), 2, 0)
        grid.addWidget(QtWidgets.QLabel('Delta freq: '), 3, 0)
        grid.addWidget(self.box_alpha, 0, 1)
        grid.addWidget(self.cmb_window_function, 1, 1)
        grid.addWidget(self.box_delta_tau, 2, 1)
        grid.addWidget(self.box_delta_f, 3, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.params = {
            'window_length': self.box_alpha.value(),
            'window_function': self.cmb_window_function.currentText(),
            'delta_tau': self.box_delta_tau.value(),
            'delta_freq': self.box_delta_f.value()
        }
        self.close()
        self.complete = True


class GetWaveletParams(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('Gabor transform parameters')

        self.complete = False
        self.params = self.params = {
            'window_length': 0.1,
            'window_function': 'Morlet',
            'delta_tau': 0.5,
            'delta_freq': 0.1
        }

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Transform')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_alpha = QtWidgets.QDoubleSpinBox()
        self.box_alpha.setDecimals(3)
        self.box_alpha.setSingleStep(1.0)
        self.box_alpha.setMinimum(0.0)
        self.box_alpha.setMaximum(10.0)
        self.box_alpha.setValue(0.2)

        self.cmb_window_function = QtWidgets.QComboBox()
        self.cmb_window_function.addItems([
            'Morlet',
            'Haar'
        ])

        self.box_delta_tau = QtWidgets.QDoubleSpinBox()
        self.box_delta_tau.setDecimals(3)
        self.box_delta_tau.setSingleStep(1.0)
        self.box_delta_tau.setMinimum(0.001)
        self.box_delta_tau.setMaximum(10.000)
        self.box_delta_tau.setValue(0.2)

        self.box_delta_f = QtWidgets.QDoubleSpinBox()
        self.box_delta_f.setDecimals(1)
        self.box_delta_f.setSingleStep(1.0)
        self.box_delta_f.setMinimum(0.1)
        self.box_delta_f.setMaximum(10.0)
        self.box_delta_f.setValue(1.0)

        self.build_layout()
        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('Window length: '), 0, 0)
        grid.addWidget(QtWidgets.QLabel('Window function: '), 1, 0)
        grid.addWidget(QtWidgets.QLabel('Delta tau: '), 2, 0)
        grid.addWidget(QtWidgets.QLabel('Delta freq: '), 3, 0)
        grid.addWidget(self.box_alpha, 0, 1)
        grid.addWidget(self.cmb_window_function, 1, 1)
        grid.addWidget(self.box_delta_tau, 2, 1)
        grid.addWidget(self.box_delta_f, 3, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.params = {
            'window_length': self.box_alpha.value(),
            'window_function': self.cmb_window_function.currentText(),
            'delta_tau': self.box_delta_tau.value(),
            'delta_freq': self.box_delta_f.value()
        }
        self.close()
        self.complete = True


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
        self.box_alpha.setValue(0.1)

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

