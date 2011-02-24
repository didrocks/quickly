# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Helpers for an Ubuntu application."""
import logging
import optparse
import os

import gtk

from python_name_lib.python_nameconfig import get_data_file
from python_name_lib.Builder import Builder

import gettext
from gettext import gettext as _
gettext.textdomain('project_name')

def get_builder(builder_file_name):
    """Return a fully-instantiated gtk.Builder instance from specified ui 
    file
    
    :param builder_file_name: The name of the builder file, without extension.
        Assumed to be in the 'ui' directory under the data path.
    """
    # Look for the ui file that describes the user interface.
    ui_filename = get_data_file('ui', '%s.ui' % (builder_file_name,))
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = Builder()
    builder.set_translation_domain('project_name')
    builder.add_from_file(ui_filename)
    return builder


# Owais Lone : To get quick access to icons and stuff.
def get_media_file(media_file_name):
    media_filename = get_data_file('media', '%s' % (media_file_name,))
    if not os.path.exists(media_filename):
        media_filename = None

    return "file:///"+media_filename

def set_up_logging(opts):
    formatter = logging.Formatter("%(levelname)s:%(name)s: %(funcName)s() '%(message)s'")
    logger = logging.getLogger('python_name')
    logger_sh = logging.StreamHandler()
    logger_sh.setFormatter(formatter)
    logger.addHandler(logger_sh)

    # FIXME: 
    # calling desktopcouch.records.server.CouchDatabase()
    # adds a basic handler to lib_logger only !!!!!
    lib_logger = logging.getLogger('python_name_lib')
    #~ lib_logger_sh = logging.StreamHandler()
    #~ lib_logger_sh.setFormatter(formatter)
    #~ lib_logger.addHandler(lib_logger_sh)
    #print lib_logger.handlers

    # Set the logging level to show debug messages.
    if opts.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug('logging enabled')
    if opts.verbose > 1:
        lib_logger.setLevel(logging.DEBUG)

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%prog %ver")
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs python_name_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def get_help_uri(page=None):
    # help_uri from source tree - default language
    here = os.path.dirname(__file__)
    help_uri = os.path.abspath(os.path.join(here, '..', 'help', 'C'))

    if not os.path.exists(help_uri):
        # installed so use gnome help tree - user's language
        help_uri = 'project_name'

    # unspecified page is the index.page
    if page is not None:
        help_uri = '%s#%s' % (help_uri, page)

    return help_uri

def show_uri(parent, link):
    screen = parent.get_screen()
    gtk.show_uri(screen, link, gtk.get_current_event_time())

def alias(alternative_function_name):
    '''see http://www.drdobbs.com/web-development/184406073#l9'''
    def decorator(function):
        '''attach alternative_function_name(s) to function'''
        if not hasattr(function, 'aliases'):
            function.aliases = []
        function.aliases.append(alternative_function_name)
        return function
    return decorator
