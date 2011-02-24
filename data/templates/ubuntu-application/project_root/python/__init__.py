# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from python_name import camel_case_nameWindow
from python_name_lib import parse_options, preferences

def main():
    'constructor for your class instances'
    # Support for command line options.
    # See python_name_lib.helpers.py to add more.
    parse_options()

    # preferences
    # set some values for our first session
    # TODO: replace defaults with your own values
    default_preferences = {
    'example_entry': 'I remember stuff',
    }
    preferences.update(default_preferences)
    # user's stored preferences are used for 2nd and subsequent sessions
    preferences.db_connect()
    preferences.load()

    # Run the application.    
    window = camel_case_nameWindow.camel_case_nameWindow()
    window.show()
    gtk.main()
    
    preferences.save()
