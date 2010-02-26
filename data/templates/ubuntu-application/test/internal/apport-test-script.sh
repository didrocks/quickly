#!/bin/bash

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Created a standalone tree (format: 2a)
# adding .quickly
# adding AUTHORS
# adding bin
# adding data
# adding setup.py
# adding test-project.desktop.in
# adding test_project
# adding bin/test-project
# adding data/media
# adding data/ui
# adding test_project/AboutTestProjectDialog.py
# adding test_project/PreferencesTestProjectDialog.py
# adding test_project/__init__.py
# adding test_project/helpers.py
# adding test_project/test_projectconfig.py
# adding data/media/background.png
# adding data/media/icon.png
# adding data/media/logo.png
# adding data/media/logo.svg
# adding data/ui/AboutTestProjectDialog.ui
# adding data/ui/PreferencesTestProjectDialog.ui
# adding data/ui/TestProjectWindow.ui
# adding data/ui/about_test_project_dialog.xml
# adding data/ui/preferences_test_project_dialog.xml
# adding data/ui/test_project_window.xml
# Committing to: /tmp/test-project/
# added .quickly
# added AUTHORS
# added bin
# added data
# added setup.py
# added test-project.desktop.in
# added test_project
# added bin/test-project
# added data/media
# added data/ui
# added data/media/background.png
# added data/media/icon.png
# added data/media/logo.png
# added data/media/logo.svg
# added data/ui/AboutTestProjectDialog.ui
# added data/ui/PreferencesTestProjectDialog.ui
# added data/ui/TestProjectWindow.ui
# added data/ui/about_test_project_dialog.xml
# added data/ui/preferences_test_project_dialog.xml
# added data/ui/test_project_window.xml
# added test_project/AboutTestProjectDialog.py
# added test_project/PreferencesTestProjectDialog.py
# added test_project/__init__.py
# added test_project/helpers.py
# added test_project/test_projectconfig.py
# Committed revision 1.
# Creating project directory data
# Creating project directory bin
# Directory bin created
# 
# Creating data/ui/TestProjectWindow.ui
# data/ui/TestProjectWindow.ui created
# 
# Creating data/ui/test_project_window.xml
# data/ui/test_project_window.xml created
# 
# Creating data/ui/AboutTestProjectDialog.ui
# data/ui/AboutTestProjectDialog.ui created
# 
# Creating data/ui/about_test_project_dialog.xml
# data/ui/about_test_project_dialog.xml created
# 
# Creating data/ui/PreferencesTestProjectDialog.ui
# data/ui/PreferencesTestProjectDialog.ui created
# 
# Creating data/ui/preferences_test_project_dialog.xml
# data/ui/preferences_test_project_dialog.xml created
# 
# Creating test_project/AboutTestProjectDialog.py
# test_project/AboutTestProjectDialog.py created
# 
# Creating test_project/PreferencesTestProjectDialog.py
# test_project/PreferencesTestProjectDialog.py created
# 
# Creating test_project/test_projectconfig.py
# test_project/test_projectconfig.py created
# 
# Creating test_project/helpers.py
# test_project/helpers.py created
# 
# Creating test_project/__init__.py
# test_project/__init__.py created
# 
# Creating ./setup.py
# ./setup.py created
# 
# Creating ./test-project.desktop.in
# ./test-project.desktop.in created
# 
# Creating bin/test-project
# bin/test-project created
# 
# Creating ./AUTHORS
# ./AUTHORS created
# 
# Creating bzr repository and commiting
# Launching your newly created project!
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project
# Directory test-project created
# 

cd test-project

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connexion is ok
# Creating new apport crashdb configuration
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 
# Creating new apport hooks
# Creating apport/source_test-project.py
# apport/source_test-project.py created
# 

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

bzr status
# modified:
#   .quickly
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
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

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
#   data/ui/AboutTestProjectDialog.ui
#   setup.py

bzr commit -m "Test save"
# Committing to: /tmp/test-project/
# modified .quickly
# added apport
# added etc
# modified setup.py
# added apport/source_test-project.py
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
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

bzr status
# modified:
#   .quickly
#   data/ui/AboutTestProjectDialog.ui
#   etc/apport/crashdb.conf.d/test-project-crashdb.conf
#   setup.py

bzr commit -m "Renaming hooks"
# Committing to: /tmp/test-project/
# modified .quickly
# modified setup.py
# modified data/ui/AboutTestProjectDialog.ui
# modified etc/apport/crashdb.conf.d/test-project-crashdb.conf
# Committed revision 3.

rm -rf apport

quickly configure lp-project hudson-notifier
# Get Launchpad Settings
# Launchpad connexion is ok
# Updating project name references in existing apport crashdb configuration
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 
# Creating new apport hooks
# Creating apport/source_test-project.py
# apport/source_test-project.py created
# 

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

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
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

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
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 
# Creating new apport hooks
# Creating apport/source_test-project.py
# apport/source_test-project.py created
# 

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
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 

bzr status
# modified:
#   .quickly
#   data/ui/AboutTestProjectDialog.ui
#   etc/apport/crashdb.conf.d/test-project-crashdb.conf
#   setup.py

bzr commit -m "Prior to upgrade"
# Committing to: /tmp/test-project/
# modified .quickly
# modified setup.py
# modified data/ui/AboutTestProjectDialog.ui
# modified etc/apport/crashdb.conf.d/test-project-crashdb.conf
# Committed revision 4.

quickly upgrade

bzr status
# modified:
#   test_project/test_projectconfig.py

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
# modified test_project/test_projectconfig.py
# Committed revision 5.

bzr status

quickly upgrade
# Creating new apport crashdb configuration
# Creating etc/apport/crashdb.conf.d/test-project-crashdb.conf
# etc/apport/crashdb.conf.d/test-project-crashdb.conf created
# 
# Creating new apport hooks
# Creating apport/source_test-project.py
# apport/source_test-project.py created
# 

grep LaunchpadIntegration.set_sourcepackagename bin/test-project
#         LaunchpadIntegration.set_sourcepackagename('test-project')

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
