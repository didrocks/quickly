''' apport package hook for Quickly

Copyright 2009 Canonical Ltd.
Author 2009 Didier Roche

This file is part of Quickly

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License version 3, as published 
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranties of 
MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along 
with this program.  If not, see <http://www.gnu.org/licenses/>.'''


from quickly import tools

import os

def add_info(report):
    ''' Add data path and available templates'''

    templates = []
    try:
        quickly_data_path = tools.get_quickly_data_path()
    except tools.project_path_not_found:
        quickly_data_path = "No quickly data path found."
    try:
        template_directories = tools.get_template_directories()
        for template_dir in template_directories:       
            templates.extend([os.path.join(template_dir, template_name) for template_name in os.listdir(template_dir)])
    except tools.template_path_not_found:
        template_directories = "No template found."
    report['QuicklyDataPath'] = quickly_data_path
    report['QuicklyTemplatesDirectories'] = "\n".join(template_directories)
    report['QuicklyTemplates'] =  "\n".join(templates)

