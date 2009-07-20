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
$quickly new ubuntu-project path/to/project_name

where "project_name" is one or more words separated by an underscore and
path/to can be any existing path.

This will create and run a new project, including Python code, 
Glade files, and packaging files to make the project work. After
creating the project, get started by:

1. Changing your working directory to the new project:
$cd path/to/project_name

2. Edit the UI with Glade:
$quickly glade

3. Edit the Python code:
$quickly edit

"""

import sys
import os
import shutil
import subprocess

from quickly import tools
from internal import quicklyutils

import gettext
from gettext import gettext as _


# set domain text
gettext.textdomain('quickly')

# get origin path
pathname = os.path.dirname(__file__)
abs_path = os.path.abspath(pathname) + "/"

#workaround for bug #40189 in python-launchpadlib (import new.py file)
if __name__ == "__main__":

    # get the name of the project
    if len(sys.argv)< 2:
        print _("""
    ERROR: project name not defined. Usage is project_name""")
        sys.exit(1)

    path_and_project = sys.argv[1].split('/')
    project_name = path_and_project[-1]

    # check that project name follow quickly rules and reformat it.
    project_name = tools.quickly_name(project_name)

    # create additional directories
    ui_dir = "ui"
    print _("Creating project directory %s") % ui_dir
    os.mkdir(ui_dir)
    print _("Directory %s created\n") % ui_dir

    python_dir = project_name
    print _("Creating project directory %s") % python_dir
    os.mkdir(python_dir)
    print _("Directory %s created\n") % python_dir

    bin_dir = "bin"
    print _("Creating project directory %s") % bin_dir
    os.mkdir(bin_dir)
    print _("Directory %s created\n") % bin_dir

    sentence_name, camel_case_name = quicklyutils.conventional_names(project_name)

    # copy files
    template_ui_dir = abs_path + "ui/"
    target_ui_dir = "ui"

    substitutions = (("project_name",project_name),
                ("camel_case_name",camel_case_name),
                ("sentence_name",sentence_name),)


    # create the files for glade to use
    quicklyutils.file_from_template(template_ui_dir, "camel_case_nameWindow.ui", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "project_name_window.xml", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "Aboutcamel_case_nameDialog.ui", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "about_project_name_dialog.xml", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "Preferencescamel_case_nameDialog.ui", target_ui_dir, substitutions)
    quicklyutils.file_from_template(template_ui_dir, "preferences_project_name_dialog.xml", target_ui_dir, substitutions)

    # create the python directory and files
    template_python_dir = abs_path + "python/"
    target_python_dir = project_name
    quicklyutils.file_from_template(template_python_dir, "Aboutcamel_case_nameDialog.py", target_python_dir, substitutions)
    quicklyutils.file_from_template(template_python_dir, "Preferencescamel_case_nameDialog.py", target_python_dir, substitutions)

    # copy the files needed for packaging
    quicklyutils.file_from_template(abs_path, "internal/setup.py", ".", substitutions)
    quicklyutils.file_from_template(template_python_dir, "__init__.py", target_python_dir)

    # create the data directory, and copy them
    template_data_dir = abs_path + "data/"
    target_data_dir = "data"
    shutil.copytree(template_data_dir,target_data_dir)

    # copy the desktop file
    quicklyutils.file_from_template(abs_path ,"internal/project_name.desktop.in",".", substitutions)

    # copy the executable file, set the mode to executable
    quicklyutils.file_from_template(abs_path ,"internal/project_name","bin", substitutions)
    os.chmod("bin/" + project_name, 0755)

    # add it to revision control
    print _("Creating bzr repository and commiting")
    subprocess.call(["bzr", "init"])
    subprocess.call(["bzr", "add"])
    subprocess.call(["bzr", "commit", "-m", "Initial project creation with Quickly!"])

    # run the new application
    print _("Launching your newly created project!")
    subprocess.call(["./bin/" + project_name])

    # put project name in setup.py
    quicklyutils.set_setup_value('name', project_name)

    print _("Congrats, your new project is setup! cd %s/ to start hacking. Then '$ quickly help' for quickly tutorial and reference") % os.getcwd()

    sys.exit(0)

