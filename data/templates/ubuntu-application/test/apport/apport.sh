#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and commiting
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connection is ok
# Creating new apport crashdb configuration
# Creating new apport hooks

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

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
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

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
# # -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

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
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration
# Creating new apport hooks

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

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
# # -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

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
# # -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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
# # -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration
# Creating new apport hooks

cat apport/source_test-project.py
# # Apport integration for test-project
# #
# # -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration

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

quickly upgrade 0.3 0.4

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

quickly upgrade 0.3 0.4
# Creating new apport crashdb configuration
# Creating new apport hooks

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

grep helpmenu bin/test-project
#             helpmenu = self.builder.get_object('helpMenu')
#             if helpmenu:
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

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
# # -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
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

cp "$TEST_SCRIPT_DIR/test-project.no_lpi" ./bin/test-project

cp "$TEST_SCRIPT_DIR/TestProjectWindow.ui.renamed_help_menu" ./data/ui/TestProjectWindow.ui

rm -rf apport

rm -rf etc

grep LaunchpadIntegration. bin/test-project

grep helpmenu bin/test-project

quickly upgrade 0.3 0.4
# Adding launchpad integration to existing application
# Creating new apport crashdb configuration
# Creating new apport hooks

grep LaunchpadIntegration. bin/test-project
#                 LaunchpadIntegration.set_sourcepackagename('test-project')
#                 LaunchpadIntegration.add_items(helpmenu, 0, False, True)

cp "$TEST_SCRIPT_DIR/test-project.no_lpi" ./bin/test-project

cp "$TEST_SCRIPT_DIR/TestProjectWindow.ui.no_gtk-about" ./data/ui/TestProjectWindow.ui

rm -rf apport

rm -rf etc

grep LaunchpadIntegration. bin/test-project

grep helpmenu bin/test-project

grep gtk-about data/ui/TestProjectWindow.ui

bzr commit -m "Committing after removing all lpi integration"
# Committing to: /tmp/test-project/
# modified bin/test-project
# modified data/ui/TestProjectWindow.ui
# Committed revision 6.

quickly upgrade 0.3 0.4
# Creating new apport crashdb configuration
# Creating new apport hooks

grep LaunchpadIntegration. bin/test-project

grep helpmenu bin/test-project

bzr status
# unknown:
#   apport/
#   etc/

cp "$TEST_SCRIPT_DIR/test-project.no_lpi" ./bin/test-project

rm ./data/ui/TestProjectWindow.ui

grep LaunchpadIntegration. bin/test-project

grep helpmenu bin/test-project

quickly upgrade 0.3 0.4
