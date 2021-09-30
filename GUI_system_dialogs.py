# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
            self.cmb_component_1.addItem(component.designation)
            self.cmb_component_2.addItem(component.designation)

        self.update_node_1()
        self.update_node_2()

    def update_node_1(self):
        index = self.cmb_component_1.currentIndex()
        self.cmb_node_1.clear()
        for i, node in enumerate(self.system_interface.system_scene.components[index].nodes):
            self.cmb_node_1.addItem('node {}'.format(i))

    def update_node_2(self):
        index = self.cmb_component_2.currentIndex()
        self.cmb_node_2.clear()
        for i, node in enumerate(self.system_interface.system_scene.components[index].nodes):
            self.cmb_node_2.addItem('node {}'.format(i))

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


class NewSystem(QtWidgets.QDialog):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle('New system')

        self.complete = False
        self.stack = QtWidgets.QStackedWidget()
        self.params = dict()

        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)
        self.btn_next = QtWidgets.QPushButton('Ok')
        self.btn_next.clicked.connect(self.btn_next_trigger)

        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems(['empty', 'LTI'])

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

        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addWidget(self.stack)
        top_layout.addLayout(btn_layout)

        self.setLayout(top_layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):
        self.gen_system()
        self.complete = True
        self.close()

    def gen_system(self):
        self.params['type'] = self.cmb_type.currentText()

