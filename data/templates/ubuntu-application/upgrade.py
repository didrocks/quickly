#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
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

from quickly import templatetools

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')

# get project version and template version if no argument given
if len(sys.argv) < 3:
    (project_version, template_version) = templatetools.get_project_and_template_versions("ubuntu-application")
else:
    project_version = sys.argv[1]
    template_version = sys.argv[2]
#print project_version
#print template_version

# transition to 0.3
#if project_version < 0.3:
# do_stuff
print("updated")
sys.exit(0)
