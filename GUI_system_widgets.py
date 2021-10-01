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


class SystemComponent(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args)
        self.component_id = id
        self.scene = scene
        self.in_nodes = []
        self.out_nodes = []
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    def mouseReleaseEvent(self, event):
        self.scene.update_connectors()
        super(QtWidgets.QGraphicsItemGroup, self).mouseReleaseEvent(event)

    def build_component(self):
        pass


class SystemComponentSystem(SystemComponent):

    def __init__(self, *args, scene=None, id=0, inputs=1, outputs=1):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'sys{}'.format(id)
        self.inputs = inputs
        self.outputs = outputs
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        height = max([20, 10 * self.inputs, 10 * self.outputs])

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, height)
        box.setBrush(self.scene.brushes['system_brush'])

        for o in range(self.outputs):

            node = QtWidgets.QGraphicsEllipseItem(17.5, 10 * o + 2.5, 5, 5)
            node.setBrush(self.scene.brushes['node_brush'])
            node.pen().setWidth(0)
            self.out_nodes.append(node)

        for i in range(self.inputs):

            node = QtWidgets.QGraphicsEllipseItem(-2.5, 10 * i + 2.5, 5, 5)
            node.setBrush(self.scene.brushes['node_brush'])
            node.pen().setWidth(0)
            self.in_nodes.append(node)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        for node in self.in_nodes:
            self.addToGroup(node)
        for node in self.out_nodes:
            self.addToGroup(node)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentAdd(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'add{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = QtWidgets.QGraphicsEllipseItem(-2.5, 2.5, 5, 5)
        node_1.setBrush(self.scene.brushes['node_brush'])
        node_1.pen().setWidth(0)
        self.in_nodes.append(node_1)

        node_2 = QtWidgets.QGraphicsEllipseItem(-2.5, 12.5, 5, 5)
        node_2.setBrush(self.scene.brushes['node_brush'])
        node_2.pen().setWidth(0)
        self.in_nodes.append(node_2)

        node_3 = QtWidgets.QGraphicsEllipseItem(17.5, 7.5, 5, 5)
        node_3.setBrush(self.scene.brushes['node_brush'])
        node_3.pen().setWidth(0)
        self.out_nodes.append(node_3)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        self.addToGroup(node_1)
        self.addToGroup(node_2)
        self.addToGroup(node_3)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentSplit(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'splt{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = QtWidgets.QGraphicsEllipseItem(-2.5, 7.5, 5, 5)
        node_1.setBrush(self.scene.brushes['node_brush'])
        node_1.pen().setWidth(0)
        self.in_nodes.append(node_1)

        node_2 = QtWidgets.QGraphicsEllipseItem(17.5, 2.5, 5, 5)
        node_2.setBrush(self.scene.brushes['node_brush'])
        node_2.pen().setWidth(0)
        self.out_nodes.append(node_2)

        node_3 = QtWidgets.QGraphicsEllipseItem(17.5, 12.5, 5, 5)
        node_3.setBrush(self.scene.brushes['node_brush'])
        node_3.pen().setWidth(0)
        self.out_nodes.append(node_3)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        self.addToGroup(node_1)
        self.addToGroup(node_2)
        self.addToGroup(node_3)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentOutput(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'y{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        circle = QtWidgets.QGraphicsEllipseItem(0, 0, 20, 20)
        circle.setBrush(self.scene.brushes['output_brush'])

        node = QtWidgets.QGraphicsEllipseItem(-2.5, 7.5, 5, 5)
        node.setBrush(self.scene.brushes['node_brush'])
        node.pen().setWidth(0)
        self.in_nodes.append(node)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(circle)
        self.addToGroup(node)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentInput(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'x{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

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
        self.out_nodes.append(node)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width())
        label.setY(10 - rect.height() / 2)

        self.addToGroup(triangle)
        self.addToGroup(node)
        self.addToGroup(label)
        self.setZValue(1)


class SystemConnector(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, scene=None, id=0, nodes=None):
        super().__init__(*args)

        self.component_id = id
        self.designation = 'wire{}'.format(id)

        self.scene = scene
        self.nodes = nodes

        self.build_connector()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    def build_connector(self):

        for item in self.childItems():
            self.removeFromGroup(item)

        point_1 = self.nodes[0].sceneBoundingRect().center()
        point_2 = self.nodes[1].sceneBoundingRect().center()
        line = QtWidgets.QGraphicsLineItem(point_1.x(), point_1.y(), point_2.x(), point_2.y())
        line.setPen(self.scene.pens['wire_pen'])

        self.addToGroup(line)
        self.setZValue(0)


class SystemScene(QtWidgets.QGraphicsScene):

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

    def add_component_system(self, inputs, outputs):
        component = SystemComponentSystem(scene=self, id=len(self.components), inputs=inputs, outputs=outputs)
        self.add_component(component)

    def add_component_add(self):
        component = SystemComponentAdd(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_split(self):
        component = SystemComponentSplit(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_output(self):
        component = SystemComponentOutput(scene=self, id=len(self.components))
        self.add_component(component)

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


class SystemView(QtWidgets.QGraphicsView):

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
            self.list.addItem(signal.name())
            self.system_interface.system_scene.add_component_input()
            self.system_interface.system.add_input_signal(signal)
            self.system_interface.update_info()

    def btn_del_trigger(self):
        index = self.list.currentIndex()

    def btn_up_trigger(self):
        pass

    def btn_down_trigger(self):
        pass

    def btn_edit_trigger(self):
        pass


