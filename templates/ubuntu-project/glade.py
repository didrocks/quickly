import os
import sys
import subprocess

command_path = os.path.dirname(sys.argv[0])
subprocess.Popen(["sh",command_path + "/glade.sh"])
