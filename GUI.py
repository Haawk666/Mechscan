# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
# Internals
import GUI_widgets
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MainUI(QtWidgets.QMainWindow):
    """Main GUI. Inherits PyQt5.QtWidgets.QMainWindow."""

    def __init__(self, *args, settings_file=None):
        super().__init__(*args)

        self.config = settings_file

        self.data_interface = GUI_widgets.DataInterface()
        self.model_interface = GUI_widgets.ModelInterface()

        self.central_widget = QtWidgets.QWidget()

        self.build_layout()

        # Generate elements
        self.setWindowTitle('MechScan')
        self.resize(1500, 900)
        self.move(50, 30)
        self.statusBar().showMessage('Ready')

        # Display
        self.show()

        # Intro
        logger.info('Welcome to MechScan by Haakon Tvedt')

    def build_layout(self):

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.data_interface)
        layout.addWidget(self.model_interface)

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)






