# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals
import GUI_elements
import GUI_system_dialogs
import GUI_system_widgets
import System
import System_2
import System_processing
import Signal
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

        self.menu.addAction(GUI_elements.Action('New', self, trigger_func=self.menu_new_trigger))

        self.menu.addAction(GUI_elements.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_elements.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_elements.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_elements.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

        self.menu.addSeparator()

        components = self.menu.addMenu('Components')
        components.addAction(GUI_elements.Action('Input', self, trigger_func=self.menu_components_input))
        components.addAction(GUI_elements.Action('Output', self, trigger_func=self.menu_components_output))
        components.addAction(GUI_elements.Action('System', self, trigger_func=self.menu_components_system))
        components.addSeparator()
        components.addAction(GUI_elements.Action('Add', self, trigger_func=self.menu_components_add))
        components.addAction(GUI_elements.Action('Split', self, trigger_func=self.menu_components_split))
        components.addAction(GUI_elements.Action('Sum', self, trigger_func=self.menu_components_sum))
        components.addAction(GUI_elements.Action('Delay', self, trigger_func=self.menu_components_delay))
        components.addAction(GUI_elements.Action('Scale', self, trigger_func=self.menu_components_scale))

        self.menu.addAction(GUI_elements.Action('Connect', self, trigger_func=self.menu_connect_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_elements.Action('Calculate', self, trigger_func=self.menu_calculate_trigger))
        self.menu.addAction(GUI_elements.Action('Simulate', self, trigger_func=self.menu_simulate_trigger))

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
                system_interface.system = System_2.System()
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
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load system", '', "")
        if filename[0]:
            system_interface = SystemInterface(config=self.config)
            system_interface.system = System_2.System.static_load(filename[0])
            system_interface.plot_system()
            self.add_interface(system_interface)

    def menu_close_trigger(self):
        if len(self.tabs) > 0:
            index = self.tabs.currentIndex()
            self.system_interfaces.pop(index)
            self.tabs.removeTab(index)

    def menu_close_all_trigger(self):
        self.system_interfaces = []
        self.tabs.clear()

    def menu_components_input(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
                if filename[0]:
                    signal = Signal.TimeSignal.static_load(filename[0])
                    self.system_interfaces[index].system_scene.add_component_input()
                    self.system_interfaces[index].system.add_input(signal)

    def menu_components_output(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_output()
                self.system_interfaces[index].system.add_output()

    def menu_components_system(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load system", '', "")
            if filename[0]:
                system = System_2.System.static_load(filename[0])
                inputs = 0
                outputs = 0
                for component in system.components:
                    if component.type == 'input':
                        inputs += 1
                    if component.type == 'output':
                        outputs += 1
                self.system_interfaces[index].system_scene.add_component_system(inputs, outputs)
                self.system_interfaces[index].system.add_system(system)

    def menu_components_add(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_add()
                self.system_interfaces[index].system.add_add()

    def menu_components_split(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_split()
                self.system_interfaces[index].system.add_split()

    def menu_components_sum(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_sum()
                self.system_interfaces[index].system.add_sum()

    def menu_components_delay(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_delay()
                self.system_interfaces[index].system.add_delay()

    def menu_components_scale(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                get_const = GUI_system_dialogs.GetCoefficient()
                if get_const.complete:
                    self.system_interfaces[index].system_scene.add_component_scale()
                    self.system_interfaces[index].system.add_scale(get_const.params['coefficient'])

    def menu_connect_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            wiz = GUI_system_dialogs.NewConnector(system_interface=self.system_interfaces[index])
            if wiz.complete:
                a = wiz.params['component_1_id']
                b = wiz.params['component_2_id']
                i = wiz.params['node_1_id']
                j = wiz.params['node_2_id']
                scene = self.system_interfaces[index].system_scene
                node_1 = scene.components[a].out_nodes[i]
                node_2 = scene.components[b].in_nodes[j]
                scene.add_connector(node_1, node_2)
                self.system_interfaces[index].system.add_connector(((a, i), (b, j)))

    def menu_calculate_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            out_signals = System_processing.calculate(system)
            for s, signal in enumerate(out_signals):
                filename = QtWidgets.QFileDialog.getSaveFileName(self, 'save output signal {}'.format(s), '', "")
                if filename[0]:
                    signal.save(filename[0])

    def menu_simulate_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            progress_window = GUI_elements.ProgressDialog('Simulating...', 'Cancel', 0, 100, self)
            out_signals = System_processing.simulate(self.system_interfaces[index].system, update=progress_window)
            for s, signal in enumerate(out_signals):
                filename = QtWidgets.QFileDialog.getSaveFileName(self, 'save output signal {}'.format(s), '', "")
                if filename[0]:
                    signal.save(filename[0])


class SystemInterface(QtWidgets.QWidget):

    def __init__(self, *args, config=None):
        super().__init__(*args)

        self.config = config

        self.system = None

        self.btn_simulate = GUI_elements.MediumButton('Simulate', self)

        self.system_scene = GUI_system_widgets.SystemScene(system_interface=self)
        self.system_view = GUI_system_widgets.SystemView(system_interface=self)
        self.system_view.setScene(self.system_scene)

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
        panel_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.system_view)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def plot_system(self):
        for component in self.system.components:
            if component.type == 'input':
                self.system_scene.add_component_input()
            elif component.type == 'output':
                self.system_scene.add_component_output()
            elif component.type == 'add':
                self.system_scene.add_component_add()
            elif component.type == 'split':
                self.system_scene.add_component_split()
            elif component.type == 'sum':
                self.system_scene.add_component_sum()
            elif component.type == 'delay':
                self.system_scene.add_component_delay()
            elif component.type == 'scale':
                self.system_scene.add_component_scale()
            elif component.type == 'system':
                inputs = len(component.in_nodes)
                outputs = len(component.out_nodes)
                self.system_scene.add_component_system(inputs, outputs)
            else:
                raise TypeError('Unknown component type!')
        for connector in self.system.connectors:
            a = connector[0][0]
            b = connector[1][0]
            i = connector[0][1]
            j = connector[1][1]
            node_1 = self.system_scene.components[a].out_nodes[i]
            node_2 = self.system_scene.components[b].in_nodes[j]
            self.system_scene.add_connector(node_1, node_2)

    def update_info(self):
        if self.system:
            meta_data = ''
            key_string = ''
            value_string = ''
        else:
            # self.system_scene.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')


