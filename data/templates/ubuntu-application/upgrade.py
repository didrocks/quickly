#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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
import shutil
import subprocess
import sys

import internal.apportutils

from internal import quicklyutils
from quickly import commands, configurationhandler, templatetools
import license

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')

options = ["--internal",]

def usage():
    templatetools.print_usage('quickly upgrade')
def help():
    print _("""Tells Quickly that you have manually upgraded your project to
the latest framework.""")

templatetools.handle_additional_parameters(sys.argv, help, usage=usage)

i = 1
internal_run = False
project_version = None
template_version = None
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg.startswith('-'):
        if arg == '--internal':
            internal_run = True
        else:
            cmd = commands.get_command('upgrade', 'ubuntu-application')
            templatetools.usage_error(_("Unknown option: %s."  % arg), cmd=cmd)
    else:
        if project_version is None:
            project_version = arg
        elif template_version is None:
            template_version = arg
    i += 1

(project_version_inspected, template_version_inspected) = templatetools.get_project_and_template_versions("ubuntu-application")
if project_version is None:
    project_version = project_version_inspected
if template_version is None:
    template_version = template_version_inspected

if not configurationhandler.project_config:
    configurationhandler.loadConfig()

project_name = configurationhandler.project_config['project']
python_name = templatetools.python_name(project_name)
project_sentence_name, project_camel_case_name = \
    templatetools.conventional_names(project_name)

substitutions = (("project_name",project_name),
                 ("project_camel_case_name",project_camel_case_name),
                 ("project_sentence_name",project_sentence_name),
                 ("python_name",python_name))

##### 0.4 update
if project_version < '0.4':
    ## new licensing format
    if os.path.isfile("LICENSE"):
        bzr_instance = subprocess.Popen(["bzr", "mv", "LICENSE", "COPYING"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # if file not versionned, try traditional move, (bzr returncode is None if dir not writable)
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
        setup_license = quicklyutils.get_setup_value('license')
    except quicklyutils.cant_deal_with_setup_value:
        setup_license = ''
    try:
        skip = 0
        config_file = '%s/%sconfig.py' % (python_name, python_name)
        fin = file(config_file, 'r')
        fout = file(fin.name + '.new', 'w')
        license_found_in_file = False
        data_file_function_found = False
        for line in fin:
            if skip > 0:
                fout.write(line)
                skip -= 1
                continue
            fields = line.split(' = ') # Separate variable from value
            if fields[0] == '__license__':
                license_found_in_file = True
                continue
            if fields[0] == '__%s_data_directory__' % python_name:
                fout.write(line)
                line = "__license__ = '%s'\n" % setup_license
            if "get_data_file(*path_segments):" in line:
                data_file_function_found = True
                skip = 9
                continue
            if "getdatapath" in line:
                fout.write('''def get_data_file(*path_segments):
    """Get the full path to a data file.

    Returns the path to a file underneath the data directory (as defined by
    `get_data_path`). Equivalent to os.path.join(get_data_path(),
    *path_segments).
    """
    return os.path.join(getdatapath(), *path_segments)

''')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        if not license_found_in_file or not data_file_function_found:
            os.rename(fout.name, fin.name)
        else:
            os.remove(fout.name)
    except (OSError, IOError), e:
        pass
    ## new ~public becomes -public
    try:
        version = quicklyutils.get_setup_value('version')
        if "~public" in version:
            quicklyutils.set_setup_value('version', version.replace("~public", "-public"))
    except quicklyutils.cant_deal_with_setup_value:
        pass

    # add apport hooks if launchpad application is configured
    lp_project_name = configurationhandler.project_config.get('lp_id', None)
    if lp_project_name is not None:
        internal.apportutils.update_apport(project_name, lp_project_name, lp_project_name)

if project_version < '0.4.3':
    ## update dependencies format
    if 'dependencies' in configurationhandler.project_config \
        and not ',' in configurationhandler.project_config['dependencies']:
        dependencies = [elem for elem 
                        in configurationhandler.project_config['dependencies'].split(' ')
                        if elem]
        configurationhandler.project_config['dependencies'] = ", ".join(dependencies)
        configurationhandler.saveConfig()

if project_version < '0.4.4':
    # Use full modelines for all python files
    sedline = "sed -i 's/-\*- coding: utf-8 -\*-/-*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-/'"
    os.system("find . -name '*.py' -exec %s {} \;" % sedline)

### EPOCH CHANGE
### This is where we upgraded the default projects to GTK3, PyGI, and GSettings.
### Warn the user that this happened and they should upgrade manually to fix.
if project_version and project_version < '11.12' and internal_run:
    print _("""WARNING: Your project is out of date.  Newly created projects use
GTK+ 3, PyGI, and GSettings.  See https://wiki.ubuntu.com/Quickly/GTK3 for
porting information and when you have finished porting your code, run
'quickly upgrade' to get rid of this message.""")
    sys.exit(0)

if project_version < '12.08.1':
    sedline = "sed -i '" + \
              "s|^import gettext$|import locale|g;" + \
              "s|^from gettext import |from locale import |g;" + \
              "s|^gettext.textdomain|locale.textdomain|g;" + \
              "'"
    # This find only hits the main module, and that is fine, other files will
    # be updated by normal overwriting mechanism below.
    os.system("find %s -name '*.py' -exec %s {} \;" % (python_name, sedline))

# Overwrite quickly-owned files as necessary
if project_version < template_version:
    print _(
"""Note: This is the first time you have run Quickly since it has been updated.
Quickly will now upgrade its files (bin/*, %s_lib/*, and setup.py).
But first it will save your project.  View Quickly's changes by running:
bzr diff""" % python_name)
    subprocess.call(["bzr", "add", "-q"])
    subprocess.call(["bzr", "commit", "--unchanged", "-q",
                     "-m", "Pre-upgrade checkpoint"])
    templatetools.copy_dirs_from_template(dirs = ['bin', 'python_lib'])
    templatetools.copy_setup_py_from_template()
    try:
        # License new files as needed
        license.licensing()
    except license.LicenceError as e:
        pass  # Don't worry about it, user may not have set it up yet
    subprocess.call(["bzr", "add", "-q"])  # bzr diff will show new files

templatetools.update_version_in_project_file(template_version, 'ubuntu-application')
sys.exit(0)
