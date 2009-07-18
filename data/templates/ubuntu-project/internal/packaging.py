
import re
import subprocess
import sys


import gettext
from gettext import gettext as _

#set domain text
gettext.textdomain('quickly')

def updatepackaging():
    """create or update a package using python-mkdebian.
    
    Commit after the first packaging creation"""
    
    dpkg_return_code = subprocess.call(["python-mkdebian"])
    if dpkg_return_code == 0:
        print _("Ubuntu packaging created in debian/")
    else:
        print _("An error has occurred")
        return(dpkg_return_code)
        
    # check if first python-mkdebian (debian/ creation) to commit it
    # that means debian/ under unknown
    bzr_instance = subprocess.Popen(["bzr", "status"], stdout=subprocess.PIPE)
    bzr_status = bzr_instance.stdout.read()
    if re.match('(.|\n)*unknown:\n.*debian/(.|\n)*', bzr_status):
        dpkg_return_code = subprocess.call(["bzr", "add"])
        if dpkg_return_code == 0:
            dpkg_return_code = subprocess.call(["bzr", "commit", "-m 'Creating ubuntu package'"])

    return(dpkg_return_code)

