# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from python_name.helpers import make_window


class dialog_camel_case_nameDialog(gtk.Dialog):
    __gtype_name__ = "dialog_camel_case_nameDialog"

    def __init__(self):
        """Construct a dialog_camel_case_nameDialog.

        This function is typically not called directly. Creation of a
        dialog_camel_case_nameDialog requires rereading the associated UI file
        and parsing the UI definition externally, and then calling
        dialog_camel_case_nameDialog.finish_initializing().

        Use the convenience function Newdialog_camel_case_nameDialog to create
        a dialog_camel_case_nameDialog object.
        """
        pass

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a dialog_camel_case_nameDialog object with it in order to
        finish initializing the start of the new dialog_camel_case_nameDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

    def ok(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns gtk.RESONSE_OK from run().
        """
        pass

    def cancel(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        pass


def Newdialog_camel_case_nameDialog():
    """Return a fully instantiated dialog-camel_case_nameDialog object.

    Use this function rather than creating dialog_camel_case_nameDialog
    instance directly.
    """
    return make_window(
        'dialog_camel_case_nameDialog', "dialog_name_dialog")


if __name__ == "__main__":
    dialog = Newdialog_camel_case_nameDialog()
    dialog.show()
    gtk.main()
