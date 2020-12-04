from re import template
import boto3, yaml, json
from tweakJson import tweakStack
# file must in the same dir as script
import json
from time import sleep
import sys
stack_name = 'DBPJT3'

# calls tweakStack to create cloudformationjson for number of datanodes indicated
tweakStack(stack_name,int(sys.argv[5]))
template_file_location = "./testsavenew.json"
# template_file_location = "./testsave3.json"

# read entire file as yaml
with open(template_file_location, 'r') as content_file:
    content = json.load(content_file)
content = json.dumps(content)

# creates the stack with all EC2 instances
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3],region_name="us-east-1")
print("Creating {}".format(stack_name))
response = cloud_formation_client.create_stack(
    StackName=stack_name,
    Parameters=[{
        'ParameterKey':"KeyName",
        'ParameterValue':sys.argv[4]
    },],
    TemplateBody=content
)
#Sleep wait so as to wait for the stack to finish instantiation
sleep(150)
print(response)