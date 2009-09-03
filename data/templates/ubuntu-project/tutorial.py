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

import os
import sys
import webbrowser

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from quickly import templatetools

def help():
    print _("""Usage:
$ quickly tutorial

Opens a web browser with the tutorial for ubuntu-project template.
""")
templatetools.handle_additional_parameters(sys.argv, help)

webbrowser.open(os.path.dirname(__file__) + "/help/index.html")

sys.exit(0)

