# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk
import logging

from python_name import (
    Aboutcamel_case_nameDialog, Preferencescamel_case_nameDialog)
import python_name.helpers as helpers
from python_name.preferences import preferences

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')


# This class is meant to be subclassed by camel_case_nameWindow.  It provides
# common functions and some boilerplate.
class Basecamel_case_nameWindow(gtk.Window):
    __gtype_name__ = "Basecamel_case_nameWindow"

    # To construct a new instance of this method, the following notable 
    # methods are called in this order:
    # __new__(cls)
    # __init__(self)
    # finish_initializing(self, builder)
    # __init__(self)
    #
    # For this reason, it's recommended you leave __init__ empty and put
    # your initialization code in finish_initializing
    
    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated Basecamel_case_nameWindow object.
        """
        builder = helpers.get_builder('camel_case_nameWindow')
        new_object = builder.get_object("python_name_window")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initializing should be called after parsing the UI definition
        and creating a camel_case_nameWindow object with it in order to finish
        initializing the start of the new camel_case_nameWindow instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)
        self.preferences_dialog = None

        # Optional Launchpad integration
        # This shouldn't crash if not found as it is simply used for bug reporting.
        # See https://wiki.ubuntu.com/UbuntuDevelopment/Internationalisation/Coding
        # for more information about Launchpad integration.
        try:
            import LaunchpadIntegration
            LaunchpadIntegration.add_items(self.ui.helpMenu, 1, True, True)
            LaunchpadIntegration.set_sourcepackagename('project_name')
        except ImportError:
            pass

        # Optional application indicator support
        # Run 'quickly add indicator' to get started.
        # More information:
        #  http://owaislone.org/quickly-add-indicator/
        #  https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators
        try:
            from python_name import indicator
            # self is passed so methods of this class can be called from indicator.py
            # Comment this next line out to disable appindicator
            self.indicator = indicator.new_application_indicator(self)
        except ImportError:
            pass

    def on_mnu_contents_activate(self, widget, data=None):
        helpers.show_uri(self, "ghelp:%s" % helpers.get_help_uri())

    def on_mnu_about_activate(self, widget, data=None):
        """Display the about box for project_name."""
        about = Aboutcamel_case_nameDialog.Aboutcamel_case_nameDialog()
        response = about.run()
        about.destroy()

    def on_mnu_preferences_activate(self, widget, data=None):
        """Display the preferences window for project_name."""

        """ From the PyGTK Reference manual
           Say for example the preferences dialog is currently open,
           and the user chooses Preferences from the menu a second time;
           use the present() method to move the already-open dialog
           where the user can see it."""
        if self.preferences_dialog is not None:
            logging.debug('show existing preferences_dialog')
            self.preferences_dialog.present()
        else:
            logging.debug('create new preferences_dialog')
            self.preferences_dialog = Preferencescamel_case_nameDialog.Preferencescamel_case_nameDialog()
            self.preferences_dialog.connect('destroy', self.on_preferences_dialog_destroyed)
            self.preferences_dialog.show()
        # destroy command moved into dialog to allow for a help button

    def on_mnu_quit_activate(self, widget, data=None):
        """Signal handler for closing the camel_case_nameWindow."""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """Called when the camel_case_nameWindow is closed."""
        # Clean up code for saving application state should be added here.
        gtk.main_quit()

    def on_preferences_dialog_destroyed(self, widget, data=None):
        '''only affects gui
        
        logically there is no difference between the user closing,
        minimising or ignoring the preferences dialog'''
        logging.debug('on_preferences_dialog_destroyed')
        # to determine whether to create or present preferences_dialog
        self.preferences_dialog = None

if __name__ == "__main__":
    window = Basecamel_case_nameWindow()
    window.show()
    gtk.main()
