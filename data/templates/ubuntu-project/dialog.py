#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
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

import os
import sys
import internal.quicklyutils as quicklyutils
from quickly import configurationhandler, templatetools

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')


def help():
    print _("""Usage:
$ quickly dialog dialog_name
where dialog_name is one or more words seperated with underscore

This will create:
1. A subclass of gtk.Dialog called DialogNameDialog in the module DialogNameDialog.py
2. A glade file called DialogNameDialog.ui in the ui directory
3. A catalog file called dialog_name_dialog.xml also in the ui directory

To edit the UI for the dialog, run:
$ quickly glade

To edit the behavior, run:
$ quickly edit

To use the dialog you have to invoke it from another python file:
1. Import the dialog
import DialogNameDialog

2. Create an instance of the dialog
dialog = DialogNameDialog.NewDialogNameDialog()

3. Run the dialog and hide the dialog
result = dialog.run()
dialog.hide()
""")
templatetools.handle_additional_parameters(sys.argv, help)

pathname = os.path.dirname(sys.argv[0])
abs_path = os.path.abspath(pathname)

if len(sys.argv) != 2:
    print _("Dialog command needs to be followed by new dialog name.")
    sys.exit(1)

try:
    dialog_name = templatetools.quickly_name(sys.argv[1])
except templatetools.bad_project_name, e:
    print(e)
    sys.exit(1)

path_and_project = sys.argv[0].split('/')

if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

template_ui_dir = abs_path + "/data/ui/"
template_python_dir = abs_path + "/python/"
target_ui_dir = "data/ui"
target_python_dir = project_name

dialog_sentence_name, dialog_camel_case_name = quicklyutils.conventional_names(dialog_name)
project_sentence_name, project_camel_case_name = quicklyutils.conventional_names(project_name)


substitutions = (("project_name",project_name),
            ("dialog_name",dialog_name),
            ("dialog_camel_case_name",dialog_camel_case_name),
            ("project_camel_case_name",project_camel_case_name),
            ("project_sentence_name",project_sentence_name),
            ("dialog_sentence_name",dialog_sentence_name))

quicklyutils.file_from_template(template_ui_dir, 
                                "dialog_camel_case_nameDialog.ui", 
                                target_ui_dir, 
                                substitutions)

quicklyutils.file_from_template(template_ui_dir, 
                                "dialog_name_dialog.xml", 
                                target_ui_dir,
                                substitutions)

quicklyutils.file_from_template(template_python_dir, 
                                "dialog_camel_case_nameDialog.py", 
                                target_python_dir, 
                                substitutions)

