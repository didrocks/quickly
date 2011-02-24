# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# This is your preferences dialog.
#
# Define your preferences dictionary in the __init__.main() function.
# The widget names in the PreferencesTestProjectDialog.ui
# file need to correspond to the keys in the preferences dictionary.
#
# Each preference also need to be defined in the 'widget_methods' map below
# to show up in the dialog itself.  Provide three bits of information:
#  1) The first entry is the method on the widget that grabs a value from the
#     widget.
#  2) The second entry is the method on the widget that sets the widgets value
#      from a stored preference.
#  3) The third entry is a signal the widget will send when the contents have
#     been changed by the user. The preferences dictionary is always up to
# date and will signal the rest of the application about these changes.
# The values will be saved to desktopcouch when the application closes.
#
# TODO: replace widget_methods with your own values


widget_methods = {
    'example_entry': ['get_text', 'set_text', 'changed'],
}

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

from python_name_lib.PreferencesDialog import PreferencesDialog

class Preferencescamel_case_nameDialog(PreferencesDialog):
    __gtype_name__ = "Preferencescamel_case_nameDialog"

    def finish_initializing(self, builder):
        """Set up the preferences dialog"""
        super(Preferencescamel_case_nameDialog, self).finish_initializing(builder)

        # populate the dialog from the preferences dictionary
        # using the methods from widget_methods
        self.widget_methods = widget_methods
        self.set_widgets_from_preferences()

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
