# -*- coding: utf-8 -*-

import sys
import os
import shutil
import subprocess

import gettext
from gettext import gettext as _

def file_from_template(template_dir, template_file, target_dir, project_name, rename = False):
    if rename:
     frags = template_file.split(".")
     target_file = project_name
     if len(frags) > 1:
         target_file += "." + frags[1]
    else:
        target_file = template_file

    print "Creating %s" % target_dir + "/" + target_file
    fin = open(template_dir + template_file,'r')
    file_contents1 = fin.read().replace("project_name",project_name)
    fout = open(target_dir + target_file, 'w')
    fout.write(file_contents1)
    fout.flush()
    fout.close()
    fout.close()
    print "%s created\n" % (target_dir + "/" + target_file,)
 

#set domain text
gettext.textdomain('quickly')

#get the name of the project
if len(sys.argv)< 2:
    print _("""
ERROR: project name not defined. Usage is project_name
Aborting""")
    sys.exit(0)

pathname = os.path.dirname(sys.argv[0])
abs_path = os.path.abspath(pathname)

project_name = sys.argv[1]

# create additional directories
glade_dir = project_name + "/glade"
print _("Creating project directory %s") % glade_dir
os.mkdir(glade_dir)
print _("Directory %s created\n") % glade_dir

python_dir = project_name + "/python"
print _("Creating project directory %s") % python_dir
os.mkdir(python_dir)
print _("Directory %s created\n") % python_dir

media_dir = project_name + "/media"
print _("Creating project directory %s") % media_dir
os.mkdir(media_dir)
print _("Directory %s created\n") % media_dir

#copy files
template_glade_dir = abs_path + "/glade/"
target_glade_dir = project_name + "/glade/"
file_from_template(template_glade_dir, "project_name.ui", target_glade_dir, project_name, True)
file_from_template(template_glade_dir, "about.ui", target_glade_dir, project_name)

template_python_dir = abs_path + "/python/"
target_python_dir = project_name + "/python/"
file_from_template(template_python_dir, "project_name.py", target_python_dir, project_name, True)
file_from_template(template_python_dir, "about.py", target_python_dir, project_name)

template_media_dir = abs_path + "/media/"
target_media_dir = project_name + "/media/"
print _("Copying media files to %s") % target_media_dir
shutil.copy2(template_media_dir + "background.png",target_media_dir)
shutil.copy2(template_media_dir + "logo.png",target_media_dir)
print _("Media files copied to %s\n") % target_media_dir

print _("Creating bzr repository and commiting")
subprocess.call(["bzr", "init"], cwd=project_name)
subprocess.call(["bzr", "add"], cwd=project_name)
subprocess.call(["bzr", "commit", "-m",    "initial project creation"], cwd=project_name)

print _("Launching a first demo")

#run the program
subprocess.call(["python",project_name + ".py"], cwd=project_name + "/python/")

print _("Congrats, your new project is setup! You can now cd %s and start hacking.") % project_name

sys.exit(0)


