# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtCore, QtGui
# Internals
import GUI_model_dialogs
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Component(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args)
        self.designation = 'generic'
        self.component_id = id
        self.scene = scene
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    def mouseReleaseEvent(self, event):
        self.scene.update_connectors()
        super(QtWidgets.QGraphicsItemGroup, self).mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        properties_action = QtWidgets.QAction('Properties', None)
        properties_action.triggered.connect(self.properties)
        menu.addAction(properties_action)
        menu.exec_(event.screenPos())

    def properties(self):
        wiz = GUI_model_dialogs.ComponentProperties(model_component=self.scene.model_interface.model.graph.vertices[self.component_id], scene_component=self, scene=self.scene)
        if wiz.complete:
            params = wiz.params
            self.designation = params['designation']

    def build_component(self):
        pass


class ComponentInput(Component):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'Input{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)

        body = QtWidgets.QGraphicsEllipseItem(0, 0, 20, 20)
        body.setBrush(self.scene.brushes['input_brush'])

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(body)
        self.addToGroup(label)
        self.setZValue(1)


class ComponentOutput(Component):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'Output{}'.format(id)
        self.build_component()

    def build_component(self):
        for item in self.childItems():
            self.removeFromGroup(item)

        body = QtWidgets.QGraphicsEllipseItem(0, 0, 20, 20)
        body.setBrush(self.scene.brushes['output_brush'])

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(body)
        self.addToGroup(label)
        self.setZValue(1)


class ComponentNode(Component):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'Node{}'.format(id)
        self.build_component()

    def build_component(self):
        for item in self.childItems():
            self.removeFromGroup(item)

        body = QtWidgets.QGraphicsEllipseItem(0, 0, 20, 20)
        body.setBrush(self.scene.brushes['node_brush'])

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(body)
        self.addToGroup(label)
        self.setZValue(1)


class ComponentConnector(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, scene=None, id=0, nodes=None):
        super().__init__(*args)

        self.component_id = id
        self.designation = 'wire{}'.format(id)

        self.scene = scene
        self.nodes = nodes

        self.build_connector()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)

    def build_connector(self):

        for item in self.childItems():
            self.removeFromGroup(item)

        point_1 = self.nodes[0].sceneBoundingRect().center()
        point_2 = self.nodes[1].sceneBoundingRect().center()
        line = QtWidgets.QGraphicsLineItem(point_1.x(), point_1.y(), point_2.x(), point_2.y())
        line.setPen(self.scene.pens['wire_pen'])

        self.addToGroup(line)
        self.setZValue(0)


class ModelScene(QtWidgets.QGraphicsScene):

    def __init__(self, *args, model_interface=None):
        super().__init__(*args)

        self.model_interface = model_interface

        self.brushes = {
            'background': QtGui.QBrush(QtGui.QColor(45, 45, 45)),
            'input_brush': QtGui.QBrush(QtGui.QColor(20, 200, 20)),
            'output_brush': QtGui.QBrush(QtGui.QColor(200, 20, 20)),
            'node_brush': QtGui.QBrush(QtGui.QColor(20, 120, 120)),
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
        component = ComponentOutput(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_input(self):
        component = ComponentInput(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_node(self):
        component = ComponentNode(scene=self, id=len(self.components))
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
        connector = ComponentConnector(scene=self, id=0, nodes=[node_1, node_2])
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

    def __init__(self, *args, model_interface=None):
        super().__init__(*args)
        self.model_interface = model_interface

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






