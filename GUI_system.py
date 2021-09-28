# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals
import GUI_subwidgets
import GUI_system_dialogs
import System
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SystemsInterface(QtWidgets.QWidget):

    def __init__(self, *args, menu=None, config=None):
        super().__init__(*args)

        self.system_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.menu = menu.addMenu('System')
        self.populate_menu()

        self.config = config

        self.build_layout()

    def populate_menu(self):

        self.menu.addAction(GUI_subwidgets.Action('New', self, trigger_func=self.menu_new_trigger))

        self.menu.addAction(GUI_subwidgets.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_subwidgets.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

    def build_layout(self):

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def add_interface(self, interface):
        if interface.system:
            self.tabs.addTab(interface, '{}'.format(interface.system.name()))
        else:
            self.tabs.addTab(interface, 'Empty')
        self.system_interfaces.append(interface)
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def add_system(self, system):
        interface = SystemInterface(config=self.config)
        interface.system = system
        interface.update_info()
        self.add_interface(interface)

    def update_config(self, config):

        self.config = config
        for interface in self.system_interfaces:
            interface.config = self.config
            interface.update_info()

    def menu_new_trigger(self):
        system_interface = SystemInterface(config=self.config)
        wizard = GUI_system_dialogs.NewSystem()
        if wizard.complete:
            if wizard.params['type'] == 'empty':
                system_interface.system = System.System()
            elif wizard.params['type'] == 'LTI':
                system_interface.system = System.SystemLTI()
            else:
                system_interface.system = System.System()
            system_interface.update_info()
            self.add_interface(system_interface)

    def menu_save_trigger(self):
        if len(self.system_interfaces) > 0:
            index = self.tabs.currentIndex()
            system_interface = self.system_interfaces[index]
            if system_interface.system:
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save signal", '', "")
                if filename[0]:
                    system_interface.system.save(filename[0])
                    self.tabs.setTabText(index, system_interface.system.name())

    def menu_load_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            system_interface = SystemInterface(config=self.config)
            system_interface.system = System.System.static_load(filename[0])
            system_interface.update_info()
            self.add_interface(system_interface)

    def menu_close_trigger(self):
        if len(self.tabs) > 0:
            index = self.tabs.currentIndex()
            self.system_interfaces.pop(index)
            self.tabs.removeTab(index)

    def menu_close_all_trigger(self):
        self.system_interfaces = []
        self.tabs.clear()


class SystemInterface(QtWidgets.QWidget):

    def __init__(self, *args, config=None):
        super().__init__(*args)

        self.config = config

        self.system = None

        self.btn_simulate = GUI_subwidgets.MediumButton('Simulate', self, trigger_func=self.simulate_trigger)

        self.graphs = QtWidgets.QTabWidget()
        self.graphs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.input_widget = GUI_subwidgets.InputSignalList('Input signals', system_interface=self)
        self.output_widget = GUI_subwidgets.OutputSignalList('Output signals', system_interface=self)

        self.lbl_info_keys = QtWidgets.QLabel('')
        self.lbl_info_values = QtWidgets.QLabel('')

        self.build_layout()
        self.update_info()

    def build_layout(self):

        btn_layout = QtWidgets.QVBoxLayout()
        btn_layout.addWidget(self.btn_simulate)
        btn_layout.addStretch()

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addLayout(btn_layout)
        info_layout.addWidget(self.lbl_info_keys)
        info_layout.addWidget(self.lbl_info_values)
        info_layout.addStretch()

        panel_layout = QtWidgets.QHBoxLayout()
        panel_layout.addLayout(info_layout)
        panel_layout.addWidget(self.input_widget)
        panel_layout.addWidget(self.output_widget)
        panel_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphs)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def plot_system(self):
        self.graphs.clear()

    def update_info(self):
        if self.system:
            self.plot_system()
            meta_data = self.system.info()
            key_string = ''
            value_string = ''
        else:
            self.graphs.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')

    def simulate_trigger(self):
        pass










