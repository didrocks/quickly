# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly ubuntu-application template
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

import os
import sys
import subprocess
from xml.etree import ElementTree as etree

import gettext
from gettext import gettext as _
#set domain text
gettext.textdomain('quickly')

from quickly import configurationhandler
from quickly import templatetools

class cant_deal_with_setup_value(Exception):
    pass

def conventional_names(name):
    sentence_name = templatetools.get_sentence_name(name)
    camel_case_name = templatetools.get_camel_case_name(name)
    return sentence_name, camel_case_name

def file_from_template(template_dir, template_file, target_dir, substitutions=[], rename = True):
    target_file = os.path.basename(template_file) # to get only file name (template_file can be internal/file)
    if rename:
        for s in substitutions:
            pattern, sub = s
            target_file = target_file.replace(pattern,sub)

    print "Creating %s" % target_dir + "/" + target_file
    fin = open(template_dir + template_file,'r')
    file_contents = fin.read()
    for s in substitutions:
        pattern, sub = s
        file_contents = file_contents.replace(pattern,sub)

    fout = open(target_dir + "/" + target_file, 'w')
    fout.write(file_contents)
    fout.flush()
    fout.close()
    fin.close()
    print "%s created\n" % (target_dir + "/" + target_file,)

def get_setup_value(key):
    """ get value from setup.py file.
    
    raise cant_deal_with_setup_value if nothing found
    : return found value"""
    
    result = None
    in_setup = False
    try:
        fsetup = file('setup.py', 'r')
        for line in fsetup: 
            if in_setup:
                fields = line.split('=') # Separate variable from value
                if key in fields[0] and not '#' in fields[0]: # if key found and not commented
                    result = fields[1].partition(',')[0].strip()
                    result = result[1:-1]
                    break
            if "setup(" in line:
                in_setup = True
            # if end of the function, finished
            if in_setup and ')' in line:
                in_setup = False
        fsetup.close()
    except (OSError, IOError), e:
        print _("ERROR: Can't load setup.py file")
        sys.exit(1)

    if result is None:
        raise cant_deal_with_setup_value()
    return result

def set_setup_value(key, value):
    """ set value from setup.py file
    
        it adds new key in the setup() function if not found.
        it uncomments a commented value if changed.
        
        exit with 0 if everything's all right
    """

    has_changed_something = False
    in_setup = False
    try:
        fsetup = file('setup.py', 'r')
        fdest = file(fsetup.name + '.new', 'w')
        for line in fsetup:
            if in_setup:
                fields = line.split('=') # Separate variable from value
                if key in fields[0]:
                    # add new value, uncommenting it if present
                    line = "%s='%s',\n" % (fields[0].replace('#',''), value)
                    has_changed_something = True

            if "setup(" in line:
                in_setup = True
            # add it if the value was not present and reach end of setup() function
            if not has_changed_something and in_setup and ")" in line:
                fdest.write("    %s='%s',\n" % (key, value))
                in_setup = False
            fdest.write(line)
        
        fdest.close()
        fsetup.close()
        os.rename(fdest.name, fsetup.name)
    except (OSError, IOError), e:
        print _("ERROR: Can't load setup.py file")
        sys.exit(1)

    return 0

def check_gpg_secret_key():
    """Check that the gpg secret key corresponding to the right email is present on the system"""
    
    gpg_instance = subprocess.Popen(['gpg', '--list-secret-keys', '--with-colon'], stdout=subprocess.PIPE)
    
    result, err = gpg_instance.communicate()
    
    if gpg_instance.returncode != 0:
        print(err)
        return(False)
    splitted_gpg_list = result.strip().split(':')
    # prendre la partie mail de DEBEMAIL, puis EMAIL
    # Sinon, prendre mail LP

    # regarder s'il se trouve dans gpg, puis reprendre
    # nom gpg -> DEBEMAIL

    #launchpadlib: avoir la clef gpg qui est settée?

    if 'sec' in splitted_gpg_list:
        #TODO: check there that DEBEMAIL (or failback to lp email adress email) gpg key exists and put
        # the name <adress> in DEBEMAIL if doesn't exists.
        return(True)


    print _("No gpg key set. Take a look at quickly tutorial to learn how to setup one")
    return(False)

def get_about_file_name():
    """Get about file name if exists"""
    if not configurationhandler.project_config:
        configurationhandler.loadConfig()
    about_file_name = "data/ui/About%sDialog.ui" % templatetools.get_camel_case_name(configurationhandler.project_config['project'])
    if not os.path.isfile(about_file_name):
        return None
    return about_file_name
   
def change_xml_elem(xml_file, path, attribute_name, attribute_value, value, attributes_if_new):
    """change an elem in a xml tree and save it

    xml_file: url of the xml file
    path -> path to tag to change
    attribute_value -> attribute name to match
    attribute_value -> attribute value to match
    value -> new value
    attributes_if_new -> dictionnary of additional attributes if we create a new node"""
    found = False
    xml_tree = etree.parse(xml_file)
    if not attributes_if_new:
        attributes_if_new = {}
    attributes_if_new[attribute_name] = attribute_value
    for node in xml_tree.findall(path):
        if not attribute_name or node.attrib[attribute_name] == attribute_value:
            node.text = value
            found = True
    if not found:
        parent_node = "/".join(path.split('/')[:-1])
        child_node = path.split('/')[-1]
        new_node = etree.Element(child_node, attributes_if_new)
        new_node.text = value
        xml_tree.find(parent_node).insert(0, new_node)
    xml_tree.write(xml_file + '.new')
    os.rename(xml_file + '.new', xml_file)

