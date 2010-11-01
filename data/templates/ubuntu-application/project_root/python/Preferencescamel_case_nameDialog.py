# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""this dialog adjusts values in the preferences dictionary

requirements:
in module preferences: defaults[key] has a value
a widget, named key, created using glade therefore
self.builder.get_object(key) is a suitable widget to adjust value
widget_methods[key] provides method names for the widget
each widget calls set_preference(...) when it has adjusted value
"""

# defined because there are choices for many widget types
# TODO: replace example widget_methods with your values
widget_methods = {
'FileChooserButton (folder)': ['get_filename', 'set_current_folder'],
'folder': ['get_filename', 'set_current_folder'],
'SpinButton (integer)': ['get_value_as_int', 'set_value'],
'example_entry': ['get_text', 'set_text'],
"height": ['get_value', 'set_value'],
"zoom": ['get_active', 'set_active'],
}

import gtk
import logging

from python_name.helpers import get_builder
from python_name.preferences import preferences

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

class Preferencescamel_case_nameDialog(gtk.Dialog):
    __gtype_name__ = "Preferencescamel_case_nameDialog"

    __gsignals__ = {
        "configure-event" : "override"
        }

    def do_configure_event(self, event):
        '''save size and position
        
        when user resizes or moves window'''
        w, h = event.width, event.height
        x, y = event.x, event.y
        preferences['preferences dialog geometry'] = [w, h, x, y]
        gtk.Window.do_configure_event(self, event)

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated Preferencescamel_case_nameDialog object.
        """
        builder = get_builder('Preferencescamel_case_nameDialog')
        new_object = builder.get_object("preferences_python_name_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a Preferencescamel_case_nameDialog object with it in order to
        finish initializing the start of the new Perferencescamel_case_nameDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        # TODO: code for other initialization actions should be added here
        self.set_geometry_from_preferences()
        self.set_widgets_from_preferences()

    def set_geometry_from_preferences(self):
        [w, h, x, y] = preferences.get('preferences dialog geometry', [0, 0, 0, 0])
        if [w, h, x, y] != [0, 0, 0, 0]:
            self.resize(w, h)
            self.move(x, y)

    def set_widgets_from_preferences(self):
        ''' these widgets show values in the preferences dictionary '''
        for key in preferences.keys():
            self.set_widget_from_preference(key)

    def set_widget_from_preference(self, key):
        '''set widget value from item in preferences'''

        value = preferences.get(key)
        widget = self.builder.get_object(key)
        if widget is None:
            # this preference is not adjustable by this dialog
            # for example: window and dialog geometries
            logging.debug('no widget for preference: %s' % key)
            return

        logging.debug('set_widget_from_preference: %s' % key)
        try:
            write_method_name=widget_methods[key][1]
        except KeyError:
            logging.warn('%s not in widget_methods' % key)
            return
    
        method = getattr(widget, write_method_name)
        method(value)

    def get_key_for_widget(self, widget):
        key = None
        for key_try in preferences.keys():
            obj = self.builder.get_object(key_try)
            if obj == widget:
                key = key_try
        return key
 
    def set_preference(self, widget, data=None):
        '''set a preference from a widget'''
        key = self.get_key_for_widget(widget)
        if key is None:
            logging.warn('''This widget will not write to a preference.
The preference must already exist so add this widget's name
to defaults in preferences module''')
            return

        # set_widget_from_preference is called first
        # so no KeyError test is needed here
        read_method_name=widget_methods[key][0]

        read_method = getattr(widget, read_method_name)
        value=read_method()
        logging.debug('set_preference: %s = %s' % (key, str(value)))
        preferences[key] = value

    def on_button_close_clicked(self, widget, data=None):
        self.destroy()

    def on_btn_help_clicked(self, widget, data=None):
        no_help = gtk.MessageDialog(parent=self,
        flags=gtk.DIALOG_MODAL,
        type=gtk.MESSAGE_INFO, 
        buttons=gtk.BUTTONS_CLOSE,
        message_format='No help written yet')
        no_help.run()
        # destroy the help dialog
        no_help.destroy()

if __name__ == "__main__":
    dialog = Preferencescamel_case_nameDialog()
    dialog.show()
    gtk.main()
