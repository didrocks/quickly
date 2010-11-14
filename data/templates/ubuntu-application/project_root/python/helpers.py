# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Helpers for an Ubuntu application."""

import os
import gtk

from python_name.python_nameconfig import get_data_file

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

    builder = gtk.Builder()
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
    parser = optparse.OptionParser(version="%prog %ver")
    parser.add_option(
        "-v", "--verbose", action="store_true", dest="verbose",
        help=_("Show debug messages"))
    (options, args) = parser.parse_args()

    # Set the logging level to show debug messages.
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('logging enabled')

def get_help_uri(page=None):
    here = os.path.dirname(__file__)
    trunk_help_path = os.path.abspath(os.path.join(here, '../help'))
    if os.path.exists(trunk_help_path):
        # running in trunk - default language
        help_uri = os.path.join(trunk_help_path, 'C')
    else:
        # running installed - user's language
        help_uri = 'project_name'

    if page is not None:
        help_uri = '%s#%s' % (help_uri, page)

    return help_uri

def show_uri(parent, link):
    # pythonised version of vala code from deja-dup
    screen = parent.get_screen()
    # TODO: hide yelp's asserts
    # stderr = sys.stderr
    # sys.stderr = file('/dev/null')
    gtk.show_uri(screen, link, gtk.gdk.CURRENT_TIME)
    # sys.stderr = stderr
