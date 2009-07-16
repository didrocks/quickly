# -*- coding: utf-8 -*-

import os
import stat
import sys
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

from quickly import configurationhandler

# if config not already loaded
if not configurationhandler.project_config:
    configurationhandler.loadConfig()

project_bin = 'bin/' + configurationhandler.project_config['project']
command_line = [project_bin]
command_line.extend(sys.argv[1:])

# run with args if bin/project exist
st = os.stat(project_bin)
mode = st[stat.ST_MODE]
if mode & stat.S_IEXEC:
    subprocess.call(command_line)
else:
    print _("Can't execute %s") % project_bin
    sys.exit(1)

