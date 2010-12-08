# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

'''Enhances builder connections, provides object to access glade objects'''


from gi.repository import GObject # pylint: disable=E0611

import gtk
import inspect
import functools
import logging

# pylint: disable=R0904
# the many public methods is a feature of gtk.Builder
#  so not a fault in Builder
class Builder(gtk.Builder):
    ''' extra features
    connects glade defined handler to default_handler if necessary
    auto connects handlers to several widgets via signals attribute
    auto connects handler to widget with similar name
    allow handlers to lookup widget name
    ''' 
    
    def __init__(self):
        gtk.Builder.__init__(self)
        self.widgets = {}
        self.glade_handlers = {}
        self._reverse = {}
        
# pylint: disable=W0613
# we don't use variables args or kwargs, but we accept any parameters
# pylint: disable=R0201
# this is a method so that a subclass of Builder can redefine it
    def default_handler(self,
     handler_name, filename, *args, **kwargs):
        '''helps the apprentice guru
        
    glade defined handlers that do not exist come here instead.
    An apprentice guru might wonder which signal does what he wants,
    now he can define any likely candidates in glade and notice which
    ones get triggered when he plays with the project.'''
        
        logging.warn('cannot find %s() in %s', handler_name, filename)
# pylint: enable=R0201
# pylint: enable=W0613

    def get_name(self, widget):
        ''' allows a handler to get the name (id) of a widget
        
        this method does not appear in gtk.Builder'''
        return self._reverse.get(widget)

    def add_from_file(self, filename):
        '''parses xml file and stores wanted details'''
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
            self.glade_handlers.update({i.attrib["handler"]: None})

    def connect_signals(self, callback_obj):
        '''connect the handlers defined in glade
        
        and logs call to missing handlers'''
        filename = inspect.getfile(callback_obj.__class__)
        methods = inspect.getmembers(callback_obj, inspect.ismethod)
        public_methods = [x for x in methods if x[0][0] != '_']
        funcs = dict(public_methods)
        
        connection_dictionary = {}
        connection_dictionary.update(self.glade_handlers)
        connection_dictionary.update(funcs)

        for item in connection_dictionary.items():
            if item[1] is None:
                # the handler is missing so reroute to default_handler
                handler = functools.partial(
                    self.default_handler, item[0], filename)

                connection_dictionary[item[0]] = handler

                # replace the run time warning
                logging.warn("expected handler '%s' in %s",
                 item[0], filename)

        # connect glade define handlers
        gtk.Builder.connect_signals(self, connection_dictionary)

    def get_ui(self, callback_obj=None, by_name=False):
        '''Creates the ui object with widgets as attributes
        
        connects signals by 2 methods
        this method does not appear in gtk.Builder'''
        
        result = Uifactory(self.widgets)

        # Hook up any signals the user defined in glade
        if callback_obj is not None:
            # connect glade define handlers
            self.connect_signals(callback_obj)

            if by_name:
                auto_connect_by_name(callback_obj, self)

        return result


# object interface
# pylint: disable=R0903
# this class deliberately does not provide any public interfaces
# apart from the glade widgets
class Uifactory():
    ''' provides an object with attributes as glade widgets'''
    def __init__(self, data):
        for item in data.items():
            setattr(self, item[0], item[1])

        # Mangle any non-usable names (like with spaces or dashes)
        # into pythonic ones
        for (name, obj) in data.items():
            pyname = make_pyname(name)
            if pyname != name:
                if hasattr(self, pyname):
                    logging.debug(
                    "Builder: Not binding %s, name already exists", pyname)
                else:
                    setattr(self, pyname, obj)

        def iterator():
            '''Support 'for o in self' '''
            return iter(data.values())
        setattr(self, '__iter__', iterator)
# pylint: enable=R0903

def make_pyname(name):
    ''' mangles non-pythonic names into pythonic ones'''
    pyname = ''
    for character in name:
        if (character.isalpha() or character == '_' or
            (pyname and character.isdigit())):
            pyname += character
        else:
            pyname += '_'
    return pyname

def parse_callback_obj(callback_obj):
    '''a dictionary interface to callback_obj'''
    methods = inspect.getmembers(callback_obj, inspect.ismethod)
    handlers = [x for x in methods if x[0].startswith('on_')]
    simple_handlers = [x for x in handlers if not hasattr(x[1], 'signals')]
    
    funcs = dict(simple_handlers)
    return funcs

def auto_connect_by_name(callback_obj, builder):
    '''finds handlers like on_<widget_name>_<signal> and connects them

    i.e. widget.connect(signal, on_<widget_name>_<signal>)'''
    funcs = parse_callback_obj(callback_obj)

    for handler in builder.glade_handlers.keys():
        # ignore glade connected handler
        try:
            del funcs[handler]
        except KeyError:
            pass
            # glade file specifies a handler but it doesn't exist
            # in callback_obj so it cannot be removed

    for (widget_name, widget) in builder.widgets.items():
        sig_ids = []
        try:
            widget_type = type(widget)
            while widget_type:
                sig_ids.extend(GObject.signal_list_ids(widget_type))
                widget_type = GObject.type_parent(widget_type)
        except RuntimeError: # pylint want a specific error
            pass
        sigs = [GObject.signal_name(sid) for sid in sig_ids]
        
        # Now, automatically find any the user didn't specify
        pyname = make_pyname(widget_name)

        def connect_handler(sig, cb_name):
            '''connect this signal to an unused handler'''
            if cb_name in funcs.keys():
                widget.connect(sig, funcs[cb_name])
                del funcs[cb_name]
                logging.debug("connect by name '%s' '%s' to %s",
                 widget_name, sig, cb_name)

        for sig in sigs:
            # using convention suggested by glade
            connect_handler(sig, "on_%s_%s" % (pyname, sig))

            # Using the convention that the top level window is not
            # specified in the handler name. That is use
            # on_destroy() instead of on_windowname_destroy()
            if widget is callback_obj:
                connect_handler(sig, "on_%s" % sig)
    
    filename = inspect.getfile(callback_obj.__class__)
    for event_handler in funcs.keys():
        logging.debug('Not connected to glade %s.%s', filename, event_handler)
