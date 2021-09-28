# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui
# Internals
import Signal
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class InputSignalList(QtWidgets.QGroupBox):

    def __init__(self, *args, system_interface=None):
        super().__init__(*args)

        self.system_interface = system_interface

        self.data_map = []

        self.list = QtWidgets.QListWidget()
        self.btn_add = MediumButton('Add', self, trigger_func=self.btn_add_trigger)
        self.btn_del = MediumButton('Del', self, trigger_func=self.btn_del_trigger)
        self.btn_up = MediumButton('^', self, trigger_func=self.btn_up_trigger)
        self.btn_down = MediumButton('v', self, trigger_func=self.btn_down_trigger)
        self.btn_edit = MediumButton('Edit', self, trigger_func=self.btn_edit_trigger)

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
        self.btn_add = MediumButton('Add', self, trigger_func=self.btn_add_trigger)
        self.btn_del = MediumButton('Del', self, trigger_func=self.btn_del_trigger)
        self.btn_up = MediumButton('^', self, trigger_func=self.btn_up_trigger)
        self.btn_down = MediumButton('v', self, trigger_func=self.btn_down_trigger)
        self.btn_edit = MediumButton('Edit', self, trigger_func=self.btn_edit_trigger)

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


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, *args, minimum=0.0, maximum=100.0, step=1.0, decimals=1, value=50.0):
        super().__init__(*args)

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setSingleStep(step)
        self.setDecimals(decimals)
        self.setValue(value)


class ProgressDialog(QtWidgets.QProgressDialog):

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle('MechScan')
        self.setCancelButton(None)
        self.setMinimumDuration(0)

    def setValue(self, progress: int) -> None:
        super().setValue(progress)
        QtWidgets.QApplication.processEvents()


class Action(QtWidgets.QAction):

    def __init__(self, *args, trigger_func=None):
        super().__init__(*args)

        if trigger_func:
            self.triggered.connect(trigger_func)


class SmallButton(QtWidgets.QPushButton):

    def __init__(self, *args, trigger_func=None):
        super().__init__(*args)

        if trigger_func:
            self.clicked.connect(trigger_func)
        self.setMaximumHeight(20)
        self.setMaximumWidth(50)
        self.setMinimumWidth(50)


class MediumButton(QtWidgets.QPushButton):

    def __init__(self, *args, trigger_func=None):
        super().__init__(*args)

        if trigger_func:
            self.clicked.connect(trigger_func)
        self.setMaximumHeight(20)
        self.setMaximumWidth(100)
        self.setMinimumWidth(100)


class ColorButton(QtWidgets.QWidget):

    def __init__(self, *args, r=0, g=0, b=0, a=255, color_title='color', trigger_func=None):
        super().__init__(*args)

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.color_title = color_title

        self.trigger = trigger_func

        self.preview = ColorPreview(r=self.r, g=self.g, b=self.b, a=self.a)
        self.btn_change_color = MediumButton(self.color_title, self, trigger_func=self.btn_change_color_trigger)

        self.build_layout()

    def build_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.btn_change_color)
        layout.addWidget(self.preview)
        layout.addStretch()
        self.setLayout(layout)

    def btn_change_color_trigger(self):
        color = QtWidgets.QColorDialog.getColor(
            self.rgba_to_q(self.r, self.g, self.b, self.a)
        )
        color = self.q_to_rgba(color)
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.a = color[3]
        self.preview.set_color(r=self.r, g=self.g, b=self.b, a=self.a)
        if self.trigger:
            self.trigger(
                self.r,
                self.g,
                self.b,
                self.a
            )

    @staticmethod
    def q_to_rgba(q_color):
        r = q_color.red()
        g = q_color.green()
        b = q_color.blue()
        a = q_color.alpha()
        return r, g, b, a

    @staticmethod
    def rgba_to_q(r, g, b, a):
        return QtGui.QColor(r, g, b, alpha=a)


class ColorPreview(QtWidgets.QFrame):

    def __init__(self, *args, r=0, g=0, b=0, a=255):
        super().__init__(*args)

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setMaximumWidth(40)
        self.setMinimumWidth(40)
        self.setStyleSheet('background-color: rgb({}, {}, {})'.format(self.r, self.g, self.b))

    def set_color(self, r, g, b, a):

        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.setStyleSheet('background-color: rgb({}, {}, {})'.format(self.r, self.g, self.b))


class HorSeparator(QtWidgets.QFrame):

    def __init__(self, *args):
        super().__init__(*args)

        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class VerSeparator(QtWidgets.QFrame):

    def __init__(self, *args):
        super().__init__(*args)

        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
