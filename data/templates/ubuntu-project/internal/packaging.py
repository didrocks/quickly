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


from quickly import launchpadaccess, configurationhandler

import gettext
from gettext import gettext as _

#set domain text
gettext.textdomain('quickly')

class ppa_not_found(Exception):
    pass
class not_ppa_owner(Exception):
    pass
class user_team_not_found(Exception):
    pass

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

def shell_complete_ppa(ppa_to_complete):
    ''' Complete from available ppas '''
    
    # connect to LP and get ppa to complete
    launchpad = launchpadaccess.initialize_lpi()
    (ppa_user, ppa_name) = get_ppa_parameters(ppa_to_complete)

    
    
    

def get_ppa_parameters(launchpad, full_ppa_name):
    ''' Check if we can catch good parameters for specified ppa in form user/ppa or ppa '''

    if '/' in full_ppa_name:
        ppa_user_name = full_ppa_name.split('/')[0]
        ppa_name = full_ppa_name.split('/')[1]
        # check that we are in the team/or that we are the user
        try:
            lp_ppa_user = launchpad.people[ppa_user_name]
            if lp_ppa_user.name == launchpad.me.name:
                ppa_user = launchpad.me
            else:
                # check if we are a member of this team
                team = [mem.team for mem in launchpad.me.memberships_details if mem.status in ("Approved", "Administrator") and mem.team.name == ppa_user_name]
                if team:
                    ppa_user = team[0]
                else:
                    raise not_ppa_owner(ppa_user_name)
        except KeyError:
            raise user_team_not_found(ppa_user_name)
    else:
        ppa_user = launchpad.me
        ppa_name = full_ppa_name
    return(ppa_user, ppa_name)

def compute_chosen_ppa(launchpad, ppa_name=None):
    '''Look for right ppa parameters where to push the package'''

    if not ppa_name:
        if not configurationhandler.project_config:
            configurationhandler.loadConfig()
        try:
            (ppa_user, ppa_name) = get_ppa_parameters(launchpad, configurationhandler.project_config['ppa'])
        except KeyError:
            ppa_user = launchpad.me
            if (launchpadaccess.lp_server == "staging"):
                ppa_name = 'staging'
            else: # default ppa
                ppa_name = 'ppa'
    else:
        (ppa_user, ppa_name) = get_ppa_parameters(launchpad, ppa_name)
    ppa_url = '%s/~%s/+archive/%s' % (launchpadaccess.LAUNCHPAD_URL, ppa_user.name, ppa_name)
    dput_ppa_name = 'ppa:%s/%s' % (ppa_user.name, ppa_name)
    return (ppa_user, ppa_name, dput_ppa_name, ppa_url.encode('UTF-8'))

def push_to_ppa(dput_ppa_name, changes_file):
    """ Push some code to a ppa """
    
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
    return_code = subprocess.call(["dput", dput_ppa_name, changes_file])
    if return_code != 0:
        print _("ERROR: an error occurred during source upload to launchpad")
        return(return_code)
    return(0)

def get_all_ppas(launchpad, lp_team_or_user):
    """ get all from a team or users

    Return list of tuples (ppa_name, ppa_display_name)"""
    
    ppa_list = []
    for ppa in lp_team_or_user.ppas:
        ppa_list.append((ppa.name, ppa.displayname))
    return ppa_list

def find_ppa(launchpad, lp_team_or_user, ppa_name):
    """ check wether ppa exists using its name or display name """

    # check that the owner really has this ppa:
    ppa_found = False
    for current_ppa_name, current_ppa_displayname in get_all_ppas(launchpad, lp_team_or_user):
        if current_ppa_name == ppa_name or current_ppa_displayname == ppa_name:
            ppa_found = True
            break
    if not ppa_found:
        raise ppa_not_found('ppa:%s:%s' % (lp_team_or_user.name, ppa_name.encode('UTF-8')))
    return(current_ppa_name)

