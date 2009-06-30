default: all

all:
	$(MAKE) -C po $@

INSTALL ?= install
DESTDIR ?=

prefix ?= usr
libdir ?= $(prefix)/lib/quickly
bindir ?= $(prefix)/bin
datadir ?= $(prefix)/share
templatedir = $(datadir)/quickly/templates
localedir = $(datadir)/locale

install: all
	$(INSTALL) -m 755 -d $(DESTDIR)/$(libdir)
	$(INSTALL) -m 755 quickly $(DESTDIR)/$(libdir)
	$(INSTALL) -m 755 -d $(DESTDIR)/$(libdir)/builtins
	$(INSTALL) -m 644 builtins/*.py $(DESTDIR)/$(libdir)/builtins
	$(INSTALL) -m 755 -d $(DESTDIR)/$(bindir)
	ln -s ../lib/quickly/quickly $(DESTDIR)/$(bindir)/quickly
	# Ubuntu templates
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project
	$(INSTALL) -m 644 templates/ubuntu-project/*.py $(DESTDIR)/$(templatedir)/ubuntu-project
	$(INSTALL) -m 755 templates/ubuntu-project/project_name $(DESTDIR)/$(templatedir)/ubuntu-project
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/help
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/help/images
	$(INSTALL) -m 644 templates/ubuntu-project/help/*.html $(DESTDIR)/$(templatedir)/ubuntu-project/help
	$(INSTALL) -m 644 templates/ubuntu-project/help/images/*.png $(DESTDIR)/$(templatedir)/ubuntu-project/help/images	
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/internal
	$(INSTALL) -m 644 templates/ubuntu-project/internal/*.py $(DESTDIR)/$(templatedir)/ubuntu-project/internal
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/media
	$(INSTALL) -m 644 templates/ubuntu-project/media/*.png $(DESTDIR)/$(templatedir)/ubuntu-project/media
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/python
	$(INSTALL) -m 644 templates/ubuntu-project/python/*.py $(DESTDIR)/$(templatedir)/ubuntu-project/python
	$(INSTALL) -m 755 -d $(DESTDIR)/$(templatedir)/ubuntu-project/ui
	$(INSTALL) -m 644 templates/ubuntu-project/ui/*.ui $(DESTDIR)/$(templatedir)/ubuntu-project/ui
	$(INSTALL) -m 644 templates/ubuntu-project/ui/*.xml $(DESTDIR)/$(templatedir)/ubuntu-project/ui
	# translations
	for file in po/*.mo; do \
	    lang=`basename $$file .mo`; \
	    $(INSTALL) -m 755 -d $(DESTDIR)/$(localedir)/$$lang/LC_MESSAGES; \
	    $(INSTALL) -m 644 $$file $(DESTDIR)/$(localedir)/$$lang/LC_MESSAGES/quickly.mo; \
	done

.PHONY: default all install
