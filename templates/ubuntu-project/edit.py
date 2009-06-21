import os
import sys
import subprocess

command_path = os.path.dirname(sys.argv[0])
subprocess.call(["sh",command_path + "/edit.sh"])
