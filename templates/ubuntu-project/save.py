# -*- coding: utf-8 -*-

import os
import sys
import subprocess
# default to looking up lpi integration related to the current dir
pathname = os.path.dirname(sys.argv[0])
builtins_directory = pathname + '/../../builtins/'
if os.path.exists('/usr/share/quickly/builtins'):
    builtins_directory = '/usr/share/quickly/builtins'
builtins_directory =  os.path.abspath(builtins_directory)
sys.path.append(builtins_directory)

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

#set either a default message or the specified message
commit_msg = ""
if len(sys.argv) > 1:
 i = 1
 while i < len(sys.argv):
  if i > 1:
   commit_msg += " "
  commit_msg += sys.argv[i]
  i += 1

if commit_msg == "":
 commit_msg = _('quickly saved')

print commit_msg

#save away
subprocess.call(["bzr", "add"])
subprocess.call(["bzr", "commit", "-m" + commit_msg])

