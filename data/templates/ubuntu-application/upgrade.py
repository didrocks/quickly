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
import subprocess
import sys

from internal import quicklyutils
from quickly import configurationhandler, templatetools

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

if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']
python_name = templatetools.python_name(project_name)


##### 0.4 update
# transition to 0.3.1: new licensing format
if project_version < '0.3.1':
    # don't handle error in upgrade (maybe the file doesn't exist)
    bzr_instance = subprocess.Popen(["bzr", "mv", "LICENSE", "COPYING"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # if file not versionned, try traditional move, (bzr returncode is None if dir not writable ??)
    if bzr_instance.returncode == 3 or bzr_instance.returncode is None:
        try:
            os.rename('LICENSE', 'COPYING')
        except OSError, e:
            if e.errno == 13:
                sys.stderr.write(_("Can't rename LICENSE file, check your file permission\n"))
                sys.exit(1)
    # transition Copyright -> AUTHORS
    if os.path.isfile('AUTHORS'):
        source_file = 'AUTHORS'
    else:
        source_file = 'Copyright'
    try:
        fauthor_out = file('AUTHORS.new', 'w')
        for line in file(source_file):
            if '### BEGIN AUTOMATIC LICENSE GENERATION' in line:
                break
            if line.startswith('#'):
                line = line[1:].lstrip()
            fauthor_out.write(line)
        fauthor_out.flush()
        fauthor_out.close()
        os.rename('AUTHORS.new', 'AUTHORS')
        os.remove('Copyright')
    except (OSError, IOError), e:
        pass
    # update config file to add __license__
    try:
        license = quicklyutils.get_setup_value('license')
    except quicklyutils.cant_deal_with_setup_value:
        license = ''
    try:
        config_file = '%s/%sconfig.py' % (python_name, python_name)
        fin = file(config_file, 'r')
        fout = file(fin.name + '.new', 'w')
        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] == '__%s_data_directory__' % python_name:
                fout.write(line)
                line = "__license__ = '%s'\n" % license
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        pass


sys.exit(0)
