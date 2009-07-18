
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
    
    return_code = subprocess.call(["python-mkdebian"])
    if return_code == 0:
        print _("Ubuntu packaging created in debian/")
    else:
        print _("An error has occurred")
        return(return_code)
        
    # check if first python-mkdebian (debian/ creation) to commit it
    # that means debian/ under unknown
    bzr_instance = subprocess.Popen(["bzr", "status"], stdout=subprocess.PIPE)
    bzr_status = bzr_instance.stdout.read()
    if re.match('(.|\n)*unknown:\n.*debian/(.|\n)*', bzr_status):
        return_code = subprocess.call(["bzr", "add"])
        if return_code == 0:
            return_code = subprocess.call(["bzr", "commit", "-m 'Creating ubuntu package'"])

    return(return_code)

def push_to_ppa(ppa_user, changes_file):
    """ Push some code to a ppa """
    
    # creation/update debian packaging
    return_code = updatepackaging()
    if return_code != 0:
        print _("ERROR: can't create or update ubuntu package")
        return(return_code)
    
    # creating local binary package
    return_code = subprocess.call(["debuild", "-S"])
    if return_code != 0:
        print _("ERROR: an error occurred during source package creation")
        return(return_code)

    # now, pushing it to launchpad personal ppa (or team later)
    return_code = subprocess.call(["dput", "ppa:%s/ppa" % ppa_user, changes_file])
    if return_code != 0:
        print _("ERROR: an error occurred during source upload to launchpad")
        return(return_code)
    
    return(0)

