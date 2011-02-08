# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from python_name_quickly.helpers import get_builder

class BaseAboutcamel_case_nameDialog(gtk.AboutDialog):
    __gtype_name__ = "BaseAboutcamel_case_nameDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated BaseAboutcamel_case_nameDialog object.
        """
        builder = get_builder('Aboutcamel_case_nameDialog')
        new_object = builder.get_object("about_python_name_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a BaseAboutcamel_case_nameDialog object with it in order
        to finish initializing the start of the new Aboutcamel_case_nameDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

