#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

## Just a nothing command to run implicit upgrade

quickly configure bzr testing

grep '11\.10' .quickly

quickly upgrade

sed -i 's/version = .*/version = 11.10/' .quickly

grep '11\.10' .quickly
# version = 11.10

quickly configure bzr testing
# WARNING: Your project is out of date.  Newly created projects use
# GTK+ 3, PyGI, and GSettings.  See https://wiki.ubuntu.com/Quickly/GTK3 for
# porting information and when you have finished porting your code, run
# 'quickly upgrade' to get rid of this message.

grep '11\.10' .quickly
# version = 11.10

quickly upgrade

grep '11\.10' .quickly

quickly configure bzr testing

quickly upgrade

quickly configure bzr testing
