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
import stat
import string
import sys
import re

import gettext
from gettext import gettext as _

class bad_project_name(Exception):
    pass

def handle_additional_parameters(args, help=None, shell_completion=None):
    """Enable handling additional parameter like help of shell_completion"""

    if len(args) > 1 and args[1] == "help":
        if help:
            help()
        else:
            print _("No help for this command")
        sys.exit(0)
    elif len(args) > 1 and args[1] == "shell-completion":
        if shell_completion:
            shell_completion(args[2:])
        sys.exit(0)

def quickly_name(name):
    """Enforce quickly name to be ascii and digit only and lowercase

    return formated name"""
    forbidden_name = ['bin', 'data']
    name = name.strip().lower()
    
    # Some characters that you might like to have in a name, but are not
    # allowed, include '_' and '-'. The underscore is not allowed because
    # it indicates the separation between a Debian package name and its
    # version. The '-' is not allowed in Python module names.
    if not re.match("[a-z0-9]+$", name):
        raise bad_project_name(_("""ERROR: unpermitted character in name.
Letters and digits only."""))

    if name in forbidden_name:
        raise bad_project_name(_('ERROR: %s is not permitted as a quickly project name'))
    return name

def apply_file_rights(src_file_name, dest_file_name):
    """Keep file rights from src to dest"""

    st = os.stat(src_file_name)
    mode = stat.S_IMODE(st.st_mode)
    os.chmod(dest_file_name, mode)

def in_verbose_mode():
    """Return true if verbose mode is on"""

    if os.getenv('QUICKLY') is not None and "verbose" in os.getenv('QUICKLY').lower():
        return True
    return False

