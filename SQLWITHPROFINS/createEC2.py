from re import template
import boto3, yaml, json
from tweakJson import tweakStack
import json
from time import sleep
import sys
import os

#Default stack name
stack_name = 'DBPJT3'
#Default Keyname
keyname='newawskey'

# calls tweakStack to create cloudformationjson for number of datanodes indicated
tweakStack(stack_name,int(sys.argv[4]))
template_file_location = "./testsavenew.json"

# read entire file and dumps json into content
with open(template_file_location, 'r') as content_file:
    content = json.load(content_file)
content = json.dumps(content)

#create EC2keypair and write to key.pem
ec2 = boto3.client('ec2',region_name=sys.argv[5],aws_access_key_id=sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3])
response = ec2.create_key_pair(KeyName=keyname)
key2 = response['KeyMaterial']
f = open("key.pem", "w")
f.write(key2)
f.close()

# # creates the stack with all EC2 instances
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3],region_name=sys.argv[5])
print("Creating {}".format(stack_name))
response = cloud_formation_client.create_stack(
    StackName=stack_name,
    Parameters=[{
        'ParameterKey':"KeyName",
        'ParameterValue': keyname
    },],
    TemplateBody=content
)
#Sleep wait so as to wait for the stack to finish instantiation
sleep(150)
print(response)