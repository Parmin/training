profile := $(shell if [ ! -z $(PROFILE) ]; then echo --profile $(PROFILE); fi)

noop:
	$(info *** Some available targets: ***)
	$(info   s3-devel      push files to S3, in the dev area)
	$(info   s3-diff-devel diff workspace files with the dev area in S3)
	$(info   s3-prod       push files to S3, in the prod area)
	$(info   s3-diff-prod  diff workspace files with the prod area in S3)
	$(info   validate-cf   validate templates):
	@true

s3-devel:
	aws $(profile) s3 sync s3 s3://mongodb-training/advadmin-devel --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers

s3-diff-devel:
	rm -rf /tmp/s3
	mkdir /tmp/s3
	aws $(profile) s3 cp s3://mongodb-training/advadmin-devel /tmp/s3 --recursive
	$(info *** Showing differences with files in S3 ***)
	diff -r -x "usb_drive.zip" /tmp/s3 s3

s3-prod:
	aws $(profile) s3 sync s3 s3://mongodb-training/advadmin --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers

s3-diff-prod:
	rm -rf /tmp/s3
	mkdir /tmp/s3
	aws $(profile) s3 cp s3://mongodb-training/advadmin /tmp/s3 --recursive
	$(info *** Showing differences with files in S3 ***)
	diff -r -x "usb_drive.zip" /tmp/s3 s3

test:
	echo "No automated tests yet"

validate-cf:
	aws $(profile) cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-added_team.template
	aws $(profile) cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-ami.template
	aws $(profile) cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-base_team.template


