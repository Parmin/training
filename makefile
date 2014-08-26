noop:
	@true

include build/makefile.meta

giza-stage: 
	@giza push --deploy stage-student stage-instructor --builder latex dirhtml html singlehtml slides --serial_sphinx --edition instructor student
