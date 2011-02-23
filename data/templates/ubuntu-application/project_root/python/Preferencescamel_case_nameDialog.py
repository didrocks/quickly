# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# This is your preferences dialog.
#
# Define preferences and their defaults in the 'defaults' map below.  These
# definitions are used in the python_name_lib.preferences module to load
# from and save in desktopcouch.  The preference names need to correspond to
# a widget in the Preferencescamel_case_nameDialog.ui file.
#
# Each preference also need to be defined in the 'widget_methods' map below
# to show up in the dialog itself.  Provide three bits of information:
#  1) The first entry is the method on the widget that grabs a string from the
#     widget.
#  2) The second entry is the method on the widget that sets the widget from a
#     string.
#  3) The third entry is a signal the widget will send when the contents should
#     be saved to desktopcouch.
#
# TODO: replace defaults and widget_methods with your own values

defaults = {
    'example_entry': 'I remember stuff',
}

widget_methods = {
    'example_entry': ['get_text', 'set_text', 'changed'],
}

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

from python_name_lib.BasePreferencescamel_case_nameDialog import BasePreferencescamel_case_nameDialog

class Preferencescamel_case_nameDialog(BasePreferencescamel_case_nameDialog):
    __gtype_name__ = "Preferencescamel_case_nameDialog"

    def finish_initializing(self, builder):
        """Set up the preferences dialog"""
        super(Preferencescamel_case_nameDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

