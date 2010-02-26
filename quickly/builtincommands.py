# -*- coding: utf-8 -*-
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
import shutil

import configurationhandler
import commands as commands_module
import quicklyconfig
import tools
import templatetools

import gettext
from gettext import gettext as _


def pre_create(command_template, project_template, project_dir, command_args):
    """Create the project directory before create command call"""

    if len(command_args) < 1:
        print _("Create command must be followed by a template and a project path.\nUsage: quickly create <template> <project_name>")
        return(4)
 
    path_and_project = command_args[0].split('/')
    project_name = path_and_project[-1]
    
    # if a path is present, create it
    if len(path_and_project) > 1:
        path = str(os.path.sep).join(path_and_project[0:-1])
        if not os.path.exists(path):
            print _("%s does not exist") % path
            return 1
        os.chdir(path)
    
    # check that project name follow quickly rules and reformat it.
    try:
        project_name = templatetools.quickly_name(project_name)
    except templatetools.bad_project_name, e:
        print(e)
        return(1)

    #bail if the name if taken
    if os.path.exists(project_name):
        print _("There is already a file or directory named %s") % project_name
        return(1)

    #create directory and template file
    print _("Creating project directory %s" % project_name)
    os.mkdir(project_name)
    print _("Directory %s created\n" % project_name)

    # creating quickly file
    configurationhandler.project_config['version'] = quicklyconfig.__version__
    configurationhandler.project_config['project'] = project_name
    configurationhandler.project_config['template'] = project_template
    configurationhandler.saveConfig(config_file_path=project_name)
    
    os.chdir(project_name)

    return 0

def commands(project_template, project_dir, command_args, shell_completion=False):
    """List all commands ordered by templates"""

    # We have nothing for this
    if shell_completion:
        return("")

    all_commands = commands_module.get_all_commands()
    for template_available in all_commands:
        # copie all commands to a list (as sort() is an inplace function)
        command_for_this_template = list(all_commands[template_available].keys())
        command_for_this_template.sort()
        for command_name in command_for_this_template:
            command = all_commands[template_available][command_name]
            print "[%s]\t%s" % (template_available, command_name)
            
    return(0)
    
def getstarted(project_template, project_dir, command_args, shell_completion=False):
    """ Give some getstarted advice"""

    # We have nothing for this
    if shell_completion:
        return("")

    print _('''-------------------------------
    Welcome to quickly!
-------------------------------

You can create a project by executing 'quickly create <template_name> <your project>'.

Example with ubuntu-application template:
1. create an ubuntu application and run the tutorial:
$ quickly create ubuntu-application foo
$ cd foo
$ quickly tutorial

2. You can also try:
$ quickly edit
$ quickly design
$ quickly run
Use bash completion to get every available command

3. How to play with a package and release it:

Optional (but recommended): build your package locally:
$ quickly package

BE WARNED: the two following commands will connect to Launchpad. Make sure that you have a Launchpad account and a PPA! You can find out more about setting up a Launchpad account and Launchpad features at https://launchpad.net/
$ quickly release or $ quickly share

Have Fun!''')
    return 0

def help(project_template, project_dir, command_args, shell_completion=False):
    """Get help from commands"""

    # We have nothing for this
    if shell_completion:
        return("")
    
    if len(command_args) > 0:
        command_name = command_args[0]
    else:
        print _("No command provided to help command.\nUsage is: quickly help [template] <command>")
        return(4)

    template = project_template
    if template is None:
        template = "builtins"
    try:
        command = commands_module.get_commands_by_criteria(name=command_name, template=project_template)[0]
    except IndexError:
        # check if a builtin commands corresponds
        template = "builtins"
        try:
            command = commands_module.get_commands_by_criteria(name=command_name, template=template)[0]
        except IndexError:       
            # there is really not such command
            if template == "builtins":
                # to help the user, we can search if this command_name corresponds to a command in a template
                list_possible_commands = commands_module.get_commands_by_criteria(name=command_name, followed_by_template=True)
                if list_possible_commands:
                   print _("help command must be followed by a template name for getting help from templates commands like %s.\nUsage is: quickly help [template] <command>" % command_name)
                   print _("Candidates template are: %s") % ", ".join([command.template for command in list_possible_commands])
                   return(4)
                else:
                    print _("ERROR: No %s command found.") % command_name
            else:
                print _("ERROR: No %s command found in %s template.") % (command_name, template)
            return(1)
        
    return(command.help(project_dir, command_args))


def quickly(project_template, project_dir, command_args, shell_completion=False):
    """Create a new quickly template from an existing one"""

    # We have nothing for this
    if shell_completion:
        return("")

    if len(command_args) < 1:
        print _("Quickly command must be followed by a template and a template destination path\nUsage is: quickly quickly [origin_template] destination_template")
        return(4)

    destination_path = os.path.expanduser("~/quickly-templates/")
    # create ~/quickly-templates/ if needed
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    template_destination_path = destination_path + command_args[0]
    if os.path.exists(template_destination_path):
        print _("%s already exists." % template_destination_path)
        return 1

    if not os.path.exists(template_destination_path):
        print _("Copy %s to create new %s template") % (project_template, template_destination_path)

    try:
        template_source_path = tools.get_template_directory(project_template)
    except tools.template_path_not_found, e:
        print(e)
        return 1
    except tools.template_not_found, e:
        print(e)
        return 1

    shutil.copytree(template_source_path, template_destination_path)
    return 0



# here, special builtin commands properties (if nothing specified, commands can be launched inside and outside projects)
launched_inside_project_only = []
launched_outside_project_only = []
followed_by_template = ['help', 'quickly']
followed_by_command = ['help']

