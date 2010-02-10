# -*- coding: utf-8 -*-
# Copyright 2010 Canonical Ltd.
# Author 2010 Didier Roche
#
# This file is part of Quickly
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

import commands
import tools

'''public Quickly api'''

def get_template_list():
    '''get a generator of available template'''
    return commands.get_all_templates()

def get_all_commands():
    '''return a dictionnary of template: (commands)'''
    
    templates_commands_dict = {}
    all_commands = commands.get_all_commands()
    for template in all_commands:
        commands_in_template = (command_name for command_name in all_commands[template])
        templates_commands_dict[template] = commands_in_template
    return templates_commands_dict

def get_commands_in_template(template):
    '''get a list of commands for a template'''
    return commands.get_command_names_by_criteria(template=template)

def get_commands_in_context(path):
    '''typle of available commands in context (depending on path)'''

    # simulate a call with completion statement
    result = tools.get_completion_in_context(['quickly', 'shell-completion',
                                            'quickly', ''], path)
    return result
