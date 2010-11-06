#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2009 Didier Roche
#
# This file is part of Quickly ubuntu-application template
#
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.

#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from quickly import templatetools, commands

import gettext
from gettext import gettext as _
# set domain text
gettext.textdomain('quickly')

argv = sys.argv

from store import *
import store

addable = [x for x in dir(store) if x[0] != '_']

options = {}
for module in addable:
    try:
        options[module] = getattr(store, module).option
    except:
        print 'warn:', getattr(store, module)

def usage():
    templatetools.print_usage(options.values())

def help():
    help_list = ['Add something to your project\n']
    for module in addable:
        help_list.append(getattr(store, module).help_text)
    help_text = ''.join(help_list)
    print _(help_text)

def shell_completion(argv):
    ''' Complete args '''
    # option completion
    rv = []
    if len(argv) == 1:
        rv = options.keys()
    if rv:
        rv.sort()
        print ' '.join(rv)
templatetools.handle_additional_parameters(sys.argv, help, shell_completion, usage=usage)

if len(sys.argv) < 2:
    cmd = commands.get_command('add', 'ubuntu-application')
    templatetools.usage_error(_("No action name provided."), cmd=cmd, template='ubuntu-application')

if argv[1] in addable:
    getattr(store, argv[1]).add(options)
else:
    print _('cannot add %s: it is not in the store' % argv[1])
    sys.exit(4)
