import sys
import subprocess

comment = sys.argv[1]

subprocess.call(["bzr", "add"])
subprocess.call(["bzr", "commit", "-m",   comment])
