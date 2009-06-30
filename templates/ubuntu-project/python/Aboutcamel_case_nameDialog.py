import sys
import gtk

class Aboutcamel_case_nameDialog(gtk.AboutDialog):
    __gtype_name__ = "Aboutcamel_case_nameDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a Aboutcamel_case_nameDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling camel_case_nameWindow.finish_initializing().
    
        Use the convenience function NewAboutcamel_case_nameDialog to create 
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

def NewAboutcamel_case_nameDialog():
    """NewAboutcamel_case_nameDialog - returns a fully instantiated
    Aboutcamel_case_nameDialog object. Use this function rather than
    creating a Aboutcamel_case_nameDialog instance directly.
    
    """
    builder = gtk.Builder()
    builder.add_from_file("../ui/Aboutcamel_case_nameDialog.ui")    
    dialog = builder.get_object("about_project_name_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewAboutcamel_case_nameDialog()
    dialog.show()
    gtk.main()

