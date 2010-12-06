#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import unittest
import sys
import os
import gtk

proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","project_root"))
sys.path.insert(0, proj_root)

from python import BuilderGlue
from python.helpers import ui

# Clean up after ourselves
os.remove(os.path.join(proj_root, 'python', '__init__.pyc'))
os.remove(os.path.join(proj_root, 'python', 'BuilderGlue.pyc'))

class TestBuilderGlue(unittest.TestCase):
    def setUp(self):
        self.builder = BuilderGlue.Architect()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), 'test.ui'))

    def test_interface(self):
        builder = dir(gtk.Builder)
        
        # sanity test
        self.assertTrue('add_from_file' in builder)
        
        # any name clashes ?
        self.assertTrue('widgets' not in builder)
        self.assertTrue('ui' not in builder)
        self.assertTrue('_glade_handlers' not in builder)
        self.assertTrue('_reverse' not in builder)
        self.assertTrue('get_name' not in builder)

    def test_iterate(self):
        glue = self.builder.get_ui()
        objs = list(glue)
        objs2 = []
        for obj in glue:
            objs2.append(obj)
        self.assertTrue(len(objs) == 12)
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

@ui('widget', 'signal')
def widgetname_as_string(*args, **kwargs):
    pass

@ui(('up', 'down', 'left', 'right'), 'clicked')
def widgetnames_as_tuple(*args, **kwargs):
    pass

@ui(['up', 'down', 'left', 'right'], 'clicked')
def widgetnames_as_list(*args, **kwargs):
    pass

class TestDecorator(unittest.TestCase):

    def test_widgetname_as_string(self):
        connection_dict = widgetname_as_string.signals
        self.assertEqual(connection_dict, {'signal': ['widget']})

    def test_widgetnames_as_tuple(self):
        connection_dict = widgetnames_as_tuple.signals
        self.assertEqual(connection_dict, {'clicked': ['up', 'down', 'left', 'right']})

    def test_widgetnames_as_list(self):
        connection_dict = widgetnames_as_list.signals
        self.assertEqual(connection_dict, {'clicked': ['up', 'down', 'left', 'right']})

unittest.main()
