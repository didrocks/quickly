# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('jotty')

import os
from gi.repository import GLib # pylint: disable=E0611
from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('jotty')

from jotty_lib import Window
from jotty.AboutJottyDialog import AboutJottyDialog
from jotty.PreferencesJottyDialog import PreferencesJottyDialog

# See jotty_lib.Window.py for more details about how this class works
class JottyWindow(Window):
    __gtype_name__ = "JottyWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JottyWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutJottyDialog
        self.PreferencesDialog = PreferencesJottyDialog

        # Code for other initialization actions should be added here.

    def on_mnu_save_activate(self, widget, data=None):
        #get the title for the note
        title = self.ui.entry1.get_text()

        #get the string
        buff = self.ui.textview1.get_buffer()
        start_iter = buff.get_start_iter()
        end_iter = buff.get_end_iter()
        text = buff.get_text(start_iter, end_iter, True)

        #create the filename
        data_dir = GLib.get_user_data_dir()
        jotty_dir = os.path.join(data_dir, "jotty")
        filename = os.path.join(jotty_dir, title)

        #write the data
        GLib.mkdir_with_parents(jotty_dir, 0o700)
        GLib.file_set_contents(filename, text)

    def on_mnu_open_activate(self, widget, data=None):
        #get the name of the document to open
        title = self.ui.entry1.get_text()
        text = ""

        #create the filename
        data_dir = GLib.get_user_data_dir()
        jotty_dir = os.path.join(data_dir, "jotty")
        filename = os.path.join(jotty_dir, title)

        #try to get the data from the file if it exists
        try:
            success, text = GLib.file_get_contents(filename)
        except Exception:
            text = ""

        #set the UI to display the string
        buff = self.ui.textview1.get_buffer()
        buff.set_text(text)

    def on_mnu_new_activate(self, widget, data=None):
        self.ui.entry1.set_text("Note Title")
        buff = self.ui.textview1.get_buffer()
        buff.set_text("")
