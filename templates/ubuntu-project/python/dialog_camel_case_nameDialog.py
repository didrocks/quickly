import sys
import gtk

class dialog_camel_case_nameDialog(gtk.Dialog):
    __gtype_name__ = "dialog_camel_case_nameDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a dialog_camel_case_nameDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling dialog_camel_case_nameDialog.finish_initializing().
    
        Use the convenience function Newdialog_camel_case_nameDialog to create 
        a dialog_camel_case_nameDialog object.
    
        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a dialog_camel_case_nameDialog object with it in order to finish
        initializing the start of the new dialog_camel_case_nameDialog instance.
    
        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)


    def ok(self, widget, data=None):
        """ok - The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().

        """
        pass

    def cancel(self, widget, data=None):
        """cancel - The user has elected cancel changes.
        Called before the dialog returns gtk.RESPONSE_CANCEL for run()

        """         
        pass

def Newdialog_camel_case_nameDialog():
    """Newdialog_camel_case_nameDialog - returns a fully instantiated
    dialog-camel_case_nameDialog object. Use this function rather than
    creating dialog_camel_case_nameDialog instance directly.
    
    """
    builder = gtk.Builder()
    builder.add_from_file("../ui/dialog_camel_case_nameDialog.ui")    
    dialog = builder.get_object("dialog_name_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = Newdialog_camel_case_nameDialog()
    dialog.show()
    gtk.main()

