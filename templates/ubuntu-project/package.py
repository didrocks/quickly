# -*- coding: utf-8 -*-

import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

#create a package
dpkg_return_code = subprocess.call(["python-mkdebian"])
if dpkg_return_code == 0:
    print _("Ubuntu packaging created in debian/")
else:
    print _("An error has occurred")
    sys.exit(dpkg_return_code)

#create sources suitable for upload
return_code = subprocess.call(["debuild", "-S"])
if return_code == 0:
    print _("Ubuntu package sources have been created")
else:
    print _("An error has occurred")

sys.exit(return_code)


