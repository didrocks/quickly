import sys
import gtk

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

        #code for other initialization actions should be added here
    def get_preferences(self):
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

