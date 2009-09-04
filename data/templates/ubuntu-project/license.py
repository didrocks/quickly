#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly ubuntu-project-template
#
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import os
import re
import shutil
import sys

from quickly import configurationhandler, templatetools
from internal import quicklyutils

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')


BEGIN_COPYRIGHT_TAG = '### BEGIN AUTOMATIC LICENSE GENERATION'
END_COPYRIGHT_TAG = '### END AUTOMATIC LICENSE GENERATION'
BEGIN_LICENCE_TAG = '### BEGIN LICENSE'
END_LICENCE_TAG = '### END LICENSE'


def help():
    print _("""Usage:
$quickly license <Your_Licence>

Adds license to project files. Before using this command, you should:

1. Edit the file Copyright to include your authorship (this step is automatically done
   if you directly launch "$ quickly release" or "$ quickly share" before changing license)
   In this case, license is GPL-3 by default.
2. If you want to put your own quickly unsupported Licence, remove and replace the tags
   ### BEGIN AUTOMATIC LICENCE GENERATION and ### END AUTOMATIC LICENCE GENERATION
   in it by your own licence.
3. Executes either $ quickly license or $ quickly licence <License>
   where <License> can be either:
   - GPL-3 (default)
   - GPL-2

This will modify the Copyright file with the chosen licence (with GPL-3 by default).
Updating previous chosen Licence if needed.
If you previously removed the tags to add your own licence, it will leave it pristine.
If no name is attributed to the Copyright, it will try to retrieve it from Launchpad
(in quickly release or quickly share command only)

Finally, this will copy the Copyright at the head of every files.

Note that if you don't run quickly licence before calling quickly release or quickly
share, this one will execute it for you and guess the copyright holder from your
launchpad account if you didn't update it.
""")

def get_supported_licenses():
    """Get supported licenses"""

    available_licenses = []
    
    for license_file in os.listdir(os.path.dirname(__file__) + "/available_licenses"):
        result = re.split("header_(.*)", license_file)
        if len(result) == 3:
            available_licenses.append(result[1])
 
    return available_licenses
    

def copy_license_to_files():
    """Copy generated Copyright file to every .py files"""

    # get the project name
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()
    project_name = configurationhandler.project_config['project']

    # put full license into a string, stripping metatags
    fcopyright_name = "Copyright"
    try:
        license = file(fcopyright_name, 'r').read().replace(BEGIN_COPYRIGHT_TAG + '\n', '').replace(END_COPYRIGHT_TAG + '\n', '')
    except (OSError, IOError), e:
        print _("%s file was not found") % fcopyright_name
        sys.exit(1)

    # open each python file and main bin file
    for root, dirs, files in os.walk('./'):
        for name in files:
            if name.endswith('.py') or os.path.join(root, name) == "./bin/" + project_name:
                skip_until_end_found = False
                try:
                    target_file_name = os.path.join(root, name)
                    ftarget_file_name = file(target_file_name, 'r')
                    ftarget_file_name_out = file(ftarget_file_name.name + '.new', 'w')
                    for line in ftarget_file_name:
                        # seek if we have to add or Replace a License
                        if BEGIN_LICENCE_TAG in line:
                            ftarget_file_name_out.write(line) # write this line, otherwise will be skipped
                            skip_until_end_found = True
                            ftarget_file_name_out.write(license)

                        if END_LICENCE_TAG in line:
                            skip_until_end_found = False

                        if not skip_until_end_found:
                            ftarget_file_name_out.write(line)

                    ftarget_file_name.close()
                    ftarget_file_name_out.close()

                    if skip_until_end_found: # that means we didn't find the END_LICENCE_TAG, don't copy the file
                        print _("WARNING: %s was not found in the file %s. No licence replacement") % (END_LICENCE_TAG, ftarget_file_name.name)
                        os.remove(ftarget_file_name_out.name)
                    else:
                        templatetools.apply_file_rights(ftarget_file_name.name, ftarget_file_name_out.name)
                        os.rename(ftarget_file_name_out.name, ftarget_file_name.name)

                except (OSError, IOError), e:
                    print _("%s file was not found") % fcopyright_name
                    return(1)


def licensing(license=None):
    """Add license or update it to the project files

    Default is GPL-3"""


    # if file was never licensed, choose GPL-3
    fcopyright_name = "Copyright"
    fauthors_name = "AUTHORS"

    if license is None:
        try:
            # check if file already licensed
            fcopyright = file(fcopyright_name, 'r').read()
            if fcopyright.find(BEGIN_COPYRIGHT_TAG + '\n' + END_COPYRIGHT_TAG) != -1:
                license = "GPL-3"  

        except (OSError, IOError), e:
            print _("%s file was not found") % fcopyright_name
            sys.exit(1)

    # if license is still None, that means that user uses a either a generated license
    # or personal one and don't want to update it

    # check that provided licensed is supported
    if not license is None and license not in get_supported_licenses():
        print _("This license seems to be unsupported by quickly. If you think it really should, " \
                "please open a bug in quickly bugtracker")
        return(1)


    # check and update (if needed, cf before) Copyright and AUTHORS file
    skip_until_end_found = False
    try:
        fcopyright = file(fcopyright_name, 'r')
        fcopyright_out = file(fcopyright.name + '.new', 'w')
        fauthors_out = file(fauthors_name + '.new', 'w')        
        for line in fcopyright:

            # add autorship if needed
            if "<Your Name> <Your E-mail>" in line:
                # if we have an author in setup.py, put it there
                try:
                    author = quicklyutils.get_setup_value('author')
                    author_email = quicklyutils.get_setup_value('author_email')
                    line = "# Copyright (C) %s %s <%s>\n" % (datetime.datetime.now().year, author, author_email)
                except quicklyutils.cant_deal_with_setup_value:
                    print _('Copyright is not attributed. ' \
                            'Edit the Copyright file to include your name for the copyright in ' \
                            'place of <Your Name> <Your E-mail> or use quickly share/quickly release')
                    return 1

            # update AUTHORS file
            if 'copyright' in line.lower():
                fauthors_out.write(line)

            # if we want to update/create the license
            if license:                
                # seek if we have to add or Replace a License
                if BEGIN_COPYRIGHT_TAG in line:
                    fcopyright_out.write(line) # write this line, otherwise will be skipped
                    skip_until_end_found = True
                    
                    # get license file to read and write in Copyright
                    flicense = open(os.path.dirname(__file__) + "/available_licenses/header_" + license, 'r')
                    fcopyright_out.write(flicense.read())
                    flicense.close

                if END_COPYRIGHT_TAG in line:
                    skip_until_end_found = False

            if not skip_until_end_found:
                fcopyright_out.write(line)

        fcopyright_out.close()
        fcopyright.close()
        fauthors_out.close()

        if skip_until_end_found: # that means we didn't find the END_LICENCE_TAG, don't copy the file
            print _("WARNING: %s was not found in the file %s. No licence replacement") % (END_COPYRIGHT_TAG, fcopyright.name)
            os.remove(fcopyright_out.name)
            sys.exit(1)
        else:
            templatetools.apply_file_rights(fcopyright.name, fcopyright_out.name)
            os.rename(fcopyright_out.name, fcopyright.name)
        # finish updating copyright file
        os.rename(fauthors_out.name, fauthors_name)

    except (OSError, IOError), e:
        print _("%s file was not found") % fcopyright_name
        return(1)
    
    # copy system license file to LICENSE    
    # if not licence variable, that means it has already be copied
    if license is not None:
        src_license_file = "/usr/share/common-licenses/" + license
        if os.path.isfile(src_license_file):
            shutil.copy("/usr/share/common-licenses/" + license, "LICENSE")
        # license has been changed, remove LICENSE file if exists
        else:
            if os.path.isfile("LICENSE"):
                os.remove("LICENSE")
                            
        # write license to setup.py
        quicklyutils.set_setup_value('license', license)

    return(copy_license_to_files())


def shell_completion():
    """Propose available license as the third parameter"""
    
    # if then license argument given, returns available licenses
    if len(sys.argv) == 3:
        print " ".join(get_supported_licenses())


if __name__ == "__main__":

    templatetools.handle_additional_parameters(sys.argv, help, shell_completion)
    license = None
    if len(sys.argv) > 2:
        print _("This command only take one optional argument: License")
        sys.exit(1)
    if len(sys.argv) == 2:
        license = sys.argv[1]

    sys.exit(licensing(license))

