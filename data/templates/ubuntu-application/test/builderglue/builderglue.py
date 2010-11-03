#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import unittest
import sys
import os
import gtk

proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","project_root"))
sys.path.insert(0, proj_root)

from python import BuilderGlue

# Clean up after ourselves
os.remove(os.path.join(proj_root, 'python', '__init__.pyc'))
os.remove(os.path.join(proj_root, 'python', 'BuilderGlue.pyc'))

class TestBuilderGlue(unittest.TestCase):
    def setUp(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), 'test.ui'))

    def test_iterate(self):
        glue = BuilderGlue.BuilderGlue(self.builder)
        objs = list(glue)
        objs2 = []
        for obj in glue:
            objs2.append(obj)
        self.assertTrue(len(objs) == 3)
        self.assertEqual(objs, objs2)

    def test_dot_access(self):
        glue = BuilderGlue.BuilderGlue(self.builder)
        # This first one is False because Builder can't provide the name of
        # such non-Buildable objects.  When we have a fix for that, we can
        # switch this to True.
        self.assertFalse(hasattr(glue, 'filefilter'))
        self.assertTrue(hasattr(glue, 'window'))
        self.assertTrue(hasattr(glue, 'label'))

unittest.main()
