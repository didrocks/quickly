
import os
import sys

import gettext
from gettext import gettext as _


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
    
