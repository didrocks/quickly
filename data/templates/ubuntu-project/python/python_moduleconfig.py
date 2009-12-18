# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# THIS IS camel_case_name CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch until you know what you're doing.
# you're warned :)

# where your project will head for your data (for instance, images and ui files)
# by default, this is ../data, relative your trunk layout
__python_module_data_directory__ = '../data/'


import os

class project_path_not_found(Exception):
    pass

def getdatapath():
    """Retrieve project_name data path

    This path is by default <project_name_lib_path>/../data/ in trunk
    and /usr/share/project_name in an installed version but this path
    is specified at installation time.
    """

    # get pathname absolute or relative
    if __python_module_data_directory__.startswith('/'):
        pathname = __python_module_data_directory__
    else:
        pathname = os.path.dirname(__file__) + '/' + __python_module_data_directory__

    abs_data_path = os.path.abspath(pathname)
    if os.path.exists(abs_data_path):
        return abs_data_path
    else:
        raise project_path_not_found

