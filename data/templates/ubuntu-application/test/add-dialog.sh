#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and commiting
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

bzr status

quickly add dialog foo-bar

bzr status
# unknown:
#   data/ui/FooBarDialog.ui
#   data/ui/foo_bar_dialog.xml
#   test_project/FooBarDialog.py

cat data/ui/foo_bar_dialog.xml
# <glade-catalog name="foo_bar_dialog" domain="glade-3" 
#                depends="gtk+" version="1.0">
#   <glade-widget-classes>
#     <glade-widget-class title="Foo Bar Dialog" name="FooBarDialog" 
#                         generic-name="foo_bar_dialog" parent="GtkDialog"
#                         icon-name="widget-gtk-dialog"/>
#   </glade-widget-classes>
# 
# </glade-catalog>
