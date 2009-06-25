import sys
import gtk
from couchdb.client import Server
from couchdb.schema import Document

class camel_case_namePreferencesDialog(gtk.Dialog):
    __gtype_name__ = "camel_case_namePreferencesDialog"
    prefernces = {}

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a camel_case_namePreferencesDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling camel_case_namePreferencesDialog.finish_initializing().
    
        Use the convenience function Newcamel_case_namePreferencesDialog to create 
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
        self.server = Server('http://127.0.0.1:5984/')
        self.db_name = "project_name_preferences"
        self.preferences = None
        self.key = None
        self.preferences = self.get_preferences()

        #TODO:code for other initialization actions should be added here

    def get_preferences(self):
        if self.preferences == None: #the dialog is initializing
            if self.db_name in self.server: #check for preferences already stored
                db = self.server[self.db_name]
                filt = """function(doc) { emit(doc._id, doc); }"""
                results = db.query(filt)
                if len(results) > 0:
                    self.preferences = results.rows[0].value
                    self.key = results.rows[0].key

            else:
                db = self.server.create(self.db_name) #this is the first run
                #TODO: set default preferences here
                self.preferences = {"preference1":"value1"} 
                db.create(self.preferences)
        return self.preferences

    def ok(self, widget, data=None):
        """ok - The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().

        """
        #make any updates to self.preferences here
        pass

    def cancel(self, widget, data=None):
        """cancel - The user has elected cancel changes.
        Called before the dialog returns gtk.RESPONSE_CANCEL for run()

        """         
        #restore any changes to self.preferences here
        pass

def Newcamel_case_namePreferencesDialog():
    """NewAboutcamel_case_nameDialog - returns a fully instantiated
    Aboutcamel_case_nameDialog object. Use this function rather than
    creating a Aboutcamel_case_nameDialog instance directly.
    
    """
    builder = gtk.Builder()
    builder.add_from_file("../ui/camel_case_namePreferencesDialog.ui")    
    dialog = builder.get_object("project_name_preferences_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = Newcamel_case_namePreferencesDialog()
    dialog.show()
    gtk.main()

