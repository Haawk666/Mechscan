# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
import pandas as pd
# Internals
import GUI_base_widgets
import GUI_model_dialogs
import GUI_model_widgets
from MechSys import Model
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
        new.addAction(GUI_base_widgets.Action('Random Forest', self, trigger_func=self.menu_new_RF_trigger))

        self.menu.addAction(GUI_base_widgets.Action('Save', self, trigger_func=self.menu_save_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Load', self, trigger_func=self.menu_load_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close', self, trigger_func=self.menu_close_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Close all', self, trigger_func=self.menu_close_all_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_base_widgets.Action('Import', self, trigger_func=self.menu_import_trigger))
        self.menu.addAction(GUI_base_widgets.Action('Export', self, trigger_func=self.menu_export_trigger))

        self.menu.addSeparator()

        self.menu.addAction(GUI_base_widgets.Action('Fit', self, trigger_func=self.menu_fit_trigger))

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
        interface.plot_model()
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

    def menu_new_RF_trigger(self):
        wiz = GUI_model_dialogs.GetRandomForestParams()
        if wiz.complete:
            model = Model.RandomForest(wiz.params['estimators'])
            self.add_model(model)

    def menu_save_trigger(self):
        if len(self.model_interfaces) > 0:
            index = self.tabs.currentIndex()
            model_interface = self.model_interfaces[index]
            if model_interface.model:
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save model", '', "")
                if filename[0]:
                    model_interface.model.save(filename[0])
                    self.tabs.setTabText(index, model_interface.model.name())

    def menu_load_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load model", '', "")
        if filename[0]:
            model_interface = ModelInterface(config=self.config)
            model_interface.model = Model.ANN.static_load(filename[0])
            model_interface.plot_model()
            model_interface.update_info()
            self.add_interface(model_interface)

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

    def menu_fit_trigger(self):
        if len(self.model_interfaces) > 0:
            index = self.tabs.currentIndex()
            model_interface = self.model_interfaces[index]
            if model_interface.model:
                wiz = GUI_model_dialogs.SetFit(model=model_interface.model)
                if wiz.complete:
                    X_train = pd.read_csv(wiz.params['train'])
                    target = X_train[wiz.params['target']]
                    X_train.drop([wiz.params['target']], axis=1)
                    X_test = pd.read_csv(wiz.params['test'])
                    model_interface.model.model.fit(X_train, target)
                    prediction = pd.DataFrame()
                    prediction['id'] = X_test['id']
                    prediction['{}_prediction'.format(wiz.params['target'])] = model_interface.model.model.predict(X_test)
                    prediction.to_csv('submission_rf_haakon_test_1.csv', index=False)


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

    def plot_model(self):
        self.model_scene.clear()
        if self.model.type == 'nn':
            for component in self.model.graph.vertices:
                if component.type == 'input':
                    self.model_scene.add_component_input()
                elif component.type == 'output':
                    self.model_scene.add_component_output()
                elif component.type == 'node':
                    self.model_scene.add_component_node()
                else:
                    raise TypeError('Unknown component type!')
                self.model_scene.components[-1].setPos(component.x, component.y)
                self.model_scene.components[-1].setRotation(component.r)
            for connector in self.model.get_arcs():
                i = connector[0]
                j = connector[1]
                node_1 = self.model_scene.components[i]
                node_2 = self.model_scene.components[j]
                self.model_scene.add_connector(node_1, node_2)

    def update_info(self):
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

        else:
            self.model_scene.clear()
            self.lbl_info_keys.setText('')
            self.lbl_info_values.setText('')




