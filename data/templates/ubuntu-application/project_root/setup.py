#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build project_name you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_config(values = {}):

    oldvalues = {}
    try:
        fin = file('python_name_lib/python_nameconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find python_name_lib/python_nameconfig.py")
        sys.exit(1)
    return oldvalues


def move_desktop_file(root, target_data, prefix):
    # The desktop file is rightly installed into install_data.  But it should
    # always really be installed into prefix, because while we can install
    # normal data files anywhere we want, the desktop file needs to exist in
    # the main system to be found.  Only actually useful for /opt installs.

    old_desktop_path = os.path.normpath(root + target_data +
                                        '/share/applications')
    old_desktop_file = old_desktop_path + '/project_name.desktop'
    desktop_path = os.path.normpath(root + prefix + '/share/applications')
    desktop_file = desktop_path + '/project_name.desktop'

    if not os.path.exists(old_desktop_file):
        print ("ERROR: Can't find", old_desktop_file)
        sys.exit(1)
    elif target_data != prefix + '/':
        # This is an /opt install, so rename desktop file to use extras-
        desktop_file = desktop_path + '/extras-project_name.desktop'
        try:
            os.makedirs(desktop_path)
            os.rename(old_desktop_file, desktop_file)
            os.rmdir(old_desktop_path)
        except OSError as e:
            print ("ERROR: Can't rename", old_desktop_file, ":", e)
            sys.exit(1)

    return desktop_file

def update_desktop_file(filepath, target_pkgdata, target_scripts):

    try:
        fin = file(filepath, 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                line = "Icon=%s\n" % (target_pkgdata + 'media/project_name.svg')
            elif 'Exec=' in line:
                line = "Exec=%s\n" % (target_scripts + 'project_name')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find", filepath)
        sys.exit(1)

def compile_schemas(root, target_data):
    if target_data == '/usr/':
        return  # /usr paths don't need this, they will be handled by dpkg
    schemadir = os.path.normpath(root + target_data + 'share/glib-2.0/schemas')
    if (os.path.isdir(schemadir) and
            os.path.isfile('/usr/bin/glib-compile-schemas')):
        os.system('/usr/bin/glib-compile-schemas "%s"' % schemadir)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        target_data = '/' + os.path.relpath(self.install_data, self.root) + '/'
        target_pkgdata = target_data + 'share/project_name/'
        target_scripts = '/' + os.path.relpath(self.install_scripts, self.root) + '/'

        values = {'__python_name_data_directory__': "'%s'" % (target_pkgdata),
                  '__version__': "'%s'" % self.distribution.get_version()}
        previous_values = update_config(values)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)

        desktop_file = move_desktop_file(self.root, target_data, self.prefix)
        update_desktop_file(desktop_file, target_pkgdata, target_scripts)
        compile_schemas(self.root, target_data)

        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='project_name',
    version='0.1',
    #license='GPL-3',
    #author='Your Name',
    #author_email='email@ubuntu.com',
    #description='UI for managing …',
    #long_description='Here a longer description',
    #url='https://launchpad.net/project_name',
    cmdclass={'install': InstallAndUpdateDataDirectory}
    )

