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
import os
import shutil
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
$ quickly glade

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
abs_path = os.path.abspath(pathname) + "/"

# create additional directories
data_dir = "data"
if os.path.isdir(abs_path + data_dir):
    print _("Creating project directory %s") % data_dir
    os.mkdir(data_dir)

python_name = templatetools.python_name(project_name)
if os.path.isdir(abs_path + python_name):
    print _("Creating project directory %s") % python_name
    os.mkdir(python_name)

bin_dir = "bin"
print _("Creating project directory %s") % bin_dir
os.mkdir(bin_dir)
print _("Directory %s created\n") % bin_dir

sentence_name, camel_case_name = quicklyutils.conventional_names(project_name)

# copy files
template_ui_dir = abs_path + "data/ui/"

substitutions = (("project_name",project_name),
            ("camel_case_name",camel_case_name),
            ("python_name",python_name),
            ("sentence_name",sentence_name),)

if os.path.isdir(template_ui_dir):
    target_ui_dir = "data/ui"
    os.mkdir(target_ui_dir)

    # create the files for glade to use
    quicklyutils.file_from_template(template_ui_dir, "camel_case_nameWindow.ui", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "python_name_window.xml", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "Aboutcamel_case_nameDialog.ui", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "about_python_name_dialog.xml", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "Preferencescamel_case_nameDialog.ui", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "preferences_python_name_dialog.xml", target_ui_dir, substitutions)

# create the python directory and files
template_python_dir = abs_path + "python/"
if os.path.isdir(template_python_dir):
    target_python_dir = python_name
    os.mkdir(target_python_dir)
    quicklyutils.file_from_template(template_python_dir, "Aboutcamel_case_nameDialog.py", target_python_dir, substitutions)
    quicklyutils.file_from_template(template_python_dir, "Preferencescamel_case_nameDialog.py", target_python_dir, substitutions)
    quicklyutils.file_from_template(template_python_dir, "python_nameconfig.py", target_python_dir, substitutions)
    quicklyutils.file_from_template(template_python_dir, 'helpers.py', target_python_dir, substitutions)
    quicklyutils.file_from_template(template_python_dir, "__init__.py", target_python_dir)

# copy the files needed for packaging
quicklyutils.file_from_template(abs_path, "project_root/setup.py", ".", substitutions)

# create the media directory, and copy them
template_media_dir = abs_path + "data/media"
if os.path.isdir(template_media_dir):
    target_media_dir = "data/media"
    shutil.copytree(template_media_dir,target_media_dir)

# copy the desktop file
if os.path.isfile(abs_path + "/project_root/project_name.desktop.in"):
    quicklyutils.file_from_template(abs_path ,"project_root/project_name.desktop.in",".", substitutions)

# copy the executable file, set the mode to executable
quicklyutils.file_from_template(abs_path ,"bin/project_name","bin", substitutions)
os.chmod("bin/" + project_name, 0755)

# copy the author file
quicklyutils.file_from_template(abs_path ,"project_root/AUTHORS",".", substitutions)

# add it to revision control
print _("Creating bzr repository and commiting")
subprocess.call(["bzr", "init"])
subprocess.call(["bzr", "add"])
subprocess.call(["bzr", "commit", "-m", "Initial project creation with Quickly!"])

# run the new application if X display
if templatetools.is_X_display():
    print _("Launching your newly created project!")
    subprocess.call(['./' + project_name], cwd='bin/')

print _("Congrats, your new project is setup! cd %s/ to start hacking.") % os.getcwd()

sys.exit(0)

