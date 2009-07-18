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

import os
import sys
import internal.quicklyutils as quicklyutils

pathname = os.path.dirname(sys.argv[0])
abs_path = os.path.abspath(pathname)

project_path = os.path.abspath(os.curdir)
project_name = os.path.basename(project_path)

dialog_name = quicklyutils.quickly_name(sys.argv[1])

template_ui_dir = abs_path + "/ui/"
template_python_dir = abs_path + "/python/"
target_ui_dir = "ui"
target_python_dir = "python"

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

