# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2009 Didier Roche
#
# This file is part of Quickly
#
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.

#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.

from gettext import gettext as _

def bzr_set_login(display_name, preferred_email_adress, launchpad_name=None):
    ''' try to setup bzr whoami for commit and sshing and bzr launchpad_login if provided

        launchpadname is optional if you don't want user to use launchpad in your template
        if already setup, it will not overwrite existing data
    '''
    try:
        import bzrlib.config
        from bzrlib.errors import (
            BzrError,
            )
    except ImportError, e:
        return (1, _("Bzr not properly installed %s" % e))

    config = bzrlib.config.GlobalConfig()

    # retrieve the current bzr login
    try:
        bzr_user = config.username()
    except BzrError, err:
        try:
            from bzrlib.errors import NoWhoami
        except ImportError:
            return (1, err)
        else:
            if isinstance(err, NoWhoami):
                # no bzr whoami set
                identifier = display_name + ' <' + preferred_email_adress + '>'
                config.set_user_option("email", identifier)
            else:
                return (1, err)

    # if no bzr launchpad-login set, set it now !
    if launchpad_name:
        from bzrlib.plugins.launchpad import account
        stored_username = account.get_lp_login()
        if stored_username is not None:
            # No account set yet
            launchpad_name = launchpad_name.lower()
            account.check_lp_login(launchpad_name)
            account.set_lp_login(launchpad_name)
        elif stored_username != launchpad_name:
            return (1,
                _("Stored username %s and specified username %s mismatch." % (
                    stored_username, launchpad_name)))
    return (0, "")

