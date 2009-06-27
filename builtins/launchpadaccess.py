# -*- coding: utf-8 -*-

import getpass
import os
import sys
import subprocess

try:
    from launchpadlib.launchpad import Launchpad, EDGE_SERVICE_ROOT, STAGING_SERVICE_ROOT
    from launchpadlib.errors import HTTPError
    from launchpadlib.credentials import Credentials
except ImportError:
    suggestion = _("Check whether python-launchpadlib is installed")


import bzrbinding
import configurationhandler

import gettext
from gettext import gettext as _

def die(message):
    print >> sys.stderr, _("Fatal: ") + message
    sys.exit(1)


def initialize_lpi():
    ''' Initialize launchpad binding, asking for crendential

            :return the launchpad object
    '''

    launchpad = None

    # setup right cache, credential and server
    lp_cache_dir = os.path.expanduser('~/.quickly-data/cache/')
    if not os.path.isdir(lp_cache_dir):
        os.makedirs(lp_cache_dir)

    lp_cred_dir = os.path.expanduser("~/.quickly-data/lp_credentials/")
    if not os.path.isdir(lp_cred_dir):
        os.makedirs(lp_cred_dir)
        os.chmod(lp_cred_dir, 0700)

    lp_server = "edge"
    # check if there is no global variable specifying staging
    if os.getenv('QUICKLY') is not None and "staging" in os.getenv('QUICKLY').lower():
        lp_server = "staging"

    # check which server to address
    if lp_server == "staging":
        lp_cred = lp_cred_dir + "quickly-cred-staging"
        SERVICE_ROOT = STAGING_SERVICE_ROOT
    else:
        lp_cred = lp_cred_dir + "quickly-cred"
        SERVICE_ROOT = EDGE_SERVICE_ROOT

    # load stored LP credentials
    try:
        print _("Get Launchpad Settings")
        lp_cred_file = open(lp_cred, 'r')
        credentials = Credentials()
        credentials.load(lp_cred_file)
        lp_cred_file.close()
        launchpad = Launchpad(credentials, SERVICE_ROOT, lp_cache_dir)
    except IOError:
        print _("Initial Launchpad binding")
        launchpad = Launchpad.get_token_and_login('quickly', SERVICE_ROOT, lp_cache_dir)
        lp_cred_file = open(lp_cred, 'w')
        launchpad.credentials.save(lp_cred_file)
        lp_cred_file.close()

        # try to setup bzr
        me = launchpad.me
        bzrbinding.bzr_set_login(me.display_name, me.preferred_email_address.email)        

    if launchpad is None:
        if suggestion is None:
             suggestion = _("Unknown reason")
        die(_("Couldn't setup Launchpad for quickly ; %s") % suggestion)
    print _("Launchpad connexion is ok")

    return launchpad


def link_project(launchpad, question):
    ''' Link to launchpad project, erasing previous one if already set
    
    
        :return project object'''

    # if config not already loaded
    if not configurationhandler.config:
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
            print _("Launchpad url: https://launchpad.net/%s") % project.name
            project_names.append(project.name)
            print project.summary
            project_number += 1            
        print
        choice = raw_input("Choose your project number, leave blank to abort, 0 for another search.\nYour project number: ")

    try:
        choice = int(choice)
        if choice in range(1, project_number):
            project = launchpad.projects[project_names[choice - 1]]
        else:
            raise ValueError
    except ValueError:
        print _("No right number given, aborting.")
        exit(1)
    configurationhandler.config['lp_id'] = project.name
    configurationhandler.saveConfig()
    
    return project

def get_project(launchpad):
    ''' Get quickly project through launchpad.
    
        :return project object
    '''

    # if config not already loaded
    if not configurationhandler.config:
        configurationhandler.loadConfig()        
        
    # try to get project
    try:
        lp_id = configurationhandler.config['lp_id']
        project = launchpad.projects[lp_id]
       
    # else, bind the project to LP
    except KeyError:        
        project = link_project(launchpad, "No Launchpad project set")
        
    return project

