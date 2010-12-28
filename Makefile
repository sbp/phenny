# Makefile
# Copyright 2008, Sean B. Palmer, inamidst.com
# Licensed under the Eiffel Forum License 2.

# archive - Create phenny.tar.bz2 using git archive
archive: ;
	# hg archive -t tbz2 phenny-hg.tar.bz2
	git archive --format=tar --prefix=phenny/ HEAD | bzip2 > phenny.tar.bz2

# ci - Check the code into git and push to github
ci: ;
	# hg ci
	git commit -a && git push origin master

# log - Show a log of recent updates
log: ;
	# git log --date=short --format='%h %ad %s'
	git graph

# sync - Push phenny to pubble:opt/phenny/
sync: ;
	rsync -avz ./ pubble:opt/phenny/

help: ;
	@egrep '^# [a-z]+ - ' Makefile | sed 's/# //'
