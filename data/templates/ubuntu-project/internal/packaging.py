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

import re
import subprocess
import sys


from quickly import launchpadaccess

import gettext
from gettext import gettext as _

#set domain text
gettext.textdomain('quickly')

def updatepackaging():
    """create or update a package using python-mkdebian.
    
    Commit after the first packaging creation"""
    
    return_code = subprocess.call(["python-mkdebian"])
    if return_code == 0:
        print _("Ubuntu packaging created in debian/")
    else:
        print _("An error has occurred")
        return(return_code)

    # check if first python-mkdebian (debian/ creation) to commit it
    # that means debian/ under unknown
    bzr_instance = subprocess.Popen(["bzr", "status"], stdout=subprocess.PIPE)
    bzr_status, err = bzr_instance.communicate()
    if bzr_instance.returncode != 0:
        return(bzr_instance.returncode)
    
    if re.match('(.|\n)*unknown:\n.*debian/(.|\n)*', bzr_status):
        return_code = subprocess.call(["bzr", "add"])
        if return_code == 0:
            return_code = subprocess.call(["bzr", "commit", "-m 'Creating ubuntu package'"])

    return(return_code)

def compute_chosen_ppa(lp_team_or_user, ppa_name=None)
    '''Look for right ppa parameters where to push the package'''

    if not ppa_name:
        if (launchpadaccess.lp_server == "staging"):
            ppa_name = 'staging'
        else: # default ppa
            ppa_name = 'ppa'
    ppa_url = '%s/~%s/+archive/%s' % (launchpadaccess.LAUNCHPAD_URL, lp_team_or_user.name, ppa_name)
    ppa_fullname = '~%s/%s' % (lp_team_or_user.name, ppa_name)
    return (ppa_name, ppa_fullname, ppa_url)

def push_to_ppa(ppa_fullname, changes_file):
    """ Push some code to a ppa """
    
    dput_target = "ppa:%s" % ppa_fullname
    # creation/update debian packaging
    return_code = updatepackaging()
    if return_code != 0:
        print _("ERROR: can't create or update ubuntu package")
        return(return_code)
    # creating local binary package
    return_code = subprocess.call(["dpkg-buildpackage", "-S", "-I.bzr"])
    if return_code != 0:
        print _("ERROR: an error occurred during source package creation")
        return(return_code)
    # now, pushing it to launchpad personal ppa (or team later)
    return_code = subprocess.call(["dput", dput_target, changes_file])
    if return_code != 0:
        print _("ERROR: an error occurred during source upload to launchpad")
        return(return_code)
    return(0)

def check_for_ppa(launchpad, lp_team_or_user, ppa_name):
    """ check wether ppa exists """

    # check that the owner really has an ppa:
    ppa_found = False
    for ppa in lp_team_or_user.ppas:
        if ppa.name == ppa_name:
            ppa_found = True
            break

    if not ppa_found:
        return(1)

    return(0)

