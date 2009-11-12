# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly
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

import getpass
import os
import sys
import subprocess

LAUNCHPAD_URL = "https://launchpad.net"
LAUNCHPAD_STAGING_URL = "https://staging.launchpad.net"
LAUNCHPAD_CODE_STAGING_URL = "https://code.staging.launchpad.net"


def die(message):
    print >> sys.stderr, _("Fatal: ") + message
    sys.exit(1)

try:
    from launchpadlib.launchpad import Launchpad, EDGE_SERVICE_ROOT, STAGING_SERVICE_ROOT
    from launchpadlib.errors import HTTPError
    from launchpadlib.credentials import Credentials
except ImportError:
    die(_("Check whether python-launchpadlib is installed"))


from quickly import bzrbinding
from quickly import configurationhandler

import gettext
from gettext import gettext as _


# check if there is no global variable specifying staging
if os.getenv('QUICKLY') is not None and "staging" in os.getenv('QUICKLY').lower():
    launchpad_url = LAUNCHPAD_STAGING_URL
    lp_server = "staging"
else:
    launchpad_url = LAUNCHPAD_URL
    lp_server = "edge"



def initialize_lpi(interactive = True):
    ''' Initialize launchpad binding, asking for crendential

        interactive is True by default if we want to ask the user to setup LP
        :return the launchpad object
    '''

    # if config not already loaded
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()

    launchpad = None
    return_code = 0

    # setup right cache, credential and server
    lp_cred_dir = os.path.expanduser("~/.cache/lp_credentials/")
    if not os.path.isdir(lp_cred_dir):
        os.makedirs(lp_cred_dir)
        os.chmod(lp_cred_dir, 0700)

    lp_cache_dir = os.path.expanduser('~/.cache/lp_credentials/lp-cache/')
    if not os.path.isdir(lp_cache_dir):
        os.makedirs(lp_cache_dir)

    # check which server to address
    if lp_server == "staging":
        lp_cred = lp_cred_dir + "quickly-cred-staging"
        SERVICE_ROOT = STAGING_SERVICE_ROOT
        print _("WARNING: you are using staging and not launchpad real production server")
    else:
        lp_cred = lp_cred_dir + "quickly-cred"
        SERVICE_ROOT = EDGE_SERVICE_ROOT

    # load stored LP credentials
    try:
        if interactive:
            print _("Get Launchpad Settings")
        lp_cred_file = open(lp_cred, 'r')
        credentials = Credentials()
        credentials.load(lp_cred_file)
        lp_cred_file.close()
        launchpad = Launchpad(credentials, SERVICE_ROOT, lp_cache_dir)
    except IOError:
        if interactive:
            print _('Initial Launchpad binding. You must choose "Change Anything"')
            launchpad = Launchpad.get_token_and_login('quickly', SERVICE_ROOT, lp_cache_dir)
            lp_cred_file = open(lp_cred, 'w')
            launchpad.credentials.save(lp_cred_file)
            lp_cred_file.close()

            # try to setup bzr
            me = launchpad.me
            (return_code, suggestion) = bzrbinding.bzr_set_login(me.display_name, me.preferred_email_address.email, me.name)

    if interactive:
        if launchpad is None or return_code != 0:
            if suggestion is None:
                 suggestion = _("Unknown reason")
            os.remove(lp_cred)
            die(_("Couldn't setup Launchpad for quickly ; %s") % suggestion)
        print _("Launchpad connexion is ok")

    return launchpad


def link_project(launchpad, question):
    ''' Link to launchpad project, erasing previous one if already set
    
    
        :return project object'''

    # if config not already loaded
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()

    choice = "0"
    while choice == "0":    
        
        lp_id = raw_input("%s, leave blank to abort.\nLaunchpad project name: " % question)
        if lp_id == "":
            print _("No launchpad project give, aborting.")
            exit(1)
            
        prospective_projects = launchpad.projects.search(text=lp_id)
        project_number = 1
        project_names = []
        for project in prospective_projects:
            print ("---------------- [%s] ----------------") % project_number
            print "  " + project.title
            print ("--------------------------------------")
            print _("Project name: %s") % project.display_name
            print _("Launchpad url: %s/%s") % (launchpad_url, project.name)
            project_names.append(project.name)
            print project.summary
            project_number += 1            
        print

        if not list(prospective_projects):
            message = _("No project found")
        else:
            message = _("Choose your project number")
        choice = raw_input("%s, leave blank to abort, 0 for another search.\nYour choice: " % message)

    try:
        choice = int(choice)
        if choice in range(1, project_number):
            project = launchpad.projects[project_names[choice - 1]]
        else:
            raise ValueError
    except ValueError:
        print _("No right number given, aborting.")
        exit(1)
    configurationhandler.project_config['lp_id'] = project.name
    configurationhandler.saveConfig()
    
    return project

def get_project(launchpad):
    ''' Get quickly project through launchpad.
    
        :return project object
    '''
 
    # if config not already loaded
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()
       
    # try to get project
    try:
        lp_id = configurationhandler.project_config['lp_id']
        project = launchpad.projects[lp_id]
       
    # else, bind the project to LP
    except KeyError:        
        project = link_project(launchpad, "No Launchpad project set")
        
    return project

