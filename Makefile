default: all

all:
	$(MAKE) -C po $@

INSTALL ?= install
DESTDIR ?=

prefix ?= usr
libdir ?= $(prefix)/lib/quickly
bindir ?= $(prefix)/bin
datadir ?= $(prefix)/share
templatedir = $(datadir)/quickly
localedir = $(datadir)/locale

install: all
	$(INSTALL) -m 755 -d $(DESTDIR)/$(libdir)
	$(INSTALL) -m 755 quickly.py $(DESTDIR)/$(libdir)
	$(INSTALL) -m 755 -d $(DESTDIR)/$(libdir)/builtins
	$(INSTALL) -m 644 builtins/*.py $(DESTDIR)/$(libdir)/builtins
	$(INSTALL) -m 755 -d $(DESTDIR)/$(bindir)
	ln -s ../lib/quickly/quickly.py $(DESTDIR)/$(bindir)/quickly
	# Ubuntu templates
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project
	$(INSTALL) -m 755 templates/ubuntu-project/*.py $(DESTDIR)/$(templatedir)/ubuntu-project
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/glade
	$(INSTALL) -m 644 templates/ubuntu-project/glade/*.ui $(DESTDIR)/$(templatedir)/ubuntu-project/glade
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/media
	$(INSTALL) -m 644 templates/ubuntu-project/media/*.png $(DESTDIR)/$(templatedir)/ubuntu-project/media
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/python
	$(INSTALL) -m 755 templates/ubuntu-project/python/*.py $(DESTDIR)/$(templatedir)/ubuntu-project/python
	# translations
	for file in po/*.mo; do \
	    lang=`basename $$file .mo`; \
	    $(INSTALL) -m 755 -d $(DESTDIR)/$(localedir)/$$lang/LC_MESSAGES; \
	    $(INSTALL) -m 644 $$file $(DESTDIR)/$(localedir)/$$lang/LC_MESSAGES; \
	done

.PHONY: default all install
