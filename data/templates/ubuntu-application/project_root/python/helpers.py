# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Helpers for an Ubuntu application."""

__all__ = [
    'make_window',
    ]

import os
import gtk

from python_name.python_nameconfig import get_data_file

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

def make_window(builder_file_name, window_name):
    """Return a fully-instantiated window or dialog.

    :param builder_file_name: The name of the builder file, without extension.
        Assumed to be in the 'ui' directory under the data path.
    :param window_name: The name of the window or dialog in the builder file.
    """
    # Look for the ui file that describes the user interface.
    ui_filename = get_data_file('ui', '%s.ui' % (builder_file_name,))
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.set_translation_domain('project_name')
    builder.add_from_file(ui_filename)
    dialog = builder.get_object(window_name)
    dialog.finish_initializing(builder)
    return dialog
