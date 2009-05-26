#!/usr/bin/env python
# -*- coding: utf-8 -*-

from builtins import main
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

def look_for_commands(template_path=None):
  """ seek for availables commands
  
TEMPLATE direct…
  template_path: where template are located. None if we want to list all commands for all templates.

  : return tuples with list of available commands and origin (default or template)
  """

  if template_path is not None:
    print "in progress"


def check_this_command(command_name, template_path, opt_template):
  """ check if the command exist in and in a template

      For instance, for a command like foo, the inside template foo.py script file is prefered
      to built-in foo() function.
      There can be pre_foo() and post_foo() built-in functions.

      :command_name
      :template_path

      return list of commands ready to be launched
  """

  commands = {}

  # check for template command
  command_path = template_path + "/" + command_name + ".py"
  if os.path.exists(command_path):
    commands[opt_template] = command_path
  else:
    #check for built-in command
    if hasattr(main, command_name):
      commands[opt_template] = getattr(main, command_name)
    else:
      print "ERROR: command '" + command_name + "' in '" + opt_template + "' not found."
      print "Aborting"
      exit(1)    

  #check for pre-post built-in commands
  for hook in ("pre", "post"):
    if hasattr(main, hook + '_' + command_name):
      commands[hook] = getattr(main, hook + '_' + command_name)
  
  return commands


def process_command_line(template_directory):
  """ Entry point for command line processing

  template_directory: where template are located

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
    elif arg == '--help' or arg == '-h':
      usage()
      return 0
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

  #else, execute the commands
  else:
    commands_to_execute = check_this_command(opt_command[0], template_path, opt_template)
    return_code = 0
    #pre-hook
    if 'pre' in commands_to_execute:
      return_code = commands_to_execute['pre'](opt_template, opt_command[1:])
    if return_code != 0:
      print "ERROR: pre_%s command failed" % opt_command[0]
      print "Aborting"
      return return_code

    #main execution
    if callable(commands_to_execute[opt_template]):
      return_code = commands_to_execute[opt_template](opt_template, opt_command[1:])
    else:
      return_code = subprocess.call(["python", commands_to_execute[opt_template], " ".join(opt_command[1:])])

    if return_code != 0:
      print "ERROR: %s command failed" % opt_command[0]
      print "Aborting"
      return return_code

    #post-hook
    if 'post' in commands_to_execute:
       commands_to_execute['post'](opt_template, opt_command[1:])
    if return_code != 0:
      print "ERROR: post_%s command failed" % opt_command[0]
      print "Aborting"
      return return_code

    return 0

if __name__ == '__main__':

  #figure out where the templates are kept
  pathname = os.path.dirname(sys.argv[0])
  abs_path =  os.path.abspath(pathname)
  template_directory = abs_path + "/templates"

  #process the command line to send the right instructions
  exit(process_command_line(template_directory))
