import os
import sys
import subprocess

pathname = os.path.dirname(sys.argv[0])
abs_path = os.path.abspath(pathname)

subprocess.call(["sh",pathname + "/glade.sh"])
