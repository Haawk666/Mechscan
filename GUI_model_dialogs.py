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


class GetANNTopology(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('New topology')

        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_inputs = QtWidgets.QSpinBox()
        self.box_inputs.setMinimum(1)
        self.box_inputs.setMaximum(10000)
        self.box_inputs.setSingleStep(10)
        self.box_inputs.setValue(10)

        self.box_outputs = QtWidgets.QSpinBox()
        self.box_outputs.setMinimum(1)
        self.box_outputs.setMaximum(10000)
        self.box_outputs.setSingleStep(10)
        self.box_outputs.setValue(10)

        self.lst_layers = QtWidgets.QListWidget()

        self.btn_add = QtWidgets.QPushButton('Add')
        self.btn_add.clicked.connect(self.btn_add_trigger)
        self.btn_del = QtWidgets.QPushButton('Del')
        self.btn_del.clicked.connect(self.btn_del_trigger)
        self.btn_up = QtWidgets.QPushButton('^')
        self.btn_up.clicked.connect(self.btn_up_trigger)
        self.btn_down = QtWidgets.QPushButton('v')
        self.btn_down.clicked.connect(self.btn_down_trigger)

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        lst_btns = QtWidgets.QHBoxLayout()
        lst_btns.addWidget(self.btn_add)
        lst_btns.addWidget(self.btn_up)
        lst_btns.addWidget(self.btn_down)
        lst_btns.addWidget(self.btn_del)
        lst_btns.addStretch()

        lst_layout = QtWidgets.QVBoxLayout()
        lst_layout.addWidget(self.lst_layers)
        lst_layout.addLayout(lst_btns)

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Inputs: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Hidden layers: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Outputs: '), 2, 0)
        base_grid.addWidget(self.box_inputs, 0, 1)
        base_grid.addLayout(lst_layout, 1, 1)
        base_grid.addWidget(self.box_outputs, 2, 0)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_add_trigger(self):
        wiz = GetLayer()
        if wiz.complete:
            self.lst_layers.addItem('{} {} {}'.format(self.lst_layers.count(), wiz.params['activation'], wiz.params['nodes']))

    def btn_del_trigger(self):
        pass

    def btn_up_trigger(self):
        pass

    def btn_down_trigger(self):
        pass

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.close()
        self.complete = True

    def gen_params(self):
        self.params['inputs'] = self.box_inputs.value()
        self.params['outputs'] = self.box_outputs.value()
        self.params['layers'] = []
        for i in range(self.lst_layers.count()):
            index, activation, nodes = self.lst_layers.itemFromIndex(i).text().split(' ')
            self.params['layers'].append({
                'index': int(index),
                'activation': activation,
                'nodes': int(nodes)
            })


class GetLayer(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('New layer')

        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_nodes = QtWidgets.QSpinBox()
        self.box_nodes.setMinimum(1)
        self.box_nodes.setMaximum(10000)
        self.box_nodes.setSingleStep(10)
        self.box_nodes.setValue(10)

        self.cmb_activation_func = QtWidgets.QComboBox()
        self.cmb_activation_func.addItems(['Sigmoid'])

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Nodes: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Activation function: '), 1, 0)
        base_grid.addWidget(self.box_nodes, 0, 1)
        base_grid.addWidget(self.cmb_activation_func, 1, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.close()
        self.complete = True

    def gen_params(self):
        self.params['nodes'] = self.box_nodes.value()
        self.params['activation'] = self.cmb_activation_func.currentText()


class NewModel(QtWidgets.QDialog):

    def __init__(self, *args, ui_object=None):
        super().__init__(*args)

        self.setWindowTitle('New model')

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


