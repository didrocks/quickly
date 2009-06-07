# -*- coding: utf-8 -*-

import getpass
import os
import sys
import subprocess

import ubuntutools.lp.libsupport as lp_libsupport
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
    try:
        print _("Get Launchpad Settings")
        launchpad = lp_libsupport.get_launchpad("quickly")
    except ImportError:
        suggestion = _("Check whether python-launchpadlib is installed")
    except IOError:
        print _("Initial Launchpad binding")
        valid_user = False
        while(valid_user == False):
            email = raw_input(_('E-mail of your Launchpad account: '))
            password = getpass.getpass(_('Your Launchpad password: '))
            try:
               subprocess.call(["manage-credentials", "create", "-c", "quickly", "-l", "2",
                                                       "--email", email, "--password", password])
               launchpad = lp_libsupport.get_launchpad("quickly")
            #except HTTPError:
            #    print "test" doesn't work, when importing launchpadlib.errors
            except IOError:
                print _('''ERROR: email or password does not match a valid user in Launchpad. Be sure you are registered at http://www.launchpad.net.
Another reason can be a network error.''')
            else:
                valid_user = True

        me = launchpad.me
        bzrbinding.bzr_set_login(me.display_name, me.preferred_email_address.email)        

    if launchpad is None:
        die(_("Couldn't setup Launchpad for quickly ; %s") % suggestion)
    print _("Launchpad connexion is ok")

    return launchpad


def get_project(launchpad):
    ''' Get quickly project through launchpad. Create it if needed.
    
            :return project launchpad object
    '''
    
    
    
    return project

