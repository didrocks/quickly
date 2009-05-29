# -*- coding: utf-8 -*-

import os
import sys
# default to looking up lpi integration related to the current dir
pathname = os.path.dirname(sys.argv[0])
builtins_directory = pathname + '/../../builtins/'
if os.path.exists('/usr/share/quickly/builtins'):
  builtins_directory = '/usr/share/quickly/builtins'
builtins_directory =  os.path.abspath(builtins_directory)
sys.path.append(builtins_directory)

import launchpadaccess
launchpadaccess.initialize_lpi()

