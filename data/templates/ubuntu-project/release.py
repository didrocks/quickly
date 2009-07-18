# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import webbrowser


from quickly import launchpadaccess, configurationhandler
from internal import quicklyutils, packaging

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')


args = sys.argv

if len(args) == 1:
    # TODO: try to guess new release version in setup.py
    try:
        release_version = quicklyutils.get_setup_value('version')
    except quicklyutils.cant_deal_with_setup_value:
        print _("Release version not found in setup.py and no version specified in command line.")
        sys.exit(1)       
    commit_msg = _('quickly released')
elif len(args) == 2:
    release_version = args[1]
    # add .0 to release if nothing specified (avoid for mess in search in bzr tags)
    if "." not in release_version:
        release_version + '.0'
    commit_msg = _('quickly released: %s' % release_version)
elif len(args) > 2:
    release_version = args[1]
    commit_msg = " ".join(args[2:])

try:
    float(release_version)
except ValueError:
    # two cases:
    # a "quickly share" has already be done, and so, we just remove all the ~privateX stuff
    splitted_release_version = release_version.split("~public")
    if len(splitted_release_version) > 1:
        release_version = splitted_release_version[0]

    # elsewhere, it's an error
    else:
        print _("Release version specified in command arguments or in setup.py " \
                "is not a valid number.")
        sys.exit(1)

launchpad = None
project = None

# warning: project_name can be different from project.name (one local, one on launchpad)
if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

# connect to LP
launchpad = launchpadaccess.initialize_lpi()

# changed upstream author and email
quicklyutils.set_setup_value('author', launchpad.me.display_name)
quicklyutils.set_setup_value('author_email', launchpad.me.preferred_email_address.email)

# get the project now and save the url into setup.py
project = launchpadaccess.get_project(launchpad)
quicklyutils.set_setup_value('url', launchpadaccess.launchpad_url + '/' + project.name)


# check that the owner really has an ppa:
#TODO: change this if we finally release to a team ppa
lp_team_or_user = launchpad.me
if (launchpadaccess.lp_server == "staging"):
    ppa_name = 'staging'
else:
    ppa_name = 'ppa'
ppa_url = launchpadaccess.LAUNCHPAD_URL + '/~' + lp_team_or_user.name + "/+archive/" + ppa_name

if packaging.check_for_ppa(launchpad, lp_team_or_user) != 0:
    print _("ppa:%s:%s does not exist. Please create one on launchpad before releasing") % (lp_team_or_user.name, ppa_name)
    webbrowser.open(launchpadaccess.LAUNCHPAD_URL + '/~' + lp_team_or_user.name)
    sys.exit(1)

    
# check if already released with this name
if release_version: # TODO: remove test when release detected
    bzr_instance = subprocess.Popen(["bzr", "tags"], stdout=subprocess.PIPE)
    bzr_tags = bzr_instance.stdout.read()
    if release_version in bzr_tags:
        print _("ERROR: quickly can't release: %s seems to be already released. Choose another name.") % release_version
        sys.exit(1)

    
# add files, commit and push !
subprocess.call(["bzr", "add"])
return_code = subprocess.call(["bzr", "commit", '-m', commit_msg])
if return_code != 0:
    print _("ERROR: quickly can't release as it can't commit. Are you sure you made any changes?")
    sys.exit(return_code)
subprocess.call(["bzr", "tag", release_version]) # tag revision


# TODO: handle bzr rm

# check if pull branch is set
bzr_instance = subprocess.Popen(["bzr", "info"], stdout=subprocess.PIPE)
bzr_info = bzr_instance.stdout.read()

# TODO: see if we want a strategy to set main branch in the project

if (launchpadaccess.lp_server == "staging"):
    bzr_staging = "//staging/"
else:
    bzr_staging = ""

branch_location = []
# if no branch, create it in ~user_name/project_name/quickly_trunk
# or switch from staging to production
if not ("parent branch" in bzr_info) or ((".staging." in bzr_info) and not bzr_staging) or (not (".staging." in bzr_info) and bzr_staging):

    branch_location = ['lp:', bzr_staging, '~', launchpad.me.name, '/', project.name, '/quickly_trunk']
    return_code = subprocess.call(["bzr", "push", "--remember", "--overwrite", "".join(branch_location)])
    if return_code != 0:
        print _("ERROR: quickly can't release: can't push to launchpad.")
        sys.exit(return_code)
    
    # make first pull too
    return_code = subprocess.call(["bzr", "pull", "--remember", "".join(branch_location)])
    if return_code != 0:
        print _("ERROR: quickly can't release correctly: can't pull from launchpad.")
        sys.exit(return_code)
    
else:

    return_code = subprocess.call(["bzr", "pull"])
    if return_code != 0:
        print _("ERROR: quickly can't release: can't pull from launchpad.")
        sys.exit(return_code)
        
    subprocess.call(["bzr", "push"])
    if return_code != 0:
        print _("ERROR: quickly can't release: can't push to launchpad.")
        sys.exit(return_code)

    # upload to launchpad
    print _("pushing to launchpad")
    return_code = packaging.push_to_ppa(lp_team_or_user.name, "../%s_%s_source.changes" % (project_name, release_version)) != 0
    if return_code != 0:
        sys.exit(return_code)

print _("%s %s released and building on Launchpad. Wait for half an hour and have look at %s.") % (project_name, release_version, ppa_url)

# now, we can bump version for next release
next_release_version = float(release_version) + 0.1
quicklyutils.set_setup_value('version', next_release_version)

# as launchpad-open doesn't support staging server, put an url
if launchpadaccess.lp_server == "staging":
    webbrowser.open(launchpadaccess.LAUNCHPAD_CODE_STAGING_URL + '/~' + launchpad.me.name + '/' + project.name + '/quickly_trunk')
else:
    subprocess.call(["bzr", "launchpad-open"])
