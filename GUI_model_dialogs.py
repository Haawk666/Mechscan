# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import pandas as pd
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SetFit(QtWidgets.QDialog):

    def __init__(self, *args, model=None):
        super().__init__(*args)

        self.setWindowTitle('Fit model')

        self.model = model

        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.btn_set_train_data = QtWidgets.QPushButton('Set')
        self.btn_set_train_data.clicked.connect(self.btn_set_train_trigger)

        self.lin_train = QtWidgets.QLineEdit()
        self.cmb_target = QtWidgets.QComboBox()

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Training data: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Target column: '), 1, 0)
        base_grid.addWidget(self.lin_train, 0, 1)
        base_grid.addWidget(self.cmb_target, 1, 1)
        base_grid.addWidget(self.btn_set_train_data, 0, 2)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_set_train_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Set training data", '', "")
        if filename[0]:
            self.lin_train.setText(filename[0])
            self.cmb_target.clear()
            for column in pd.read_csv(filename[0]):
                self.cmb_target.addItem(column)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.close()
        self.complete = True

    def gen_params(self):
        self.params['train'] = self.lin_train.text()
        self.params['target'] = self.cmb_target.currentText()


class ComponentProperties(QtWidgets.QDialog):

    def __init__(self, *args, model_component=None, scene_component=None, scene=None):
        super().__init__(*args)

        self.setWindowTitle('Component properties')

        self.model_component = model_component
        self.scene_component = scene_component
        self.scene = scene
        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Apply')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.btn_change_signal = QtWidgets.QPushButton('Change')
        self.btn_change_signal.clicked.connect(self.btn_change_signal_trigger)
        self.btn_change_function = QtWidgets.QPushButton('Change')
        self.btn_change_function.clicked.connect(self.btn_change_function_trigger)
        self.btn_change_coefficient = QtWidgets.QPushButton('Change')
        self.btn_change_coefficient.clicked.connect(self.btn_change_coefficient_trigger)

        self.lbl_id = QtWidgets.QLabel('{}'.format(self.scene_component.component_id))
        self.lbl_type = QtWidgets.QLabel('{}'.format(sys_component.type))
        self.lbl_inputs = QtWidgets.QLabel('{}'.format(len(sys_component.in_nodes)))
        self.lbl_outputs = QtWidgets.QLabel('{}'.format(len(sys_component.out_nodes)))

        self.lin_designation = QtWidgets.QLineEdit()
        self.lin_designation.setText(self.scene_component.designation)

        self.lbl_signal_path = QtWidgets.QLabel('')
        self.lbl_n = QtWidgets.QLabel('')
        self.lbl_coefficient = QtWidgets.QLabel('')
        self.lbl_function = QtWidgets.QLabel('')

        if self.sys_component.type == 'input':
            self.lbl_signal_path = QtWidgets.QLabel('{}'.format(sys_component.signal.path))
        if self.sys_component.type == 'gain':
            self.lbl_coefficient = QtWidgets.QLabel('{}'.format(sys_component.coefficient))
        if self.sys_component.type == 'function':
            self.lbl_function = QtWidgets.QLabel('{}'.format(sys_component.function_string))

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('Component id: '), 0, 0)
        grid.addWidget(self.lbl_id, 0, 1)
        grid.addWidget(QtWidgets.QLabel('Component type: '), 1, 0)
        grid.addWidget(self.lbl_type, 1, 1)
        grid.addWidget(QtWidgets.QLabel('Inputs: '), 2, 0)
        grid.addWidget(self.lbl_inputs, 2, 1)
        grid.addWidget(QtWidgets.QLabel('Outputs: '), 3, 0)
        grid.addWidget(self.lbl_outputs, 3, 1)
        grid.addWidget(QtWidgets.QLabel('Designation: '), 4, 0)
        grid.addWidget(self.lin_designation, 4, 1)

        if self.sys_component.type == 'input':
            grid.addWidget(QtWidgets.QLabel('Signal: '), 5, 0)
            grid.addWidget(self.lbl_signal_path, 5, 1)
            grid.addWidget(self.btn_change_signal, 5, 2)
        elif self.sys_component.type == 'gain':
            grid.addWidget(QtWidgets.QLabel('Gain: '), 5, 0)
            grid.addWidget(self.lbl_coefficient, 5, 1)
            grid.addWidget(self.btn_change_coefficient, 5, 2)
        elif self.sys_component.type == 'function':
            grid.addWidget(QtWidgets.QLabel('Function: '), 5, 0)
            grid.addWidget(self.lbl_function, 5, 1)
            grid.addWidget(self.btn_change_function, 5, 2)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_change_signal_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            self.lbl_signal_path.setText(filename[0])

    def btn_change_function_trigger(self):
        wiz = GetFunctionString()
        if wiz.complete:
            self.lbl_function.setText(wiz.params['function_string'])

    def btn_change_coefficient_trigger(self):
        wiz = GetCoefficient()
        if wiz.complete:
            self.lbl_coefficient.setText(str(wiz.params['coefficient']))

    def btn_next_trigger(self):
        designation = self.lin_designation.text()
        for component in self.scene.components:
            if component.designation == designation and not component.component_id == self.scene_component.component_id:
                msg = QtWidgets.QMessageBox()
                msg.setText('Invalid designation!')
                msg.exec()
                break
        else:
            self.params['designation'] = designation
            if self.sys_component.type == 'input':
                self.params['signal_path'] = self.lbl_signal_path.text()
            if self.sys_component.type == 'gain':
                self.params['coefficient'] = float(self.lbl_coefficient.text())
            if self.sys_component.type == 'function':
                self.params['function_string'] = self.lbl_function.text()
            self.complete = True
            self.close()


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
        base_grid.addWidget(self.box_outputs, 2, 1)

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
            index, activation, nodes = self.lst_layers.item(i).text().split(' ')
            self.params['layers'].append({
                'index': int(index),
                'activation': activation,
                'nodes': int(nodes)
            })


class GetRandomForestParams(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('New random forest')

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

        self.box_estimators = QtWidgets.QSpinBox()
        self.box_estimators.setMinimum(1)
        self.box_estimators.setMaximum(10000)
        self.box_estimators.setSingleStep(10)
        self.box_estimators.setValue(100)

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Inputs: '), 0, 0)
        base_grid.addWidget(QtWidgets.QLabel('Outputs: '), 1, 0)
        base_grid.addWidget(QtWidgets.QLabel('Estimators: '), 2, 0)
        base_grid.addWidget(self.box_inputs, 0, 1)
        base_grid.addWidget(self.box_outputs, 1, 1)
        base_grid.addWidget(self.box_estimators, 2, 1)

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
        self.params['inputs'] = self.box_inputs.value()
        self.params['outputs'] = self.box_outputs.value()
        self.params['estimators'] = self.box_estimators.value()


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


