branch := $(shell git symbolic-ref --short HEAD)

osverbosity := $(shell if [ ! -z $(EDU_VERBOSITY) ]; then echo -v; fi)
gizaverbosity := $(shell if [ -z $(EDU_VERBOSITY) ]; then echo --level warning; else echo --level $(EDU_VERBOSITY); fi)

noop:
	$(info *** Some available targets: ***)
	$(info   instructor-package   build the courses with instructor notes)
	$(info   student-package      build the material for the students)
	$(info   internal-package     build the course: NHTT, and all classes as instructor)
	$(info   )
	$(info   set EDU_VERBOSITY to 'info' or 'debug' to increase the verbosity):
	@true

%:
	giza make $@

stage giza-stage: 
	@giza push --deploy stage-student stage-instructor --builder latex dirhtml html singlehtml slides --serial_sphinx --edition instructor student

instructor-package:
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition instructor
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-instructor/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-instructor/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/

student-package:
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition student
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-student/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-student/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/

internal-package:
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition internal
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-internal/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-internal/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/
