# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Helpers for an Ubuntu application."""

import os
import gtk

from python_name.python_nameconfig import get_data_file, __version__
from python_name.Builder import Builder

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


def parse_options():
    """Support for command line options"""
    import logging
    import optparse
    parser = optparse.OptionParser(version="%%prog %s" % __version__)
    parser.add_option(
        "-v", "--verbose", action="store_true", dest="verbose",
        help=_("Show debug messages"))
    (options, args) = parser.parse_args()

    # Set the logging level to show debug messages.
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('logging enabled')

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
