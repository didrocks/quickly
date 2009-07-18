# -*- coding: utf-8 -*-

try:
    import DistUtilsExtra.auto
except ImportError:
    import sys
    print >> sys.stderr, 'To build Apport you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)

assert DistUtilsExtra.auto.__version__ >= '2.6', 'needs DistUtilsExtra.auto >= 2.6'


DistUtilsExtra.auto.setup(
    name='project_name',
    version='0.1',
    license='GPL v3',
    #author='Your Name',
    #author_email='email@ubuntu.com',
    #description='UI for managing …',
    #long_description='Here a longer description'
    #url='https://launchpad.net/project_name',
    )

