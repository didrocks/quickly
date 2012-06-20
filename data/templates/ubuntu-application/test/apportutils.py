#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import unittest

import os
import sys
import StringIO
from lxml import etree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..","..")))

from internal import apportutils

class TestApportUtils(unittest.TestCase):
    def test_find_about_menu(self):
        xml_tree = etree.parse(StringIO.StringIO("""<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-requires python_name_window 1.0 -->
  <!-- interface-naming-policy project-wide -->
  <!-- interface-local-resource-path ../media -->
  <object class="camel_case_nameWindow" id="python_name_window">
    <property name="title" translatable="yes">sentence_name</property>
    <property name="icon">../media/project_name.svg</property>
    <signal name="destroy" handler="on_destroy"/>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <property name="spacing">5</property>
        <child>
          <object class="GtkMenuBar" id="menubar1">
            <property name="visible">True</property>
            <child>
              <object class="GtkMenuItem" id="menuitem4">
                <property name="visible">True</property>
                <property name="label" translatable="yes">_Help</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="testHelpMenu">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem10">
                        <property name="label">gtk-about</property>
                        <property name="visible">True</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <signal name="activate" handler="about"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>"""))
        self.assertEqual("testHelpMenu", apportutils.find_about_menu(xml_tree))

unittest.main()
