# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk
from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record

from project_name.project_nameconfig import getdatapath

class Preferencescamel_case_nameDialog(gtk.Dialog):
    __gtype_name__ = "Preferencescamel_case_nameDialog"
    prefernces = {}

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a Preferencescamel_case_nameDialog requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling Preferencescamel_case_nameDialog.finish_initializing().

        Use the convenience function NewPreferencescamel_case_nameDialog to create
        NewAboutcamel_case_nameDialog objects.
        """

        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a Aboutcamel_case_nameDialog object with it in order to finish
        initializing the start of the new Aboutcamel_case_nameDialog instance.
        """

        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #set up couchdb and the preference info
        self.__db_name = "project_name"
        self.__database = CouchDatabase(self.__db_name, create=True)
        self.__preferences = None
        self.__key = None

        #set the record type and then initalize the preferences
        self.__record_type = "http://wiki.ubuntu.com/Quickly/RecordTypes/camel_case_name/Preferences"
        self.__preferences = self.get_preferences()
        #TODO:code for other initialization actions should be added here

    def get_preferences(self):
        """get_preferences  -returns a dictionary object that contain
        preferences for project_name. Creates a couchdb record if
        necessary.
        """

        if self.__preferences == None: #the dialog is initializing
            self.__load_preferences()
            
        #if there were no saved preference, this 
        return self.__preferences

    def __load_preferences(self):
        #TODO: add prefernces to the self.__preferences dict
        #default preferences that will be overwritten if some are saved
        self.__preferences = {"record_type":self.__record_type,
                                "sample_pref":"boo"}
        
        results = self.__database.get_records(record_type=self.__record_type, create_view=True)
       
        if len(results.rows) == 0:
            #no preferences have ever been saved
            #save them before returning
            self.__key = self.__database.put_record(Record(self.__preferences))
        else:
            self.__preferences = results.rows[0].value
            self.__key = results.rows[0].keyy
        
    def __save_preferences(self):
        self.__database.update_fields(self.__key, self.__preferences)

    def ok(self, widget, data=None):
        """ok - The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().
        """

        #make any updates to self.__preferences here
        #self.__preferences["preference1"] = "value2"
        self.__save_preferences()

    def cancel(self, widget, data=None):
        """cancel - The user has elected cancel changes.
        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """

        #restore any changes to self.__preferences here
        pass

def NewPreferencescamel_case_nameDialog():
    """NewPreferencescamel_case_nameDialog - returns a fully instantiated
    Preferencescamel_case_nameDialog object. Use this function rather than
    creating a Preferencescamel_case_nameDialog instance directly.
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'Preferencescamel_case_nameDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    dialog = builder.get_object("preferences_project_name_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewPreferencescamel_case_nameDialog()
    dialog.show()
    gtk.main()

