# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
# Internals
import GUI_base_widgets
import GUI_data_dialogs
import GUI_data_widgets
from MechSys import Data, Data_processing
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DatasetsInterface(QtWidgets.QWidget):

    def __init__(self, *args, menu=None, config=None):
        super().__init__(*args)

        self.dataset_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.menu = menu.addMenu('Data')
        self.populate_menu()

        self.config = config

        self.build_layout()

    def populate_menu(self):

        self.menu.addAction(GUI_base_widgets.Action('New', self, trigger_func=self.menu_new_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_base_widgets.Action('Import', self, trigger_func=self.menu_import_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Export', self, trigger_func=self.menu_export_trigger))

        self.menu.addSeparator()

        frames = self.menu.addMenu('Frames')
        frames.addAction(GUI_base_widgets.Action('New', self, trigger_func=self.menu_frames_new_trigger))
        frames.addAction(GUI_base_widgets.Action('Subset', self, trigger_func=self.menu_frames_subset_trigger))
        frames.addAction(GUI_base_widgets.Action('Combine', self, trigger_func=self.menu_frames_combine_trigger))
        frames.addAction(GUI_base_widgets.Action('Delete', self, trigger_func=self.menu_frames_delete_trigger))

        plots = self.menu.addMenu('Plots')
        plots.addAction(GUI_base_widgets.Action('Wizard', self, trigger_func=self.menu_plots_wizard_trigger))

        self.menu.addSeparator()

        methods = self.menu.addMenu('Methods')
        methods.addAction(GUI_base_widgets.Action('PCA', self, trigger_func=self.menu_methods_pca_trigger))

    def build_layout(self):

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def add_interface(self, interface):
        if interface.data:
            self.tabs.addTab(interface, '{}'.format(interface.data.name()))
        else:
            self.tabs.addTab(interface, 'Empty')
        self.dataset_interfaces.append(interface)
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def add_data(self, data):
        interface = DatasetInterface(config=self.config)
        interface.data = data
        interface.update_info()
        self.add_interface(interface)

    def update_config(self, config):

        self.config = config
        for interface in self.dataset_interfaces:
            interface.config = self.config
            interface.update_info()

    def menu_new_trigger(self):
        data_interface = DatasetInterface(config=self.config)
        data_interface.data = Data.Dataset()
        data_interface.update_info()
        self.add_interface(data_interface)

    def menu_save_trigger(self):
        pass

    def menu_load_trigger(self):
        pass

    def menu_close_trigger(self):
        if len(self.tabs) > 0:
            index = self.tabs.currentIndex()
            self.dataset_interfaces.pop(index)
            self.tabs.removeTab(index)

    def menu_close_all_trigger(self):
        self.dataset_interfaces = []
        self.tabs.clear()

    def menu_import_trigger(self):
        if len(self.tabs) > 0:
            index = self.tabs.currentIndex()
            data_interface = self.dataset_interfaces[index]
            if data_interface.data is None:
                self.dataset_interfaces[index].data = Data.Dataset()
        else:
            data_interface = DatasetInterface(config=self.config)
            data_interface.data = Data.Dataset()
            data_interface.update_info()
            self.add_interface(data_interface)

        wizard = GUI_data_dialogs.Import(ui_object=data_interface)
        if wizard.complete:
            if wizard.params['type'] == 'CSV':
                data_interface.data.import_csv(wizard.params['path'])
            else:
                raise NotImplemented('Unknown import type')
            data_interface.update_info()

    def menu_export_trigger(self):
        pass

    def menu_frames_new_trigger(self):
        pass

    def menu_frames_subset_trigger(self):
        pass

    def menu_frames_combine_trigger(self):
        pass

    def menu_frames_delete_trigger(self):
        pass

    def menu_plots_wizard_trigger(self):
        pass

    def menu_methods_pca_trigger(self):
        pass


class DatasetInterface(QtWidgets.QWidget):

    def __init__(self, *args, config=None):
        super().__init__(*args)

        self.config = config

        self.data = None

        self.lbl_info_keys = QtWidgets.QLabel('')
        self.lbl_info_values = QtWidgets.QLabel('')

        self.graphs = QtWidgets.QTabWidget()
        self.graphs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

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
        layout.addWidget(self.graphs)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def plot_data(self):
        pass

    def update_info(self):
        if self.data is not None:
            self.graphs.clear()
            meta_data = self.data.info()
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

            for f, frame in enumerate(self.data.dataframes):
                table = QtWidgets.QTableView()
                table.setModel(GUI_data_widgets.TableModel(frame))
                self.graphs.addTab(table, 'Frame {}'.format(f))
                print(frame.head())
                print(frame.describe())
                print(frame.info())

        else:
            self.graphs.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')




