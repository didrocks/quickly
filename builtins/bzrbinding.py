# -*- coding: utf-8 -*-


import subprocess

def bzr_set_login(login):

  #try:
  subprocess.call(["bzr", "launchpad-login", login])
  #except TRY WITHOUT bzr installed

  
