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

from internal import quicklyutils, packaging
from quickly import configurationhandler, templatetools
try:
    from quickly import launchpadaccess
except launchpadaccess.launchpad_connexion_error, e:
    print(e)
    sys.exit(1)


import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')

argv = sys.argv
options = ('lp-project', 'ppa')

def help():
    print _("""Usage:
$ quickly configure [%s] <args>

Enable to set or change some parameters of the project, like to which
launchpad project should be binded with the current ubuntu project, what
ppa should we use by default to share your package…
""") % ("|".join(available_options))
def shell_completion(argv):
    ''' Complete args '''
    # option completion
    if len(argv) == 1:
        print " ".join([option for option in options if option.startswith(sys.argv[-1])])
    elif len(argv) > 1 and argv[-2] == 'ppa': # if argument following ppa keyname, complete by ppa
        print " ".join(packaging.shell_complete_ppa(argv[-1]))

templatetools.handle_additional_parameters(sys.argv, help, shell_completion)


# connect to LP
try:
    launchpad = launchpadaccess.initialize_lpi()
except launchpadaccess.launchpad_connexion_error, e:
    print(e)
    sys.exit(1)

# set the project, skipping the interactive phase if project_name is provided
if argv[1] == "lp-project":
    project_name = None
    if len(argv > 2):
        project_name = argv[2]
    try:
        project = launchpadaccess.link_project(launchpad, "Change your launchpad project:", project_name)
    except launchpadaccess.launchpad_project_error, e:
        print(e)
        sys.exit(1)
    # get the project now and save the url into setup.py
    quicklyutils.set_setup_value('url', launchpadaccess.launchpad_url + '/' + project.name)

# change default ppa
elif argv[1] == "ppa":
    if len(argv != 3):
        print(_('''Changing ppa parameter should be: quickly configure ppa <ppaname>.
Use shell completion to find all available ppas'''))
        sys.exit(1)

    ppa_name = argv[2]
    # choose right ppa parameter (users, etc.) ppa or staging
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
        print(_("%s does not exist. Please create it on launchpad if you want to upload to it. %s has the following ppas available:") % (e, ppa_user.name))
        for ppa_name, ppa_display_name in packaging.get_all_ppas(launchpad, ppa_user):
            print "%s - %s" % (ppa_name, ppa_display_name)
        sys.exit(1)

    configurationhandler.project_config['ppa'] = ppa_name
    configurationhandler.saveConfig()

