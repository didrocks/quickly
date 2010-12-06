#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import pygtk
pygtk.require("2.0")
import gtk
import logging
logging.basicConfig(level=logging.DEBUG)

import os
import sys

proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","project_root"))
sys.path.insert(0, proj_root)

from python.BuilderGlue import Architect
from python.helpers import ui

# Clean up after ourselves
try:
    os.remove(os.path.join(proj_root, 'python', '__init__.pyc'))
except OSError:
    pass
try:
    os.remove(os.path.join(proj_root, 'python', 'BuilderGlue.pyc'))
except OSError:
    pass
try:
    os.remove(os.path.join(proj_root, 'python', 'helpers.pyc'))
except OSError:
    pass
try:
    # if we are imported
    os.remove('%sc' % os.path.abspath(__file__))
except OSError:
    pass

class App(object):       
    def __init__(self):       
        self.builder = builder = Architect(self._default_handler)
        builder.add_from_file("test.ui")
        builder.get_ui(self)
        
        self.window = builder.get_object("window")
        self.builder = builder
        self.window.show()

        # the competition! our connect code must be easier than this
        for w_name in ['up', 'down', 'left', 'right']:
            builder.get_object(w_name).connect('clicked', self.move)

    def on_window_destroy(self, widget, data=None):
        '''convenience signal added to test.ui'''
        gtk.main_quit()

    def _default_handler(self, *args, **kwargs):
        # captures handlers defined in glade but missing from code
        logging.info('%s wants handler: <%s> but using _default_handler instead' % (args[1], args[0]))

    #~ def on_label_show(self, widget, data=None):
        #~ '''boilerplate because test.ui wants this handler'''
        #~ logging.info('on_label_show')

    def window_show_cb(self, widget, data=None):
        logging.info('on_window_show')

    def on_move(self, widget, data=None):
        # this function is connected by glade file, one entry per widget
        logging.info('glade connected: move %s' % self.builder.get_name(widget))

    def move(self, widget, data=None):
        # this function is connected by code in __init__
        logging.info('code connected: move %s' % self.builder.get_name(widget))

    @ui(['up', 'down', 'left', 'right'], 'clicked')
    def move_cb(self, widget, data=None):
        # this function is connected by observing widget signals
        # decorator makes this explicit at a convenient place in code
        logging.info('decorator connected: move %s' % self.builder.get_name(widget))

if __name__ == "__main__":
    app = App()
    gtk.main()
    
