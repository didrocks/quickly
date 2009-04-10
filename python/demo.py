import sys
import gtk
from about import About

class demo:
 def __init__(self):
  builder = gtk.Builder()
  builder.add_from_file("../glade/demo.glade")
  self.window = builder.get_object("window")
  builder.connect_signals(self)
    
 def about(self, widget, data=None):
  about = About()
  about.run()

 def on_window_destroy(self, widget, data=None):
  gtk.main_quit()


if __name__ == "__main__":
    d = demo()
    d.window.show()
    gtk.main()

