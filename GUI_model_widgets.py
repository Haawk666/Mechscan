# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtCore, QtGui
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)





class ModelScene(QtWidgets.QGraphicsScene):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.system_interface = system_interface

        self.brushes = {
            'background': QtGui.QBrush(QtGui.QColor(45, 45, 45)),
            'input_brush': QtGui.QBrush(QtGui.QColor(20, 200, 20)),
            'output_brush': QtGui.QBrush(QtGui.QColor(200, 20, 20)),
            'node_brush': QtGui.QBrush(QtGui.QColor(20, 20, 200)),
            'add_brush': QtGui.QBrush(QtGui.QColor(120, 120, 120)),
            'system_brush': QtGui.QBrush(QtGui.QColor(20, 120, 120))
        }
        self.pens = {
            'label_pen': QtGui.QPen(QtGui.QColor(0, 0, 0), 1),
            'wire_pen': QtGui.QPen(QtGui.QColor(0, 0, 0), 1)
        }
        self.fonts = {
            'label_font': QtGui.QFont('Helvetica [Cronyx]', 5)
        }

        self.setBackgroundBrush(self.brushes['background'])

        self.components = []
        self.connectors = []

    def add_component_output(self):
        component = SystemComponentOutput(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_input(self):
        component = SystemComponentInput(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_function(self):
        component = SystemComponentFunction(scene=self, id=len(self.components))
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

    def add_connector(self, node_1, node_2):
        connector = SystemConnector(scene=self, id=0, nodes=[node_1, node_2])
        self.connectors.append(connector)
        self.addItem(connector)

    def update_connectors(self):
        for connector in self.connectors:
            connector.build_connector()

    def assert_id(self):
        for c, component in enumerate(self.components):
            component.component_id = c

    def keyPressEvent(self, event):
        modifier = QtWidgets.QApplication.keyboardModifiers()
        for component in self.components:
            if component.isSelected():
                if event.key() == QtCore.Qt.Key_R:
                    if modifier == QtCore.Qt.ShiftModifier:
                        component.setRotation(component.rotation() - self.system_interface.config.getfloat('Systems', 'Rotation_increment_(r)'))
                    else:
                        component.setRotation(component.rotation() + self.system_interface.config.getfloat('Systems', 'Rotation_increment_(r)'))
        self.update_connectors()


class ModelView(QtWidgets.QGraphicsView):

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






