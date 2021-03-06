# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
# Internals
import GUI_system_dialogs
from MechSys import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Node(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, x, y, brush):
        super().__init__(QtGui.QPolygonF([
            QtCore.QPointF(0, 0),
            QtCore.QPointF(0, 5),
            QtCore.QPointF(5, 2.5),
            QtCore.QPointF(0, 0)
        ]))
        self.setPos(QtCore.QPointF(x, y))
        self.setBrush(brush)
        self.pen().setWidth(0)


class SystemComponent(QtWidgets.QGraphicsItemGroup):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args)
        self.designation = 'generic'
        self.component_id = id
        self.scene = scene
        self.in_nodes = []
        self.out_nodes = []
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
        wiz = GUI_system_dialogs.ComponentProperties(sys_component=self.scene.system_interface.system.components[self.component_id], scene_component=self, scene=self.scene)
        if wiz.complete:
            params = wiz.params
            self.designation = params['designation']

    def build_component(self):
        pass


class SystemComponentModel(SystemComponent):

    def __init__(self, *args, scene=None, id=0, inputs=1, outputs=1):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'model{}'.format(id)
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
            node = Node(17.5, 10 * o + 2.5, self.scene.brushes['node_brush'])
            self.out_nodes.append(node)

        for i in range(self.inputs):
            node = Node(-2.5, 10 * i + 2.5, self.scene.brushes['node_brush'])
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
            node = Node(17.5, 10 * o + 2.5, self.scene.brushes['node_brush'])
            self.out_nodes.append(node)

        for i in range(self.inputs):
            node = Node(-2.5, 10 * i + 2.5, self.scene.brushes['node_brush'])
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

        node_1 = Node(-2.5, 2.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(-2.5, 12.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_2)

        node_3 = Node(17.5, 7.5, self.scene.brushes['node_brush'])
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


class SystemComponentAddN(SystemComponent):

    def __init__(self, *args, scene=None, id=0, n=2):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'addn{}'.format(id)
        self.n = n
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        height = max([20, 10 * self.n])

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, height)
        box.setBrush(self.scene.brushes['system_brush'])

        node = Node(17.5, 2.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node)

        for i in range(self.n):
            node = Node(-2.5, 10 * i + 2.5, self.scene.brushes['node_brush'])
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


class SystemComponentMultiply(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'mul{}'.format(id)
        self.build_component()

    def build_component(self):
        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = Node(-2.5, 2.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(-2.5, 12.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_2)

        node_3 = Node(17.5, 7.5, self.scene.brushes['node_brush'])
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


class SystemComponentMultiplyN(SystemComponent):

    def __init__(self, *args, scene=None, id=0, n=2):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'muln{}'.format(id)
        self.n = n
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        height = max([20, 10 * self.n])

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, height)
        box.setBrush(self.scene.brushes['system_brush'])

        node = Node(17.5, 2.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node)

        for i in range(self.n):
            node = Node(-2.5, 10 * i + 2.5, self.scene.brushes['node_brush'])
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

        node_1 = Node(-2.5, 7.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(17.5, 2.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node_2)

        node_3 = Node(17.5, 12.5, self.scene.brushes['node_brush'])
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


class SystemComponentSum(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'sum{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = Node(-2.5, 7.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(17.5, 7.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node_2)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        self.addToGroup(node_1)
        self.addToGroup(node_2)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentDelay(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = '1/z{}'.format(id)
        self.build_component()

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = Node(-2.5, 7.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(17.5, 7.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node_2)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        self.addToGroup(node_1)
        self.addToGroup(node_2)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentGain(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'K{}'.format(id)
        self.build_component()

    def properties(self):
        wiz = GUI_system_dialogs.ComponentProperties(sys_component=self.scene.system_interface.system.components[self.component_id], scene_component=self, scene=self.scene)
        if wiz.complete:
            params = wiz.params
            self.designation = params['designation']
            self.scene.system_interface.system.components[self.component_id].coefficient = params['coefficient']

    def build_component(self):

        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = Node(-2.5, 7.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(17.5, 7.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node_2)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        self.addToGroup(node_1)
        self.addToGroup(node_2)
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

        node = Node(-2.5, 7.5, self.scene.brushes['node_brush'])
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


class SystemComponentFunction(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'f{}'.format(id)
        self.build_component()

    def properties(self):
        wiz = GUI_system_dialogs.ComponentProperties(sys_component=self.scene.system_interface.system.components[self.component_id], scene_component=self, scene=self.scene)
        if wiz.complete:
            params = wiz.params
            self.designation = params['designation']
            self.scene.system_interface.system.components[self.component_id].function_string = params['function_string']

    def build_component(self):
        for item in self.childItems():
            self.removeFromGroup(item)
        self.in_nodes = []
        self.out_nodes = []

        box = QtWidgets.QGraphicsRectItem()
        box.setRect(0, 0, 20, 20)
        box.setBrush(self.scene.brushes['add_brush'])

        node_1 = Node(-2.5, 7.5, self.scene.brushes['node_brush'])
        self.in_nodes.append(node_1)

        node_2 = Node(17.5, 7.5, self.scene.brushes['node_brush'])
        self.out_nodes.append(node_2)

        label = QtWidgets.QGraphicsSimpleTextItem()
        label.setText('{}'.format(self.designation))
        label.setFont(self.scene.fonts['label_font'])
        rect = label.boundingRect()
        label.setX(10 - rect.width() / 2)
        label.setY(10 - rect.height() / 2)

        self.addToGroup(box)
        self.addToGroup(node_1)
        self.addToGroup(node_2)
        self.addToGroup(label)
        self.setZValue(1)


class SystemComponentInput(SystemComponent):

    def __init__(self, *args, scene=None, id=0):
        super().__init__(*args, scene=scene, id=id)
        self.designation = 'x{}'.format(id)
        self.build_component()

    def properties(self):
        wiz = GUI_system_dialogs.ComponentProperties(sys_component=self.scene.system_interface.system.components[self.component_id], scene_component=self, scene=self.scene)
        if wiz.complete:
            params = wiz.params
            self.designation = params['designation']
            self.scene.system_interface.system.components[self.component_id].signal = Signal.TimeSignal.static_load(params['signal_path'])

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

        node = Node(17.5, 7.5, self.scene.brushes['node_brush'])
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

    def add_component_model(self, inputs, outputs):
        component = SystemComponentModel(scene=self, id=len(self.components), inputs=inputs, outputs=outputs)
        self.add_component(component)

    def add_component_system(self, inputs, outputs):
        component = SystemComponentSystem(scene=self, id=len(self.components), inputs=inputs, outputs=outputs)
        self.add_component(component)

    def add_component_add(self):
        component = SystemComponentAdd(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_add_n(self, n):
        component = SystemComponentAddN(scene=self, id=len(self.components), n=n)
        self.add_component(component)

    def add_component_multiply(self):
        component = SystemComponentMultiply(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_multiply_n(self, n):
        component = SystemComponentMultiplyN(scene=self, id=len(self.components), n=n)
        self.add_component(component)

    def add_component_split(self):
        component = SystemComponentSplit(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_sum(self):
        component = SystemComponentSum(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_delay(self):
        component = SystemComponentDelay(scene=self, id=len(self.components))
        self.add_component(component)

    def add_component_gain(self):
        component = SystemComponentGain(scene=self, id=len(self.components))
        self.add_component(component)

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

