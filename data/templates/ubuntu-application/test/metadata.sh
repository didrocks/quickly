#!/bin/sh

cd /tmp

rm -rf test-project

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

quickly package --extras | sed 's/^\.\+//'
# Ubuntu packaging created in debian/
# Ubuntu package has been successfully created in ../test-project_0.1_all.deb

grep -C1 "^XB-" debian/control | sed "s/project-$(lsb_release -c | cut -f2)*\./project-RELEASE./"
# Architecture: all
# XB-Python-Version: ${python:Versions}
# XB-AppName: Test Project
# XB-Category: GNOME;Utility;
# XB-Screenshot-Url: https://software-center.ubuntu.com/screenshots/t/test-project-RELEASE.png
# XB-Thumbnail-Url: https://software-center.ubuntu.com/screenshots/t/test-project-RELEASE.thumb.png
# XB-Icon: test-project.svg
# Depends: ${misc:Depends},

cat debian/rules
# #!/usr/bin/make -f
# %:
# ifneq ($(shell dh -l | grep -xF translations),)
# 	dh $@ --with python2,translations
# else
# 	dh $@ --with python2
# endif
# 
# override_dh_auto_install:
# 	dh_auto_install -- --install-scripts=/opt/extras.ubuntu.com/test-project                 --install-lib=/opt/extras.ubuntu.com/test-project
# 
# override_dh_python2:
# 	dh_python2 /opt/extras.ubuntu.com/test-project
# 
# 
# override_dh_install::
# 	dh_install
# 	cp data/media/test-project.svg ../test-project.svg
# 	dpkg-distaddfile test-project.svg raw-meta-data -

## Older versions of quickly had logo.svg instead of project_name.svg, so test those too

mv data/media/test-project.svg data/media/logo.svg

quickly package --extras | sed 's/^\.\+//'
# Ubuntu packaging created in debian/
# Ubuntu package has been successfully created in ../test-project_0.1_all.deb

grep XB-Icon debian/control
# XB-Icon: test-project.svg

tail -n 4 debian/rules
# override_dh_install::
# 	dh_install
# 	cp data/media/logo.svg ../test-project.svg
# 	dpkg-distaddfile test-project.svg raw-meta-data -

## Finally, make sure we gracefully handle no icon at all

rm data/media/logo.svg

quickly package --extras | sed 's/^\.\+//'
# Ubuntu packaging created in debian/
# Ubuntu package has been successfully created in ../test-project_0.1_all.deb

grep XB-Icon debian/control

grep dpkg-distaddfile debian/rules
