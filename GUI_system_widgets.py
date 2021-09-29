# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui
# Internals
import GUI_elements
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SystemComponentInput(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, system_interface=None, id=0, brush=QtGui.QBrush(QtGui.QColor(0, 0, 0))):
        super().__init__(*args)

        self.component_id = id
        self.brush = brush

        self.system_interface = system_interface

        self.build_component()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 10, 10)

        self.addToGroup(box)
        self.setZValue(1)


class SystemScene(QtWidgets.QGraphicsScene):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.system_interface = system_interface

        self.brushes = {
            'background': QtGui.QBrush(QtGui.QColor(45, 45, 45)),
            'input_brush': QtGui.QBrush(QtGui.QColor(0, 0, 0))
        }

        self.pens = dict()

        self.setBackgroundBrush(self.brushes['background'])

        self.components = []

    def add_component_input(self):
        component = SystemComponentInput(system_interface=self.system_interface)
        self.add_component(component)

    def add_component(self, component):
        self.components.append(component)
        self.addItem(component)
        self.assert_id()

    def remove_component(self, component):
        for comp in self.components:
            if comp.component_id == component.component_id:
                self.removeItem(comp)
                self.components.remove(comp)
                break
        self.assert_id()

    def assert_id(self):
        for c, component in enumerate(self.components):
            component.component_id = c


class InputSignalList(QtWidgets.QGroupBox):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.system_interface = system_interface

        self.data_map = []

        self.list = QtWidgets.QListWidget()
        self.btn_add = GUI_elements.MediumButton('Add', self, trigger_func=self.btn_add_trigger)
        self.btn_del = GUI_elements.MediumButton('Del', self, trigger_func=self.btn_del_trigger)
        self.btn_up = GUI_elements.MediumButton('^', self, trigger_func=self.btn_up_trigger)
        self.btn_down = GUI_elements.MediumButton('v', self, trigger_func=self.btn_down_trigger)
        self.btn_edit = GUI_elements.MediumButton('Edit', self, trigger_func=self.btn_edit_trigger)

        self.build_layout()

    def build_layout(self):
        btn_1_layout = QtWidgets.QHBoxLayout()
        btn_1_layout.addWidget(self.btn_add)
        btn_1_layout.addWidget(self.btn_edit)
        btn_1_layout.addWidget(self.btn_del)
        btn_1_layout.addStretch()

        btn_2_layout = QtWidgets.QHBoxLayout()
        btn_2_layout.addWidget(self.btn_up)
        btn_2_layout.addWidget(self.btn_down)
        btn_2_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_1_layout)
        layout.addWidget(self.list)
        layout.addLayout(btn_2_layout)

        self.setLayout(layout)

    def btn_add_trigger(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal", '', "")
        if filename[0]:
            signal = Signal.TimeSignal.static_load(filename[0])
            self.system_interface.system.add_input_signal(signal)
            self.list.addItem(signal.name())
            self.system_interface.system_scene.add_component_input()
            self.system_interface.update_info()

    def btn_del_trigger(self):
        index = self.list.currentIndex()

    def btn_up_trigger(self):
        pass

    def btn_down_trigger(self):
        pass

    def btn_edit_trigger(self):
        pass


class OutputSignalList(QtWidgets.QGroupBox):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.system_interface = system_interface

        self.data_map = []

        self.list = QtWidgets.QListWidget()
        self.btn_add = GUI_elements.MediumButton('Add', self, trigger_func=self.btn_add_trigger)
        self.btn_del = GUI_elements.MediumButton('Del', self, trigger_func=self.btn_del_trigger)
        self.btn_up = GUI_elements.MediumButton('^', self, trigger_func=self.btn_up_trigger)
        self.btn_down = GUI_elements.MediumButton('v', self, trigger_func=self.btn_down_trigger)
        self.btn_edit = GUI_elements.MediumButton('Edit', self, trigger_func=self.btn_edit_trigger)

        self.build_layout()

    def build_layout(self):
        btn_1_layout = QtWidgets.QHBoxLayout()
        btn_1_layout.addWidget(self.btn_add)
        btn_1_layout.addWidget(self.btn_edit)
        btn_1_layout.addWidget(self.btn_del)
        btn_1_layout.addStretch()

        btn_2_layout = QtWidgets.QHBoxLayout()
        btn_2_layout.addWidget(self.btn_up)
        btn_2_layout.addWidget(self.btn_down)
        btn_2_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(btn_1_layout)
        layout.addWidget(self.list)
        layout.addLayout(btn_2_layout)

        self.setLayout(layout)

    def btn_add_trigger(self):
        name = QtWidgets.QInputDialog.getText(self, 'Set name', 'Name')
        if name[1] and not name[0] == '':
            self.list.addItem(str(name[0]))
            self.system_interface.update_info()

    def btn_del_trigger(self):
        pass

    def btn_up_trigger(self):
        pass

    def btn_down_trigger(self):
        pass

    def btn_edit_trigger(self):
        pass

