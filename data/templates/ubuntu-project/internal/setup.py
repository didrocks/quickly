# -*- coding: utf-8 -*-
#Copyright 2009 Canonical Ltd.
#
# This file is part of Quickly ubuntu-project-template
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



###################### DO NOT TOUCH THIS (GO TO THE SECOND PART) ######################

try:
    import DistUtilsExtra.auto
except ImportError:
    import sys
    print >> sys.stderr, 'To build Apport you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)

#assert DistUtilsExtra.auto.__version__ >= '2.7', 'needs DistUtilsExtra.auto >= 2.7'
import os


def update_data_path(prefix, oldvalue=None):

    try:
        fin = file('project_name/project_nameconfig.py', 'r')
        fout = file(fin.name + '.swp', 'w')

        for line in fin:            
            fields = line.split(' = ') # Separate variable from value
            if fields[0] == '__project_name_data_directory__':
                # update to prefix, store oldvalue
                if not oldvalue:
                    oldvalue = fields[1]
                    line = "%s = '%s'\n" % (fields[0], prefix)
                else: # restore oldvalue
                    line = "%s = %s" % (fields[0], oldvalue)
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find project_name/project_nameconfig.py")
        sys.exit(1)
    return oldvalue

class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        if self.root or self.home:
            print "WARNING: You don't use a standard --prefix installation, take care that you eventually " \
            "need to update quickly/quicklyconfig.py file to adjust __quickly_data_directory__. You can " \
            "ignore this warning if you are packaging and uses --prefix."
        previous_value = update_data_path(self.prefix + '/share/project_name/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_data_path(self.prefix, previous_value)
        
        
###################### YOU CAN MODIFY ONLY BELOW THIS LINE ######################

DistUtilsExtra.auto.setup(
    name='project_name',
    version='0.1',
    license='GPL v3',
    #author='Your Name',
    #author_email='email@ubuntu.com',
    #description='UI for managing …',
    #long_description='Here a longer description',
    #url='https://launchpad.net/project_name',
    cmdclass={'install': InstallAndUpdateDataDirectory}
    )

