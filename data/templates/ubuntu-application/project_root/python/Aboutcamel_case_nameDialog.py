# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from python_name.helpers import make_window

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

class Aboutcamel_case_nameDialog(gtk.AboutDialog):
    __gtype_name__ = "Aboutcamel_case_nameDialog"

    def __init__(self):
        """Construct an Aboutcamel_case_nameDialog.

        This function is typically not called directly. Creation of an
        Aboutcamel_case_nameDialog requires redeading the associated UI file
        and parsing the UI definition externally, and then calling
        Aboutcamel_case_nameDialog.finish_initializing().

        Use the convenience function NewAboutcamel_case_nameDialog to create
        NewAboutcamel_case_nameDialog objects.
        """
        pass

    def finish_initializing(self, builder):
        """Called after we've finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a Aboutcamel_case_nameDialog object with it in order to
        finish initializing the start of the new Aboutcamel_case_nameDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        # Code for other initialization actions should be added here.


def NewAboutcamel_case_nameDialog():
    """Returns a fully instantiated Aboutcamel_case_nameDialog object.

    Use this function rather than creating a Aboutcamel_case_nameDialog
    instance directly.
    """
    return make_window(
        'Aboutcamel_case_nameDialog', "about_python_name_dialog")


if __name__ == "__main__":
    dialog = NewAboutcamel_case_nameDialog()
    dialog.show()
    gtk.main()
