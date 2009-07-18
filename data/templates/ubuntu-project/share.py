import sys
import subprocess
import webbrowser


from quickly import launchpadaccess, configurationhandler
from internal import quicklyutils, packaging

import gettext
from gettext import gettext as _
gettext.textdomain('quickly')

launchpad = None
# warning: project_name can be different from project.name (one local, one on launchpad)
if not configurationhandler.project_config:
    configurationhandler.loadConfig()
project_name = configurationhandler.project_config['project']

# connect to LP
launchpad = launchpadaccess.initialize_lpi()

# changed upstream author and email
quicklyutils.set_setup_value('author', launchpad.me.display_name)
quicklyutils.set_setup_value('author_email', launchpad.me.preferred_email_address.email)    

    
# check that the owner really has an ppa:
#TODO: change this if we finally release to a team ppa
lp_user = launchpad.me
if (launchpadaccess.lp_server == "staging"):
    ppa_name = 'staging'
else:
    ppa_name = 'ppa'
ppa_url = launchpadaccess.LAUNCHPAD_URL + '/~' + lp_user.name + "/+archive/" + ppa_name

if packaging.check_for_ppa(launchpad, lp_user) != 0:
    print _("ppa:%s:%s does not exist. Please create one on launchpad before sharing") % (lp_user.name, ppa_name)
    webbrowser.open(launchpadaccess.LAUNCHPAD_URL + '/~' + lp_user.name)
    sys.exit(1)

# check version
try:
    release_version = quicklyutils.get_setup_value('version')
except quicklyutils.cant_deal_with_setup_value:
    print _("Release version not found in setup.py and no version specified in command line.")
    sys.exit(1)       


try:
    float(release_version)
except ValueError:
    # two cases:
    # a "quickly share" has already be done, and so, we just bump the number after ~private
    splitted_release_version = release_version.split("~public")
    if len(splitted_release_version) > 1:
        try:
            minor_version = float(splitted_release_version[1])
        except ValueError:
            print _("Minor release version specified after ~public in setup.py is not a valid number: %s") % splitted_release_version[1]
            sys.exit(1)
        version = splitted_release_version[0] + '~public' + str(int(minor_version + 1))

    # elsewhere, it's an error
    else:
        print _("Release version specified in setup.py is not a valid number.")
        sys.exit(1)
    
# we have to minimize the release_version to enable futur release (release_version is already at NEXT version release)
# change setup.py as needed for python-mkdebian
else:
    version = release_version + '~public1'
quicklyutils.set_setup_value('version', version)

# upload to launchpad
print _("pushing to launchpad")
return_code = packaging.push_to_ppa(lp_user.name, "../%s_%s_source.changes" % (project_name, version)) != 0
if return_code != 0:
    sys.exit(return_code)


print _("%s %s is building on Launchpad. Wait for half an hour and have look at %s.") % (project_name, version, ppa_url)

sys.exit(0)

