# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NewDataset(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('New dataset')

        self.complete = False
        self.params = dict()

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.close()
        # self.complete = True

    def gen_params(self):
        self.params = dict()


class Import(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('Import data')

        self.complete = False
        self.params = dict()

        self.ui_obj = ui_object

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems(['CSV', 'Pandas'])

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Type: '), 0, 0)
        base_grid.addWidget(self.cmb_type, 0, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.close()

    def gen_params(self):
        self.params['type'] = self.cmb_type.currentText()
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load data", '', "")
        if filename[0]:
            self.params['path'] = filename[0]
            self.complete = True


