#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def usage():
  print "quickly.py [-t <template> | --template <template>] <command [...]>"
  print
  print "Commands:"
  print "  new <project-name>"
  print "      (template is mandatory for this command)"
  print "  push <describe your changes>"
  print
  print "Examples:  quickly.py -t ubuntu-project new foobar"
  print "           quickly.py push 'awesome new comment system'"

def process_command_line(template_directory):
  """ Entry point for command line processing

  :return: exit code of quickly command.
  """
  opt_command = []
  opt_new = False
  opt_has_template = False
  argv = sys.argv
  i = 1
  while i < len(argv):
    arg = argv[i]
    if arg == 'new':
      opt_new = True
      opt_command.append(arg)
    elif arg == '--template' or arg == '-t':
      opt_has_template = True
      opt_template = argv[i + 1]
      i += 1
    else:
      opt_command.append(arg)
    i += 1

  #if processing new project, template argument and project name
  #must be there (with -t, --template or just following new)
  if opt_new:
    if not opt_has_template:
      print "ERROR: new command need a template name"
      print "Aborting\n"
      usage()
      return 1
    # also need project name
    if len(opt_command) < 2:
      print "ERROR: new command must be followed by a project name"
      print "Aborting\n"
      usage()
      return 1
    else:
      project_name = opt_command[1]

  #if no template provided, guess it from the current tree
  if not opt_has_template:
    try:
      f = open('.quickly', 'r')
      opt_template = f.readline()
      f.close()
    except IOError:
      print '''ERROR: No template provided and none found in the current tree. Ensure you 
don't want to create a new projet or that your are in your directory project.'''
      print "Aborting"
      return 1

  template_path = template_directory + "/" + opt_template
  if not os.path.exists(template_path):
    print "ERROR: Template '" + opt_template + "' not found."
    print "Aborting"
    return 1

  #ensure the command exists
  if not opt_command:
    print "ERROR: No command found"
    print "Aborting\n"
    usage()
    return 1   

  else:
    command_path = template_path + "/" + opt_command[0] + ".py"
    if not os.path.exists(command_path):
      print "ERROR: command '" + opt_command[0] + "' in '" + opt_template + "' not found."
      print "Aborting"
      return 1

    if opt_new:

      #bail if the name if taken
      if os.path.exists(project_name):
        print "There is already a file or directory named " + project_name
        print "Aborting"
        return 1

      #create directory and template file
      print "Creating project directory " + project_name
      os.mkdir(project_name)
      print "Directory " + project_name + " created\n"
      f = open(project_name + '/.quickly', 'w')
      f.write(opt_template)
      f.close

    #execute the command
    return subprocess.call(["python", command_path, " ".join(opt_command[1:])])


if __name__ == '__main__':

  #figure out where the templates are kept
  pathname = os.path.dirname(sys.argv[0])
  abs_path =  os.path.abspath(pathname)
  template_directory = abs_path + "/templates"

  #process the command line to send the right instructions
  exit(process_command_line(template_directory))
