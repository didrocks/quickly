import sys
import subprocess

comment = "quickly saved"
if sys.argv[1] != "":
    comment = sys.argv[1]

subprocess.call(["bzr", "add"])
subprocess.call(["bzr", "commit", "-m",   comment])
