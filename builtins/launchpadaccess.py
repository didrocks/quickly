# -*- coding: utf-8 -*-

import getpass
import os
import sys
import subprocess

import ubuntutools.lp.libsupport as lp_libsupport
import bzrbinding

def die(message):
  print >> sys.stderr, "Fatal: " + message
  sys.exit(1)


def initialize_lpi():
  ''' Initialize launchpad binding, asking for crendential

      :return the launchpad object
  '''


  launchpad = None
  try:
    print "Get Launchpad Settings"
    launchpad = lp_libsupport.get_launchpad("quickly")
  except ImportError:
    suggestion = "check whether python-launchpadlib is installed"
  except IOError:
    print "Initial Launchpad creation"
    email = raw_input('Mail of your Launchpad account:')
    password = getpass.getpass('Your Launchpad password:')
    return_code = subprocess.call(["manage-credentials", "create", "-c", "quickly", "-l", "2",
                                   "--email", email, "--password", password])
    lp_user_login=email.rsplit('@',1)[0]
    print lp_user_login
    bzrbinding.bzr_set_login(lp_user_login)
    launchpad = lp_libsupport.get_launchpad("quickly")
  if launchpad is None:
    die("Couldn't setup Launchpad for the quickly consumer; %s" % suggestion)
  print "Launchpad connexion is ok"

  return launchpad



# common settings
home_dir = os.path.expanduser("~")
launchpadlib_dir = home_dir + "/.launchpadlib/"

