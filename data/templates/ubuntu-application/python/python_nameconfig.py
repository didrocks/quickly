# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# THIS IS camel_case_name CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch unless you know what you're doing.
# you're warned :)

# Where your project will look for your data (for instance, images and ui
# files). By default, this is ../data, relative your trunk layout
__python_name_data_directory__ = '../data/'
__license__ = ''

import os


class project_path_not_found(Exception):
    pass


def getdatapath():
    """Retrieve project_name data path

    This path is by default <python_name_lib_path>/../data/ in trunk
    and /usr/share/project_name in an installed version but this path
    is specified at installation time.
    """

    # get pathname absolute or relative
    path = os.path.join(
        os.path.dirname(__file__), __python_name_data_directory__)

    abs_data_path = os.path.abspath(path)
    if not os.path.exists(abs_data_path):
        raise project_path_not_found

    return abs_data_path
