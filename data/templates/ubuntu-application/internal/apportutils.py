import os
import shutil
import subprocess

from gettext import gettext as _
from quickly import templatetools, configurationhandler
import quicklyutils

LPI_LINE = "LaunchpadIntegration.set_sourcepackagename('%s')"

def update_apport(project_name, old_lp_project, new_lp_project):
    if not new_lp_project:
        return
    # crashdb file doesn't support spaces or dashes in the crash db name
    safe_project_name = project_name.replace(" ", "_").replace("-","_")
    crashdb_file = "%s-crashdb.conf"%project_name
    hook_file = "source_%s.py"%project_name

    pathname = templatetools.get_template_path_from_project()
    template_pr_path = os.path.join(os.path.abspath(pathname),"apport")
    relative_crashdb_dir = os.path.join("etc", "apport", "crashdb.conf.d")
    relative_apport_dir = "apport"
    
    existing_crashdb = os.path.join(relative_crashdb_dir, crashdb_file)
    existing_hook = os.path.join(relative_apport_dir, hook_file)
    
    template_crashdb_dir = os.path.join(template_pr_path, relative_crashdb_dir)
    template_hook_dir = os.path.join(template_pr_path, relative_apport_dir)

    # if the project name has changed, or any of the files are missing, then
    # attempt to set up the apport configuration and hooks
    if  not old_lp_project == new_lp_project \
        or not os.path.isfile(existing_crashdb) \
        or not os.path.isfile(existing_hook):

        subst_existing = ((old_lp_project, new_lp_project),)
        subst_new = (   ("safe_project_name", safe_project_name),
                        ("project_name", project_name),
                        ("lp_project", new_lp_project))

        if os.path.isfile(existing_crashdb):
            print _("Updating project name references in existing apport crashdb configuration")
            quicklyutils.file_from_template(existing_crashdb, relative_crashdb_dir, subst_existing)
        elif os.path.isdir(template_crashdb_dir):
            print _("Creating new apport crashdb configuration")
            if not os.path.isdir(relative_crashdb_dir):
                os.makedirs(relative_crashdb_dir)
            quicklyutils.file_from_template(template_crashdb_dir, "project_name-crashdb.conf", relative_crashdb_dir, subst_new)

        if not os.path.isfile(existing_hook) and os.path.isdir(template_hook_dir):
            print _("Creating new apport hooks")
            if not os.path.isdir(relative_apport_dir):
                os.makedirs(relative_apport_dir)
            quicklyutils.file_from_template(template_hook_dir, "source_project_name.py", relative_apport_dir, subst_new)

        print _("Updating launchpad integration references in existing application")
        old_lpi_line = LPI_LINE%old_lp_project
        old_lpi_pn_line = LPI_LINE%project_name
        new_lpi_line = LPI_LINE%new_lp_project
        for root, dirs, files in os.walk('.'):
            for name in files:
                line_replaced = False
                if name.endswith('.py') or root == os.path.join(".","bin"):
                    target_file_name = os.path.join(root, name)
                    ftarget_file_name = file(target_file_name, 'r')
                    ftarget_file_name_out = file(ftarget_file_name.name + '.new', 'w')
                    for line in ftarget_file_name:
                        # seek the old launchpad integration line and replace it with the new
                        if old_lpi_line in line:
                            line_replaced = True
                            ftarget_file_name_out.write(line.replace(old_lpi_line, new_lpi_line)) # write this line, otherwise will be skipped
                        elif old_lpi_pn_line in line:
                            line_replaced = True
                            ftarget_file_name_out.write(line.replace(old_lpi_pn_line, new_lpi_line)) # write this line, otherwise will be skipped
                        else:
                            ftarget_file_name_out.write(line) # write this line, otherwise will be skipped

                    ftarget_file_name.close()
                    ftarget_file_name_out.close()
                    if not line_replaced: # that means we didn't find the LPI_LINE, don't copy the file
                        os.remove(ftarget_file_name_out.name)
                    else:
                        templatetools.apply_file_rights(ftarget_file_name.name, ftarget_file_name_out.name)
                        os.rename(ftarget_file_name_out.name, ftarget_file_name.name)