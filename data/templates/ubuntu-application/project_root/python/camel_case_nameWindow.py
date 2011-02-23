# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

from python_name_lib.Window import Window

# See python_name_lib.Window.py for more details about how this class works
class camel_case_nameWindow(Window):
    __gtype_name__ = "camel_case_nameWindow"
    
    def finish_initializing(self, builder):
        """Set up the main window"""
        super(camel_case_nameWindow, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

