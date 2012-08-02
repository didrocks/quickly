#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-cli test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

sed -i 's/import os/import os #test-blarg/' setup.py

(echo "#test-blarg" >> setup.py)

(echo "#test-blarg" >> bin/test-project)

(echo "#test-blarg" >> test_project/__init__.py)

grep -R "#test-blarg" .
# ./setup.py:import os #test-blarg
# ./setup.py:#test-blarg
# ./bin/test-project:#test-blarg
# ./test_project/__init__.py:#test-blarg

quickly upgrade 11.04

grep -R "#test-blarg" .
# ./setup.py:#test-blarg
# ./test_project/__init__.py:#test-blarg
