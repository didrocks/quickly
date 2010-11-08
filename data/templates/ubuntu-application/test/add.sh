#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

quickly add
# ERROR: No action name provided.
# Usage:
#   quickly add dialog <dialog-name>
#   quickly add indicator

quickly add foo
# ERROR: Cannot add foo: it is not in the store
# Usage:
#   quickly add dialog <dialog-name>
#   quickly add indicator

quickly add dialog
# Usage: quickly add dialog <dialog-name>

quickly add dialog 1 2
# Usage: quickly add dialog <dialog-name>

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

rm data/ui/FooBarDialog.ui data/ui/foo_bar_dialog.xml test_project/FooBarDialog.py

quickly add indicator 1
# Usage: quickly add indicator

quickly add indicator

bzr status
# unknown:
#   test_project/indicator.py

grep new_application_indicator test_project/indicator.py
# def new_application_indicator(window):
