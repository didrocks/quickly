
import os
import sys

import gettext
from gettext import gettext as _

class project_path_not_found(Exception):
    pass

def get_template_directories():
    '''Retreive all directories where quickly templates are

    :return a list of directories
    '''

    # default to looking up templates in the current dir
    template_directories = []
    if os.path.exists(os.path.expanduser('~/.quickly-data/templates/')):
        template_directories.append(os.path.expanduser('~/.quickly-data/templates/'))
    pathname = os.path.dirname(sys.argv[0])
    abs_path = os.path.abspath(pathname)
    if os.path.exists(abs_path + '/templates'):
        template_directories.append(abs_path + '/templates')
    if os.path.exists('/usr/share/quickly/templates'):
        template_directories.append('/usr/share/quickly/templates')

    if not template_directories:
        print _("No template directory found. Aborting")
        exit(1)
    
    return template_directories


def get_template_directory(template):
    '''Detect where the quickly template and if it exists'''

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
    '''Try to guess where the .quickly config file is.
    
    config_file_path is optional (needed by the new command, for instance).
    getcwd() is taken by default.
    If nothing found, try to find it up to 6 parent directory
    
    :return project_path. Raise a project_path_not_found elsewhere.
    '''

    if config_file_path is None:
        current_path = os.getcwd()
    else:
        current_path = config_file_path

    for related_directory in ('./', './', '../', '../../', '../../../', '../../../../', '../../../../../', '../../../../../../'):
        quickly_file_path = os.path.abspath(current_path + '/' + related_directory)
        quickly_file = quickly_file_path + "/.quickly"
        if os.path.isfile(quickly_file):
            return quickly_file_path
    raise project_path_not_found()

