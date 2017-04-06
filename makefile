branch := $(shell git symbolic-ref --short HEAD)
profile := $(shell if [ ! -z $(PROFILE) ]; then echo --profile $(PROFILE); fi)

osverbosity := $(shell if [ ! -z $(EDU_VERBOSITY) ]; then echo -v; fi)
gizaverbosity := $(shell if [ -z $(EDU_VERBOSITY) ]; then echo --level warning; else echo --level $(EDU_VERBOSITY); fi)

noop:
	$(info *** Some available targets: ***)
	$(info   instructor-package   build the courses with instructor notes)
	$(info   student-package      build the material for the students)
	$(info   latex                build the PDFs for all classes)
	$(info   )
	$(info   diff-aws             diff workspace files with the dev area in S3)
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

clean:
	rm -rf build

instructor-package: diff-aws-vms
	rm -f conf.py
	ln conf-default.py conf.py
	rm -rf build/$@/ build/$@.tar.gz
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition instructor 2>&1 | grep -v "isn't included in any toctree" | grep -v "/internal/" || true
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
	giza $(gizaverbosity) sphinx --builder slides html --serial_sphinx --edition internal 2>&1 | grep -v "isn't included in any toctree" || true
	mkdir -p build/$@/slides/
	rsync $(osverbosity) -r build/$(branch)/html-internal/ build/$@/
	rsync $(osverbosity) -r build/$(branch)/slides-internal/ build/$@/slides/
	tar $(osverbosity) -C build/ -czf build/$@.tar.gz $@/
	# Temp workaround for console not seeing images for 'internal' until EDU-3946 is fixed
	ln -s $@/_images build/_images
	ln -s ../_static build/$@/slides/modules/_static

internal-pdfs:
	rm -f conf.py
	ln conf-internal.py conf.py
	rm -rf build/$@/ build/$@.tar.gz
	# TODO - remove the next 2 lines once everyone in the team uses Giza version 0.5.10 (Dec 2016)
	mkdir -p build/$(branch)/latex-internal
	cp source/images/*.eps build/$(branch)/latex-internal/.
	# TODO Copy the PDFs we still generate manually from PowerPoint slides
	giza $(gizaverbosity) sphinx --builder latex --serial_sphinx --edition internal 2>&1 | grep -v "isn't included in any toctree" || true

diff-aws-vms: archive-vms
	rm -rf /tmp/{s3,vms}
	mkdir /tmp/{s3,vms}
	aws $(profile) s3 cp s3://mongodb-training/vms /tmp/s3 --recursive
	$(info *** Showing differences with files in S3 ***)
	cp -r ./build/vms/* /tmp/vms
	tar -xvf /tmp/vms/*.tar.gz -C /tmp/vms/
	tar -xvf /tmp/s3/*.tar.gz -C /tmp/s3
	rm /tmp/s3/*.tar.gz /tmp/vms/*.tar.gz
	diff -r /tmp/s3 /tmp/vms

archive-vms:
	rm -rf build/vms
	mkdir -p build/vms
	find vms -type d -maxdepth 1 -mindepth 1 -exec tar -czf build/{}.tar.gz {} \;
