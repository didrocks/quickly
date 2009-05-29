# this is expected by intltool in Makefile
top_srcdir = ..

include Makevars

translated := $(addprefix $(top_srcdir)/,$(shell cat POTFILES.in))

default: pot

pot: $(DOMAIN).pot
$(DOMAIN).pot: $(translated)
	intltool-update --pot

missing: FORCE
	intltool-update --maintain

FORCE:

.PHONY: default pot FORCE
