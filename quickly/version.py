#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
#
# This file is part of Quickly
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

import os
import sys
import gettext
from gettext import gettext as _

import quicklyconfig, tools

gettext.textdomain('quickly')

def show_version():
    """ print version information """
    
    
    print _("""Quickly %s
  Python interpreter: %s %s
  Python standard library: %s
  
  Quickly used library: %s
  Quickly data path: %s
  Quickly detected template directories:
          %s

Copyright 2009 Canonical Ltd.
  #Author 2009 Rick Spencer
  #Author 2009 Didier Roche
https://launchpad.net/quickly

quickly comes with ABSOLUTELY NO WARRANTY. quickly is free software, and
you may use, modify and redistribute it under the terms of the GNU
General Public License version 3 or later.""") % (
    quicklyconfig.__version__, sys.executable, ".".join([str(x) for x in sys.version_info[0:3]]),
    os.path.dirname(os.__file__), os.path.dirname(__file__), tools.get_quickly_data_path(),
    "\n          ".join(tools.get_template_directories()))
    sys.exit(0)
