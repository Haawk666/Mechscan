# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
import configparser
import os
import sys
# 3rd party
from PyQt5 import QtWidgets, QtGui, QtCore
# Internals
import GUI
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Check for existence of config file:
    if not os.path.isfile('config.ini'):
        with open('config.ini', 'w') as f:
            f.write(GUI.get_default_settings_string())

    # Import configurations from config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Set theme
    if config.get('GUI', 'Theme') == 'Dark':
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(200, 200, 200))
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(45, 45, 45))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(50, 50, 50))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(200, 200, 200))
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(0, 0, 0))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(200, 200, 200))
        dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(220, 220, 220))
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(dark_palette)
    else:
        pass

    # Start app
    program_session = GUI.MainUI(settings_file=config)
    app.exec_()

