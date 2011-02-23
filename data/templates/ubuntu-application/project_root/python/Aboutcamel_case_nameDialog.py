# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

from python_name_lib.BaseAboutcamel_case_nameDialog import BaseAboutcamel_case_nameDialog

# See BaseAboutcamel_case_nameWindow.py for more details about how this class works.
class Aboutcamel_case_nameDialog(BaseAboutcamel_case_nameDialog):
    __gtype_name__ = "Aboutcamel_case_nameDialog"
    
    def finish_initializing(self, builder):
        """Set up the about dialog"""
        super(Aboutcamel_case_nameDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

