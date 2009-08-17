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


import os
import stat
import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from quickly import configurationhandler

def help():
    print _("""Usage:
$quickly run

Runs your application. This is the best way to try test it out
while you are developing it. It starts up the main project window.
""")

def shell_completion():
    pass

if sys.argv[1] == "help":
    help()
    sys.exit(0)
elif sys.argv[1] == "shell-completion":
    shell_completion()
    sys.exit(0)

# if config not already loaded
if not configurationhandler.project_config:
    configurationhandler.loadConfig()

project_bin = 'bin/' + configurationhandler.project_config['project']
command_line = [project_bin]
command_line.extend(sys.argv[1:])

# run with args if bin/project exist
st = os.stat(project_bin)
mode = st[stat.ST_MODE]
if mode & stat.S_IEXEC:
    subprocess.call(command_line)
else:
    print _("Can't execute %s") % project_bin
    sys.exit(1)

