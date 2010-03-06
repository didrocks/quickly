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

import os
import sys
import internal.quicklyutils as quicklyutils
from quickly import configurationhandler, templatetools

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')

argv = sys.argv
options = ('dialog', )

def help():
    print _("""Usage:
$ quickly add [dialog dialog_name]
add something to your project_bin

Here, dialog_name is one or more words seperated with underscore

For instance $ quickly add dialog DialogName will create:
1. A subclass of gtk.Dialog called DialogNameDialog in the module
   DialogNameDialog.py
2. A glade file called DialogNameDialog.ui in the ui directory
3. A catalog file called dialog_name_dialog.xml also in the ui directory

To edit the UI for the dialog, run:
$ quickly design

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
def shell_completion(argv):
    ''' Complete args '''
    # option completion
    if len(argv) == 1:
        print " ".join([option for option in options
                        if option.startswith(sys.argv[-1])])
templatetools.handle_additional_parameters(sys.argv, help, shell_completion)

abs_template_path = templatetools.get_template_path_from_project()
abs_command_path = os.path.abspath(os.path.dirname(sys.argv[0]))


if len(sys.argv) < 2:
    print _("add command needs to be followed an action name.\n"
"Usage is: quickly add [dialog|] …")
    sys.exit(4)

if argv[1] == "dialog":
    if len(argv) != 3:
        print(_('''Usage is: $ quickly add dialog <dialogname>'''))
        sys.exit(4)
    else:
        try:
            dialog_name = templatetools.quickly_name(argv[2])
        except templatetools.bad_project_name, e:
            print(e)
            sys.exit(1)

        path_and_project = sys.argv[0].split('/')

        if not configurationhandler.project_config:
            configurationhandler.loadConfig()
        project_name = configurationhandler.project_config['project']

        template_ui_dir = os.path.join(abs_template_path, 'store', 'data', 'ui')
        template_python_dir = os.path.join(abs_template_path, 'store', 'python')
        # take files from command directory if don't exist
        origin_ui_file_list = [os.path.join(template_ui_dir,
                                            'dialog_camel_case_nameDialog.ui'),
                               os.path.join(template_ui_dir,
                                            'dialog_python_name_dialog.xml')]
        python_file = os.path.join(template_ui_dir,
                                   'dialog_camel_case_nameDialog.py')
        if len([file_exist for file_exist in origin_ui_file_list if
                os.path.isfile(file_exist)]) != len(origin_ui_file_list):
            template_ui_dir = os.path.join(abs_command_path, 'store', 'data',
                                           'ui')
        if not os.path.isfile(python_file):
            template_python_dir = os.path.join(abs_command_path, 'store',
                                               'python')

        target_ui_dir = os.path.join('data', 'ui')
        python_name = templatetools.python_name(project_name)
        target_python_dir = python_name

        dialog_python_name = templatetools.python_name(dialog_name)
        dialog_sentence_name, dialog_camel_case_name = \
            quicklyutils.conventional_names(dialog_name)
        project_sentence_name, project_camel_case_name = \
            quicklyutils.conventional_names(project_name)

        substitutions = (("project_name",project_name),
                    ("dialog_name",dialog_name),
                    ("dialog_python_name",dialog_python_name),
                    ("dialog_camel_case_name",dialog_camel_case_name),
                    ("project_camel_case_name",project_camel_case_name),
                    ("project_sentence_name",project_sentence_name),
                    ("dialog_sentence_name",dialog_sentence_name),
                    ("python_name",python_name))

        quicklyutils.file_from_template(template_ui_dir, 
                                        "dialog_camel_case_nameDialog.ui", 
                                        target_ui_dir, 
                                        substitutions)

        quicklyutils.file_from_template(template_ui_dir, 
                                        "dialog_python_name_dialog.xml", 
                                        target_ui_dir,
                                        substitutions)

        quicklyutils.file_from_template(template_python_dir, 
                                        "dialog_camel_case_nameDialog.py", 
                                        target_python_dir, 
                                        substitutions)

