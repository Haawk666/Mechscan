# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals
import GUI_base_widgets
import GUI_system_dialogs
import GUI_system_widgets
from MechSys import System_processing, Signal, System
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

        new = self.menu.addMenu('New')
        new.addAction(GUI_base_widgets.Action('Empty', self, trigger_func=self.menu_new_trigger))
        new.addAction(GUI_base_widgets.Action('DLTI', self, trigger_func=self.menu_new_dlti_trigger))

        self.menu.addAction(GUI_base_widgets.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

        self.menu.addSeparator()

        components = self.menu.addMenu('Components')
        components.addAction(GUI_base_widgets.Action('Input', self, trigger_func=self.menu_components_input))
        components.addAction(GUI_base_widgets.Action('Output', self, trigger_func=self.menu_components_output))
        components.addAction(GUI_base_widgets.Action('System', self, trigger_func=self.menu_components_system))
        components.addSeparator()
        components.addAction(GUI_base_widgets.Action('Add', self, trigger_func=self.menu_components_add))
        components.addAction(GUI_base_widgets.Action('Add multiple', self, trigger_func=self.menu_components_addn))
        components.addAction(GUI_base_widgets.Action('Multiply', self, trigger_func=self.menu_components_multiply))
        components.addAction(GUI_base_widgets.Action('Multiply multiple', self, trigger_func=self.menu_components_multiply_multiple))
        components.addAction(GUI_base_widgets.Action('Split', self, trigger_func=self.menu_components_split))
        components.addAction(GUI_base_widgets.Action('Sum', self, trigger_func=self.menu_components_sum))
        components.addAction(GUI_base_widgets.Action('Delay', self, trigger_func=self.menu_components_delay))
        components.addAction(GUI_base_widgets.Action('Gain', self, trigger_func=self.menu_components_gain))
        components.addAction(GUI_base_widgets.Action('Function', self, trigger_func=self.menu_components_function))

        self.menu.addAction(GUI_base_widgets.Action('Connect', self, trigger_func=self.menu_connect_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_base_widgets.Action('Simulate', self, trigger_func=self.menu_simulate_trigger))

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
        system_interface.system = System.System()
        system_interface.update_info()
        self.add_interface(system_interface)

    def menu_new_dlti_trigger(self):
        system_interface = SystemInterface(config=self.config)
        wizard = GUI_system_dialogs.NewDLTISystem()
        if wizard.complete:
            if wizard.params['type'] == 'state_space':
                system_interface.system = System_processing.state_system(
                    wizard.params['A'],
                    wizard.params['B'],
                    wizard.params['C'],
                    wizard.params['D']
                )
            else:
                system_interface.system = System.System()
            system_interface.update_info()
            system_interface.plot_system()
            self.add_interface(system_interface)

    def menu_save_trigger(self):
        if len(self.system_interfaces) > 0:
            index = self.tabs.currentIndex()
            system_interface = self.system_interfaces[index]
            if system_interface.system:
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save signal", '', "")
                if filename[0]:
                    for c, component in enumerate(self.system_interfaces[index].system.components):
                        component.x = system_interface.system_scene.components[c].scenePos().x()
                        component.y = system_interface.system_scene.components[c].scenePos().y()
                        component.r = system_interface.system_scene.components[c].rotation()
                    system_interface.system.save(filename[0])
                    self.tabs.setTabText(index, system_interface.system.name())

    def menu_load_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load system", '', "")
        if filename[0]:
            system_interface = SystemInterface(config=self.config)
            system_interface.system = System.System.static_load(filename[0])
            system_interface.plot_system()
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
                    self.system_interfaces[index].update_info()

    def menu_components_output(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_output()
                self.system_interfaces[index].system.add_output()
                self.system_interfaces[index].update_info()

    def menu_components_system(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load system", '', "")
            if filename[0]:
                system = System.System.static_load(filename[0])
                inputs = 0
                outputs = 0
                for component in system.components:
                    if component.type == 'input':
                        inputs += 1
                    if component.type == 'output':
                        outputs += 1
                self.system_interfaces[index].system_scene.add_component_system(inputs, outputs)
                self.system_interfaces[index].system.add_system(system)
                self.system_interfaces[index].update_info()

    def menu_components_add(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_add()
                self.system_interfaces[index].system.add_add()
                self.system_interfaces[index].update_info()

    def menu_components_addn(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                get_n = GUI_system_dialogs.GetN()
                if get_n.complete:
                    self.system_interfaces[index].system_scene.add_component_add_n(get_n.params['n'])
                    self.system_interfaces[index].system.add_addn(get_n.params['n'])
                    self.system_interfaces[index].update_info()

    def menu_components_multiply(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_multiply()
                self.system_interfaces[index].system.add_multiply()
                self.system_interfaces[index].update_info()

    def menu_components_multiply_multiple(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                get_n = GUI_system_dialogs.GetN()
                if get_n.complete:
                    self.system_interfaces[index].system_scene.add_component_multiply_n(get_n.params['n'])
                    self.system_interfaces[index].system.add_multiplyn(get_n.params['n'])
                    self.system_interfaces[index].update_info()

    def menu_components_split(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_split()
                self.system_interfaces[index].system.add_split()
                self.system_interfaces[index].update_info()

    def menu_components_sum(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_sum()
                self.system_interfaces[index].system.add_sum()
                self.system_interfaces[index].update_info()

    def menu_components_delay(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                self.system_interfaces[index].system_scene.add_component_delay()
                self.system_interfaces[index].system.add_delay()
                self.system_interfaces[index].update_info()

    def menu_components_gain(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                get_const = GUI_system_dialogs.GetCoefficient()
                if get_const.complete:
                    self.system_interfaces[index].system_scene.add_component_gain()
                    self.system_interfaces[index].system.add_gain(get_const.params['coefficient'])
                    self.system_interfaces[index].update_info()

    def menu_components_function(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            system = self.system_interfaces[index].system
            if system is not None:
                get_func = GUI_system_dialogs.GetFunctionString()
                if get_func.complete:
                    self.system_interfaces[index].system_scene.add_component_function()
                    self.system_interfaces[index].system.add_function(get_func.params['function_string'])
                    self.system_interfaces[index].update_info()

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
                self.system_interfaces[index].update_info()

    def menu_simulate_trigger(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            progress_window = GUI_base_widgets.ProgressDialog('Simulating...', 'Cancel', 0, 100, self)
            if len(self.system_interfaces[index].system.get_input_components(get_index=False)) > 0 and len(self.system_interfaces[index].system.get_output_components(get_index=False)):
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

        self.btn_simulate = GUI_base_widgets.MediumButton('Simulate', self)

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

        outer_info_layout = QtWidgets.QVBoxLayout()
        outer_info_layout.addLayout(info_layout)
        outer_info_layout.addStretch()

        panel_layout = QtWidgets.QHBoxLayout()
        panel_layout.addLayout(outer_info_layout)
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
            elif component.type == 'gain':
                self.system_scene.add_component_gain()
            elif component.type == 'system':
                inputs = len(component.in_nodes)
                outputs = len(component.out_nodes)
                self.system_scene.add_component_system(inputs, outputs)
            elif component.type == 'addn':
                n = component.n
                self.system_scene.add_component_add_n(n)
            elif component.type == 'multiply':
                self.system_scene.add_component_multiply()
            elif component.type == 'multiplyn':
                n = component.n
                self.system_scene.add_component_multiply_n(n)
            elif component.type == 'function':
                self.system_scene.add_component_function()
            else:
                raise TypeError('Unknown component type!')
            self.system_scene.components[-1].setPos(component.x, component.y)
            self.system_scene.components[-1].setRotation(component.r)
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
            meta_data = self.system.info()
            key_string = ''
            value_string = ''
            for key, value in meta_data.items():
                key_string += '{}:    \n'.format(key)
                value_string += '{}\n'.format(value)
            self.lbl_info_keys.setText(key_string)
            self.lbl_info_values.setText(value_string)
        else:
            # self.system_scene.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')


