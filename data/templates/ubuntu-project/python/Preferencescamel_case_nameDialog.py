# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os
import gtk
from couchdb.client import Server
from couchdb.schema import Document

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
        self.__server = Server('http://127.0.0.1:5984/')
        self.__db_name = "project_name"
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
            #TODO: add prefernces to the self.__preferences dict
            self.__preferences = {"record_type":self.__record_type}

            if self.__db_name in self.__server: #check for preferences already stored
                db = self.__server[self.__db_name]
                filt = "function(doc) { if(doc.record_type == '%s') {emit(doc._id, doc); }}" %self.__record_type
                results = db.query(filt)

                if len(results) > 0: #there are preferences saved
                    self.__preferences = results.rows[0].value
                    self.__key = results.rows[0].key
                else: #there are no preferences saved
                    db.create(self.__preferences)

            else:#this is the first run, create db and preferences
                db = self.__server.create(self.__db_name) 
                db.create(self.__preferences)

        return self.__preferences


    def __save_preferences(self):
        db = self.__server[self.__db_name]
        filt = """function(doc) {if(doc.record_type == '%s') { emit(doc._id, doc); }}""" %self.__record_type
        results = db.query(filt)
        document_id = results.rows[0].key
        doc = db[document_id]
        for k, v in self.__preferences.items():
            doc[k] = v
        db[document_id] = doc

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

