import os
import shutil
import subprocess

from gettext import gettext as _
from quickly import templatetools, configurationhandler
import quicklyutils, bzrutils

LPI_LINE = "LaunchpadIntegration.set_sourcepackagename("

def update_apport(old_project_name, new_project_name):
    if not new_project_name:
        return

    old_crashdb_file = "%s-crashdb.conf"%old_project_name
    new_crashdb_file = "%s-crashdb.conf"%new_project_name
    old_hook_file = "source_%s.py"%old_project_name
    new_hook_file = "source_%s.py"%new_project_name

    if (not old_project_name == new_project_name):
        pathname = templatetools.get_template_path_from_project()
        template_pr_path = os.path.abspath(pathname) + "/project_root/"
        relative_etc_dir = "etc/apport/crashdb.conf.d"
        relative_apport_dir = "apport"

        subst_existing = ((old_project_name, new_project_name),)
        subst_new = (("project_name",new_project_name),)

        file_is_revisioned = bzrutils.is_file_versioned(relative_etc_dir+'/'+old_crashdb_file)
        if os.path.isfile(relative_etc_dir + '/' + old_crashdb_file):
            print _("Updating project name references in existing apport crashdb configuration")
            quicklyutils.file_from_template(relative_etc_dir + '/', old_crashdb_file, relative_etc_dir, subst_existing)
            os.remove(relative_etc_dir + '/' + old_crashdb_file)    
        elif os.path.isdir(template_pr_path + relative_etc_dir):
            print _("Creating new apport crashdb configuration")
            if not os.path.isdir(relative_etc_dir):
                os.makedirs(relative_etc_dir)
            quicklyutils.file_from_template(template_pr_path + relative_etc_dir + '/', "project_name-crashdb.conf", relative_etc_dir, subst_new)
        if file_is_revisioned:
            subprocess.call(["bzr", "rename","--after",relative_etc_dir+'/'+old_crashdb_file,relative_etc_dir+'/'+new_crashdb_file])
                
        file_is_revisioned = bzrutils.is_file_versioned(relative_apport_dir+'/'+old_hook_file)
        if os.path.isfile(relative_apport_dir + '/' + old_hook_file):
            print _("Updating project name references in existing apport hooks configuration")
            quicklyutils.file_from_template(relative_apport_dir + '/', old_hook_file, relative_apport_dir, subst_existing)
            os.remove(relative_apport_dir + '/' + old_hook_file)
        elif os.path.isdir(template_pr_path + relative_apport_dir):
            print _("Creating new apport hooks")
            if not os.path.isdir(relative_apport_dir):
                os.makedirs(relative_apport_dir)
            quicklyutils.file_from_template(template_pr_path + relative_apport_dir+ '/', "source_project_name.py", relative_apport_dir, subst_new)
        if file_is_revisioned:
            subprocess.call(["bzr", "rename","--after",relative_apport_dir+'/'+old_hook_file,relative_apport_dir+'/'+new_hook_file])
            
        print _("Updating launchpad integration references in existing application")
        for root, dirs, files in os.walk('./'):
            for name in files:
                line_replaced = False
                if name.endswith('.py') or root == "./bin":
                    target_file_name = os.path.join(root, name)
                    ftarget_file_name = file(target_file_name, 'r')
                    ftarget_file_name_out = file(ftarget_file_name.name + '.new', 'w')
                    for line in ftarget_file_name:
                        # seek if we have to add or Replace a License
                        if LPI_LINE in line:
                            line_replaced = True
                            new_line = line.split(LPI_LINE)
                            ftarget_file_name_out.write(new_line[0] + LPI_LINE + "'" + new_project_name + "')\n") # write this line, otherwise will be skipped
                        else:
                            ftarget_file_name_out.write(line) # write this line, otherwise will be skipped

                    ftarget_file_name.close()
                    ftarget_file_name_out.close()
                    if not line_replaced: # that means we didn't find the LPI_LINE, don't copy the file
                        os.remove(ftarget_file_name_out.name)
                    else:
                        templatetools.apply_file_rights(ftarget_file_name.name, ftarget_file_name_out.name)
                        os.rename(ftarget_file_name_out.name, ftarget_file_name.name)
