noop:
	@true

include build/makefile.meta

stage giza-stage: 
	@giza push --deploy stage-student stage-instructor --builder latex dirhtml html singlehtml slides --serial_sphinx --edition instructor student

instructor-package:
	rm -rf build/$@/ build/$@.tar.gz
	giza sphinx --builder slides html --serial_sphinx --edition instructor
	mkdir -p build/$@/slides/
	rsync -rv $(branch-output)/html-instructor/ build/$@/
	rsync -rv $(branch-output)/slides-instructor/ build/$@/slides/
	tar -C build/ -czvf build/$@.tar.gz $@/

