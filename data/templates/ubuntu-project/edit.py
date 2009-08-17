#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly ubuntu-project-template
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


import subprocess
import os

from quickly import configurationhandler

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')


def help():
    print _("""Usage:
$quickly edit

A convenience command to open all of your python files in your project 
directory in your default editor, ready for editing.
""")

def shell_completion():
    pass

if len(sys.argv) > 1 and sys.argv[1] == "help":
    help()
    sys.exit(0)
elif len(sys.argv) > 1 and sys.argv[1] == "shell-completion":
    shell_completion()
    sys.exit(0)


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

editor = "gedit"
default_editor = os.environ.get("EDITOR")
if default_editor != None:
 editor = default_editor

subprocess.Popen("%s %s" % (editor, filelist), shell=True)
