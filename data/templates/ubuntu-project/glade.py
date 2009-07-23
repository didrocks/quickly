# -*- coding: utf-8 -*-
# Copyright 2009 Canonical Ltd.
# Author 2009 Didier Roche
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
"""
Usage:
$quickly glade

Opens Glade UI editor so that you can edit the UI for dialogs
and windows in your project. Note that you *must* open Glade
in this manner for quickly to work. If you try to open Glade
directly, and the open the UI files, Glade will throw errors
and won't open the files.

"""


import os
import subprocess

#run glade with env variables pointing to catalogue xml files
if os.getenv('QUICKLY') is not None and "verbose" in os.getenv('QUICKLY').lower():
    subprocess.Popen("GLADE_CATALOG_PATH=./ui glade-3 ui/*.ui", shell=True)
else:
    nullfile=file("/dev/null") 
    subprocess.Popen("GLADE_CATALOG_PATH=./data/ui glade-3 data/ui/*.ui", shell=True, stderr=nullfile)
