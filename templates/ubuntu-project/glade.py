import os
import subprocess

# workaround as this doesn't work:
#os.environ['GLADE_CATALOG_PATH'] = './ui'
#subprocess.Popen(["glade-3", "ui/*.ui"], shell=True)

if os.getenv('QUICKLY') is not None and "verbose" in os.getenv('QUICKLY').lower():
    subprocess.Popen("GLADE_CATALOG_PATH=./ui glade-3 ui/*.ui", shell=True)
else:
    nullfile=file("/dev/null") 
    subprocess.Popen("GLADE_CATALOG_PATH=./ui glade-3 ui/*.ui", shell=True, stderr=nullfile)
