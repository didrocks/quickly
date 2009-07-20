# -*- coding: utf-8 -*-
#Copyright 2009 Canonical Ltd.
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
"""
Usage:
$quickly package

Creates a debian file (deb) from your project. Before running
the package command you should:

1. Edit the *.desktop.in file, where * is the name of 
your project.
2. Edit the setup.py file to include your email, name, and
version number for the project.

"""

import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from internal import packaging, quicklyutils
from quickly import configurationhandler

# retreive useful information
if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

try:
    release_version = quicklyutils.get_setup_value('version')
except quicklyutils.cant_deal_with_setup_value:
    print _("Release version not found in setup.py.")


# creation/update debian packaging
if packaging.updatepackaging() != 0:
    print _("ERROR: can't create or update ubuntu package")
    sys.exit(1)


# creating local binary package
return_code = subprocess.call(["debuild", "-tc"])
if return_code == 0:
    print _("Ubuntu package has been successfully created in ../%s_%s_all.deb") % (project_name, release_version)
else:
    print _("An error has occurred during package building")

sys.exit(return_code)


