# -*- coding: utf-8 -*-
#Copyright 2009 Canonical Ltd.
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
"""
Usage:
$quickly license

Adds license to project files. Before using this command, you should:

1. run $quickly save in case something goes wrong
2. Edit the file data/license to include your copyright info
3. Edit the file data/license to include your authorship

Note that if you make a mistake you will need to manually delete the
license from each file before re-running the command.

"""

import sys
import os
import shutil
from quickly import configurationhandler

#check to ensure if it's been edited
license_path = "LICENSE"
license_string = open(license_path, 'r').read()
error = False
if license_string.find("Copyright 2009 Your Name") > -1:
    print """Copyright is not attributed.
            Edited the file data/license to include your name
            for the copyright."""
    error = True
if license_string.find("your.email.com") > -1:
    print """Authorship is not attributed.
            Edited the file data/license to include your email
            for the author."""
    error = True

if error:
    exit(1)

#helper functions
def string_from_file(root,name):
    py_file = os.path.join(root, name)
    return open(py_file,'r').read()

def has_license(temp_str):
    contains_gpl = False
    contains_copyright = False
    if temp_str.find("GNU General Public License") > -1:
        contains_gpl = True

    if temp_str.find("Copyright") > -1:
        contains_copyright = True

    return contains_gpl and contains_copyright

#create the license for python file
py_lic = ""
lic_file = open(license_path,'r')
line = lic_file.readline()
while line != "":
    py_lic += "#" + line
    line = lic_file.readline()

#create the xml_lic
xml_lic = "#<!--" + "\n"
xml_lic += license_string
xml_lic += "-->"

#get the project name
if not configurationhandler.project_config:
    configurationhandler.loadConfig()

project_name = configurationhandler.project_config['project']

#open each python file
for root, dirs, files in os.walk('./'):
    for name in files:
        if name.endswith('.py'):

            #read the file into a string
            temp_str = string_from_file(root, name)
            py_file = os.path.join(root, name)

            #don't license already licensed files            
            if has_license(temp_str):
                print "Skipping %s. It appears to already be licensed" %py_file
            
            else:
                print "adding license to %s" %py_file
                #write the new file
                new_file = open(py_file, 'w')
                new_file.write(py_lic + temp_str)
                new_file.flush()
                new_file.close()

        elif name == project_name:
            bin_file = os.path.join(root, name)

            #read into a string, and delete the shbang
            temp_str = string_from_file(root, name)
            temp_str.replace ("#!/usr/bin/python","")
            if has_license(temp_str):
                print "Skipping %s. It appears to already be licensed" %bin_file

            else:
                #write the newe file
                new_file = open(bin_file, 'w')
                shbang = "#!/usr/bin/python\n\n"
                print "adding license to %s" %bin_file
                new_file.write(shbang + py_lic + temp_str)
                new_file.flush()
                new_file.close()

        elif name.endswith('.ui') or name.endswith('.xml'):
            ui_file = os.path.join(root, name)
            temp_str = string_from_file(root, name)
            if has_license(temp_str):
                print "Skipping %s. It appears to already be licensed" %ui_file

            else:
                new_file = open(ui_file, 'w')
                print "adding license to %s" %ui_file
                #new_file.write(xml_lic + temp_str)
                #new_file.flush()
                #new_file.close()
                #glade files don't load if it does not begin with an element

        else:
            unkown_file = os.path.join(root, name)
            print "no template to license %s" %unkown_file

