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

# connect to LP
from quickly import launchpadaccess
from internal import quicklyutils

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

def shell_completion():
    pass

if len(sys.argv) > 1 and sys.argv[1] == "help":
    help()
    sys.exit(0)
elif len(sys.argv) > 1 and sys.argv[1] == "shell-completion":
    shell_completion()
    sys.exit(0)

launchpad = launchpadaccess.initialize_lpi()

# set the project
launchpadaccess.link_project(launchpad, "Change your launchpad project")
quicklyutils.set_setup_value('author', launchpad.me.display_name)
quicklyutils.set_setup_value('author_email', launchpad.me.preferred_email_address.email)

# get the project now and save the url into setup.py
project = launchpadaccess.get_project(launchpad)
quicklyutils.set_setup_value('url', launchpadaccess.launchpad_url + '/' + project.name)

