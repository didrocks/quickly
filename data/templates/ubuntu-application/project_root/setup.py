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

def update_config(libdir, values = {}):

    filename = os.path.join(libdir, 'python_name_lib/python_nameconfig.py')
    oldvalues = {}
    try:
        fin = file(filename, 'r')
        fout = file(filename + '.new', 'w')

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
        print ("ERROR: Can't find %s" % filename)
        sys.exit(1)
    return oldvalues


def update_desktop_file(installdatadir, prefix):

    filename = os.path.join(installdatadir, 'share', 'applications',
                            'project_name.desktop')
    try:
        fin = file(filename, 'r')
        fout = file(filename + '.new', 'w')

        for line in fin:            
            if 'Icon=' in line:
                line = "Icon=%s\n" % os.path.join(prefix, 'share',
                                                  'project_name', 'media',
                                                  'project_name.svg')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find %s" % filename)
        sys.exit(1)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        DistUtilsExtra.auto.install_auto.run(self)

        values = {'__python_name_data_directory__': "'%s'" % (self.prefix + '/share/project_name/'),
                  '__version__': "'%s'" % self.distribution.get_version()}
        update_config(self.install_lib, values)
        update_desktop_file(self.install_data, self.prefix)


        
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

