import os
import configurationhandler

def pre_new(template, command_args):
    '''Create the project directory before new call'''

    project_name = command_args[0]
    #bail if the name if taken
    if os.path.exists(project_name):
        print "There is already a file or directory named %s" % project_name
        return 1

    #create directory and template file
    print "Creating project directory %s" % project_name
    os.mkdir(project_name)
    print "Directory %s created\n" % project_name
    configurationhandler.config['template'] = template
    configurationhandler.saveConfig(project_name)

    return 0

def foo(template, args):
    print "built-in foo"
    return 0

def pre_foo(template, args):
    print "prefoo"
    return 0

def post_foo(template, args):
    print "postfoo"
    return 0

