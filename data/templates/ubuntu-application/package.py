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

import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from internal import quicklyutils, packaging
from quickly import templatetools, configurationhandler


def help():
    print _("""Usage:
$quickly package

Creates a debian file (deb) from your project. Before running
the package command you can edit the Icon and Category entry of *.desktop.in 
file, where * is the name of your project.

Note that if you didn't run quickly release, quickly share
or quickly change-lp-project you may miss the name, email in
setup.py. You can edit them if you don't want to use any of these
commands afterwards. Those changes are not a mandatory at all for
testing purpose.
""")
templatetools.handle_additional_parameters(sys.argv, help)


# retrieve useful information
if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

try:
    release_version = quicklyutils.get_setup_value('version')
except quicklyutils.cant_deal_with_setup_value:
    print _("Release version not found in setup.py.")


# creation/update debian packaging
if packaging.updatepackaging(no_changelog=True) != 0:
    print _("ERROR: can't create or update ubuntu package")
    sys.exit(1)


# creating local binary package
return_code = packaging.filter_exec_command(["dpkg-buildpackage", "-tc",
                                      "-I.bzr", "-us", "-uc"])

if return_code == 0:
    print _("Ubuntu package has been successfully created in ../%s_%s_all.deb") % (project_name, release_version)
else:
    print _("An error has occurred during package building")

sys.exit(return_code)


