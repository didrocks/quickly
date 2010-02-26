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

    crashdb_file = "%s-crashdb.conf"%project_name
    hook_file = "source_%s.py"%project_name

    pathname = templatetools.get_template_path_from_project()
    template_pr_path = os.path.abspath(pathname) + "/project_root/"
    relative_etc_dir = "etc/apport/crashdb.conf.d"
    relative_apport_dir = "apport"

    # if the project name has changed, or any of the files are missing, then
    # attempt to set up the apport configuration and hooks
    if  not old_lp_project == new_lp_project \
        or not os.path.isfile(relative_etc_dir + '/' + crashdb_file) \
        or not os.path.isfile(relative_apport_dir + '/' + hook_file):

        subst_existing = ((old_lp_project, new_lp_project),)
        subst_new = (   ("project_name", project_name),
                        ("lp_project", new_lp_project))

        if os.path.isfile(relative_etc_dir + '/' + crashdb_file):
            print _("Updating project name references in existing apport crashdb configuration")
            quicklyutils.file_from_template(relative_etc_dir + '/', crashdb_file, relative_etc_dir, subst_existing)
        elif os.path.isdir(template_pr_path + relative_etc_dir):
            print _("Creating new apport crashdb configuration")
            if not os.path.isdir(relative_etc_dir):
                os.makedirs(relative_etc_dir)
            quicklyutils.file_from_template(template_pr_path + relative_etc_dir + '/', "project_name-crashdb.conf", relative_etc_dir, subst_new)

        if not os.path.isfile(relative_apport_dir + '/' + hook_file) and os.path.isdir(template_pr_path + relative_apport_dir):
            print _("Creating new apport hooks")
            if not os.path.isdir(relative_apport_dir):
                os.makedirs(relative_apport_dir)
            quicklyutils.file_from_template(template_pr_path + relative_apport_dir+ '/', "source_project_name.py", relative_apport_dir, subst_new)

