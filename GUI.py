# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import time
# 3rd party
import PyQt5.QtWidgets
from PyQt5 import QtWidgets
# Internals
import GUI_subwidgets
import GUI_widgets
import SignalInterface
import SystemInterface
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MainUI(QtWidgets.QMainWindow):
    """Main GUI. Inherits PyQt5.QtWidgets.QMainWindow."""

    def __init__(self, *args, settings_file=None):
        super().__init__(*args)

        self.config = settings_file

        self.menu = self.menuBar()
        self.menu.setStyleSheet("""
                                    QMenu {
                                        background: black;
                                        border: 1px solid grey;
                                    }
        
                                    QMenu::separator{
                                        height: 1px;
                                        background: grey;
                                        margin-left: 10px;
                                        margin-right: 5px;
                                    }
                                    
                                    QMenu::item:selected{
                                        background-color: rgb(200, 200, 200);
                                        color: rgb(0, 0, 0);
                                    }
                                """)
        self.populate_menu()

        self.signals_interface = SignalInterface.SignalsInterface(menu=self.menu, config=self.config)
        self.systems_interface = SystemInterface.SystemsInterface()
        self.data_interface = GUI_widgets.DataInterface()
        self.model_interface = GUI_widgets.ModelInterface()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.signals_interface, 'Signals')
        self.tabs.addTab(self.systems_interface, 'Systems')
        self.tabs.addTab(self.data_interface, 'Data')
        self.tabs.addTab(self.model_interface, 'Models')

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

    def populate_menu(self):

        app = self.menu.addMenu('App')

        app.addAction(GUI_subwidgets.Action('Debug', self, trigger_func=self.menu_debug_trigger))

    def build_layout(self):

        self.setCentralWidget(self.tabs)

    def menu_debug_trigger(self):
        pass




