PROGS=create_git_repo
create_git_repo_OBJS=

LIBS=-lgit2
CFLAGS=-Wall -std=gnu99

DST=/usr/bin
EXE=create_git_repo

################
CC=gcc

all: $(PROGS)

depend: .depend
.depend: *.c
	rm -f ./.depend
	$(CC) $(CFLAGS) -MM $^>>./.depend;
ifneq ($(wildcard .depend),)
	include .depend
endif

clean:
	rm -f ./*.o ./*~ ./.depend $(PROGS)

install: all
	cp $(EXE) $(DST)/
	chown git $(DST)/$(EXE)
	chgrp git $(DST)/$(EXE)
	chmod 6510 $(DST)/$(EXE)

.PHONY: all depend clean install

.SECONDEXPANSION:
$(PROGS): $$@.o $$($$@_OBJS)
	$(CC) $^ -o $@ $(LIBS)
