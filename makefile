branch := $(shell git symbolic-ref --short HEAD)

osverbosity := $(shell if [ ! -z $(EDU_VERBOSITY) ]; then echo -v; fi)
gizaverbosity := $(shell if [ -z $(EDU_VERBOSITY) ]; then echo --level warning; else echo --level $(EDU_VERBOSITY); fi)

noop:
	$(info *** Some available targets: ***)
	$(info   instructor-package   build the courses with instructor notes)
	$(info   student-package      build the material for the students)
	$(info   latex                build the PDFs for all classes)
	$(info   )
	$(info   internal-package     NHTT only: build the course for the instructor)
	$(info   internal-pdfs        NHTT only: build the PDFs for the students)
	$(info   )
	$(info   set EDU_VERBOSITY to 'info' or 'debug' to increase the verbosity):
	@true

%:
	giza make $@

stage giza-stage:
	@giza push --deploy stage-student stage-instructor --builder latex dirhtml html singlehtml slides --serial_sphinx --edition instructor student

instructor-package:
	rm -f conf.py
	ln conf-default.py conf.py
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition instructor
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-instructor/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-instructor/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/

student-package:
	rm -f conf.py
	ln conf-default.py conf.py
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition student
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-student/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-student/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/

internal-package:
	rm -f conf.py
	ln conf-internal.py conf.py
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition internal
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-internal/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-internal/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/
	# Temp workaround for console not seeing images for 'internal' until EDU-3946 is fixed
	ln -s $@/_images build/_images

internal-pdfs:
	rm -f conf.py
	ln conf-internal.py conf.py
	rm -rf build/$@/ build/$@.tar.gz
	# TODO - remove the next 2 lines once everyone in the team uses Giza version 0.5.10 (Dec 2016)
	mkdir -p build/$(branch)/latex-internal
	cp source/images/*.eps build/$(branch)/latex-internal/.
	# TODO Copy the PDFs we still generate manually from PowerPoint slides
	giza $(gizaverbosity) sphinx --builder latex --serial_sphinx --edition internal
