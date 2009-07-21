#!/usr/bin/env python
# -*- coding: utf-8 -*-
# quickly: quickly project handler
#
# Copyright (C) 2009 Canonical Ltd.fds
# Copyright (C) 2009 Rick Spencer
# Copyright (C) 2009 Didier Roche
# Copyright (C) 2009 Ken VanDine
# Copyright (C) 2009 Loïc Minier
# Copyright (C) 2009 Martin Albisetti   	 
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

try:
    import DistUtilsExtra.auto
except ImportError:
    import sys
    print >> sys.stderr, 'To build Apport you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)

#assert DistUtilsExtra.auto.__version__ >= '2.7', 'needs DistUtilsExtra.auto >= 2.7'

print "datarootdir: " + DistUtilsExtra.auto.distutils.command.install.get_config_vars()["datarootdir"]
print "prefix: " + DistUtilsExtra.auto.distutils.command.install.get_config_vars()["prefix"]

DistUtilsExtra.auto.setup(name='quickly',
      version='0.1',
      description='build new Ubuntu apps quickly',
      long_description='Quickly enables for prospective programmer a way to build easily new ' \
                  'apps for Ubuntu based on templates and other systems for helping them ' \
                  'write their code in a guided manner. This also includes packaging and ' \
                  'deploying code.',
      url='https://launchpad.net/quickly',
      license="GPL v3",
      author='Quickly Developer Team',
      author_email='quickly@lists.launchpad.net',
      )

