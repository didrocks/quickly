# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from gi.repository import GObject
import gtk
import string
import sys
import inspect
import functools
import logging

class Architect(gtk.Builder):
    ''' this "builder" keeps the build blueprints hence "Architect".
    
    Makes adding indexes, e.g. BuilderGlue, to builder easier''' 
    
    def __init__(self):
        gtk.Builder.__init__(self)
        self.widgets = {}
        self._glade_handlers = {}
        self._reverse = {}

    def _default_handler(self, handler_name, *args, **kwargs):
        # lets help the apprentice guru
        logging.warn('called missing handler %s()' % handler_name)

    def get_name(self, widget):
        ''' allows handler to get the name (id) of the calling widget
        
         this method does not appear in gtk.Builder'''
        return self._reverse.get(widget)

    def add_from_file(self, filename):
        gtk.Builder.add_from_file(self, filename)
        
        # extract data for the extra interfaces
        from xml.etree.ElementTree import ElementTree
        tree = ElementTree()
        tree.parse(filename)

        widgets = tree.getiterator("object")
        for widget in widgets:
            name = widget.attrib['id']
            self.widgets[name] = self.get_object(name)
            self._reverse[self.get_object(name)] = name

        signals = tree.getiterator("signal")
        for i in signals:
            self._glade_handlers.update({i.attrib["handler"]: None})

    def connect_signals(self, callback_obj):
        '''connect the handlers defined in glade
        
        and logs call to missing handlers'''
        methods = inspect.getmembers(callback_obj, inspect.ismethod)
        public_methods = [x for x in methods if x[0][0] != '_']
        funcs = dict(public_methods)
        
        connection_dictionary = {}
        connection_dictionary.update(self._glade_handlers)
        connection_dictionary.update(funcs)

        for item in connection_dictionary.items():
            if item[1] is None:
                # the handler is missing so reroute to _default_handler
                handler = functools.partial(
                    self._default_handler, item[0])

                connection_dictionary[item[0]] = handler

                # replace the run time warning
                logging.warn("missing handler '%s'" % item[0])

        # connect glade define handlers
        gtk.Builder.connect_signals(self, connection_dictionary)

    def get_ui(self, callback_obj=None, by_name=False):
        '''Creates the ui object with widgets as attributes
        
        connects signals by 3 methods
        this method does not appear in gtk.Builder'''
        
        result = make_ui(self.widgets)

        # Hook up any signals the user defined in glade
        if callback_obj is not None:
            # connect glade define handlers
            self.connect_signals(callback_obj)

            # connect decorated handlers
            auto_connect_by_decoration(callback_obj)

            if by_name:
                # connect using BuilderGlue automation
                auto_connect_by_name(callback_obj, self)

        return result

UNKNOWN_WIDGET, UNKNOWN_SIGNAL = 1, 2
def auto_connect_by_decoration(callback_obj):
    ''' find handlers and connect them to widgets'''
    status = 0
    builder = callback_obj.builder
    methods = inspect.getmembers(callback_obj, inspect.ismethod)
    decorated_functions = [x for x in methods if hasattr(x[1], 'signals')]
    for ob in decorated_functions:
        handler = ob[1]
        connection_dict = handler.signals
        for signal, widgets in connection_dict.items():
            for widget_name in widgets:
                widget = builder.get_object(widget_name)
                if widget is None:
                    message = '%s.builder.%s: unknown widget' % (
                    callback_obj.__class__, widget_name)
                    logging.warn(message)
                    status = UNKNOWN_WIDGET
                else:
                    try:
                        widget.connect(signal, handler)
                    except TypeError:
                        message = '%s.builder.%s.%s unknown signal' % (
                        callback_obj.__class__, widget_name, signal)
                        logging.warn(message)
                        status = UNKNOWN_SIGNAL
    return status

# below is the refactored mterry's BuilderGlue module 
# first part is the object interface
class UI_factory():
    def __init__(self, data):
        for item in data.items():
            setattr(self, item[0], item[1])

        # Support 'for o in self'
        def iterator():
            return iter(data.values())
        setattr(self, '__iter__', iterator)

def make_ui(widgets_dict):

    result = UI_factory(widgets_dict)

    # Mangle any non-usable names (like with spaces or dashes) into pythonic ones
    for (name, obj) in widgets_dict.items():
        pyname = make_pyname(name)
        if pyname != name:
            if hasattr(result, pyname):
                logging.debug("BuilderGlue: Not binding %s, name already exists" % pyname)
            else:
                setattr(result, pyname, obj)

    return result

# second part connect handlers by name
# This function mangles non-pythonic names into pythonic ones
def make_pyname(name):
    pyname = ''
    for l in name:
        if (l in string.ascii_letters or l == '_' or
            (pyname and l in string.digits)):
            pyname += l
        else:
            pyname += '_'
    return pyname

def auto_connect_by_name(callback_obj, achitect):

    methods = inspect.getmembers(callback_obj, inspect.ismethod)
    handlers = [x for x in methods if x[0].startswith('on_')]
    undecorated_handlers = [x for x in handlers if not hasattr(x[1], 'signals')]
    
    funcs = dict(undecorated_handlers)

    # test for typos in event handlers
    unconnected_funcs = funcs.keys()

    for handler in achitect._glade_handlers.keys():
        # clean glade connected handler
        unconnected_funcs.remove(handler)

    names = achitect.widgets

    for (name, obj) in names.items():
        sig_ids = []
        try:
            t = type(obj)
            while t:
                sig_ids.extend(GObject.signal_list_ids(t))
                t = GObject.type_parent(t)
        except:
            pass
        sigs = [GObject.signal_name(sid) for sid in sig_ids]
        
        # Now, automatically find any the user didn't specify
        pyname = make_pyname(name)

        def connect_if_present(sig, cb_name):
            if cb_name in unconnected_funcs:
                obj.connect(sig, funcs[cb_name])
                unconnected_funcs.remove(cb_name)

        for sig in sigs:
            # using convention suggested by glade
            connect_if_present(sig, "on_%s_%s" % (pyname, sig))

            # Using the convention that the top level window is not
            # specified in the handler name. Compare decorators for
            # on_destroy and on_quit in python_name_window
            if obj is callback_obj:
                connect_if_present(sig, "on_%s" % sig)

    for event_handler in unconnected_funcs:
        logging.debug(' Cannot autoconnect %s.%s' % (callback_obj.__class__, event_handler))

