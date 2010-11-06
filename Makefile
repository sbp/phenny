# Makefile
# Copyright 2008, Sean B. Palmer, inamidst.com
# Licensed under the Eiffel Forum License 2.

archive: ;
	# hg archive -t tbz2 phenny-hg.tar.bz2
	git archive --format=tar --prefix=phenny/ HEAD | bzip2 > phenny.tar.bz2

ci: ;
	# hg ci
	git commit -a && git push origin master

log: ;
	# git log --date=short --format='%h %ad %s'
	git graph

sync: ;
	rsync -avz ./ pubble:opt/phenny/
