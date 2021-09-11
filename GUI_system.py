# -*- coding: utf-8 -*-

"""Signals and systems"""

# standard library
import logging
import random
# 3rd party
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
# Internals
import GUI_subwidgets
import Signal as ss
import System
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SystemsInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.system_interfaces = []

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition(1))

        self.btn_new = GUI_subwidgets.MediumButton('New', self, trigger_func=self.btn_new_trigger)
        self.btn_save = GUI_subwidgets.MediumButton('Save', self, trigger_func=self.btn_save_trigger)
        self.btn_load = GUI_subwidgets.MediumButton('Load', self, trigger_func=self.btn_load_trigger)
        self.btn_clear = GUI_subwidgets.MediumButton('Close', self, trigger_func=self.btn_clear_trigger)

        self.build_layout()

    def build_layout(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_layout)
        layout.addWidget(GUI_subwidgets.HorSeparator())
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def btn_new_trigger(self):
        system_interface = SystemInterface()
        self.tabs.addTab(system_interface, '{}'.format(system_interface.system.name()))
        self.system_interfaces.append(system_interface)
        system_interface.update_info()
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def btn_save_trigger(self):
        index = self.tabs.currentIndex()
        system_interface = self.system_interfaces[index]
        if system_interface.system:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save system", '', "")
            if filename[0]:
                system_interface.system.save(filename[0])
                self.tabs.setTabText(index, system_interface.system.name())

    def btn_load_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load system", '', "")
        if filename[0]:
            system_interface = SystemInterface()
            system_interface.system = ss.SystemLTI.static_load(filename[0])
            self.system_interfaces.append(system_interface)
            self.tabs.addTab(system_interface, '{}'.format(system_interface.system.name()))
            system_interface.update_info()
            self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def btn_clear_trigger(self):
        index = self.tabs.currentIndex()
        self.system_interfaces.pop(index)
        self.tabs.removeTab(index)


class SystemInterface(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.system = System.SystemLTI()

        self.btn_simulate = GUI_subwidgets.MediumButton('Simulate', self, trigger_func=self.btn_simulate_trigger)
        self.btn_print = GUI_subwidgets.MediumButton('Print', self, trigger_func=self.btn_print_trigger)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor.fromRgbF(0, 0, 0, 1)))
        self.view = QtWidgets.QGraphicsView()
        self.view.setScene(self.scene)

        self.out_graph = pg.PlotWidget()
        self.out_graph.setTitle('Output signals')
        self.out_graph.setLabel('bottom', 'Time t, (s)')
        self.out_graph.setLabel('left', 'Amplitude')
        self.out_graph.showGrid(x=True, y=True)

        self.lst_input = QtWidgets.QListWidget()
        self.lst_input.setStyleSheet('QListWidget{background: black;}')
        self.lst_output = QtWidgets.QListWidget()
        self.lst_output.setStyleSheet('QListWidget{background: black;}')

        self.btn_add_input = GUI_subwidgets.MediumButton('Add', self, trigger_func=self.btn_add_input_trigger)
        self.btn_remove_input = GUI_subwidgets.MediumButton('Del', self, trigger_func=self.btn_remove_input_trigger)
        self.btn_edit_input = GUI_subwidgets.MediumButton('Edit', self, trigger_func=self.btn_edit_input_trigger)

        self.btn_add_output = GUI_subwidgets.MediumButton('Add', self, trigger_func=self.btn_add_output_trigger)
        self.btn_remove_output = GUI_subwidgets.MediumButton('Del', self, trigger_func=self.btn_remove_output_trigger)
        self.btn_edit_output = GUI_subwidgets.MediumButton('Edit', self, trigger_func=self.btn_edit_output_trigger)

        self.build_layout()
        self.update_info()

    def build_layout(self):

        input_btns_layout = QtWidgets.QHBoxLayout()
        input_btns_layout.addWidget(QtWidgets.QLabel('Input: '))
        input_btns_layout.addWidget(self.btn_add_input)
        input_btns_layout.addWidget(self.btn_edit_input)
        input_btns_layout.addWidget(self.btn_remove_input)
        input_btns_layout.addStretch()

        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addLayout(input_btns_layout)
        input_layout.addWidget(self.lst_input)

        input_widget = QtWidgets.QWidget()
        input_widget.setLayout(input_layout)

        output_btns_layout = QtWidgets.QHBoxLayout()
        output_btns_layout.addWidget(QtWidgets.QLabel('Output: '))
        output_btns_layout.addWidget(self.btn_add_output)
        output_btns_layout.addWidget(self.btn_edit_output)
        output_btns_layout.addWidget(self.btn_remove_output)
        output_btns_layout.addStretch()

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addLayout(output_btns_layout)
        output_layout.addWidget(self.lst_output)

        output_widget = QtWidgets.QWidget()
        output_widget.setLayout(output_layout)

        info_layout = QtWidgets.QGridLayout()

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn_simulate)
        btn_layout.addWidget(self.btn_print)
        btn_layout.addStretch()

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addLayout(info_layout)
        panel_layout.addLayout(btn_layout)
        panel_layout.addWidget(self.out_graph)
        panel_layout.addStretch()

        panel_widget = QtWidgets.QWidget()
        panel_widget.setLayout(panel_layout)

        split_1 = QtWidgets.QSplitter(self)
        split_1.setOrientation(QtCore.Qt.Vertical)
        split_2 = QtWidgets.QSplitter(self)
        split_3 = QtWidgets.QSplitter(self)
        split_3.setOrientation(QtCore.Qt.Vertical)

        split_3.addWidget(input_widget)
        split_3.addWidget(output_widget)
        split_2.addWidget(panel_widget)
        split_2.addWidget(split_3)
        split_2.setSizes([950, 10])
        split_1.addWidget(self.view)
        split_1.addWidget(split_2)
        split_1.setSizes([800, 10])

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(split_1)

        self.setLayout(layout)

    def btn_add_input_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            signal = ss.TimeSignal.static_load(filename[0])
            self.lst_input.addItem(signal.name())
            self.system.input_signals.append(signal)

    def btn_remove_input_trigger(self):
        pass

    def btn_edit_input_trigger(self):
        pass

    def btn_add_output_trigger(self):
        pass

    def btn_remove_output_trigger(self):
        pass

    def btn_edit_output_trigger(self):
        pass

    def btn_simulate_trigger(self):
        pass

    def btn_print_trigger(self):
        print(self.system)

    def update_info(self):
        if self.system:
            pass
        else:
            pass










