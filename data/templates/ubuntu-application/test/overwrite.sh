#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

sed -i 's/import os/import os #test-blarg/' setup.py

(echo "#test-blarg" >> setup.py)

(echo "#test-blarg" >> bin/test-project)

(echo "#test-blarg" >> test_project/TestProjectWindow.py)

(echo "#test-blarg" >> test_project_lib/Window.py)

rm test_project_lib/Builder.py

cp -a test_project_lib/helpers.py test_project_lib/helpers.py.test-bak

grep -R "#test-blarg" .
# ./test_project_lib/Window.py:#test-blarg
# ./setup.py:import os #test-blarg
# ./setup.py:#test-blarg
# ./bin/test-project:#test-blarg
# ./test_project/TestProjectWindow.py:#test-blarg

quickly upgrade 11.04
# Note: Quickly is upgrading its files (bin/*, test_project_lib/*, and setup.py).
# But first it will save your project.  View Quickly's changes by running:
# bzr diff

(test "$(ls --full-time test_project_lib/helpers.py)" = "$(ls --full-time test_project_lib/helpers.py.test-bak | sed 's/\.test-bak//')" && echo "Same")
# Same

ls test_project_lib/Builder.py
# test_project_lib/Builder.py

grep -R "#test-blarg" .
# ./setup.py:#test-blarg
# ./test_project/TestProjectWindow.py:#test-blarg

grep python_name setup.py test_project_lib/Builder.py

## A run to see if we futz with setup.py when we don't need to

cp -a setup.py setup.py.test-bak

rm test_project_lib/Builder.py

quickly upgrade 11.04
# Note: Quickly is upgrading its files (bin/*, test_project_lib/*, and setup.py).
# But first it will save your project.  View Quickly's changes by running:
# bzr diff

(test "$(ls --full-time setup.py)" = "$(ls --full-time setup.py.test-bak | sed 's/\.test-bak//')" && echo "Same")
# Same

ls test_project_lib/Builder.py
# test_project_lib/Builder.py

## A run to see if we change anything when version hasn't changed

rm test_project_lib/Builder.py

quickly upgrade

ls test_project_lib/Builder.py
# ls: cannot access test_project_lib/Builder.py: No such file or directory
