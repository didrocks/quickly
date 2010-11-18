# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from gi.repository import GObject
import gtk
import string
import sys

class BuilderGlue:
    def __init__(self, builder, callback_obj = None, autoconnect = True):
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

            # Support hooking up callback functions defined in callback_obj
            if callback_obj is not None and autoconnect:
                # Now, automatically find any the user didn't specify
                sig_ids = GObject.signal_list_ids(type(obj))
                sigs = [GObject.signal_name(sid) for sid in sig_ids]
                funcs = dict(inspect.getmembers(callback_obj, inspect.ismethod))

                def connect_if_present(cb_name):
                    if cb_name in funcs:
                        obj.connect(cb_name, funcs[cb_name])

                # We avoid clearer on_OBJ_SIG pattern, because that is
                # suggested by glade, and we don't have a way to detect if
                # the user already defined a callback in glade.
                for sig in sigs:
                    connect_if_present("%s_%s_event" % (pyname, sig))
                    # Special case where callback_obj is itself a builder obj
                    if obj is callback_obj:
                        connect_if_present("%s_event" % sig)

