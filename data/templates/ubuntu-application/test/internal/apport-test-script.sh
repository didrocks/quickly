#!/bin/bash

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and commiting
# Launching your newly created project!
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('test-project')

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connexion is ok
# Creating new apport crashdb configuration
# Creating new apport hooks
# Updating launchpad integration references in existing application

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('gpoweroff')

bzr status
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   setup.py
# unknown:
#   apport/
#   etc/

bzr add
# adding apport
# adding etc
# adding apport/source_test-project.py
# adding etc/apport
# adding etc/apport/crashdb.conf.d
# adding etc/apport/crashdb.conf.d/test-project-crashdb.conf

quickly configure lp-project hudson-notifier
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Updating launchpad integration references in existing application

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('hudson-notifier')

bzr status
# added:
#   apport/
#   apport/source_test-project.py
#   etc/
#   etc/apport/
#   etc/apport/crashdb.conf.d/
#   etc/apport/crashdb.conf.d/test-project-crashdb.conf
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   setup.py

bzr commit -m "Test save"
# Committing to: /tmp/test-project/
# modified .quickly
# added apport
# added etc
# modified setup.py
# added apport/source_test-project.py
# modified bin/test-project
# modified data/ui/AboutTestProjectDialog.ui
# added etc/apport
# added etc/apport/crashdb.conf.d
# added etc/apport/crashdb.conf.d/test-project-crashdb.conf
# Committed revision 2.

cat etc/apport/crashdb.conf.d/test-project-crashdb.conf
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# 
# test_project = {
#         'impl' : 'launchpad',
#         'project' : 'hudson-notifier',
#         'bug_pattern_base' : None,
# }

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- coding: utf-8 -*-
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# import apport
# 
# def add_info(report):
#     """add report info"""
# 
#     if not apport.packaging.is_distro_package(report['Package'].split()[0]):
#         report['ThirdParty'] = 'True'
#         report['CrashDB'] = 'test_project'

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Updating launchpad integration references in existing application

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('gpoweroff')

bzr status
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   etc/apport/crashdb.conf.d/test-project-crashdb.conf
#   setup.py

bzr commit -m "Renaming hooks"
# Committing to: /tmp/test-project/
# modified .quickly
# modified setup.py
# modified bin/test-project
# modified data/ui/AboutTestProjectDialog.ui
# modified etc/apport/crashdb.conf.d/test-project-crashdb.conf
# Committed revision 3.

rm -rf apport

quickly configure lp-project hudson-notifier
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Creating new apport hooks
# Updating launchpad integration references in existing application

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('hudson-notifier')

cat etc/apport/crashdb.conf.d/test-project-crashdb.conf
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# 
# test_project = {
#         'impl' : 'launchpad',
#         'project' : 'hudson-notifier',
#         'bug_pattern_base' : None,
# }

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- coding: utf-8 -*-
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# import apport
# 
# def add_info(report):
#     """add report info"""
# 
#     if not apport.packaging.is_distro_package(report['Package'].split()[0]):
#         report['ThirdParty'] = 'True'
#         report['CrashDB'] = 'test_project'

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Updating launchpad integration references in existing application

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('gpoweroff')

cat etc/apport/crashdb.conf.d/test-project-crashdb.conf
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# 
# test_project = {
#         'impl' : 'launchpad',
#         'project' : 'gpoweroff',
#         'bug_pattern_base' : None,
# }

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- coding: utf-8 -*-
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# import apport
# 
# def add_info(report):
#     """add report info"""
# 
#     if not apport.packaging.is_distro_package(report['Package'].split()[0]):
#         report['ThirdParty'] = 'True'
#         report['CrashDB'] = 'test_project'

bzr status

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- coding: utf-8 -*-
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# import apport
# 
# def add_info(report):
#     """add report info"""
# 
#     if not apport.packaging.is_distro_package(report['Package'].split()[0]):
#         report['ThirdParty'] = 'True'
#         report['CrashDB'] = 'test_project'

rm apport/source_test-project.py

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Creating new apport hooks
# Updating launchpad integration references in existing application

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- coding: utf-8 -*-
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# import apport
# 
# def add_info(report):
#     """add report info"""
# 
#     if not apport.packaging.is_distro_package(report['Package'].split()[0]):
#         report['ThirdParty'] = 'True'
#         report['CrashDB'] = 'test_project'

quickly configure lp-project hudson-notifier
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Updating launchpad integration references in existing application

bzr status
# modified:
#   .quickly
#   bin/test-project
#   data/ui/AboutTestProjectDialog.ui
#   etc/apport/crashdb.conf.d/test-project-crashdb.conf
#   setup.py

bzr commit -m "Prior to upgrade"
# Committing to: /tmp/test-project/
# modified .quickly
# modified setup.py
# modified bin/test-project
# modified data/ui/AboutTestProjectDialog.ui
# modified etc/apport/crashdb.conf.d/test-project-crashdb.conf
# Committed revision 4.

quickly upgrade

bzr status

rm -rf apport

rm -rf etc

bzr commit -m "Re-running upgrade again"
# Committing to: /tmp/test-project/
# missing apport
# modified apport
# missing etc
# modified etc
# missing apport/source_test-project.py
# modified apport/source_test-project.py
# missing etc/apport
# modified etc/apport
# missing etc/apport/crashdb.conf.d
# modified etc/apport/crashdb.conf.d
# missing etc/apport/crashdb.conf.d/test-project-crashdb.conf
# modified etc/apport/crashdb.conf.d/test-project-crashdb.conf
# Committed revision 5.

bzr status

quickly upgrade
# Creating new apport crashdb configuration
# Creating new apport hooks
# Updating launchpad integration references in existing application

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#             LaunchpadIntegration.set_sourcepackagename('hudson-notifier')

cat etc/apport/crashdb.conf.d/test-project-crashdb.conf
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# 
# test_project = {
#         'impl' : 'launchpad',
#         'project' : 'hudson-notifier',
#         'bug_pattern_base' : None,
# }

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- coding: utf-8 -*-
# ### BEGIN LICENSE
# # This file is in the public domain
# ### END LICENSE
# import apport
# 
# def add_info(report):
#     """add report info"""
# 
#     if not apport.packaging.is_distro_package(report['Package'].split()[0]):
#         report['ThirdParty'] = 'True'
#         report['CrashDB'] = 'test_project'
