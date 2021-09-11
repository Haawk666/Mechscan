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
import GUI_dialogs
import SignalInterface
import SystemInterface
# Instantiate logger:
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_settings_map():

    settings_map = {
        'GUI': {
            'Theme': {
                'type': 'string',
                'default': 'Dark',
                'options': ['Dark', 'Bright']
            },
            'Tooltips': {
                'type': 'bool',
                'default': True,
            },
            'Signal_interface': {
                'type': 'group',
                'members': {
                    'Display_signal_details': {
                        'type': 'string',
                        'default': 'All',
                        'options': ['All', 'Some', 'None']
                    }
                }
            }
        },
        'Plotting': {
            'Complex-valued_time_signals': {
                'type': 'group',
                'members': {
                    'Plot_real': {
                        'type': 'bool',
                        'default': True,
                    },
                    'Plot_imaginary': {
                        'type': 'bool',
                        'default': True
                    },
                    'Plot_magnitude': {
                        'type': 'bool',
                        'default': False
                    },
                    'Plot_phase': {
                        'type': 'bool',
                        'default': False
                    }
                }
            },
            'Complex-valued_frequency_signals': {
                'type': 'group',
                'members': {
                    'Y-axis': {
                        'type': 'string',
                        'default': 'Magnitude',
                        'options': ['Magnitude', 'Power', 'Decibel']
                    },
                    'Plot_phase': {
                        'type': 'bool',
                        'default': False
                    }
                }
            }
        }
    }

    return settings_map


def get_default_settings_string():

    settings_map = get_settings_map()

    settings_string = ''

    for section, dict_ in settings_map.items():
        settings_string += '[{}]\n'.format(section)
        for key, value in dict_.items():
            if value['type'] == 'group':
                for member, dict__ in value['members'].items():
                    settings_string += '{} = {}\n'.format(key + '_' + member, str(dict__['default']))
            else:
                settings_string += '{} = {}\n'.format(key, str(value['default']))
        settings_string += '\n'

    return settings_string


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
        app.addSeparator()
        app.addAction(GUI_subwidgets.Action('Settings', self, trigger_func=self.menu_settings_trigger))
        app.addSeparator()
        app.addAction(GUI_subwidgets.Action('Exit', self, trigger_func=self.menu_exit_trigger))

    def build_layout(self):

        self.setCentralWidget(self.tabs)

    def menu_debug_trigger(self):
        pass

    def menu_settings_trigger(self):
        current_settings_map = self.get_current_settings_map()
        wizard = GUI_dialogs.SetOptions(settings_map=current_settings_map)
        if wizard.complete:
            self.set_current_settings(wizard.settings_map)
            self.signals_interface.update_config(self.config)

    def menu_exit_trigger(self):
        self.close()

    def get_setting(self, section, key, group='', type_='string'):

        if not group == '':
            group = group + '_'
        args = (section, '{}{}'.format(group, key))

        if type_ == 'string':
            value = self.config.get(*args)
        elif type_ == 'bool':
            value = self.config.getboolean(*args)
        else:
            value = self.config.get(*args)

        return value

    def set_setting(self, value, section, key, group=''):

        if not group == '':
            group = group + '_'
        args = (section, '{}{}'.format(group, key), str(value))

        self.config.set(*args)

    def get_current_settings_map(self):

        settings_map = get_settings_map()

        for section, items in settings_map.items():
            for item, properties in items.items():
                if properties['type'] == 'group':
                    for member, properties_ in properties['members'].items():
                        settings_map[section][item][member]['current'] = self.get_setting(section, member, group=item, type_=properties_['type'])
                else:
                    settings_map[section][item]['current'] = self.get_setting(section, item, type_=properties['type'])

        return settings_map

    def set_current_settings(self, settings_map):

        for section, items in settings_map.items():
            for item, properties in items.items():
                if properties['type'] == 'group':
                    for member, properties_ in properties['members'].items():
                        self.set_setting(properties_['current'], section, member, group=item)
                else:
                    self.set_setting(properties['current'], section, item)

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

