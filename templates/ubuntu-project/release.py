# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import webbrowser

# default to looking up lpi integration related to the current dir
pathname = os.path.dirname(sys.argv[0])
builtins_directory = pathname + '/../../builtins/'
if os.path.exists('/usr/share/quickly/builtins'):
    builtins_directory = '/usr/share/quickly/builtins'
builtins_directory =  os.path.abspath(builtins_directory)
sys.path.append(builtins_directory)
import launchpadaccess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')


args = sys.argv

if len(args) == 1:
    # TODO: try to guess new release name in setup.py
    release_name = ""
    commit_msg = _('quickly released')
elif len(args) == 2:
    release_name = args[1]
    commit_msg = _('quickly released: %s' % release_name)
elif len(args) > 2:
    release_name = args[1]
    commit_msg = " ".join(args[2:])
    
launchpad = None
project = None

# connect to LP
launchpad = launchpadaccess.initialize_lpi()

# get the project
project = launchpadaccess.get_project(launchpad)

    
# check if already released with this name
if release_name: # TODO: remove test when release detected
    bzr_instance = subprocess.Popen(["bzr", "tags"], stdout=subprocess.PIPE)
    bzr_tags = bzr_instance.stdout.read()
    if release_name in bzr_tags:
        print _("ERROR: quickly can't release: %s seems to be already released. Choose another name.") % release_name
        sys.exit(1)
        
    
# add files, commit and push !
subprocess.call(["bzr", "add"])
return_code = subprocess.call(["bzr", "commit", '-m', commit_msg])
if return_code != 0:
    print _("ERROR: quickly can't release as it can't commit. Are you sure you made any changes?")
    sys.exit(1)

if release_name: # TODO: remove test when release detected
    subprocess.call(["bzr", "tag", release_name])

# TODO: handle bzr rm

# check if pull branch is set
bzr_instance = subprocess.Popen(["bzr", "info"], stdout=subprocess.PIPE)
bzr_info = bzr_instance.stdout.read()

# TODO: see if we want a strategy to set main branch in the project

bzr_staging = ""
if ("staging" in os.getenv('QUICKLY').lower()):
    bzr_staging = "//staging/"

branch_location = []
# if no branch, create it in ~user_name/project_name/quickly_trunk
# or switch from staging to production
if not ("parent branch" in bzr_info) or ((".staging." in bzr_info) and not bzr_staging) or (not (".staging." in bzr_info) and bzr_staging):

    branch_location = ['lp:', bzr_staging, '~', launchpad.me.name, '/', project.name, '/quickly_trunk']
    return_code = subprocess.call(["bzr", "push", "--remember", "".join(branch_location)])
    if return_code != 0:
        print _("ERROR: quickly can't release: can't push to launchpad.")
        sys.exit(1)
    
    # make first pull too
    return_code = subprocess.call(["bzr", "pull", "--remember", "".join(branch_location)])
    if return_code != 0:
        print _("ERROR: quickly can't release correctly: can't pull from launchpad.")
        sys.exit(1)
    
else:

    return_code = subprocess.call(["bzr", "pull"])
    if return_code != 0:
        print _("ERROR: quickly can't release: can't pull from launchpad.")
        sys.exit(1)
        
    subprocess.call(["bzr", "push"])
    if return_code != 0:
        print _("ERROR: quickly can't release: can't push to launchpad.")
        sys.exit(1)

print _("%s released!") % release_name

# as launchpad-open doesn't support staging server, put an url
if bzr_staging:
    webbrowser.open('https://code.staging.launchpad.net/~' + launchpad.me.name + '/' + project.name + '/quickly_trunk')
else:
    subprocess.call(["bzr", "launchpad-open"])

