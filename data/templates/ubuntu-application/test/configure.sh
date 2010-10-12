#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

## Test configure lp-project

grep url= setup.py
#     #url='https://launchpad.net/test-project',

grep website data/ui/AboutTestProjectDialog.ui
#     <property name="website"></property>

grep lp_id .quickly

quickly configure lp-project gpoweroff
# Get Launchpad Settings
# Launchpad connection is ok
# Creating new apport crashdb configuration
# Creating new apport hooks

grep lp_id .quickly
# lp_id = gpoweroff

grep url= setup.py
#     url='https://launchpad.net/gpoweroff',

grep website data/ui/AboutTestProjectDialog.ui
#     <property name="website">https://launchpad.net/gpoweroff</property>

quickly configure lp-project hudson-notifier
# Get Launchpad Settings
# Launchpad connection is ok
# Updating project name references in existing apport crashdb configuration

grep lp_id .quickly
# lp_id = hudson-notifier

grep url= setup.py
#     url='https://launchpad.net/hudson-notifier',

grep website data/ui/AboutTestProjectDialog.ui
#     <property name="website">https://launchpad.net/hudson-notifier</property>

## Test configure bzr

quickly configure bzr
# Usage is: $ quickly configure bzr <bzr-branch-string>

quickly configure bzr 1 2
# Usage is: $ quickly configure bzr <bzr-branch-string>

grep bzrbranch .quickly

quickly configure bzr lp:gpoweroff

grep bzrbranch .quickly
# bzrbranch = lp:gpoweroff

quickly configure bzr lp:hudson-notifier

grep bzrbranch .quickly
# bzrbranch = lp:hudson-notifier

## Test configure target_distribution

quickly configure target_distribution
# Usage is: $ quickly configure target_distribution <ubuntu-release-name>

quickly configure target_distribution 1 2
# Usage is: $ quickly configure target_distribution <ubuntu-release-name>

grep target_distribution .quickly

## For the eventual Quickly Quetzal release

quickly configure target_distribution quickly

grep target_distribution .quickly
# target_distribution = quickly

quickly configure target_distribution slowly

grep target_distribution .quickly
# target_distribution = slowly

## TODO: ppa and dependencies
