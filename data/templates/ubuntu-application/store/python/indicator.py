    # -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Code to add AppIndicator."""

import gtk

from python_name.helpers import get_media_file

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

import appindicator
from quickly import templatetools

class Indicator:
    def __init__(self,window):
        self.indicator = appindicator.Indicator('project_name','Messages',appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
 
        #Uncomment and choose an icon for attention state. 
        #self.indicator.set_attention_icon("ICON-NAME")
    
        #Can use self.icon once appindicator python api supports custom icons.
        #self.icon = get_media_file("logo.png")
        self.indicator.set_icon("distributor-logo")
        
        self.menu = gtk.Menu()


        # Add items to Menu and connect signals. 
        # Can access methods from bin/python_name using Window
        
        #Adding preferences button 
        self.preferences = gtk.MenuItem("Preferences")
        #Calls preferences method from the Window class in python_name.py
        self.preferences.connect("activate",window.preferences)
        self.preferences.show()
        self.menu.append(self.preferences)


        self.quit = gtk.MenuItem("Quit")
        self.quit.connect("activate",window.quit)
        self.quit.show()
        self.menu.append(self.quit)

        # Add more items here                           

        self.menu.show()

        self.indicator.set_menu(self.menu)

def new_application_indicator(window):
    ind = Indicator(window)
    return ind.indicator
