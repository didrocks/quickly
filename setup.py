#!/usr/bin/env python
# -*- coding: utf-8 -*-
# quickly: quickly project handler
#
# Copyright (C) 2009 Canonical Ltd.fds
# Author 2009 Didier Roche
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3,
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# UPDATE VERSION WHEN NEEDED (it updates all versions needed to be updated)
VERSION = '0.2.5'

import glob
import os
import sys

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, 'To build quickly you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)

assert DistUtilsExtra.auto.__version__ >= '2.10', 'needs DistUtilsExtra.auto >= 2.10'

def update_data_path(prefix, oldvalue=None):

    try:
        fin = file('quickly/quicklyconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:            
            fields = line.split(' = ') # Separate variable from value
            if fields[0] == '__quickly_data_directory__':
                # update to prefix, store oldvalue
                if not oldvalue:
                    oldvalue = fields[1]
                    line = "%s = '%s'\n" % (fields[0], prefix)
                else: # restore oldvalue
                    line = "%s = %s" % (fields[0], oldvalue)
            # update version if we forget it
            elif fields[0] == '__version__':
                line = "%s = '%s'\n" % (fields[0], VERSION)
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find quickly/quicklyconfig.py")
        sys.exit(1)
    return oldvalue


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        if self.root or self.home:
            print "WARNING: You don't use a standard --prefix installation, take care that you eventually " \
            "need to update quickly/quicklyconfig.py file to adjust __quickly_data_directory__. You can " \
            "ignore this warning if you are packaging and uses --prefix."
        previous_value = update_data_path(self.prefix + '/share/quickly/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_data_path(self.prefix, previous_value)


DistUtilsExtra.auto.setup(name='quickly',
      version="'%s'" % VERSION,
      description='build new Ubuntu apps quickly',
      long_description='Quickly enables for prospective programmer a way to easily build new ' \
                  'apps for Ubuntu based on templates and other systems for helping them ' \
                  'write their code in a guided manner. This also includes packaging and ' \
                  'deploying code.',
      url='https://launchpad.net/quickly',
      license="GPL v3",
      author='Quickly Developer Team',
      author_email='quickly@lists.launchpad.net',
      data_files=[('share/quickly/templates/ubuntu-project/project_root', glob.glob('data/templates/ubuntu-project/project_root/project_name.desktop.in'))],
      cmdclass={'install': InstallAndUpdateDataDirectory})

