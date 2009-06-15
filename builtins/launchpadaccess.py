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


def get_project(launchpad):
    ''' Get quickly project through launchpad. Create it if needed.
    
            :return project launchpad object
    '''
    
    print "ufw project test: " + str(launchpad.projects['ufw'])
    
    #return project

