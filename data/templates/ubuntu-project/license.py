import sys
import os
import shutil
from quickly import configurationhandler

#check to ensure if it's been edited
license_path = "data/license"
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

        if name == project_name:
            #read into a string, and delete the shbang
            temp_str = string_from_file(root, name)
            temp_str.replace ("#!/usr/bin/python","")

            #write the newe file
            bin_file = os.path.join(root, name)
            new_file = open(bin_file, 'w')
            shbang = "#!/usr/bin/python\n"
            print "adding license to %s" %bin_file
            new_file.write(shbang + py_lic + temp_str)


        if name.endswith('.ui'):
            pass

#check it appears that the file has a license
#for python files
#for each line, put a #, then append to the top of the file

#for xml files, put them in a comment
#<!-- This is a comment --> 
