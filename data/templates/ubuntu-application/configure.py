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

import os
import sys
import tempfile

import internal.apportutils

from internal import quicklyutils, packaging
from internal import bzrutils
from quickly import configurationhandler, templatetools
from quickly import launchpadaccess


import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')

argv = sys.argv
options = ('bzr', 'dependencies', 'lp-project', 'ppa')

def help():
    print _("""Usage:
$ quickly configure [%s] <args>

Enable to set or change some parameters of the project, like to which
launchpad project should be binded with the current ubuntu application, what
ppa should we use by default to share your package, what additional dependency
should be added…
""") % ("|".join(options))
def shell_completion(argv):
    ''' Complete args '''
    # option completion
    if len(argv) == 1:
        print " ".join([option for option in options if option.startswith(sys.argv[-1])])
    elif len(argv) > 1 and argv[-2] == 'ppa': # if argument following ppa keyname, complete by ppa
        print " ".join(packaging.shell_complete_ppa(argv[-1]))

templatetools.handle_additional_parameters(sys.argv, help, shell_completion)

if len(argv) < 2:
    help()
    sys.exit (1)

# set the project, skipping the interactive phase if project_name is provided
if argv[1] == "lp-project":
    # connect to LP
    try:
        launchpad = launchpadaccess.initialize_lpi()
    except launchpadaccess.launchpad_connection_error, e:
        print(e)
        sys.exit(1)

    project_name = None
    if len(argv) > 2:
        project_name = argv[2]
    # need to try and get the original project name if it exists.  We'll need this
    # to replace any existing settings
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()
    previous_lp_project_name = configurationhandler.project_config.get('lp_id', None)
    quickly_project_name = configurationhandler.project_config.get('project', None)
    try:
        project = launchpadaccess.link_project(launchpad, "Change your launchpad project:", project_name)
        internal.apportutils.update_apport(quickly_project_name, previous_lp_project_name, project.name)
    except launchpadaccess.launchpad_project_error, e:
        print(e)
        sys.exit(1)
    # get the project now and save the url into setup.py
    project_url  = launchpadaccess.launchpad_url + '/' + project.name
    quicklyutils.set_setup_value('url', project_url)
    about_dialog_file_name = quicklyutils.get_about_file_name()
    if about_dialog_file_name:
        quicklyutils.change_xml_elem(about_dialog_file_name, "object/property",
                                     "name", "website", project_url, {})

# change default ppa
elif argv[1] == "ppa":
    # connect to LP
    try:
        launchpad = launchpadaccess.initialize_lpi()
    except launchpadaccess.launchpad_connection_error, e:
        print(e)
        sys.exit(1)

    if len(argv) != 3:
        print(_('''Usage is: $ quickly configure ppa <ppaname>
Use shell completion to find all available ppas'''))
        sys.exit(4)

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

    if ppa_user.is_team:
        configurationhandler.project_config['ppa'] = '%s/%s' % (ppa_user.name, ppa_name)
    else:
        configurationhandler.project_config['ppa'] = ppa_name
    configurationhandler.saveConfig()

# change default bzr push branch
elif argv[1] == "bzr":
    if len(argv) != 3:
        print(_('''Usage is: $ quickly configure bzr <bzr-branch-string>'''))
        sys.exit(4)
    bzrutils.set_bzrbranch(argv[2])
    configurationhandler.saveConfig()    

# add additional depency
elif argv[1] == "dependencies":
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()
    try:
        dependencies = [elem for elem in configurationhandler.project_config['dependencies'].split(' ') if elem]
    except KeyError:
        dependencies = []
    depfile_name = tempfile.mkstemp()[1]
    open(depfile_name,'w').write("\n".join(dependencies))
    editor = quicklyutils.get_quickly_editors()
    dependencies = []
    os.system("%s %s" % (editor, depfile_name))
    for depends in file(depfile_name, 'r'):
        dependencies.extend([elem for elem in depends[:-1].split(' ') if elem])
    os.remove(depfile_name)
    configurationhandler.project_config['dependencies'] = " ".join(dependencies)
    configurationhandler.saveConfig()

