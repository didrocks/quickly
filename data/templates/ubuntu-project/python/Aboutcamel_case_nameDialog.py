# -*- coding: utf-8 -*-
# This file is in the public domain

import sys
import os
import gtk

from project_name.project_nameconfig import getdatapath

class Aboutcamel_case_nameDialog(gtk.AboutDialog):
    __gtype_name__ = "Aboutcamel_case_nameDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a Aboutcamel_case_nameDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling Aboutcamel_case_nameDialog.finish_initializing().
    
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

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'Aboutcamel_case_nameDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("about_project_name_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewAboutcamel_case_nameDialog()
    dialog.show()
    gtk.main()

