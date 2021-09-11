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
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetFunction(QtWidgets.QDialog):

    def __init__(self, *args, signal=None):
        super().__init__(*args)

        self.setWindowTitle('Functions')

        self.signal = signal
        self.functions = dict()
        self.params = dict()

        self.collect_functions()

        self.complete = False

        self.stage = 0
        self.stack = QtWidgets.QStackedWidget()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Next')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_functions = QtWidgets.QComboBox()
        self.cmb_functions.addItem('custom')
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
        for nchan in range(self.ui_obj.signal.channels):
            self.cmb_channels.addItem('Channel {}'.format(nchan + 1))
        self.cmb_channels.setDisabled(True)

        self.chb_range = QtWidgets.QCheckBox('Apply only to subdomain')
        self.chb_range.setChecked(False)

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
            self.param_boxes[function] = dict()
            for key, value in self.functions[function]['params'].items():
                self.param_boxes[function][key] = GUI_subwidgets.DoubleSpinBox(
                    minimum=value['min'],
                    maximum=value['max'],
                    step=value['step'],
                    decimals=value['dec'],
                    value=value['default']
                )

        self.build_layout()

        self.exec_()

    def collect_functions(self):

        if self.signal.dimensions == 1:

            if self.ui_obj.signal.codomain in ['int', 'float', 'bool_']:

                self.functions = {
                    'sine': {
                        'params': {
                            'A': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 10.0,
                                'dec': 1,
                                'default': 666.0
                            },
                            'f': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 1.0,
                                'dec': 1,
                                'default': 666.0
                            },
                            'phi': {
                                'min': -2 * np.pi,
                                'max': 2 * np.pi,
                                'step': 0.5 * np.pi,
                                'dec': 3,
                                'default': 0.0
                            }
                        },
                        'function_string': '{} * np.sin(2 * np.pi * {} * (x - {}))',
                        'argument_keys': ['A', 'f', 'phi']
                    },
                    'cosine': {
                        'params': {
                            'A': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 10.0,
                                'dec': 1,
                                'default': 666.0
                            },
                            'f': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 1.0,
                                'dec': 1,
                                'default': 666.0
                            },
                            'phi': {
                                'min': -2 * np.pi,
                                'max': 2 * np.pi,
                                'step': 0.5 * np.pi,
                                'dec': 3,
                                'default': 0.0
                            }
                        },
                        'function_string': '{} * np.cos(2 * np.pi * {} * (x - {}))',
                        'argument_keys': ['A', 'f', 'phi']
                    },
                    'linear chirp': {
                        'params': {
                            'A': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 10.0,
                                'dec': 1,
                                'default': 666.0
                            },
                            'x_0': {
                                'min': self.ui_obj.signal.x_start,
                                'max': self.ui_obj.signal.x_end,
                                'step': 1.0,
                                'dec': 2,
                                'default': self.ui_obj.signal.x_start
                            },
                            'x_1': {
                                'min': self.ui_obj.signal.x_start,
                                'max': self.ui_obj.signal.x_end,
                                'step': 1.0,
                                'dec': 2,
                                'default': self.ui_obj.signal.x_end
                            },
                            'f_0': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 10.0,
                                'dec': 1,
                                'default': 0.0
                            },
                            'f_1': {
                                'min': -1000.0,
                                'max': 1000.0,
                                'step': 10.0,
                                'dec': 1,
                                'default': 666.0
                            }
                        },
                        'function_string': '{} * np.sin(2 * np.pi * ((({} - {}) / ({} - {})) * x + {} - (({} - {}) / ({} - {})) * {}) * x)',
                        'argument_keys': ['A', 'f_1', 'f_0', 'x_1', 'x_0', 'f_0', 'f_1', 'f_0', 'x_1', 'x_0', 'x_0']
                    }
                }

            else:

                self.functions = dict()

        else:

            if self.ui_obj.signal.codomain in ['int', 'float', 'bool_']:

                self.functions = dict()

            else:

                self.functions = dict()

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
        base_grid.addWidget(QtWidgets.QLabel('Range: '), 4, 0)
        base_grid.addWidget(self.cmb_functions, 0, 1)
        base_grid.addWidget(self.cmb_operation, 1, 1)
        base_grid.addWidget(self.chb_all_channels, 2, 1)
        base_grid.addWidget(self.cmb_channels, 3, 1)
        base_grid.addWidget(self.chb_range, 4, 1)
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
        else:
            if self.chb_range.isChecked():
                self.btn_next.setText('Next')
                self.btn_cancel.setText('Back')
                self.stack.setCurrentIndex(1)
                self.stage = 1
            else:
                self.btn_next.setText('Next')
                self.btn_cancel.setText('Cancel')
                self.stack.setCurrentIndex(0)
                self.stage = 0

    def btn_next_trigger(self):
        if self.stage == 0:
            if self.stack.count() == 4:
                self.stack.removeWidget(self.stack.widget(3))

            param_grid = QtWidgets.QGridLayout()
            function = self.cmb_functions.currentText()
            row = 0
            for param, properties in self.functions[function]['params'].items():
                param_grid.addWidget(QtWidgets.QLabel('{}: '.format(param)), row, 0)
                param_grid.addWidget(self.param_boxes[function][param], row, 1)
                row += 1
            param_widget = QtWidgets.QWidget()
            param_widget.setLayout(param_grid)
            self.stack.addWidget(param_widget)

            if self.chb_range.isChecked():
                self.stack.setCurrentIndex(1)
                self.stage = 1
            else:
                if function == 'custom':
                    self.stack.setCurrentIndex(2)
                    self.stage = 2

                else:
                    self.stack.setCurrentIndex(3)
                    self.stage = 2
                self.btn_next.setText('Generate')
                self.btn_cancel.setText('Back')

        elif self.stage == 1:
            function = self.cmb_functions.currentText()
            if function == 'custom':
                self.stack.setCurrentIndex(2)
                self.stage = 2

            else:
                self.stack.setCurrentIndex(3)
                self.stage = 2
            self.btn_next.setText('Generate')
            self.btn_cancel.setText('Back')

        else:
            self.gen_params()
            self.complete = True
            self.close()

    def gen_params(self):

        start = self.box_from.value()
        end = self.box_to.value()

        operation = self.cmb_operation.currentText()

        channels = None
        if not self.chb_all_channels.isChecked():
            channels = self.cmb_channels.currentText().replace('Channel ', '')
            channels = [int(channels) - 1]

        self.params['a'] = start
        self.params['b'] = end
        self.params['method'] = operation
        self.params['channels'] = channels

        function = self.cmb_functions.currentText()

        if function == 'custom':
            self.params['function_string'] = self.box_custom.text()
        else:
            args = []
            for key in self.functions[function]['argument_keys']:
                args.append(self.param_boxes[function][key].value())
            self.params['function_string'] = self.functions[function]['function_string'].format(*tuple(args))


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
            'Constant',
            'Quadratic chirp'
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

        self.box_chirp_amp = QtWidgets.QDoubleSpinBox()
        self.box_chirp_amp.setDecimals(1)
        self.box_chirp_amp.setMinimum(0.0)
        self.box_chirp_amp.setMaximum(1000.0)
        self.box_chirp_amp.setSingleStep(10.0)
        self.box_chirp_amp.setValue(666.0)

        self.box_chirp_f_1 = QtWidgets.QDoubleSpinBox()
        self.box_chirp_f_1.setDecimals(1)
        self.box_chirp_f_1.setMinimum(0.0)
        self.box_chirp_f_1.setMaximum(1000.0)
        self.box_chirp_f_1.setSingleStep(10.0)
        self.box_chirp_f_1.setValue(50.0)

        self.box_chirp_f_2 = QtWidgets.QDoubleSpinBox()
        self.box_chirp_f_2.setDecimals(1)
        self.box_chirp_f_2.setMinimum(0.0)
        self.box_chirp_f_2.setMaximum(1000.0)
        self.box_chirp_f_2.setSingleStep(10.0)
        self.box_chirp_f_2.setValue(400.0)

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

        chirp_grid = QtWidgets.QGridLayout()
        chirp_grid.addWidget(QtWidgets.QLabel('Amplitude: '), 0, 0)
        chirp_grid.addWidget(QtWidgets.QLabel('f_0: '), 1, 0)
        chirp_grid.addWidget(QtWidgets.QLabel('f_1: '), 2, 0)
        chirp_grid.addWidget(self.box_chirp_amp, 0, 1)
        chirp_grid.addWidget(self.box_chirp_f_1, 1, 1)
        chirp_grid.addWidget(self.box_chirp_f_2, 2, 1)
        chirp_widget = QtWidgets.QWidget()
        chirp_widget.setLayout(chirp_grid)
        self.stack.addWidget(chirp_widget)

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
                elif self.cmb_functions.currentText() == 'Quadratic chirp':
                    next_index = 8
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
        elif self.cmb_functions.currentText() == 'Quadratic chirp':
            amp = self.box_chirp_amp.value()
            f_0 = self.box_chirp_f_1.value()
            f_1 = self.box_chirp_f_2.value()
            t_end = self.box_to.value()
            function_string = '{} * np.cos(2 * np.pi * x * ({} + ({} - {}) * x ** 2 / (3 * {} ** 2)))'.format(amp, f_0, f_1, f_0, t_end)

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
        base_grid.addWidget(QtWidgets.QLabel('From: '), 4, 0)
        base_grid.addWidget(QtWidgets.QLabel('To: '), 5, 0)
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


class GetFunction2DComplex(QtWidgets.QDialog):

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

        self.box_from_x_1 = QtWidgets.QDoubleSpinBox()
        self.box_from_x_1.setDecimals(3)
        self.box_from_x_1.setSingleStep(1.0)
        self.box_from_x_1.setMinimum(-100.0)
        self.box_from_x_1.setMaximum(100.0)
        self.box_from_x_1.setValue(0.0)

        self.box_from_x_2 = QtWidgets.QDoubleSpinBox()
        self.box_from_x_2.setDecimals(3)
        self.box_from_x_2.setSingleStep(1.0)
        self.box_from_x_2.setMinimum(-44100.0)
        self.box_from_x_2.setMaximum(44100.0)
        self.box_from_x_2.setValue(0.0)

        self.box_to_x_1 = QtWidgets.QDoubleSpinBox()
        self.box_to_x_1.setDecimals(3)
        self.box_to_x_1.setSingleStep(1.0)
        self.box_to_x_1.setMinimum(-100.0)
        self.box_to_x_1.setMaximum(100.0)
        self.box_to_x_1.setValue(1.0)

        self.box_to_x_2 = QtWidgets.QDoubleSpinBox()
        self.box_to_x_2.setDecimals(3)
        self.box_to_x_2.setSingleStep(1.0)
        self.box_to_x_2.setMinimum(-100.0)
        self.box_to_x_2.setMaximum(100.0)
        self.box_to_x_2.setValue(1.0)

        self.lbl_explain = QtWidgets.QLabel('Enter a function as a string, ie: \'100 * np.exp(0.5 * x)\'.\nIf the signal has multiple dimensions, use \'x_1\', \'x_2\', etc...')

        self.box_function = QtWidgets.QLineEdit()
        self.box_function.setText('np.complex(5 * np.sin(2 * np.pi * 420 * x_1), x_2)')

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
        base_grid.addWidget(QtWidgets.QLabel('From (x_1): '), 4, 0)
        base_grid.addWidget(QtWidgets.QLabel('To (x_1): '), 5, 0)
        base_grid.addWidget(QtWidgets.QLabel('From (x_2): '), 4, 0)
        base_grid.addWidget(QtWidgets.QLabel('To (x_2): '), 5, 0)
        base_grid.addWidget(self.cmb_functions, 0, 1)
        base_grid.addWidget(self.cmb_operation, 1, 1)
        base_grid.addWidget(self.chb_all_channels, 2, 1)
        base_grid.addWidget(self.cmb_channels, 3, 1)
        base_grid.addWidget(self.box_from_x_1, 4, 1)
        base_grid.addWidget(self.box_to_x_1, 5, 1)
        base_grid.addWidget(self.box_from_x_2, 4, 1)
        base_grid.addWidget(self.box_to_x_2, 5, 1)
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

        start = [self.box_from_x_1.value(), self.box_from_x_2.value()]
        end = [self.box_to_x_1.value(), self.box_to_x_2.value()]

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
