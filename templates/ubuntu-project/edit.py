import subprocess
import os

editor = "gedit"
default_editor = os.environ.get("EDITOR")
if default_editor != None:
 editor = default_editor

subprocess.Popen("%s python/*.py" %editor, shell=True)

