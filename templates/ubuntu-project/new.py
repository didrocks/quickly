# -*- coding: utf-8 -*-

import string
import sys
import os
import shutil
import subprocess
import internal.quicklyutils as quicklyutils

import gettext
from gettext import gettext as _


#set domain text
gettext.textdomain('quickly')

#get the name of the project
if len(sys.argv)< 2:
    print _("""
ERROR: project name not defined. Usage is project_name""")
    sys.exit(1)

pathname = os.path.dirname(sys.argv[0])
abs_path = os.path.abspath(pathname)

project_name = quicklyutils.quickly_name(sys.argv[1])

# create additional directories
ui_dir = "ui"
print _("Creating project directory %s") % ui_dir
os.mkdir(ui_dir)
print _("Directory %s created\n") % ui_dir

python_dir = "python"
print _("Creating project directory %s") % python_dir
os.mkdir(python_dir)
print _("Directory %s created\n") % python_dir


sentence_name, camel_case_name = quicklyutils.conventional_names(project_name)

#copy files
template_ui_dir = abs_path + "/ui/"
target_ui_dir = "ui"

substitutions = (("project_name",project_name),
            ("camel_case_name",camel_case_name),
            ("sentence_name",sentence_name),)


#reate the files for glade to use
quicklyutils.file_from_template(template_ui_dir, "camel_case_nameWindow.ui", target_ui_dir, substitutions)
quicklyutils.file_from_template(template_ui_dir, "project_name_window.xml", target_ui_dir, substitutions)
quicklyutils.file_from_template(template_ui_dir, "Aboutcamel_case_nameDialog.ui", target_ui_dir, substitutions)
quicklyutils.file_from_template(template_ui_dir, "about_project_name_dialog.xml", target_ui_dir, substitutions)
quicklyutils.file_from_template(template_ui_dir, "camel_case_namePreferencesDialog.ui", target_ui_dir, substitutions)
quicklyutils.file_from_template(template_ui_dir, "project_name_preferences_dialog.xml", target_ui_dir, substitutions)

#create the python directory and files
template_python_dir = abs_path + "/python/"
target_python_dir = "python"
quicklyutils.file_from_template(template_python_dir, "camel_case_nameWindow.py", target_python_dir, substitutions)
quicklyutils.file_from_template(template_python_dir, "Aboutcamel_case_nameDialog.py", target_python_dir, substitutions)
quicklyutils.file_from_template(template_python_dir, "camel_case_namePreferencesDialog.py", target_python_dir, substitutions)

#create the media directory, and copy the media
template_media_dir = abs_path + "/media/"
target_media_dir = "media"
shutil.copytree(template_media_dir,target_media_dir)


#copy over the help
template_help_dir = abs_path + "/help"
target_help_dir = "help"


shutil.copytree(template_help_dir,target_help_dir)

#def file_from_template(template_dir, template_file, target_dir, substitutions, rename = True):
#copy the executable file, set the mode to executable
quicklyutils.file_from_template(abs_path ,"/project_name",".", substitutions)
os.chmod(project_name, 0755)

#add it to revision control
print _("Creating bzr repository and commiting")
subprocess.call(["bzr", "init"])
subprocess.call(["bzr", "add"])
subprocess.call(["bzr", "commit", "-m", "Initial project creation"])

#run the new application
print _("Launching a first demo")
subprocess.call(["./" + project_name])


print _("Congrats, your new project is setup! cd %s/ to start hacking. Then '$quickly help' for quickly tutorial and reference") % project_name

sys.exit(0)

if __name__== "__main__":
 print "main"
