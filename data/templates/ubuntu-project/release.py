#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly ubuntu-project-template
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
import sys
import subprocess
import webbrowser

from internal import quicklyutils, packaging
from quickly import templatetools, configurationhandler
import license

try:
    from quickly import launchpadaccess
except launchpadaccess.launchpad_connexion_error, e:
    print(e)
    sys.exit(1)

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

def help():
    print _("""Usage:
$quickly release

Posts a release of your project to a PPA on launchpad so that
users can install the application on their system. 

You can also execute:
$quickly release <release_number> of you don't want to use current
release_number. The release_number must be a number.

$quickly release <release_number> notes about changes
where "notes about changes" is optional text describing what changes
were made since the last save

--ppa <your ppa> (name or display name) to specify to which ppa you want
to share
--ppa team/<ppa> (name or display name) to specify to which ppa team you
want to share

Before running quickly release, you should: create your account
and a project page on http://launchpad.net.
You also have to add a PPA to your launchpad account.

Name, email and version setup.py will be automatically changed.
(version will be <current_release> and bzr will commit and tagged.
Once the release is done,  <current_release> will be incremented
by 0.1 to be ready for next release.
If you previously used quickly shared <current_release>~publicX
will be dropped to release <current_release> version
(<current_release>~publicX   <   <current_release>)
You can modify the description and long description if you wish.

You can run $quickly package and test your package to make sure it
installs as expected. (This is not mandatory)
""")
templatetools.handle_additional_parameters(sys.argv, help)


launchpad = None
project = None
ppa_name = None
i = 0
args = []
argv = sys.argv

while i < len(argv):
    arg = argv[i]
    if arg.startswith('-'):
        if arg == '--ppa':
            if i + 1 < len(argv):
                ppa_name = argv[i + 1]
                i += 1
            else:
                print _("ERROR: --ppa needs one argument: <ppa name>")
                sys.exit(1)
        else:
            print _("Unknown option: %s"  % arg)
            sys.exit(1)
    else:
        args.append(arg)
    i += 1

if len(args) == 1:

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
    # write release version to setup.py if user specify it (needed for package build)
    quicklyutils.set_setup_value('version', release_version)
elif len(args) > 2:
    release_version = args[1]
    commit_msg = " ".join(args[2:])
    # write release version to setup.py if user specify it (needed for package build)
    quicklyutils.set_setup_value('version', release_version)

try:
    float(release_version)
except ValueError:
    # two cases:
    # a "quickly share" has already be done, and so, we just remove all the ~publilcX stuff
    splitted_release_version = release_version.split("~public")
    if len(splitted_release_version) > 1:
        release_version = splitted_release_version[0]

    # elsewhere, it's an error
    else:
        print _("Release version specified in command arguments or in setup.py " \
                "is not a valid number.")
        sys.exit(1)

# warning: project_name can be different from project.name (one local, one on launchpad)
if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

# connect to LP
try:
    launchpad = launchpadaccess.initialize_lpi()
except launchpadaccess.launchpad_connexion_error, e:
    print(e)
    sys.exit(1)

# check if a gpg key is available
if not quicklyutils.check_gpg_secret_key():
    sys.exit(1)

# changed upstream author and email
quicklyutils.set_setup_value('author', launchpad.me.display_name.encode('UTF-8'))
quicklyutils.set_setup_value('author_email', launchpad.me.preferred_email_address.email)

# license if needed (default with author in setup.py and GPL-3). Don't change anything if not needed
license.licensing()

# get the project now and save the url into setup.py
try:
    project = launchpadaccess.get_project(launchpad)
except launchpadaccess.launchpad_project_error, e:
    print(e)
    sys.exit(1)
quicklyutils.set_setup_value('url', launchpadaccess.launchpad_url + '/' + project.name)

# if no EMAIL or DEBEMAIL setup, use launchpad prefered email (for changelog)
#TODO: check that the gpg key contains it (or match preferred_email_adress to available gpg keys and take the name)
if not os.getenv("EMAIL") and not os.getenv("DEBEMAIL"):
    os.putenv("DEBEMAIL", "%s <%s>" % (launchpad.me.display_name.encode('UTF-8'), launchpad.me.preferred_email_address.email))

# choose right ppa parameter (users, etc.) ppa or staging if ppa_name is None
try:
    (ppa_user, ppa_name, dput_ppa_name, ppa_url) = packaging.compute_chosen_ppa(launchpad, ppa_name)
except packaging.user_team_not_found, e:
    print(_("User or Team %s not found on Launchpad") % e)
    sys.exit(1)
except packaging.not_ppa_owner, e:
    print(_("You have to be a member of %s team to upload to its ppas") % e)
    sys.exit(1)

try:
    ppa_name = packaging.find_ppa(launchpad, ppa_user, ppa_name) # ppa_name can be ppa name or ppa display name. Find the right one if exists
except packaging.ppa_not_found, e:
    print(_("%s does not exist. Please create it on launchpad if you want to upload to it. %s has the following ppas available:") % (e, ppa_user.name))
    for ppa_name, ppa_display_name in packaging.get_all_ppas(launchpad, ppa_user):
        print "%s - %s" % (ppa_name, ppa_display_name)
    sys.exit(1)
    
# check if already released with this name
bzr_instance = subprocess.Popen(["bzr", "tags"], stdout=subprocess.PIPE)
bzr_tags, err = bzr_instance.communicate()
if bzr_instance.returncode !=0:
    print(err)
    sys.exit(1)
if release_version in bzr_tags:
    print _("ERROR: quickly can't release: %s seems to be already released. Choose another name.") % release_version
    sys.exit(1)

    
# add files, setup release version, commit and push !
#TODO: check or fix if we don't have an ssh key (don't tag otherwise to be able to release again)
quicklyutils.set_setup_value('version', release_version)
subprocess.call(["bzr", "add"])
return_code = subprocess.call(["bzr", "commit", '-m', commit_msg])
if return_code != 0 and return_code != 3:
    print _("ERROR: quickly can't release as it can't commit with bzr")
    sys.exit(return_code)
subprocess.call(["bzr", "tag", release_version]) # tag revision


# TODO: handle bzr rm

# check if pull branch is set
bzr_instance = subprocess.Popen(["bzr", "info"], stdout=subprocess.PIPE)
bzr_info, err = bzr_instance.communicate()
if bzr_instance.returncode !=0:
    print(err)
    sys.exit(1)


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
return_code = packaging.push_to_ppa(dput_ppa_name, "../%s_%s_source.changes" % (project_name, release_version)) != 0
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

