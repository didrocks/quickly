#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

bzr status

quickly add indicator

bzr status
# unknown:
#   test_project/indicator.py

grep new_application_indicator test_project/indicator.py
# def new_application_indicator(window):
