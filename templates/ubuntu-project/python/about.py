import sys
import gtk

class About:
 def __init__(self):
  builder = gtk.Builder()
  builder.add_from_file("../glade/about.ui")
  self.dialog = builder.get_object("about_dialog")
  builder.connect_signals(self)

 def run(self):
  self.dialog.run()

 def about_close(self, widget, data=None):
  self.dialog.hide()
