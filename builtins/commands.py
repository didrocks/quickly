import os
import shutil

import configurationhandler
import tools

import gettext
from gettext import gettext as _

def pre_new(template, project_dir, command_args):
    '''Create the project directory before new command call'''

    project_name = command_args[0]
    #bail if the name if taken
    if os.path.exists(project_name):
        print _("There is already a file or directory named %s") % project_name
        return 1

    #create directory and template file
    print _("Creating project directory %s" % project_name)
    os.mkdir(project_name)
    print _("Directory %s created\n" % project_name)
    configurationhandler.config['project'] = project_name
    configurationhandler.config['template'] = template
    configurationhandler.saveConfig(project_name)

    return 0

def quickly(template, project_dir, command_args):
    ''' Create a new quickly template from an existing one'''

    destination_path = os.path.expanduser("~/.quickly-data/templates/")
    # create ~/.quickly-data/templates/ if needed
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


