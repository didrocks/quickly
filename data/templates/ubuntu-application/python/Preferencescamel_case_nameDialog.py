# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record
import gtk

from python_name.helpers import make_dialog


class Preferencescamel_case_nameDialog(gtk.Dialog):
    __gtype_name__ = "Preferencescamel_case_nameDialog"
    prefernces = {}

    def __init__(self):
        """Construct a Preferencescamel_case_nameDialog.

        This function is typically not called directly. Creation of a
        Preferencescamel_case_nameDialog requires rereading the associated UI
        file and parsing the UI definition extrenally, and then calling
        Preferencescamel_case_nameDialog.finish_initializing().

        Use the convenience function NewPreferencescamel_case_nameDialog to
        create NewAboutcamel_case_nameDialog objects.
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

        # Set up couchdb and the preference info.
        self.__db_name = "project_name"
        self.__database = CouchDatabase(self.__db_name, create=True)
        self.__preferences = None
        self.__key = None

        # Set the record type and then initalize the preferences.
        self.__record_type = (
            "http://wiki.ubuntu.com/Quickly/RecordTypes/camel_case_name/"
            "Preferences")
        self.__preferences = self.get_preferences()
        # TODO: code for other initialization actions should be added here

    def get_preferences(self):
        """Return a dict of preferences for project_name.

        Creates a couchdb record if necessary.
        """
        if self.__preferences == None:
            # The dialog is initializing.
            self.__load_preferences()

        # If there were no saved preference, this.
        return self.__preferences

    def __load_preferences(self):
        # TODO: add prefernces to the self.__preferences dict default
        # preferences that will be overwritten if some are saved
        self.__preferences = {"record_type": self.__record_type}

        results = self.__database.get_records(
            record_type=self.__record_type, create_view=True)

        if len(results.rows) == 0:
            # No preferences have ever been saved, save them before returning.
            self.__key = self.__database.put_record(Record(self.__preferences))
        else:
            self.__preferences = results.rows[0].value
            del self.__preferences['_rev']
            self.__key = results.rows[0].value["_id"]

    def __save_preferences(self):
        self.__database.update_fields(self.__key, self.__preferences)

    def ok(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns gtk.RESONSE_OK from run().
        """

        # Make any updates to self.__preferences here. e.g.
        #self.__preferences["preference1"] = "value2"
        self.__save_preferences()

    def cancel(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        # Restore any changes to self.__preferences here.
        pass


def NewPreferencescamel_case_nameDialog():
    """Returns a fully instantiated Preferencescamel_case_nameDialog object.

    Use this function rather than creating a Preferencescamel_case_nameDialog
    instance directly.
    """
    return make_dialog(
        'Preferencescamel_case_nameDialog',
        "preferences_python_name_dialog")


if __name__ == "__main__":
    dialog = NewPreferencescamel_case_nameDialog()
    dialog.show()
    gtk.main()
