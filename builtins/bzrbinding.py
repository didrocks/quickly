# -*- coding: utf-8 -*-

import socket
import subprocess

def bzr_set_login(display_name, preferred_email_adress):
  ''' try to setup bzr whoami for commit and sshing

      if already setup, it will not overwrite it
  '''

  #try:

  #retreive the current bzr login
  bzr_instance = subprocess.Popen(["bzr", "whoami"], stdout=subprocess.PIPE)
  bzr_user = bzr_instance.stdout.read()

  #if no bzr whoami set, the default contain the @hostname string
  if '@' + socket.gethostname() in bzr_user:
    identifier = display_name + ' <' + preferred_email_adress + '>'
    subprocess.call(["bzr", "whoami", identifier])

  #except TRY WITHOUT bzr installed

  
