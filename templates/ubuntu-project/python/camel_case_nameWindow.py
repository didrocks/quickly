import sys
import gtk
from about import About

class camel_case_nameWindow(gtk.Window):
 __gtype_name__ = "camel_case_nameWindow"
 def __init__(self):
     print '__init__'

 def about(self, widget, data=None):
    about = About()
    about.run()

 def main_quit(self, widget, data=None):
    gtk.main_quit()

 def on_window_destroy(self, widget, data=None):
    gtk.main_quit()

 def _onNew(self, *args):
    print '_onNew', args

def Newcamel_case_nameWindow():
    builder = gtk.Builder()
    builder.add_from_file("../ui/project_name_window.ui")
    
    window = builder.get_object("project_name_window")
    builder.connect_signals(window)
    
    return window

if __name__ == "__main__":
    window = Newcamel_case_nameWindow()
    window.show()
    gtk.main()

