# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
# Internals
import GUI_subwidgets
import Signals as ss
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SetOptions(QtWidgets.QDialog):

    def __init__(self, *args, settings_map=None):
        super().__init__(*args)

        self.setWindowTitle('Settings')

        self.settings_map = settings_map

        self.complete = False

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

    def build_layout(self):

        layout = QtWidgets.QVBoxLayout()

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

        self.ui_obj.config.set('signals', 'time_plot_type', plot_string)
        self.ui_obj.config.set('signals', 'spectrum_type', spectrum_type)
        self.ui_obj.config.set('signals', 'spectrum_phase', spectrum_phase)

        with open('config.ini', 'w') as configfile:
            self.ui_obj.config.write(configfile)

        self.complete = True


class SetOptionsOld(QtWidgets.QDialog):

    def __init__(self, *args, ui_obj=None):
        super().__init__(*args)

        self.setWindowTitle('Options')

        self.ui_obj = ui_obj

        self.complete = False

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

        self.ui_obj.config.set('signals', 'time_plot_type', plot_string)
        self.ui_obj.config.set('signals', 'spectrum_type', spectrum_type)
        self.ui_obj.config.set('signals', 'spectrum_phase', spectrum_phase)

        with open('config.ini', 'w') as configfile:
            self.ui_obj.config.write(configfile)

        self.complete = True

