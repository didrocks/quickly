# -*- coding: utf-8 -*-

import os
import sys

# connect to LP
from quickly import launchpadaccess
from internal import quicklyutils

launchpad = launchpadaccess.initialize_lpi()

# set the project
launchpadaccess.link_project(launchpad, "Change your launchpad project")
quicklyutils.set_setup_value('author', launchpad.me.display_name)
quicklyutils.set_setup_value('author_email', launchpad.me.preferred_email_address.email)

# get the project now and save the url into setup.py
project = launchpadaccess.get_project(launchpad)
quicklyutils.set_setup_value('url', launchpadaccess.launchpad_url + '/' + project.name)

