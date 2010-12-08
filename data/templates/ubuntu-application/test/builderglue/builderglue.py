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
        self.builder = BuilderGlue.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), 'test.ui'))

    def test_interface(self):
        builder = dir(gtk.Builder)
        
        # sanity test
        self.assertTrue('add_from_file' in builder)
        
        # any name clashes ?
        self.assertTrue('widgets' not in builder)
        self.assertTrue('get_ui' not in builder)
        self.assertTrue('glade_handlers' not in builder)
        self.assertTrue('_reverse' not in builder)
        self.assertTrue('get_name' not in builder)

    def test_iterate(self):
        glue = self.builder.get_ui()
        objs = list(glue)
        objs2 = []
        for obj in glue:
            objs2.append(obj)
        self.assertTrue(len(objs) == 6)
        self.assertEqual(objs, objs2)

    def test_dot_access(self):
        glue = self.builder.get_ui()
        
        self.assertTrue(hasattr(glue, 'filefilter'))
        self.assertTrue(hasattr(glue, 'window'))
        self.assertTrue(hasattr(glue, 'label'))
        self.assertTrue(hasattr(glue, 'wind?o-w two'))
        self.assertTrue(hasattr(glue, 'wind_o_w_two'))
        # Many glade names match one pythonic name
        self.assertFalse(getattr(glue, 'wind?o-w two') == getattr(glue, 'wind_o_w_two'))
        self.assertTrue(hasattr(glue, '1wind-o w/3'))
        self.assertTrue(hasattr(glue, '_wind_o_w_3'))
        self.assertTrue(getattr(glue, '1wind-o w/3') == getattr(glue, '_wind_o_w_3'))

unittest.main()
