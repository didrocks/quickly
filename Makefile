default: all

all:
	$(MAKE) -C po $@

INSTALL ?= install
DESTDIR ?=

install: all
	$(INSTALL) -d $(DESTDIR)/usr/lib/quickly
	$(INSTALL) -m 755 quickly.py $(DESTDIR)/usr/lib/quickly/
	$(INSTALL) -m 755 -d $(DESTDIR)/usr/share/locale
	for file in po/*.mo; do \
	    lang=`basename $$file .mo`; \
	    $(INSTALL) -m 755 -d $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES; \
	    $(INSTALL) -m 644 $$file $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES; \
	done

.PHONY: default all install
