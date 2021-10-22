# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals
import GUI_base_widgets
import GUI_model_dialogs
from MechSys import Model, Model_processing
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ModelsInterface(QtWidgets.QWidget):

    def __init__(self, *args, menu=None, config=None):
        super().__init__(*args)

        self.model_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.menu = menu.addMenu('Model')
        self.populate_menu()

        self.config = config

        self.build_layout()

    def populate_menu(self):

        new = self.menu.addMenu('New')
        new.addAction(GUI_base_widgets.Action('ANN', self, trigger_func=self.menu_new_ANN_trigger))

        self.menu.addAction(GUI_base_widgets.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_base_widgets.Action('Import', self, trigger_func=self.menu_import_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Export', self, trigger_func=self.menu_export_trigger))

    def build_layout(self):

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def add_interface(self, interface):
        if interface.model:
            self.tabs.addTab(interface, '{}'.format(interface.model.name()))
        else:
            self.tabs.addTab(interface, 'Empty')
        self.model_interfaces.append(interface)
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def add_model(self, model):
        interface = ModelInterface(config=self.config)
        interface.model = model
        interface.update_info()
        self.add_interface(interface)

    def update_config(self, config):

        self.config = config
        for interface in self.model_interfaces:
            interface.config = self.config
            interface.update_info()

    def menu_new_ANN_trigger(self):
        wiz = GUI_model_dialogs.GetANNTopology()
        if wiz.complete:
            model = Model.ANN.from_params(wiz.params)
            self.add_model(model)

    def menu_save_trigger(self):
        pass

    def menu_load_trigger(self):
        pass

    def menu_close_trigger(self):
        if len(self.tabs) > 0:
            index = self.tabs.currentIndex()
            self.model_interfaces.pop(index)
            self.tabs.removeTab(index)

    def menu_close_all_trigger(self):
        self.model_interfaces = []
        self.tabs.clear()

    def menu_import_trigger(self):
        pass

    def menu_export_trigger(self):
        pass


class ModelInterface(QtWidgets.QWidget):

    def __init__(self, *args, config=None):
        super().__init__(*args)

        self.config = config

        self.model = None

        self.lbl_info_keys = QtWidgets.QLabel('')
        self.lbl_info_values = QtWidgets.QLabel('')

        self.model_scene = GUI_model_widgets.ModelScene(model_interface=self)
        self.model_view = GUI_model_widgets.ModelView(model_interface=self)
        self.model_view.setScene(self.model_scene)

        self.build_layout()
        self.update_info()

    def build_layout(self):

        btn_layout = QtWidgets.QVBoxLayout()
        btn_layout.addStretch()

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addLayout(btn_layout)
        info_layout.addWidget(self.lbl_info_keys)
        info_layout.addWidget(self.lbl_info_values)
        info_layout.addStretch()

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addLayout(info_layout)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.model_view)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def plot_signal(self):
        pass

    def update_info(self)
        if self.model:
            meta_data = self.model.info()
            key_string = ''
            value_string = ''
            if not self.config.get('GUI', 'signal_interface_display_signal_details') == 'None':
                for key, value in meta_data.items():
                    if self.config.get('GUI', 'signal_interface_display_signal_details') == 'Some' and key == '':
                        break
                    else:
                        if key == '':
                            key_string += '\n'
                            value_string += '\n'
                        else:
                            key_string += '{}:    \n'.format(key)
                            value_string += '{}\n'.format(value)
            self.lbl_info_keys.setText(key_string)
            self.lbl_info_values.setText(value_string)

            if self.model.type == 'nn':


        else:
            self.graphs.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')




