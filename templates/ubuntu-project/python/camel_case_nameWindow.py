import sys
import gtk
import Aboutcamel_case_nameDialog
import camel_case_namePreferencesDialog

class camel_case_nameWindow(gtk.Window):
    __gtype_name__ = "camel_case_nameWindow"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation a camel_case_nameWindow requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling camel_case_nameWindow.finish_initializing().
    
        Use the convenience function Newcamel_case_nameWindow to create 
        camel_case_nameWindow object.
    
        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a camel_case_nameWindow object with it in order to finish
        initializing the start of the new camel_case_nameWindow instance.
    
        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here
        #TODO: check if there are preferences to load
        
    def about(self, widget, data=None):
        """about - display the about box for what_the_heck """
        about = Aboutcamel_case_nameDialog.NewAboutcamel_case_nameDialog()
        response = about.run()
        about.hide()
        about.destroy

    def preferences(self, widget, data=None):
        """about - display the preferences window for project_name """
        prefs = camel_case_namePreferencesDialog.Newcamel_case_namePreferencesDialog()
        response = prefs.run()
        if response == gtk.RESPONSE_OK:
            #make any updates based on changed preferences here            
            #TODO: save the preferences
            pass
        prefs.hide()
        prefs.destroy

    def quit(self, widget, data=None):
        """quit - signal handler for closing the camel_case_nameWindow"""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """on_destroy - called when the camel_case_nameWindow is close. """
        #clean up code for saving application state should be added here

        gtk.main_quit()

def Newcamel_case_nameWindow():
    """Newcamel_case_nameWindow - returns a fully instantiated
    camel_case_nameWindow object. Use this function rather than
    creating a camel_case_nameWindow directly.
    
    """
    builder = gtk.Builder()
    builder.add_from_file("../ui/camel_case_nameWindow.ui")    
    window = builder.get_object("project_name_window")
    window.finish_initializing(builder)
    return window

if __name__ == "__main__":
    window = Newcamel_case_nameWindow()
    window.show()
    gtk.main()

