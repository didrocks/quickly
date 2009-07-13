import subprocess
import os

filelist = ""
for root, dirs, files in os.walk('./'):
    for name in files:
        if name.endswith('.py') and name not in ('__init__.py', 'setup.py'):
            filelist += os.path.join(root, name) + ' '

editor = "gedit"
default_editor = os.environ.get("EDITOR")
if default_editor != None:
 editor = default_editor

subprocess.Popen("%s %s" % (editor, filelist), shell=True)
