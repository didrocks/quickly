
import os
import string
import sys

import gettext
from gettext import gettext as _

def quickly_name(name):
    """Enforce quickly name to be ascii only and lowercase
    
    return formated name"""
    name = name.lower()
    permitted_characters = string.ascii_lowercase
    permitted_characters += "_"
    for c in name:
        if c not in permitted_characters:
            print _("""
ERROR: unpermitted character in name.
Letters and underscore ("_") only.""")
            sys.exit(1)
    return name


class project_path_not_found(Exception):
    pass

def get_template_directories():
    """Retreive all directories where quickly templates are

    :return a list of directories
    """

    # default to looking up templates in the current dir
    template_directories = []
    if os.path.exists(os.path.expanduser('~/.quickly-data/templates/')):
        template_directories.append(os.path.expanduser('~/.quickly-data/templates/'))
    # for trunk usage
    pathname = os.path.dirname(sys.argv[0])
    abs_template_path = os.path.abspath(pathname + '../templates')
    if os.path.exists(abs_template_path):
        template_directories.append(abs_template_path)
    # for installed usage
    pathname = os.path.dirname(__file__)
    abs_template_path = os.path.abspath(pathname + '/../templates')
    if os.path.exists(abs_template_path):
        template_directories.append(abs_template_path)
    if not template_directories:
        print _("No template directory found. Aborting")
        exit(1)

    return template_directories


def get_template_directory(template):
    """Detect where the quickly template and if it exists"""

    # check for the first available template in template_directories
    for template_directory in get_template_directories():
        template_path = template_directory + "/" + template
        if os.path.exists(template_path):
            template_found = True
            break
        template_found = False

    # if still false, no template found in template_directories
    if not template_found:
        print _("ERROR: Template '%s' not found.") % template
        print _("Aborting")
        exit(1)

    return template_path


def get_root_project_path(config_file_path=None):
    """Try to guess where the .quickly config file is.

    config_file_path is optional (needed by the new command, for instance).
    getcwd() is taken by default.
    If nothing found, try to find it up to 6 parent directory

    :return project_path. Raise a project_path_not_found elsewhere.
    """

    if config_file_path is None:
        current_path = os.getcwd()
    else:
        current_path = config_file_path

    for related_directory in ('./', './', '../', '../../',
                              '../../../', '../../../../',
                              '../../../../../', '../../../../../../'):
        quickly_file_path = os.path.abspath(current_path + '/' + related_directory)
        quickly_file = quickly_file_path + "/.quickly"
        if os.path.isfile(quickly_file):
            return quickly_file_path
    raise project_path_not_found()

