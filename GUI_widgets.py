# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import random
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import Model as tf
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.data = None

        self.btn_new = GUI_subwidgets.MediumButton('New', self, trigger_func=self.btn_new_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Clear', self, trigger_func=self.btn_clear_trigger)
        self.lbl_current = QtWidgets.QLabel('Current data: {}'.format(None))

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

        layout.addStretch()
        self.setLayout(layout)

    def btn_new_trigger(self):
        pass

    def btn_save_trigger(self):
        pass

    def btn_load_trigger(self):
        pass

    def btn_clear_trigger(self):
        pass


class ModelInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

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
















