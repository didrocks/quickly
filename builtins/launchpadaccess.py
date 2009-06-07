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
        print _("Initial Launchpad creation")
        email = raw_input(_('E-mail of your Launchpad account: '))
        password = getpass.getpass(_('Your Launchpad password: '))
        return_code = subprocess.call(["manage-credentials", "create", "-c", "quickly", "-l", "2",
                                                                     "--email", email, "--password", password])
        launchpad = lp_libsupport.get_launchpad("quickly")

        me = launchpad.me
        bzrbinding.bzr_set_login(me.display_name, me.preferred_email_address.email)        

    if launchpad is None:
        die(_("Couldn't setup Launchpad for quickly ; %s") % suggestion)
    print _("Launchpad connexion is ok")

    return launchpad



# common settings
home_dir = os.path.expanduser("~")
launchpadlib_dir = home_dir + "/.launchpadlib/"

