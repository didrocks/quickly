#!/bin/sh

cd /tmp

rm -rf test-project

rm -rf subdir

quickly create
# ERROR: create command must be followed by a template and no template was found on the command line.
# Candidates template are: ubuntu-pygame, ubuntu-application, ubuntu-cli
# Aborting.

quickly create ubuntu-application
# ERROR: Create command must be followed by a template and a project path.
# Usage: quickly create <template> <project-name>

quickly create ubuntu-application 42
# ERROR: unpermitted character in name.
# The name must start with a letter and contain only letters, spaces, dashes (-), and digits.

quickly create ubuntu-application test_project
# ERROR: unpermitted character in name.
# The name must start with a letter and contain only letters, spaces, dashes (-), and digits.

quickly create ubuntu-application test-pröject
# ERROR: unpermitted character in name.
# The name must start with a letter and contain only letters, spaces, dashes (-), and digits.

quickly create ubuntu-application "test project"
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

quickly create ubuntu-application test-project
# There is already a file or directory named test-project
# ERROR: pre_create command failed
# Aborting

quickly create ubuntu-application subdir/test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/subdir/test-project/ to start hacking.
# Creating project directory test-project
