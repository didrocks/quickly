#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Didier Roche
#
# This file is part of Quickly ubuntu-application template
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

import sys
import webbrowser

from bzrlib.bzrdir import BzrDir
from bzrlib.errors import NoSuchRevision, NotBranchError
from bzrlib.plugin import load_plugins
load_plugins() # Needed for lp: URLs
from bzrlib.workingtree import WorkingTree

from internal import quicklyutils, packaging, launchpad_helper
from internal import bzrutils
from quickly import templatetools, configurationhandler
import license

import logging

from quickly import launchpadaccess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

options = ("--ppa",)

def help():
    print _("""Usage:
$quickly release

Posts a release of your project to a PPA on launchpad so that
users can install the application on their system.

You can also execute:
$quickly release <release_number> if you don't want to use current
release_number. The release_number must be a number.

$quickly release <release_number> notes about changes
where "notes about changes" is optional text describing what changes
were made since the last save

--ppa your_ppa (name or display name) to specify to which ppa you want
to share
--ppa team/ppa (name or display name) to specify to which ppa team you
want to share

Before running quickly release, you should: create your account
and a project page on http://launchpad.net.
You also have to add a PPA to your launchpad account.

Name, email and version setup.py will be automatically changed.
(version will be <current_release> and bzr will commit and tagged.
Once the release is done,  <current_release> will use year.month<.release>
<.release> is incremented by 1 for each release in the same month.
If you previously used quickly shared <current_release>-publicX

You can modify the description and long description if you wish.

You can run $quickly package and test your package to make sure it
installs as expected. (This is not mandatory)
""")
def shell_completion(argv):
    ''' Complete --args '''
    # option completion
    if argv[-1].startswith("-"):
        print " ".join([option for option in options if option.startswith(sys.argv[-1])])
    elif len(argv) > 1 and argv[-2] == '--ppa': # if argument following --ppa, complete by ppa
        print " ".join(packaging.shell_complete_ppa(argv[-1]))

templatetools.handle_additional_parameters(sys.argv, help, shell_completion)


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
                print _("--ppa needs one argument: <ppa_name> or <team/ppa_name>")
                sys.exit(4)
        else:
            print _("Unknown option: %s"  % arg)
            print _("General usage is: quickly release [release_version] [comments]")
            sys.exit(4)
    else:
        args.append(arg)
    i += 1

    commit_msg = None
if len(args) == 1:
    proposed_version = None
elif len(args) == 2:
    proposed_version = args[1]
elif len(args) > 2:
    proposed_version = args[1]
    commit_msg = " ".join(args[2:])

# warning: project_name can be different from project.name (one local, one on launchpad)
if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

# connect to LP
try:
    launchpad = launchpadaccess.initialize_lpi()
except launchpadaccess.launchpad_connection_error, e:
    print(e)
    sys.exit(1)

# push the gpg key and email to the env
try:
    keyid = quicklyutils.get_right_gpg_key_id(launchpad)
except quicklyutils.gpg_error, e:
    print(e)
    sys.exit(1)

# get the project now and save the url into setup.py
try:
    project = launchpadaccess.get_project(launchpad)
except launchpadaccess.launchpad_project_error, e:
    print(e)
    sys.exit(1)
project_url  = launchpadaccess.launchpad_url + '/' + project.name
quicklyutils.set_setup_value('url', project_url)
about_dialog_file_name = quicklyutils.get_about_file_name()
if about_dialog_file_name:
    quicklyutils.change_xml_elem(about_dialog_file_name, "object/property",
                                 "name", "website", project_url, {})

# choose right ppa parameter (users, etc.) ppa or staging if ppa_name is None
try:
    (ppa_user, ppa_name, dput_ppa_name, ppa_url) = packaging.choose_ppa(launchpad, ppa_name)
except packaging.user_team_not_found, e:
    print(_("User or Team %s not found on Launchpad") % e)
    sys.exit(1)
except packaging.not_ppa_owner, e:
    print(_("You have to be a member of %s team to upload to its ppas") % e)
    sys.exit(1)

try:
    ppa_name = packaging.check_and_return_ppaname(launchpad, ppa_user, ppa_name) # ppa_name can be ppa name or ppa display name. Find the right one if exists
except packaging.ppa_not_found, e:
    print(_("%s does not exist. Please create it on launchpad if you want to push a package to it. %s has the following ppas available:") % (e, ppa_user.name))
    user_has_ppa = False
    for ppa_name, ppa_display_name in packaging.get_all_ppas(launchpad, ppa_user):
        print "%s - %s" % (ppa_name, ppa_display_name)
        user_has_ppa = True
    if user_has_ppa:
        print(_("You can temporary choose one of them with --ppa switch or definitely by executing quickly configure ppa <ppa_name>."))
    sys.exit(1)

# update license if needed. Don't change anything if not needed
try:
    license.licensing()
except license.LicenceError, error_message:
    print(error_message)
    sys.exit(1)

try:
    release_version = packaging.updateversion(proposed_version)
except (packaging.invalid_versionning_scheme,
        packaging.invalid_version_in_setup), error_message:
    print(error_message)
    sys.exit(1)

if commit_msg is None:
    commit_msg = _('quickly released: %s' % release_version)

wt = WorkingTree.open(".")

tags = wt.branch.tags.get_tag_dict()

if release_version in tags:
    print _("ERROR: quickly can't release: %s seems to be already released. Choose another name.") % release_version
    sys.exit(1)

# commit current changes
wt.smart_add(["."])
wt.commit(message=_('commit before release'), allow_pointless=True)

tag_list = tags.items()

# try to get last available version in bzr
timestamps = {}
for tag, revid in tag_list:
    try:
        revobj = wt.branch.repository.get_revision(revid)
    except NoSuchRevision:
        timestamp = sys.maxint # place them at the end
    else:
        timestamp = revobj.timestamp
    timestamps[revid] = timestamp
tag_list.sort(key=lambda x: timestamps[x[1]])

revhistory = wt.branch.revision_history()
# Find the first previous version that actually exists in the branch
for previous_version, previous_revid in reversed(tag_list):
    if previous_revid in revhistory:
        revhistory = revhistory[revhistory.index(previous_revid)+1:]
        break

changelog = []
for rev in wt.branch.repository.get_revisions(revhistory):
    changelog.append(rev.message.strip())

# creation/update debian packaging
return_code = packaging.updatepackaging(changelog)
if return_code != 0:
    print _("ERROR: can't create or update ubuntu package")
    sys.exit(1)

# add files, setup release version, commit and push !
#TODO: check or fix if we don't have an ssh key (don't tag otherwise to be able to release again)
wt.smart_add(["."])
revid = wt.commit(message=commit_msg)
wt.branch.tags.set_tag(release_version, revid)

if (launchpadaccess.lp_server == "staging"):
    bzr_staging = "//staging/"
else:
    bzr_staging = ""

stored_push_location = bzrutils.get_bzrbranch()
if not stored_push_location:
    stored_push_location = wt.branch.get_push_location()

if stored_push_location:
    branch_location = stored_push_location
else:
    # No location set yet, come up with one
    branch_location = 'lp:%s~%s/%s/quickly_trunk' % (bzr_staging, launchpad.me.name, project.name)
    wt.branch.set_push_location(branch_location)
    wt.branch.set_parent_branch(branch_location)

if branch_location.startswith("lp:"):
    stored_push_location = stored_push_location.replace("lp://staging/", "lp:")
    branch_location = "lp:%s%s" % (bzr_staging, stored_push_location[3:])

# upload to launchpad
print _("pushing to launchpad")
try:
    target_dir = BzrDir.open(branch_location)
except NotBranchError:
    target_dir = BzrDir.create_branch_convenience(branch_location)
target_dir.push_branch(wt.branch, overwrite=True)

return_code = packaging.push_to_ppa(dput_ppa_name, "../%s_%s_source.changes" % (project_name, release_version), keyid=keyid) != 0
if return_code != 0:
    sys.exit(return_code)

#create new release_date
launchpad_helper.push_tarball_to_launchpad(project, release_version,
                                    "../%s_%s.tar.gz" % (project_name,
                                    release_version), changelog)

print _("%s %s released and building on Launchpad. Wait for half an hour and have look at %s.") % (project_name, release_version, ppa_url)

# as launchpad-open doesn't support staging server, put an url
if launchpadaccess.lp_server == "staging":
    webbrowser.open(launchpadaccess.LAUNCHPAD_CODE_STAGING_URL + '/' + project.name)
else:
    webbrowser.open(launchpadaccess.LAUNCHPAD_URL + '/' + project.name)
