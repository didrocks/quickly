# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

'''facade - makes python_name_lib package easy to refactor

while keeping its api constant'''
from python_name_lib.helpers import set_up_logging
from python_name_lib.preferences import preferences
from python_name_lib.Window import Window
from python_name_lib.python_nameconfig.py import get_version

