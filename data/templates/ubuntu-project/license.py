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

import os
import re
import shutil
import sys

from quickly import configurationhandler, tools


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

1. run $ quickly save in case something goes wrong
2. Edit the file Copyright to include your authorship.
3. If you want to put your own quickly unsupported Licence, remove and replace the tags
   ### BEGIN AUTOMATIC LICENCE GENERATION and ### END AUTOMATIC LICENCE GENERATION
   in it by your own licence.
4. Executes either $ quickly license or $ quickly licence <License>
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

def shell_completion():
    pass

if sys.argv[1] == "help":
    help()
    sys.exit(0)
elif sys.argv[1] == "shell-completion":
    shell_completion()
    sys.exit(0)


def get_supported_licenses():
    """Get supported licenses"""

    available_licenses = [None]
    
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
                        tools.apply_file_rights(ftarget_file_name.name, ftarget_file_name_out.name)
                        os.rename(ftarget_file_name_out.name, ftarget_file_name.name)

                except (OSError, IOError), e:
                    print _("%s file was not found") % fcopyright_name
                    return(1)


def licensing(license=None, author=None):
    """Add license or update it to the project files

    Default is GPL-3"""


    # if file was never licensed, choose GPL-3
    fcopyright_name = "Copyright"

    if license is None:
        try:
            fcopyright = file(fcopyright_name, 'r').read()
            if fcopyright.find(BEGIN_COPYRIGHT_TAG + '\n' + END_COPYRIGHT_TAG) != -1:
                license = "GPL-3"   

        except (OSError, IOError), e:
            print _("%s file was not found") % fcopyright_name
            sys.exit(1)

    # if license is still None, that means that user uses a either a generated license
    # or personal one and don't want to update it

    # check that provided licensed is supported
    if not license in get_supported_licenses():
        print _("This license seems to be unsupported by quickly. If you think it really should, " \
                "please open a bug in quickly bugtracker")
        return(1)


    # check and update (if needed, cf before) the Copyright file
    skip_until_end_found = False
    try:
        fcopyright = file(fcopyright_name, 'r')
        fcopyright_out = file(fcopyright.name + '.new', 'w')
        for line in fcopyright:

            # add autorship if needed
            if "# Copyright 2009 <Your Name> <Your E-mail>" in line:
                # if we have an author (retrieved from launchpad)
                if author:
                    line = "# Copyright 2009 %s" % author
                else:
                    print _('Copyright is not attributed. ' \
                            'Edit the Copyright file to include your name for the copyright in ' \
                            'place of <Your Name> <Your E-mail> or use quickly share/quickly release')
                    return 1

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

        if skip_until_end_found: # that means we didn't find the END_LICENCE_TAG, don't copy the file
            print _("WARNING: %s was not found in the file %s. No licence replacement") % (END_COPYRIGHT_TAG, fcopyright.name)
            os.remove(fcopyright_out.name)
            sys.exit(1)
        else:
            tools.apply_file_rights(fcopyright.name, fcopyright_out.name)
            os.rename(fcopyright_out.name, fcopyright.name)

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

    return(copy_license_to_files())



if __name__ == "__main__":

    license = None
    if len(sys.argv) > 2:
        print _("This command only take one optional argument: License")
        sys.exit(1)
    if len(sys.argv) == 2:
        license = sys.argv[1]

    sys.exit(licensing(license))

