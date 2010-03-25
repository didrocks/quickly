#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Didier Roche
#
# This file is part of Quickly ubuntu-application template
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

from internal import quicklyutils
from quickly import configurationhandler
from quickly import templatetools

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')


def help():
    print _("""Usage:
$ quickly edit

A convenience command to open all of your python files in your project 
directory in your default editor, ready for editing.

If you put yourself EDITOR or SELECTED_EDITOR environment variable, this latter
will be used. Also, if you configured sensible-editor, this one will be
choosed.
""")
templatetools.handle_additional_parameters(sys.argv, help)

filelist = ""
for root, dirs, files in os.walk('./'):
    for name in files:
        if name.endswith('.py') and name not in ('__init__.py', 'setup.py'):
            filelist += os.path.join(root, name) + ' '

# if config not already loaded
if not configurationhandler.project_config:
    configurationhandler.loadConfig()

# add launcher which does not end with .py
filelist += 'bin/' + configurationhandler.project_config['project']

editor = quicklyutils.get_quickly_editors()
# if editor is still gedit, launch it in background
if editor == "gedit":
    filelist += " &"

os.system("%s %s" % (editor, filelist))
