# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
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
import subprocess
import sys

import builtincommands
import tools

import gettext
from gettext import gettext as _


LAUNCHED_INSIDE_PROJECT = "inside"
LAUNCHED_OUTSIDE_PROJECT = "outside"
LAUNCHED_IN_OR_OUTSIDE_PROJECT = "in_or_outside"


gettext.textdomain('quickly')

# double depths tabular : template (or "builtin"), name
__commands = {}


def get_all_commands():
    """Load all commands
    
    First, load template command and then builtins one. Push right parameters depending
    if hooks are available, or if the command execution is special
    You can note that create command is automatically overloaded atm"""

    if len(__commands) > 0:
        return __commands

    for template_dir in tools.get_template_directories():
        for template in os.listdir(template_dir):
            __commands[template] = {}
            template_path = os.path.join(template_dir, template)
            for command_name in os.listdir(template_path):
                file_path = os.path.join(template_path, command_name)
                command_name = ".".join(command_name.split('.')[0:-1])
                if os.path.isfile(file_path) and os.access(file_path, os.X_OK): # add the command to the list if is executable
                    hooks = {'pre': None, 'post':None}
                    for event in ('pre', 'post'):
                        if hasattr(builtincommands, event + '_' + command_name):
                            hooks[event] = getattr(builtincommands, event + '_' + command_name)

                    # TODO: if some commands doesn't need to be launched inside a project, this is the place
                    # to perform some checks on them (and decide how templates can give their input)
                    # same for followed_by_template
                    conditional_launch = LAUNCHED_INSIDE_PROJECT # default for all commands
                    followed_by_template = False
                    # special case for create command: must be launched outside a project, even if part of templates and template creator
                    # didn't specified it
                    if command_name == "create":
                        conditional_launch = LAUNCHED_OUTSIDE_PROJECT
                        followed_by_template = True
                    __commands[template][command_name] = Command(file_path, template, conditional_launch, followed_by_template, hooks['pre'], hooks['post'])
     
    # add builtin commands (avoiding gettext and hooks)
    __commands['builtins'] = {}
    for elem in dir(builtincommands):
        command = getattr(builtincommands, elem)
        if callable(command) and not command.__name__.startswith(('pre_', 'post_', 'gettext')):
            # here, special case for some commands
            conditional_launch = LAUNCHED_IN_OR_OUTSIDE_PROJECT
            followed_by_template = False      
            if command in builtincommands.launched_outside_project:
                conditional_launch = LAUNCHED_OUTSIDE_PROJECT
            elif command in builtincommands.launched_inside_project :               
                conditional_launch = LAUNCHED_IN_OUTSIDE_PROJECT
            if command in builtincommands.followed_by_template:
                followed_by_template = True
        
            hooks = {'pre': None, 'post':None}
            for event in ('pre', 'post'):
                if hasattr(builtincommands, event + '_' + command_name):
                    hooks[event] = getattr(builtincommands, event + '_' + command_name)               

            __commands['builtins'][command.__name__] = Command(command, None, conditional_launch, followed_by_template, hooks['pre'], hooks['post'])
                
    return __commands
    

def get_command_by_criteria(**criterias):
    """Get a list of all commands corresponding to criterias
    
    Criterias correponds to Command object properties"""

    # all criterias are None by default, which means, don't care about the value
    matched_commands = []
    all_commands = get_all_commands()

    for template_available in all_commands:
        if criterias.has_key('template') and criterias['template'] != template_available:
            continue # to speed up the search
        for candidate_command_name in all_commands[template_available]:
            candidate_command = all_commands[template_available][candidate_command_name]
            command_ok = True
            # check all criterias (template has already been checked)
            for elem in criterias:
                if elem is not 'template' and getattr(candidate_command, elem) != criterias[elem]:
                    command_ok = False
                    continue # no need to check other criterias
            if command_ok:
                matched_commands.append(candidate_command)    
    
    return matched_commands


def get_all_templates():
    """Get a list of all templates"""
    
    return [template for template in get_all_commands().keys() if template != "builtins"]


class Command:

    def _die(self, function_name, return_code):
            print _("ERROR: %s command failed") % function_name
            print _("Aborting")
            sys.exit(return_code)

    def __init__(self, command, template=None, inside_project=LAUNCHED_INSIDE_PROJECT, followed_by_template=False, prehook=None, posthook=None):

        self.command = command
        self.template = template
        self.prehook = prehook
        self.posthook = posthook
        self.inside_project = inside_project
        self.followed_by_template = followed_by_template
        
        if callable(command):
            self.name = command.__name__
        else:
            self.name = ".".join(os.path.basename(command).split('.')[0:-1])

    def shell_completion(self, template_in_cli, args):
        """Smart completion of a command
  
        This command try to see if the command is followed by a template and present template
        if it's the case. Otherwise, it calls the corresponding command argument"""

        if len(args) == 0 and not template_in_cli and self.followed_by_template:
            return(self.template)
        
        #else:
        # TODO: give to the command the opportunity of giving some shell-completion features


    def is_right_context(self, dest_path, verbose=True):
        """Check if we are in the right context for launching the command"""
        
        # verbose à false pour l'introspection des commandes dispos
        
        # check if dest_path corresponds to a project path
        if self.inside_project == LAUNCHED_INSIDE_PROJECT:
            try:
                project_path = tools.get_root_project_path(dest_path)
            except tools.project_path_not_found:
                if verbose:
                    print _("ERROR: Can't find project in %s.\nEnsure you launch this command from a quickly project directory.") % dest_path
                    print _("Aborting")
                return False
        elif self.inside_project == LAUNCHED_OUTSIDE_PROJECT:
            try:
                project_path = tools.get_root_project_path(dest_path)
                if verbose:
                    print _("ERROR: %s is a project. You can't launch %s command within a project. " \
                            "Please choose another path." % (project_path, self.command))
                    print _("Aborting")
                return False
            except tools.project_path_not_found:
                pass
            
        return True


    def launch(self, current_dir, command_args, template=None):
        """Launch command and hooks for it
        
        This command will perform the right action (insider function or script execution) after having
        checked the context"""
    
        # template is current template (it will be useful for builtin commands)

        # if template not specified, take the one for the command
        # the template argument is useful when builtin commands which behavior take into account the template namee
        if template is None:
            template = self.template # (which can be None if it's a builtin command launched outside a project)

        if not self.is_right_context(current_dir): # check in verbose mode
            return(1)

        # get root project dir
        try:
            project_path = tools.get_root_project_path(current_dir)
        except tools.project_path_not_found:       
            # launch in current project
            project_path = current_dir

        if self.prehook:
            return_code = self.prehook(template, project_path, command_args)
            if return_code != 0:
                self._die(self.prehook.__name__, return_code)
        
        if callable(self.command): # Internal function
            return_code = self.command(template, project_path, command_args)
        else: # External command
            return_code = subprocess.call(["python", self.command] + command_args, cwd=project_path)
        if return_code != 0:
            self._die(self.name,return_code)

        if self.posthook:
            return_code = self.posthook(template, project_path, command_args)
            if return_code != 0:
                self._die(self.posthook.__name__, return_code)
        
        return(0)



