import os
import subprocess



#run glade with env variables pointing to catalogue xml files
if os.getenv('QUICKLY') is not None and "verbose" in os.getenv('QUICKLY').lower():
    subprocess.Popen("GLADE_CATALOG_PATH=./ui glade-3 ui/*.ui", shell=True)
else:
    nullfile=file("/dev/null") 
    subprocess.Popen("GLADE_CATALOG_PATH=./ui glade-3 ui/*.ui", shell=True, stderr=nullfile)
