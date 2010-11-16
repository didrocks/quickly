#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

bzr status

bzr ls -R
# .quickly
# AUTHORS
# bin/
# bin/test-project
# data/
# data/media/
# data/media/background.png
# data/media/icon.png
# data/media/logo.png
# data/media/logo.svg
# data/ui/
# data/ui/AboutTestProjectDialog.ui
# data/ui/PreferencesTestProjectDialog.ui
# data/ui/TestProjectWindow.ui
# data/ui/about_test_project_dialog.xml
# data/ui/preferences_test_project_dialog.xml
# data/ui/test_project_window.xml
# setup.py
# test-project.desktop.in
# test_project/
# test_project/AboutTestProjectDialog.py
# test_project/BaseTestProjectWindow.py
# test_project/BuilderGlue.py
# test_project/PreferencesTestProjectDialog.py
# test_project/__init__.py
# test_project/helpers.py
# test_project/test_projectconfig.py