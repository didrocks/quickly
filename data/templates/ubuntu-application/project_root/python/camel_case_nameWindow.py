# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

import logging
logger = logging.getLogger('python_name')

from python_name_lib import Window
from python_name.Aboutcamel_case_nameDialog import Aboutcamel_case_nameDialog
from python_name.Preferencescamel_case_nameDialog import Preferencescamel_case_nameDialog

# See python_name_lib.Window.py for more details about how this class works
class camel_case_nameWindow(Window):
    __gtype_name__ = "camel_case_nameWindow"
    
    def finish_initializing(self, builder):
        """Set up the main window"""
        super(camel_case_nameWindow, self).finish_initializing(builder)

        self.AboutDialog = Aboutcamel_case_nameDialog
        self.PreferencesDialog = Preferencescamel_case_nameDialog

        # Optional Launchpad integration
        # This shouldn't crash if not found as it is simply used for bug reporting.
        # See https://wiki.ubuntu.com/UbuntuDevelopment/Internationalisation/Coding
        # for more information about Launchpad integration.
        try:
            import LaunchpadIntegration
            LaunchpadIntegration.add_items(self.ui.helpMenu, 1, False, True)
            LaunchpadIntegration.set_sourcepackagename('project_name')
        except:
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
        except:
            pass

        # Code for other initialization actions should be added here.

