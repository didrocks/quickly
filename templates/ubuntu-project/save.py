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

commit_msg = _('quickly saved')

if len(sys.argv) > 1:
 commit_msg = sys.argv[1]

subprocess.call(["bzr", "add"])
subprocess.call(["bzr", "commit", "-m" + commit_msg])

