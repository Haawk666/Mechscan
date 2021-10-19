# -*- coding: utf-8 -*-

"""Module docstring"""

# standard library
import logging
# 3rd party
from PyQt5 import QtWidgets
# Internals
import GUI_base_widgets
import GUI_base_dialogs
import GUI_data
import GUI_model
import GUI_signal
import GUI_system
import Library
from MechSys import Signal
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

        self.signals_interface = GUI_signal.SignalsInterface(menu=self.menu, config=self.config)
        self.systems_interface = GUI_system.SystemsInterface(menu=self.menu, config=self.config)
        self.datasets_interface = GUI_data.DatasetsInterface(menu=self.menu, config=self.config)
        self.models_interface = GUI_model.ModelsInterface(menu=self.menu, config=self.config)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.signals_interface, 'Signals')
        self.tabs.addTab(self.systems_interface, 'Systems')
        self.tabs.addTab(self.datasets_interface, 'Data')
        self.tabs.addTab(self.models_interface, 'Models')

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

        app.addAction(GUI_base_widgets.Action('Debug', self, trigger_func=self.menu_debug_trigger))
        app.addSeparator()
        app.addAction(GUI_base_widgets.Action('Settings', self, trigger_func=self.menu_settings_trigger))
        app.addSeparator()
        app.addAction(GUI_base_widgets.Action('Exit', self, trigger_func=self.menu_exit_trigger))

    def build_layout(self):

        self.setCentralWidget(self.tabs)

    def menu_debug_trigger(self):
        signal = Signal.TimeSignal.static_load('Signals/10Hz')

        b_0 = 0.5
        b_1 = 0.8
        b_2 = 1.1
        a_1 = 0.1
        a_2 = 0.4
        calculation = Signal.TimeSignal(
            x_start=signal.x_start,
            x_end=signal.x_end,
            delta_x=signal.delta_x,
            bit_depth=signal.bit_depth,
            codomain=signal.codomain,
            channels=signal.channels,
            units=signal.units
        )
        for k in range(signal.n):
            if k == 0:
                y = b_0 * signal.Y[k, 0]
            elif k == 1:
                y = b_0 * signal.Y[k, 0] + b_1 * signal.Y[k - 1, 0] - a_1 * calculation.Y[k - 1, 0]
            else:
                y = b_0 * signal.Y[k, 0] + b_1 * signal.Y[k - 1, 0] + b_2 * signal.Y[k - 2, 0] - a_1 * calculation.Y[k - 1, 0] - a_2 * calculation.Y[k - 2, 0]
            calculation.Y[k, 0] = y
        calculation.save('Signals/calculation')

    def menu_settings_trigger(self):
        current_settings_map = self.get_current_settings_map()
        wizard = GUI_base_dialogs.SetOptions(settings_map=current_settings_map)
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
        elif type_ == 'float':
            value = self.config.getfloat(*args)
        else:
            value = self.config.get(*args)

        return value

    def set_setting(self, value, section, key, group=''):

        if not group == '':
            group = group + '_'
        args = (section, '{}{}'.format(group, key), str(value))

        self.config.set(*args)

    def get_current_settings_map(self):

        settings_map = Library.get_settings_map()

        for section, items in settings_map.items():
            for item, properties in items.items():
                if properties['type'] == 'group':
                    for item_item, properties_properties in properties['members'].items():
                        settings_map[section][item]['members'][item_item]['current'] = self.get_setting(section, item_item, group=item, type_=properties_properties['type'])
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
