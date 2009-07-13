# -*- coding: utf-8 -*-

import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

#create a package
return_code = subprocess.call(["debuild"])
if return_code == 0:
    print _("Ubuntu package has been created")
else:
    print _("An error has occurred")
sys.exit(return_code)


