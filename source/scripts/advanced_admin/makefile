profile := $(shell if [ ! -z $(PROFILE) ]; then echo --profile $(PROFILE); fi)

noop:
	@true

s3-devel:
	aws $(profile) s3 sync s3 s3://mongodb-training/advadmin-devel --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers

s3-prod:
	aws $(profile) s3 sync s3 s3://mongodb-training/advadmin --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers

test:
	echo "No automated tests yet"

validate-cf:
	aws $(profile) cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-added_team.template
	aws $(profile) cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-ami.template
	aws $(profile) cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-base_team.template


