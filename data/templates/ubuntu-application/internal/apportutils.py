import os
import shutil
import subprocess

from gettext import gettext as _
from quickly import templatetools, configurationhandler
import quicklyutils

def update_apport(old_project_name, new_project_name):
    if not new_project_name:
        return

    old_crashdb_file = "%s-crashdb.conf"%old_project_name
    new_crashdb_file = "%s-crashdb.conf"%new_project_name
    old_hook_file = "source_%s.py"%old_project_name
    new_hook_file = "source_%s.py"%new_project_name

    if (not old_project_name == new_project_name) and enable_apport_bindings(new_project_name):
        pathname = templatetools.get_template_path_from_project()
        template_pr_path = os.path.abspath(pathname) + "/project_root/"
        relative_etc_dir = "etc/apport/crashdb.conf.d"
        relative_apport_dir = "apport"

        subst_existing = ((old_project_name, new_project_name),)
        subst_new = (("project_name",new_project_name),)

        if os.path.isfile(relative_etc_dir + '/' + old_crashdb_file):
            print _("Updating project name references in existing apport crashdb configuration")
            quicklyutils.file_from_template(relative_etc_dir + '/', old_crashdb_file, relative_etc_dir, subst_existing)
            os.remove(relative_etc_dir + '/' + old_crashdb_file)
            subprocess.call(["bzr", "rename","--after",relative_etc_dir+'/'+old_crashdb_file,relative_etc_dir+'/'+new_crashdb_file])
        elif os.path.isdir(template_pr_path + relative_etc_dir):
            print _("Creating new apport crashdb configuration")
            if not os.path.isdir(relative_etc_dir):
                os.makedirs(relative_etc_dir)
            quicklyutils.file_from_template(template_pr_path + relative_etc_dir + '/', "project_name-crashdb.conf", relative_etc_dir, subst_new)

        if os.path.isfile(relative_apport_dir + '/' + old_hook_file):
            print _("Updating project name references in existing apport hooks configuration")
            quicklyutils.file_from_template(relative_apport_dir + '/', old_hook_file, relative_apport_dir, subst_existing)
            os.remove(relative_apport_dir + '/' + old_hook_file)
            subprocess.call(["bzr", "rename","--after",relative_apport_dir+'/'+old_hook_file,relative_apport_dir+'/'+new_hook_file])
        elif os.path.isdir(template_pr_path + relative_apport_dir):
            print _("Creating new apport hooks")
            if not os.path.isdir(relative_apport_dir):
                os.makedirs(relative_apport_dir)
            quicklyutils.file_from_template(template_pr_path + relative_apport_dir+ '/', "source_project_name.py", relative_apport_dir, subst_new)

def enable_apport_bindings(new_project_name):
    enable_apport = raw_input(_("Would you like to enable apport bindings to allow your application to report bugs to the launchpad bug tracking system (y/n)? [y] "))
    enable_apport = enable_apport.lower() in ['yes','y','']
    if enable_apport:
        print _("An example for a python-based project would look like the following.  This is to be placed in the finish_initializing section of your main window:")
        print "====================================================="
        print "import LaunchpadIntegration"
        print "LaunchpadIntegration.set_sourcepackagename('%s')"%new_project_name
        print "LaunchpadIntegration.add_items(self.builder.get_object('helpMenu'), 0, False, True)"
        print "====================================================="
        print _("Please view https://wiki.ubuntu.com/UbuntuDevelopment/Internationalisation/Coding for more code examples on how to activate the bug report menu")
    return enable_apport
