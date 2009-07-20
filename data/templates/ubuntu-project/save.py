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
"""
Usage:
$quickly save notes about changes
where "notes about changes" is optional text describing what changes
were made since the last save.

This command commits all changes since the last save to bzr. Note that 
it does not push changes to any back up location. If you need revert
or otherwise use the revision control, us bzr directly:
$bzr help

"""
import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

#set either a default message or the specified message
commit_msg = " ".join(sys.argv[1:])
if commit_msg == "":
   commit_msg = _('quickly saved')

print commit_msg

#save away
subprocess.call(["bzr", "add"])
return_code = subprocess.call(["bzr", "commit", "-m" + commit_msg])

sys.exit(return_code)

