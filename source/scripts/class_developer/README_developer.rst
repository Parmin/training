==============================================================
Advanced Administration Training - Instructions for developers
==============================================================

Simple workflow
---------------

- Make changes to templates
  - verify that the changes are syntaxily correct by validating on the command line, 

      make validate-cf

      OR run it for a single template with something like:

      aws --profile training-west cloudformation validate-template --template-body file://./s3/cf-templates/advadmin-added_team.template

 - unless the template is the top stack, you will need to upload the modified template to S3.
   For development, put your templates in 'https://console.aws.amazon.com/s3/home?region=us-west-1#&bucket=mongodb-training&prefix=cloud-formation-templates/devel-templates/'

- Create a new set of instances, using a number of teams=1, and pointing to the 'devel-templates' by using the '--testmode' option

    ./deploy.py --profile training-west --provider aws-cf --teams 1 --run dctest --testmode

  This will create 3 opsmgr instances, one node1 for a data node and a load balancer, all as 't2.micro'. Obviously, those will not support Ops Manager, but you are likely testing CloudFormation at this point.

- Destroy a stack

    ./teardown.py --profile training-west --provider aws-cf --run dctest

- Modifying and testing the 'team' and 'AMI' stacks.

  Once you have the top stack created for a run ('base_team'), you can add teams to it by simply running this stack.
  The same applies to the 'ami' stack, you can add machines to a given team by simply running this stack.
  Note that running either of those 2 stacks will require you to provide the parent artifacts as parameter, and that those stacks will not be deleted once you delete the parent stack, as they never registered as children stacks.


Artifacts created
-----------------

- 1 stack for the training class
  - 1 VPC
  - 1 internet gateway
- 1 stack per team, including a 'team0' for the trainer
  - 1 subnet 10.0.X.0/24
  - 3 hosts for Ops Manager (opsmgr1, opsmgr2, opsmgr3)
  - 12 hosts for data nodes (2 shards X 3 nodes per shard, 3 config servers, 2 mongos, all nodes named 'nodeX')
  - 1 load balancer
- 1 stack per instance

So, creating a class with 4 teams (4 teams + team 0) will create:
- 1 + 5 + 5 * (12 + 3) = 81 stacks
- 5 * 3 = 15 hosts for Ops Manager installations
- 5 * 12 = 60 hosts for MongoDB clusters

Browsing the artifacts in AWS
-----------------------------

Stacks are browsed under the "CloudFormation" section
- The top stack is named after the run, for example: dctest1
- The stacks per team have the above name, plus the team and a unique string (from AWS, wish we could remove), for example: dctest1-Team0-1153J0S5CA7VW
- The stack for the instances are appended with the machine role, for example for an opsmgr host: dctest1-Team1-1153J0S5CA7VW-opsmgr1-1VFA8BHWQYGLK

- Each stack, instance, subnet, ... has a lot of tags, you can use those to find and identify the artifacts:
  - Name: the name of the run
  - Team Number
  - Role: for instances
  - owner
Also, look for the 'Output' tab under a stack to see the important information about the created artifacts.

Additional notes
----------------
1) Uploading new version of files in 'ami' or 'datasets' requires that you make those files 'public'
   again in S3, even if the property shows it is downloadable by 'everyone'

2) You can create a stack from the command line by running something like:
  aws --profile training-west cloudformation create-stack --stack-name PaloAlto --parameters ParameterKey=KeyPair,ParameterValue=AdvancedAdministrator ParameterKey=NbTeams,ParameterValue=0 --template-body file://./s3/cf-templates/advadmin-base_team.template

3) sync with S3:
   cd source/scripts/advanced_admin
   make s3-prod
   OR
   make s3-devel