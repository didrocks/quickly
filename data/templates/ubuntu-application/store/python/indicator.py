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
    def __init__(self,Window):
        self.indicator = appindicator.Indicator('project_name','Messages',appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.icon = get_media_file("logo.png")
 
        #Uncomment and choose an icon for attention state. 
        #ind.set_attention_icon("ICON-NAME")
    
        #Can use self.icon once appindicator python api supports custom icons.
        self.indicator.set_icon("distributor-logo")

        self.menu = gtk.Menu()

        # Add items to Menu and connect signals. 
        # Can access methods from bin/python_name using Window
        
        #Adding preferences button 
        preferences = gtk.MenuItem("Preferences")
        #Calls preferences method from the Window class in python_name.py
        preferences.connect("activate",Window.preferences)
        preferences.show()
        self.menu.append(preferences)


        quit = gtk.MenuItem("Quit")
        quit.connect("activate",Window.quit)
        quit.show()
        self.menu.append(quit)

        # Add more items above                           
        self.menu.show()

        self.indicator.set_menu(self.menu)

