# -*- coding: utf-8 -*-

import osimport sys
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
