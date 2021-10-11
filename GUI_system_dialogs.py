# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
# Internals
import GUI_base_widgets
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ComponentProperties(QtWidgets.QDialog):

    def __init__(self, *args, sys_component=None, scene_component=None, scene=None):
        super().__init__(*args)

        self.setWindowTitle('Component properties')

        self.sys_component = sys_component
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


class NewConnector(QtWidgets.QDialog):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.setWindowTitle('New connector')

        self.system_interface = system_interface
        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_component_1 = QtWidgets.QComboBox()
        self.cmb_component_2 = QtWidgets.QComboBox()
        self.cmb_node_1 = QtWidgets.QComboBox()
        self.cmb_node_2 = QtWidgets.QComboBox()
        self.populate_cmbs()
        self.cmb_component_1.currentIndexChanged.connect(self.update_node_1)
        self.cmb_component_2.currentIndexChanged.connect(self.update_node_2)

        self.grp_comp_1 = QtWidgets.QGroupBox('Component 1')
        self.grp_comp_2 = QtWidgets.QGroupBox('Component 2')

        self.build_layout()

        self.exec_()

    def populate_cmbs(self):

        for component in self.system_interface.system_scene.components:
            if not component.type == 'output':
                self.cmb_component_1.addItem(component.designation)
            if not component.type == 'input':
                self.cmb_component_2.addItem(component.designation)

        self.update_node_1()
        self.update_node_2()

    def update_node_1(self):
        index = self.cmb_component_1.currentIndex()
        self.cmb_node_1.clear()
        for i, node in enumerate(self.system_interface.system.components[index].out_nodes):
            self.cmb_node_1.addItem('output node {}'.format(i))

    def update_node_2(self):
        index = self.cmb_component_2.currentIndex()
        self.cmb_node_2.clear()
        for i, node in enumerate(self.system_interface.system.components[index].in_nodes):
            self.cmb_node_2.addItem('input node {}'.format(i))

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        comp_1_layout = QtWidgets.QVBoxLayout()
        comp_1_layout.addWidget(self.cmb_component_1)
        comp_1_layout.addWidget(self.cmb_node_1)
        self.grp_comp_1.setLayout(comp_1_layout)

        comp_2_layout = QtWidgets.QVBoxLayout()
        comp_2_layout.addWidget(self.cmb_component_2)
        comp_2_layout.addWidget(self.cmb_node_2)
        self.grp_comp_2.setLayout(comp_2_layout)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.grp_comp_1)
        top_layout.addWidget(self.grp_comp_2)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.params['component_1_id'] = self.cmb_component_1.currentIndex()
        self.params['component_2_id'] = self.cmb_component_2.currentIndex()
        self.params['node_1_id'] = self.cmb_node_1.currentIndex()
        self.params['node_2_id'] = self.cmb_node_2.currentIndex()
        if self.params['component_1_id'] == self.params['component_2_id']:
            msg = QtWidgets.QMessageBox()
            msg.setText('Cannot connect a component to itself!')
            msg.exec()
        else:
            self.complete = True
            self.close()


class NewDLTISystem(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('New DLTI')

        self.complete = False
        self.stack = QtWidgets.QStackedWidget()
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Close')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems(['State space'])

        self.box_inputs = QtWidgets.QSpinBox()
        self.box_inputs.setSingleStep(1)
        self.box_inputs.setValue(2)

        self.box_outputs = QtWidgets.QSpinBox()
        self.box_outputs.setSingleStep(1)
        self.box_outputs.setValue(2)

        self.box_states = QtWidgets.QSpinBox()
        self.box_states.setSingleStep(1)
        self.box_states.setValue(2)

        self.A = []
        self.B = []
        self.C = []
        self.D = []

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
        base_widget = QtWidgets.QWidget()
        base_widget.setLayout(base_grid)
        self.stack.addWidget(base_widget)

        state_grid = QtWidgets.QGridLayout()
        state_grid.addWidget(QtWidgets.QLabel('Inputs (p): '), 0, 0)
        state_grid.addWidget(QtWidgets.QLabel('Outputs (q): '), 1, 0)
        state_grid.addWidget(QtWidgets.QLabel('State variables (n): '), 2, 0)
        state_grid.addWidget(self.box_inputs, 0, 1)
        state_grid.addWidget(self.box_outputs, 1, 1)
        state_grid.addWidget(self.box_states, 2, 1)
        state_widget = QtWidgets.QWidget()
        state_widget.setLayout(state_grid)
        self.stack.addWidget(state_widget)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.stack)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        current_index = self.stack.currentIndex()
        if current_index == 0:
            self.close()
        elif current_index == 1:
            self.stack.setCurrentIndex(0)
            self.btn_cancel.setText('Close')
        else:
            self.stack.setCurrentIndex(1)
            self.stack.removeWidget(self.stack.widget(current_index))
            self.btn_next.setText('Next')

    def btn_next_trigger(self):
        current_index = self.stack.currentIndex()
        type = self.cmb_type.currentText()
        if current_index == 0:
            if type == 'State space':
                self.stack.setCurrentIndex(1)
            else:
                raise NotImplemented('Not implemented yet!')
            self.btn_cancel.setText('Back')
        elif current_index == 1:
            if type == 'State space':

                p = self.box_inputs.value()
                q = self.box_outputs.value()
                n = self.box_states.value()

                grp_A = QtWidgets.QGroupBox('A')
                grp_B = QtWidgets.QGroupBox('B')
                grp_C = QtWidgets.QGroupBox('C')
                grp_D = QtWidgets.QGroupBox('D')

                grid_A = QtWidgets.QGridLayout()
                grid_B = QtWidgets.QGridLayout()
                grid_C = QtWidgets.QGridLayout()
                grid_D = QtWidgets.QGridLayout()

                for i in range(n):
                    row = []
                    for j in range(n):
                        row.append(QtWidgets.QLineEdit('0.0'))
                        grid_A.addWidget(row[-1], i, j)
                    self.A.append(row)
                for i in range(n):
                    row = []
                    for j in range(p):
                        row.append(QtWidgets.QLineEdit('0.0'))
                        grid_B.addWidget(row[-1], i, j)
                    self.B.append(row)
                for i in range(q):
                    row = []
                    for j in range(n):
                        if i == j:
                            row.append(QtWidgets.QLineEdit('1.0'))
                        else:
                            row.append(QtWidgets.QLineEdit('0.0'))
                        grid_C.addWidget(row[-1], i, j)
                    self.C.append(row)
                for i in range(q):
                    row = []
                    for j in range(p):
                        row.append(QtWidgets.QLineEdit('0.0'))
                        grid_D.addWidget(row[-1], i, j)
                    self.D.append(row)

                grp_A.setLayout(grid_A)
                grp_B.setLayout(grid_B)
                grp_C.setLayout(grid_C)
                grp_D.setLayout(grid_D)

                layout = QtWidgets.QHBoxLayout()
                layout.addWidget(grp_A)
                layout.addWidget(grp_B)
                layout.addWidget(grp_C)
                layout.addWidget(grp_D)

                widget = QtWidgets.QWidget()
                widget.setLayout(layout)

                self.stack.addWidget(widget)

                self.stack.setCurrentIndex(2)

            else:
                raise NotImplemented('Not implemented yet!')
            self.btn_next.setText('Generate')
        else:
            self.gen_params()
            self.complete = True
            self.close()

    def gen_params(self):
        if self.cmb_type.currentText() == 'State space':
            p = self.box_inputs.value()
            q = self.box_outputs.value()
            n = self.box_states.value()

            A = np.zeros((n, n), dtype=float)
            B = np.zeros((n, p), dtype=float)
            C = np.zeros((q, n), dtype=float)
            D = np.zeros((q, p), dtype=float)

            for i in range(n):
                for j in range(n):
                    A[i, j] = float(self.A[i][j].text())

            for i in range(n):
                for j in range(p):
                    B[i, j] = float(self.B[i][j].text())

            for i in range(q):
                for j in range(n):
                    C[i, j] = float(self.C[i][j].text())

            for i in range(q):
                for j in range(p):
                    D[i, j] = float(self.D[i][j].text())

            self.params['type'] = 'state_space'
            self.params['A'] = A
            self.params['B'] = B
            self.params['C'] = C
            self.params['D'] = D


class GetCoefficient(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('Set coefficient')

        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_coefficient = GUI_base_widgets.DoubleSpinBox(
            minimum=-10000.0,
            maximum=10000.0,
            step=1.0,
            decimals=1,
            value=1.0
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
        base_grid.addWidget(QtWidgets.QLabel('Coefficient: '), 0, 0)
        base_grid.addWidget(self.box_coefficient, 0, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.complete = True
        self.close()

    def gen_params(self):
        self.params['coefficient'] = self.box_coefficient.value()


class GetN(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('Set number of inputs to add')

        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_n = QtWidgets.QSpinBox()
        self.box_n.setMinimum(2)
        self.box_n.setMaximum(10)
        self.box_n.setSingleStep(1)
        self.box_n.setValue(3)

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Coefficient: '), 0, 0)
        base_grid.addWidget(self.box_n, 0, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.complete = True
        self.close()

    def gen_params(self):
        self.params['n'] = self.box_n.value()


class GetFunctionString(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('Enter function (use \'x\' as argument)')

        self.complete = False
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.box_function = QtWidgets.QLineEdit()
        self.box_function.setText('0.1 * x ** 2')

        self.build_layout()

        self.exec_()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        base_grid = QtWidgets.QGridLayout()
        base_grid.addWidget(QtWidgets.QLabel('Function: '), 0, 0)
        base_grid.addWidget(self.box_function, 0, 1)

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(base_grid)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_params()
        self.complete = True
        self.close()

    def gen_params(self):
        self.params['function_string'] = self.box_function.text()

