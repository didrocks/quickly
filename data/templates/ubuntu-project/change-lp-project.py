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

from internal import quicklyutils
from quickly import templatetools

try:
    from quickly import launchpadaccess
except launchpad_connexion_error, e:
    print(e)
    sys.exit(1)


import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')


def help():
    print _("""Usage:
$ quickly change-lp-project

Enable to set or change the launchpad project binded with the current
ubuntu project.
""")
templatetools.handle_additional_parameters(sys.argv, help)


# connect to LP
try:
    launchpad = launchpadaccess.initialize_lpi()
except launchpad_connexion_error, e:
    print(e)
    sys.exit(1)

# set the project
try:
    project = launchpadaccess.link_project(launchpad, "Change your launchpad project")
except launchpadaccess.launchpad_project_error, e:
    print(e)
    sys.exit(1)
# get the project now and save the url into setup.py
quicklyutils.set_setup_value('url', launchpadaccess.launchpad_url + '/' + project.name)

