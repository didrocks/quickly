# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk
import string
import sys

class BuilderGlue:
    def __init__(self, builder, callback_obj = None):
        "Takes a gtk.Builder and makes all its objects easily accessible"

        # Hook up any signals the user defined in glade
        if callback_obj is not None:
            builder.connect_signals(callback_obj)

        # Support 'for o in self'
        def iterator():
            return iter(builder.get_objects())
        setattr(self, '__iter__', iterator)

        names = {}
        for obj in self:
            if issubclass(type(obj), gtk.Buildable):
                name = gtk.Buildable.get_name(obj)
            else:
                # The below line is the ideal, but it causes a segfault.
                # See https://bugzilla.gnome.org/show_bug.cgi?id=633727
                #name = obj.get_data('gtk-builder-name')
                # So since we can't get name, just skip this one
                continue
            names[name] = obj

        # Support self.label1
        for (name, obj) in names.items():
            if not hasattr(self, name):
                setattr(self, name, obj)

        # This function mangles non-python names into python ones (used below)
        def make_pyname(name):
            pyname = ''
            for l in name:
                if (l in string.ascii_letters or l == '_' or
                    (pyname and l in string.digits)):
                    pyname += l
                else:
                    pyname += '_'
            return pyname

        # Mangle any bad names (like with spaces or dashes) into usable ones
        for (name, obj) in names.items():
            pyname = make_pyname(name)
            if pyname != name:
                if hasattr(self, pyname):
                    print >> sys.stderr, "BuilderGlue: Not binding %s, name already exists" % pyname
                else:
                    setattr(self, pyname, obj)

