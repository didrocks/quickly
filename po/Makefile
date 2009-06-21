# this is expected by intltool in Makefile
top_srcdir = ..

include Makevars

translated := $(addprefix $(top_srcdir)/,$(shell cat POTFILES.in))

default: all

all: mos pot

%.mo: %.po
	msgfmt $< -o $@

pos := $(wildcard *.po)

mos: $(pos:%.po=%.mo)

pot: $(DOMAIN).pot
$(DOMAIN).pot: $(translated)
	intltool-update --pot

missing: FORCE
	intltool-update --maintain

clean:
	rm -f *.mo

FORCE:

.PHONY: default all pot clean FORCE
