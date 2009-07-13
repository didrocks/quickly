import subprocess
import os

from quickly import configurationhandler

filelist = ""
for root, dirs, files in os.walk('./'):
    for name in files:
        if name.endswith('.py') and name not in ('__init__.py', 'setup.py'):
            filelist += os.path.join(root, name) + ' '

# if config not already loaded
if not configurationhandler.config:
    configurationhandler.loadConfig()

# add launcher which does not end with .py
filelist += 'bin/' + configurationhandler.config['project'].lower()

editor = "gedit"
default_editor = os.environ.get("EDITOR")
if default_editor != None:
 editor = default_editor

subprocess.Popen("%s %s" % (editor, filelist), shell=True)
