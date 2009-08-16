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
import shutil

import configurationhandler
import quicklyconfig
import tools

import gettext
from gettext import gettext as _


def pre_create(template, project_dir, command_args):
    """Create the project directory before create command call"""

    if len(command_args) < 1:
        print _("ERROR: Create command must be followed by a template and a project path")
        return(1)
        
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
    quickly_project_name = tools.quickly_name(project_name)

    #bail if the name if taken
    if os.path.exists(project_name):
        print _("There is already a file or directory named %s") % project_name
        return(1)

    #create directory and template file
    print _("Creating project directory %s" % project_name)
    os.mkdir(project_name)
    print _("Directory %s created\n" % project_name)

    # creating quickly file
    configurationhandler.project_config['format'] = quicklyconfig.__version__
    configurationhandler.project_config['project'] = quickly_project_name
    configurationhandler.project_config['template'] = template
    configurationhandler.saveConfig(config_file_path=project_name)
    
    os.chdir(project_name)

    return 0

def quickly(template, project_dir, command_args):
    """Create a new quickly template from an existing one"""

    if len(command_args) < 1:
        print _("ERROR: Quickly command must be followed by a template and a template destination path")
        return(1)

    destination_path = os.path.expanduser("~/quickly-templates/")
    # create ~/quickly-templates/ if needed
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    template_destination_path = destination_path + command_args[0]
    if os.path.exists(template_destination_path):
        print _("%s already exists." % template_destination_path)
        return 1

    if not os.path.exists(template_destination_path):
        print _("Copy %s to create new %s template") % (template, template_destination_path)

    shutil.copytree(tools.get_template_directory(template), template_destination_path)
    return 0

def getstarted(template, project_dir, command_args):
    print _('''-------------------------------
    Welcome to quickly!
-------------------------------

You can create a project in executing 'quickly create <template_name> <your project>'.


Example with ubuntu-project template:
1. create a Ubuntu Project and run the tutorial:
$ quickly create ubuntu-project foo
$ cd foo
$ quickly help

2. You can also try:
$ quickly edit
$ quickly glade
$ quickly run
Use bash completion to get every available commands

3. How to play with package and release:

optional, but recommended to build first your package locally:
$ quickly package

BE WARNED: the two following commands will connect to Launchpad. You need at least having a Launchpad account and an opened ppa.
You need also for quickly release a project where you can bind your work with.
$ quickly release or $ quickly share

Have Fun!''')
    return 0



# here, special builtin commands properties
launched_outside_project = []
launched_inside_project = []
followed_by_template = [quickly]
