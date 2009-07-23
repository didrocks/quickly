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

import socket
import subprocess

def bzr_set_login(display_name, preferred_email_adress, launchpad_name=None):
    ''' try to setup bzr whoami for commit and sshing and bzr launchpad_login if provided

        launchpadname is optional if you don't want user to use launchpad in your template
        if already setup, it will not overwrite existing data
    '''

    #try:

    # retreive the current bzr login
    bzr_instance = subprocess.Popen(["bzr", "whoami"], stdout=subprocess.PIPE)
    bzr_user = bzr_instance.stdout.read()

    # if no bzr whoami set, the default contain the @hostname string
    if '@' + socket.gethostname() in bzr_user:
        identifier = display_name + ' <' + preferred_email_adress + '>'
        subprocess.call(["bzr", "whoami", identifier])

    # if no bzr launchpad-login set, set it now !
    if launchpad_name:
        bzr_instance = subprocess.Popen(["bzr", "launchpad-login"], stdout=subprocess.PIPE)
        bzr_id = bzr_instance.stdout.read()
        
        if "No Launchpad user ID configured" in bzr_id:
            subprocess.call(["bzr", "launchpad-login", launchpad_name])

    
    # except TRY WITHOUT bzr installed

    
