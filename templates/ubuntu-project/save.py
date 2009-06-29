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

from optparse import OptionParser
import sys

#set domain text
gettext.textdomain('quickly')

# parse entry parameter
option_message = {'name': ('-m', '--message'), 'dest': 'commit_message',
                  'help': _('Description of the new revision')}

options = [option_message]
parser = OptionParser()
for option in options:
    param = option['name']
    del option['name']
    parser.add_option(*param, **option)
options, args = parser.parse_args()

# commit!
additional_bzr_option = ['-m', " ".join(args)]
if options.commit_message:
    additional_bzr_option = ['-m'] + [options.commit_message]
subprocess.call(["bzr", "commit"] + additional_bzr_option)

