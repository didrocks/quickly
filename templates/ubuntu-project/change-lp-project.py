# -*- coding: utf-8 -*-

import os
import sys

# connect to LP

from quickly import launchpadaccess
launchpad = launchpadaccess.initialize_lpi()

# set the project
launchpadaccess.link_project(launchpad, "Change your launchpad project")

