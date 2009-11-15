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

from quickly import templatetools
import license

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from quickly import configurationhandler
from internal import quicklyutils, packaging

try:
    from quickly import launchpadaccess
except launchpadaccess.launchpad_connexion_error, e:
    print(e)
    sys.exit(1)


launchpad = None
ppa_name = None
i = 0
args = []
argv = sys.argv


def help():
    print _("""Usage:
$quickly share

Updates your PPA with the the latest saved project changes.

Before running quickly release, you should: create your account
on http://launchpad.net.
You also have to add a PPA to your launchpad account.

Name, email and version setup.py will be automatically changed.
(version will be <current_release~publicX> where X will be incremented
at each quickly share execution)
You can modify the description and long description if you wish.

--ppa <your ppa> (name or display name) to specify to which ppa you want
to share
--ppa team/<ppa> (name or display name) to specify to which ppa team you
want to share
""")
def shell_completion(argv):
    ''' Complete --args '''
    # option completion
    if sys.argv[-1].startswith("-"):
        options = ("--ppa",)
        available_completion = [option for option in options if option.startswith(sys.argv[-1])]
        print " ".join(available_completion)
    else:
        if len(argv) > 1 and sys.argv[-2] == '--ppa': # if last argument, this one is to compete
            packaging.shell_complete_ppa(argv[i + 1])

templatetools.handle_additional_parameters(sys.argv, help, shell_completion)


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

# check version
try:
    release_version = quicklyutils.get_setup_value('version')
except quicklyutils.cant_deal_with_setup_value:
    print _("Release version not found in setup.py and no version specified in command line.")
    sys.exit(1)       


try:
    float(release_version)
except ValueError:
    # two cases:
    # a "quickly share" has already be done, and so, we just bump the number after ~private
    splitted_release_version = release_version.split("~public")
    if len(splitted_release_version) > 1:
        try:
            minor_version = float(splitted_release_version[1])
        except ValueError:
            print _("Minor release version specified before ~public in setup.py is not a valid number: %s") % splitted_release_version[1]
            sys.exit(1)
        version = splitted_release_version[0] + '~public' + str(int(minor_version + 1))

    # elsewhere, it's an error
    else:
        print _("Release version specified in setup.py is not a valid number.")
        sys.exit(1)
    
# we have to minimize the release_version to enable futur release (release_version is already at NEXT version release)
# change setup.py as needed for python-mkdebian
else:
    version = release_version + '~public1'
quicklyutils.set_setup_value('version', version)

# if no EMAIL or DEBEMAIL setup, use launchpad prefered email (for changelog).
#TODO: check that the gpg key containis it (or match preferred_email_adress to available gpg keys and take the name)
if not os.getenv("EMAIL") and not os.getenv("DEBEMAIL"):
    os.putenv("DEBEMAIL", "%s <%s>" % (launchpad.me.display_name.encode('UTF-8'), launchpad.me.preferred_email_address.email))
# upload to launchpad
print _("pushing to launchpad")
return_code = packaging.push_to_ppa(dput_ppa_name, "../%s_%s_source.changes" % (project_name, version)) != 0
if return_code != 0:
    sys.exit(return_code)


print _("%s %s is building on Launchpad. Wait for half an hour and have look at %s.") % (project_name, version, ppa_url)

sys.exit(0)

