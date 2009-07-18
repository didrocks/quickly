# -*- coding: utf-8 -*-

import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from internal import packaging, quicklyutils
from quickly import configurationhandler

# retreive useful information
if not configurationhandler.project_config:
    configurationhandler.loadConfig()

project_name = configurationhandler.project_config['project']
try:
    release_version = quicklyutils.get_setup_value('version')
except quicklyutils.cant_deal_with_setup_value:
    print _("Release version not found in setup.py.")


# creation/update debian packaging
if packaging.updatepackaging() != 0:
    print _("ERROR: can't create or update ubuntu package")
    sys.exit(1)


# creating local binary package
return_code = subprocess.call(["debuild", "-tc"])
if return_code == 0:
    print _("Ubuntu package have been successfully created in ../%s_%s_all.deb") % (project_name, release_version)
else:
    print _("An error has occurred")

sys.exit(return_code)


