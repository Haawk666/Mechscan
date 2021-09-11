# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals

# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SetOptions(QtWidgets.QDialog):

    def __init__(self, *args, settings_map=None):
        super().__init__(*args)

        self.setWindowTitle('Settings')

        self.settings_map = settings_map

        self.complete = False

        self.btn_next = QtWidgets.QPushButton('Apply')
        self.btn_next.clicked.connect(self.btn_next_trigger)
        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.btn_cancel_trigger)

        self.tabs = QtWidgets.QTabWidget()

        self.widgets = dict()

        self.build_layout()
        self.exec_()

    def build_layout(self):

        for section, items in self.settings_map.items():

            self.widgets[section] = dict()

            widget = QtWidgets.QWidget()
            tab_layout = QtWidgets.QVBoxLayout()

            for item, properties in items.items():

                if properties['type'] == 'group':

                    self.widgets[section][item] = dict()

                    group = QtWidgets.QGroupBox(item)
                    group_layout = QtWidgets.QVBoxLayout()

                    for item_item, properties_properties in properties['members'].items():

                        if properties_properties['type'] == 'string':

                            item_widget = QtWidgets.QComboBox()
                            item_widget.addItems(
                                properties_properties['options']
                            )
                            for current_index in range(item_widget.count()):
                                item_widget.setCurrentIndex(current_index)
                                if item_widget.currentText() == properties_properties['current']:
                                    break

                            item_layout = QtWidgets.QHBoxLayout()
                            item_layout.addWidget(QtWidgets.QLabel('{}: '.format(item_item)))
                            item_layout.addWidget(item_widget)

                            self.widgets[section][item][item_item] = item_widget

                            group_layout.addLayout(item_layout)

                        elif properties_properties['type'] == 'bool':

                            item_widget = QtWidgets.QCheckBox(item_item)
                            item_widget.setChecked(properties_properties['current'])

                            self.widgets[section][item][item_item] = item_widget

                            group_layout.addWidget(item_widget)

                        else:

                            raise Exception('Unknown setting type!')

                    group.setLayout(group_layout)
                    tab_layout.addWidget(group)

                else:

                    if properties['type'] == 'string':

                        item_widget = QtWidgets.QComboBox()
                        item_widget.addItems(
                            properties['options']
                        )
                        for current_index in range(item_widget.count()):
                            item_widget.setCurrentIndex(current_index)
                            if item_widget.currentText() == properties['current']:
                                break

                        item_layout = QtWidgets.QHBoxLayout()
                        item_layout.addWidget(QtWidgets.QLabel('{}: '.format(item)))
                        item_layout.addWidget(item_widget)

                        self.widgets[section][item] = item_widget

                        tab_layout.addLayout(item_layout)

                    elif properties['type'] == 'bool':

                        item_widget = QtWidgets.QCheckBox(item)
                        item_widget.setChecked(properties['current'])

                        self.widgets[section][item] = item_widget

                        tab_layout.addWidget(item_widget)

                    else:

                        raise Exception('Unknown setting type!')

            widget.setLayout(tab_layout)
            self.tabs.addTab(widget, section)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def btn_cancel_trigger(self):
        self.close()

    def btn_next_trigger(self):

        for section, items in self.settings_map.items():
            for item, properties in items.items():
                if properties['type'] == 'group':
                    for item_item, properties_properties in properties['members'].items():
                        if properties_properties['type'] == 'string':
                            self.settings_map[section][item]['members'][item_item]['current'] = self.widgets[section][item][item_item].currentText()
                        elif properties_properties['type'] == 'bool':
                            self.settings_map[section][item]['members'][item_item]['current'] = self.widgets[section][item][item_item].isChecked()
                        else:
                            raise Exception('Unknown type!')
                else:
                    if properties['type'] == 'string':
                        self.settings_map[section][item]['current'] = self.widgets[section][item].currentText()
                    elif properties['type'] == 'bool':
                        self.settings_map[section][item]['current'] = self.widgets[section][item].isChecked()
                    else:
                        raise Exception('Unknown type!')

        self.complete = True
        self.close()



