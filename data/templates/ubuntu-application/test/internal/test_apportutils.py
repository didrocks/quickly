import unittest

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..","..","..")))

from internal import apportutils

class TestApportUtils(unittest.TestCase):
    def test_lpi_existing(self):
        lines = """#!/usr/bin/python
import sys
import os
import gtk
import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

# optional Launchpad integration
# this shouldn't crash if not found as it is simply used for bug reporting
try:
    import LaunchpadIntegration
    launchpad_available = True
except:
    launchpad_available = False        
        
class camel_case_nameWindow(gtk.Window):
    __gtype_name__ = "camel_case_nameWindow"

    def __init__(self):
        pass

    def finish_initializing(self, builder):
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        if launchpad_available:
            # see https://wiki.ubuntu.com/UbuntuDevelopment/Internationalisation/Coding for more information
            # about LaunchpadIntegration
            LaunchpadIntegration.set_sourcepackagename('project_name')
            LaunchpadIntegration.add_items(self.builder.get_object('helpMenu'), 0, False, True)
            
    def about(self, widget, data=None):
        about = Aboutcamel_case_nameDialog.NewAboutcamel_case_nameDialog()
        response = about.run()
        about.destroy()
""".splitlines()
        self.failIf(apportutils.detect_or_insert_lpi(lines))

    def test_partial_lpi_import_only(self):
        lines = """#!/usr/bin/python
import sys
import os
import gtk
import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

# optional Launchpad integration
# this shouldn't crash if not found as it is simply used for bug reporting
try:
    import LaunchpadIntegration
    launchpad_available = True
except:
    launchpad_available = False        
        
class camel_case_nameWindow(gtk.Window):
    __gtype_name__ = "camel_case_nameWindow"

    def __init__(self):
        pass

    def finish_initializing(self, builder):
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)
            
    def about(self, widget, data=None):
        about = Aboutcamel_case_nameDialog.NewAboutcamel_case_nameDialog()
        response = about.run()
        about.destroy()
""".splitlines()
        self.failIf(apportutils.detect_or_insert_lpi(lines))

    def test_no_lpi(self):
        lines = """#!/usr/bin/python
import sys
import os
import gtk
import gettext
from gettext import gettext as _
gettext.textdomain('project_name')
       
class camel_case_nameWindow(gtk.Window):
    __gtype_name__ = "camel_case_nameWindow"

    def __init__(self):
        pass

    def finish_initializing(self, builder):
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)
            
    def about(self, widget, data=None):
        about = Aboutcamel_case_nameDialog.NewAboutcamel_case_nameDialog()
        response = about.run()
        about.destroy()
""".splitlines()
        expected = """#!/usr/bin/python
import sys
import os
import gtk
import gettext

# optional Launchpad integration
# this shouldn't crash if not found as it is simply used for bug reporting
try:
    import LaunchpadIntegration
    launchpad_available = True
except:
    launchpad_available = False

from gettext import gettext as _
gettext.textdomain('project_name')
       
class camel_case_nameWindow(gtk.Window):
    __gtype_name__ = "camel_case_nameWindow"

    def __init__(self):
        pass

    def finish_initializing(self, builder):
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        if launchpad_available:
            # see https://wiki.ubuntu.com/UbuntuDevelopment/Internationalisation/Coding for more information
            # about LaunchpadIntegration
            LaunchpadIntegration.set_sourcepackagename('project_name')
            LaunchpadIntegration.add_items(self.builder.get_object('helpMenu'), 0, False, True)
            
    def about(self, widget, data=None):
        about = Aboutcamel_case_nameDialog.NewAboutcamel_case_nameDialog()
        response = about.run()
        about.destroy()"""
        self.assertEqual(expected, "\n".join(apportutils.detect_or_insert_lpi(lines)))

unittest.main()