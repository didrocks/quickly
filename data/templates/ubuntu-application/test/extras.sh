#!/bin/sh

cd /tmp

rm -rf test-project*

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

(echo "Copyright (C) 2010 Oliver Twist <twist@example.com>" > AUTHORS)

quickly license GPL-3

quickly package --extras | sed 's/^\.\+//'
# Ubuntu packaging created in debian/
# Ubuntu package has been successfully created in ../test-project_0.1_all.deb

ls debian
# changelog
# compat
# control
# copyright
# rules

ls ../test-project_0.1.dsc ../test-project_0.1.tar.gz ../test-project_0.1_all.deb
# ../test-project_0.1_all.deb
# ../test-project_0.1.dsc
# ../test-project_0.1.tar.gz

## Now we want to verify that we installed things in the right place

mkdir unpacked

cd unpacked

ar p ../../test-project_0.1_all.deb data.tar.gz | tar xz

ls -F .
# opt/
# usr/

ls -F ./opt
# extras.ubuntu.com/

ls -F ./opt/extras.ubuntu.com
# test-project/

ls -F ./opt/extras.ubuntu.com/test-project
# bin/
# share/
# test_project/
# test_project-0.1.egg-info
# test_project_lib/

ls -F ./opt/extras.ubuntu.com/test-project/bin
# test-project*

ls -F ./opt/extras.ubuntu.com/test-project/share
# glib-2.0/
# gnome/
# test-project/

ls -F ./usr
# share/

ls -F ./usr/share
# applications/
# doc/
# python/

ls -F ./usr/share/applications
# extras-test-project.desktop

## Now confirm the contents of some of these files

cat ./usr/share/applications/extras-test-project.desktop
# [Desktop Entry]
# Name=Test Project
# Comment=TestProject application
# Categories=GNOME;Utility;
# Exec=/opt/extras.ubuntu.com/test-project/bin/test-project
# Icon=/opt/extras.ubuntu.com/test-project/share/test-project/media/test-project.svg
# Terminal=false
# Type=Application

grep -Rh "__test_project_data_directory__ = " ./opt/extras.ubuntu.com/test-project
# __test_project_data_directory__ = '/opt/extras.ubuntu.com/test-project/share/test-project/'
