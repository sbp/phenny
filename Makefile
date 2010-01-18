# Makefile
# Copyright 2008, Sean B. Palmer, inamidst.com
# Licensed under the Eiffel Forum License 2.

archive: ;
	hg archive -t tbz2 phenny-hg.tar.bz2
	git archive --format=tar --prefix=phenny/ HEAD | bzip2 > phenny.tar.bz2
