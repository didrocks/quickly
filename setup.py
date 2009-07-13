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
import os


def list_files(path_from_root):

    list_files = []
    root_setup = os.path.abspath('.') + "/"
    for root, dirs, files in os.walk(os.path.abspath(path_from_root)):
        for file in files:
            list_files.append(os.path.join(root, file).replace(root_setup, ''))
    return list_files





setup(name='quickly',
      version='0.1',
      description='quickly project handler',
      author='quickly dev team',
      author_email='quickly@lists.launchpad.net',
      url='https://launchpad.net/quickly',
      packages=['quickly'],
      data_files=[('/etc/bash_completion.d', ['completion/bash/quickly']),
                   ('quickly', list_files('templates'))],
      scripts=['src/quickly'],
      )

