# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2009 Didier Roche
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
import stat
import string
import sys
import re

import gettext
from gettext import gettext as _

import configurationhandler
import tools
import quicklyconfig
import commands

class bad_project_name(Exception):
    pass

def handle_additional_parameters(args, help=None, shell_completion=None, usage=None):
    """Enable handling additional parameter like help or shell_completion"""

    if len(args) > 1 and args[1] == "help":
        if help:
            help()
        else:
            print _("No help for this command")
        sys.exit(0)
    elif len(args) > 1 and args[1] == "shell-completion":
        if shell_completion:
            shell_completion(args[2:])
        sys.exit(0)
    elif len(args) > 1 and args[1] == "_usage": # use leading underscore to avoid collisions
        if usage:
            usage()
        sys.exit(0)

def quickly_name(name):
    """Enforce quickly name to be ascii, dashed and digit only in lowercase

    return formatted name"""
    forbidden_name = ['bin', 'data']
    name = name.strip().replace(" ", "-").lower()
    
    # Some characters that you might like to have in a name, but are not
    # allowed, such as '_'. The underscore is not allowed because
    # it indicates the separation between a Debian package name and its
    # version.
    if not re.match("[a-z][a-z0-9-]*$", name):
        raise bad_project_name(_("""ERROR: unpermitted character in name.
The name must start with a letter and contain only letters, spaces, dashes (-), and digits."""))

    if name in forbidden_name:
        raise bad_project_name(_('ERROR: %s is not permitted as a quickly project name'))
    return name

def python_name(name):
    """Replace all dashes (-) with underscores (_) in the name to make it suitable for use as a python module name"""
    return name.replace("-", "_")

def get_camel_case_name(name):
    """Replace all dashes (-) and spaces in the name to make it CamelCase"""
    return get_sentence_name(name).replace(" ", "")

def get_sentence_name(name):
    """Replace all dashes (-) with spaces and capitalize all words"""
    return string.capwords(name.replace("-"," "))

def apply_file_rights(src_file_name, dest_file_name):
    """Keep file rights from src to dest"""

    st = os.stat(src_file_name)
    mode = stat.S_IMODE(st.st_mode)
    os.chmod(dest_file_name, mode)

def in_verbose_mode():
    """Return true if verbose mode is on"""

    if os.getenv('QUICKLY') and "verbose" in os.getenv('QUICKLY').lower():
        return True
    return False

def get_project_and_template_versions(template_name):
    """Return project and template version"""

    # take template version. Default is current Quickly version
    template_version = quicklyconfig.__version__
    template_path = tools.get_template_directory(template_name)
    file_command_parameters = file(os.path.join(template_path, 'commandsconfig'), 'rb')
    for line in file_command_parameters: 
        fields = line.split('#')[0] # Suppress commentary after the value in configuration file and in full line
        fields = fields.split('=') # Separate variable from value
        # normally, we have two fields in "fields"
        if len(fields) == 2:
            targeted_property = fields[0].strip()
            value = fields[1].strip()
            if targeted_property == 'TEMPLATE_VERSION':
                template_version = value
                break
    
    # get current project version for this template. Default is no migration (ie take current version)
    configurationhandler.loadConfig()
    # if this project corresponding natively to this template
    if configurationhandler.project_config['template'] == template_name:
        try:
            project_version = configurationhandler.project_config['version']
        except KeyError: # it was called format in quickly 0.2.x
            project_version = configurationhandler.project_config['format']
            configurationhandler.project_config['version'] = project_version
            del configurationhandler.project_config['format']
            configurationhandler.saveConfig()
    else:
        try:
            project_version = configurationhandler.project_config['version_%s' % template_name]
        except KeyError: # initialize with an empty project version to force first upgrade
            project_version = ''

    return (project_version, template_version)

def update_version_in_project_file(new_version, template_name):
    """Update version in .quickly file"""

    configurationhandler.loadConfig()
    if configurationhandler.project_config['template'] == template_name:
        configurationhandler.project_config['version'] = new_version
    else:
        configurationhandler.project_config['version_%s' % template_name] = new_version
    configurationhandler.saveConfig()

def is_X_display():
    """Check if we have a display available"""
    if os.getenv("DISPLAY"):
        return True
    else:
        return False

def get_template_path_from_project():
    """Get current template path when in a project"""
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()
    return os.path.abspath(tools.get_template_directory(configurationhandler.project_config['template']))

def print_usage(usages):
    if not usages:
        return
    if isinstance(usages, list):
        usages.sort()
        print "\n  ".join([_("Usage:")] + usages)
    else:
        print _("Usage:") + " " + usages

def usage_error(msg=None, cmd=None, template=None, **kwargs):
    def print_template_candidates(for_cmd=None):
        templates = []
        if for_cmd:
            possible_command = commands.get_command_names_by_criteria(name=for_cmd, followed_by_template=True)
            if possible_command:
                templates = tools.list_template_for_command(for_cmd)
        else:
            templates = templates or commands.get_all_templates()
        if templates:
            templates.sort()
            print _("Candidate templates are: %s") % ", ".join(templates)

    def print_command_candidates(template=None):
        cmds = []
        if template:
            cmds.extend(commands.get_command_names_by_criteria(template=template))
        if template != "builtins":
            cmds.extend(commands.get_command_names_by_criteria(template="builtins"))
        cmds.sort()
        print _("Candidate commands are: %s") % ", ".join(cmds)

    if msg:
        print _("ERROR: %s") % msg
    if cmd:
        cmd.usage()
    if 'show_templates_for' in kwargs:
        print_template_candidates(kwargs['show_templates_for'])
    elif cmd:
        if cmd.followed_by_template and not template:
            print_template_candidates() # such commands can take any template
        if cmd.followed_by_command:
            print_command_candidates(template)
    else:
        print_command_candidates(template)
    sys.exit(4)

