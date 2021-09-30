# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
# Internals
import GUI_elements
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SystemComponentInput(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, scene=None, id=0, brush=QtGui.QBrush(QtGui.QColor(0, 0, 0))):
        super().__init__(*args)

        self.component_id = id
        self.designation = 'x{}'.format(id)
        self.brush = brush

        self.scene = scene

        self.build_component()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)

        triangle = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([
            QtCore.QPointF(0, 0),
            QtCore.QPointF(0, 20),
            QtCore.QPointF(20, 10),
            QtCore.QPointF(0, 0)
        ]))
        triangle.setBrush(self.scene.brushes['input_brush'])

        node = QtWidgets.QGraphicsEllipseItem(17.5, 7.5, 5, 5)
        node.setBrush(self.scene.brushes['node_brush'])
        node.pen().setWidth(0)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width())
        label.setY(10 - rect.height() / 2)

        # box = QtWidgets.QGraphicsRectItem()
        # box.setRect(0, 0, 10, 10)

        self.addToGroup(triangle)
        self.addToGroup(node)
        self.addToGroup(label)
        self.setZValue(1)


class SystemScene(QtWidgets.QGraphicsScene):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.system_interface = system_interface

        self.brushes = {
            'background': QtGui.QBrush(QtGui.QColor(45, 45, 45)),
            'input_brush': QtGui.QBrush(QtGui.QColor(20, 200, 20)),
            'node_brush': QtGui.QBrush(QtGui.QColor(20, 20, 200))
        }
        self.pens = {
            'label_pen': QtGui.QPen(QtGui.QColor(0, 0, 0)).setWidth(1)
        }
        self.fonts = {
            'label_font': QtGui.QFont('Helvetica [Cronyx]', 5)
        }

        self.pens = dict()

        self.setBackgroundBrush(self.brushes['background'])

        self.components = []

    def add_component_input(self):
        component = SystemComponentInput(scene=self, id=len(self.components))
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


class SystemView(QtWidgets.QGraphicsView):
    """An adaptation of QtWidgets.QGraphicsView that supports zooming"""

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)
        self.system_interface = system_interface

    def wheelEvent(self, event):

        modifier = QtWidgets.QApplication.keyboardModifiers()
        if modifier == QtCore.Qt.ControlModifier:

            # Zoom Factor
            zoom_in_factor = 1.25
            zoom_out_factor = 1 / zoom_in_factor

            # Set Anchors
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)

            # Save the scene pos
            oldPos = self.mapToScene(event.pos())

            # Zoom
            if event.angleDelta().y() > 0:
                zoomFactor = zoom_in_factor
            else:
                zoomFactor = zoom_out_factor
            self.scale(zoomFactor, zoomFactor)

            # Get the new position
            newPos = self.mapToScene(event.pos())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

        else:

            super().wheelEvent(event)


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

