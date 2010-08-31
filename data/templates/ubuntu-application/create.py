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

import sys
import os
import subprocess

from quickly import templatetools
from internal import quicklyutils

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')



def help():
    print _("""Usage:
$ quickly create ubuntu-application path/to/project_name

where "project_name" is one or more words separated by an underscore and
path/to can be any existing path.

This will create and run a new project, including Python code, 
Glade files, and packaging files to make the project work. After
creating the project, get started by:

1. Changing your working directory to the new project:
$ cd path/to/project_name

2. Edit the UI with Glade:
$ quickly design

3. Edit the Python code:
$ quickly edit
""")
templatetools.handle_additional_parameters(sys.argv, help)


# get the name of the project
if len(sys.argv) < 2:
    print _("""Project name not defined.\nUsage is: quickly create ubuntu-application project_name""")
    sys.exit(4)

path_and_project = sys.argv[1].split('/')
project_name = path_and_project[-1]

# check that project name follow quickly rules and reformat it.
try:
    project_name = templatetools.quickly_name(project_name)
except templatetools.bad_project_name, e:
    print(e)
    sys.exit(1)

os.chdir(project_name)

# get origin path
pathname = templatetools.get_template_path_from_project()
abs_path_project_root = os.path.join(pathname, 'project_root')

python_name = templatetools.python_name(project_name)
sentence_name, camel_case_name = quicklyutils.conventional_names(project_name)
substitutions = (("project_name",project_name),
            ("camel_case_name",camel_case_name),
            ("python_name",python_name),
            ("sentence_name",sentence_name),)


for root, dirs, files in os.walk(abs_path_project_root):
    try:
        relative_dir = root.split('project_root/')[1]
    except:
        relative_dir = ""
    # python dir should be replace by python_name (project "pythonified" name)
    if relative_dir.startswith('python'):
        relative_dir = relative_dir.replace('python', python_name)

    for directory in dirs:
        if directory == 'python':
            directory = python_name
        os.mkdir(os.path.join(relative_dir, directory))
    for filename in files:
        quicklyutils.file_from_template(root, filename, relative_dir, substitutions)

# set the mode to executable for executable file 
exec_file = os.path.join('bin', project_name)
try:
    os.chmod(exec_file, 0755)
except:
    pass

# add it to revision control
print _("Creating bzr repository and commiting")
from bzrlib.bzrdir import BzrDir
branch = BzrDir.create_branch_convenience(".")
wt = branch.bzrdir.open_workingtree()
wt.smart_add(["."])
wt.commit("Initial project creation with Quickly!")

# run the new application if X display
if templatetools.is_X_display() and os.path.isfile(exec_file):
    print _("Launching your newly created project!")
    subprocess.call(['./' + project_name], cwd='bin/')

print _("Congrats, your new project is setup! cd %s/ to start hacking.") % os.getcwd()

sys.exit(0)
