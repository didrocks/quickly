import unittest
import sys
import os
import tempfile

# need to set up the paths so the internals will work as expected
path_to_template = os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
path_to_quickly_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
sys.path.insert(0, path_to_quickly_root)
sys.path.insert(0, path_to_template)

from internal import bzrutils

class TestBzrUtils(unittest.TestCase):

    def test_unversioned_file(self):
        (file_handle, file_name) = tempfile.mkstemp()
        self.assertFalse(bzrutils.is_file_versioned(file_name))
        os.remove(file_name)

    def test_versioned_file(self):
        self.assertTrue(bzrutils.is_file_versioned(__file__))

unittest.main()
