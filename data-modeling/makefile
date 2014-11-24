branch := $(shell git symbolic-ref --short HEAD)

noop:
	@true

%:
	giza make $@

stage giza-stage: 
	@giza push --deploy stage-student stage-instructor --builder latex dirhtml html singlehtml slides --serial_sphinx --edition instructor student

instructor-package:
	rm -rf build/$@/ build/$@.tar.gz
	giza sphinx --builder slides html --serial_sphinx --edition instructor
	mkdir -p build/$@/slides/
	rsync -rv build/$(branch)/html-instructor/ build/$@/
	rsync -rv build/$(branch)/slides-instructor/ build/$@/slides/
	tar -C build/ -czvf build/$@.tar.gz $@/

student-package:
	rm -rf build/$@/ build/$@.tar.gz
	giza sphinx --builder slides html --serial_sphinx --edition student
	mkdir -p build/$@/slides/
	rsync -rv build/$(branch)/html-student/ build/$@/
	rsync -rv build/$(branch)/slides-student/ build/$@/slides/
	tar -C build/ -czvf build/$@.tar.gz $@/


