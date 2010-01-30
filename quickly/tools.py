# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly
#
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.

#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import stat

import gettext
from gettext import gettext as _

import quicklyconfig
import commands

__project_path = None

class project_path_not_found(Exception):
    pass

class data_path_not_found(Exception):
    def __init__(self, path):
        self.path = path
    def __str__(self):
        return repr(self.path)

class template_path_not_found(Exception):
    pass
class template_not_found(Exception):
    pass

def get_quickly_data_path():
    """Retrieve quickly data path

    This path is by default <quickly_lib_path>/../data/ in trunk
    and /usr/share/quickly in an installed version but this path
    is specified at installation time.
    """

    # get pathname absolute or relative
    if quicklyconfig.__quickly_data_directory__.startswith('/'):
        pathname = quicklyconfig.__quickly_data_directory__
    else:
        pathname = os.path.dirname(__file__) + '/' + quicklyconfig.__quickly_data_directory__
    abs_data_path = os.path.abspath(pathname)

    if os.path.exists(abs_data_path):
        return abs_data_path
    else:
        raise data_path_not_found(abs_data_path)

def get_template_directories():
    """Retrieve all directories where quickly templates are

    :return a list of directories
    """

    # default to looking up templates in the current dir
    invalid_data_path = None
    template_directories = []
    if os.path.exists(os.path.expanduser('~/quickly-templates')):
        template_directories.append(os.path.expanduser('~/quickly-templates'))

    # retrieve from trunk or installed version
    try:
        abs_template_path = get_quickly_data_path() + '/templates/'
        if os.path.exists(abs_template_path):
            template_directories.append(abs_template_path)
    except data_path_not_found, e:
        #TODO: add here some kind of warning log about data path
        invalid_data_path = e

    if not template_directories:
        error_message = None
        if invalid_data_path:
            error_message = _("%s is an invalid data path.\n") % invalid_data_path
        raise template_path_not_found(error_message + _("No template directory found. Aborting"))

    return template_directories


def get_template_directory(template):
    """Detect where the quickly template and if it exists"""

    # check for the first available template in template_directories
    for template_directory in get_template_directories():
        template_path = template_directory + "/" + template
        if os.path.exists(template_path):
            template_found = True
            break
        template_found = False

    # if still false, no template found in template_directories
    if not template_found:
        raise template_not_found(_("ERROR: Template '%s' not found. Aborting")) % template

    return template_path


def get_root_project_path(config_file_path=None):
    """Try to guess where the .quickly config file is.

    config_file_path is optional (needed by the create command, for instance).
    getcwd() is taken by default.
    If nothing found, try to find it up to 6 parent directory

    :return project_path. Raise a project_path_not_found elsewhere.
    """

    global __project_path
    if __project_path:
        return __project_path

    if config_file_path is None:
        current_path = os.getcwd()
    else:
        current_path = config_file_path

    # check for .quickly file until root is found
    while os.path.dirname(current_path) != current_path:
        quickly_file = current_path + "/.quickly"
        if os.path.isfile(quickly_file):
            __project_path = current_path
            return current_path
        current_path = os.path.abspath(os.path.dirname(current_path))
    raise project_path_not_found()

def check_template_exists(template):
    """Check if template exists"""
   
    try: 
        commands.get_all_commands()[template]
    except KeyError:
        print _("ERROR: Template %s does not exist.") % (template)
        print _("Arborting.")
        return False
    return True

