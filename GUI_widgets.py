# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
# Internals
import GUI_subwidgets
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

        self.preview = GUI_subwidgets.ColorPreview(r=self.r, g=self.g, b=self.b, a=self.a)
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