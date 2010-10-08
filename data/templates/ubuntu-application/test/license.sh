#!/bin/sh

cd /tmp

rm -rf test-project*

quickly create ubuntu-application test-project
# Creating bzr repository and committing
# Congrats, your new project is setup! cd /tmp/test-project/ to start hacking.
# Creating project directory test-project

cd test-project

quickly license
# ERROR: Copyright is not attributed. Edit the AUTHORS file to include your name for the copyright replacing <Your Name> <Your E-mail>. Update it in setup.py or use quickly share/quickly release to fill it automatically

quickly license GPL-2 GPL-3
# ERROR: This command only take one optional argument: License
# Usage is: quickly license <license>

(echo "Copyright (C) 2010 Oliver Twist <twist@example.com>" > AUTHORS)

(echo "This file is licensed under the OTL (Oliver Twist License)" > COPYING)

quickly license

grep license= setup.py
#     license='custom',

grep "Oliver Twist License" setup.py
# # This file is licensed under the OTL (Oliver Twist License)

cat COPYING
# This file is licensed under the OTL (Oliver Twist License)

sed -i "s/license=.*,/license='GPL-2',/" setup.py

quickly license

grep license= setup.py
#     license='GPL-2',

grep "General Public License version" setup.py
# # under the terms of the GNU General Public License version 2, as published 

grep -A 1 -m 1 "GENERAL PUBLIC LICENSE" COPYING
# 		    GNU GENERAL PUBLIC LICENSE
# 		       Version 2, June 1991

quickly license GPL-3

grep license= setup.py
#     license='GPL-3',

grep "General Public License version" setup.py
# # under the terms of the GNU General Public License version 3, as published 

grep -A 1 -m 1 "GENERAL PUBLIC LICENSE" COPYING
# 		    GNU GENERAL PUBLIC LICENSE
# 		       Version 3, 29 June 2007
