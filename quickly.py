#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

#figure out where the templage are kept
pathname = os.path.dirname(sys.argv[0])
abs_path =  os.path.abspath(pathname)
template_directory = abs_path + "/templates"

#make sure the user entered enough arguments
if len(sys.argv) < 3:
 print "usage instructions"
 sys.exit(0)

#get the template and command
command = sys.argv[1]
template = sys.argv[2]
if len(sys.argv) > 3:
 command_arg = sys.argv[3]
else:
 command_arg = ""

#ensure the template and command exist
template_path = template_directory + "/" + template
if not os.path.exists(template_path):
 print "ERROR: Template " + template + " not found."
 print "Aborting"
 sys.exit(1)

command_path = template_path + "/" + command + ".py"
if not os.path.exists(command_path):
 print "ERROR: command " + command + " in " + template + " not found."
 print "Aborting"
 sys.exit(1)

#execute the command
subprocess.call(["python",command_path, command_arg])

