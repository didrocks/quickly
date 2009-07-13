#
# quickly: quickly project handler
#
# Copyright (C) 2009 Canonical Ltd.
# Copyright (C) 2009 Didier Roche
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3,
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from distutils.core import setup
from DistUtilsExtra.command import *
import os


def list_files(path_from_root):

    list_files = []
    root_setup = os.path.abspath('.') + "/"
    for root, dirs, files in os.walk(os.path.abspath(path_from_root)):
        for file in files:
            list_files.append(os.path.join(root, file).replace(root_setup, ''))
    return list_files

def return_path_files(path_from_root):

    list_path_file = []
    root_setup = os.path.abspath('.') + "/"
    for root, dirs, files in os.walk(os.path.abspath(path_from_root)):
        list_files = []
        for file in files:
            path_to_file = root.replace(root_setup, '')
            list_files.append(os.path.join(path_to_file, file))
        if list_files:
            list_path_file.append((path_to_file, list_files))
    return list_path_file

def list_data_files():

    data_files=[('/etc/bash_completion.d', ['completion/bash/quickly']),
                  ('po', list_files('po'))]
    data_files.extend(return_path_files('templates'))
    return data_files


setup(name='quickly',
      version='0.1',
      description='quickly project handler',
      author='quickly dev team',
      author_email='quickly@lists.launchpad.net',
      url='https://launchpad.net/quickly',
      packages=['quickly'],
      data_files=list_data_files(),
      scripts=['src/quickly'],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n }
      )

