from re import template
import boto3, yaml, json
import sys
# file must in the same dir as script
import json
from time import sleep

stack_name = 'DBPJT3'
# template_file_location = "./testsavenew.json"

# # # read entire file as yaml
# with open(template_file_location, 'r') as content_file:
#     content = json.load(content_file)
# content = json.dumps(content)
# if use educate account
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3],region_name=sys.argv[4])

response = cloud_formation_client.delete_stack(
    StackName=stack_name,
)

#to delete the key pair
ec2 = boto3.client('ec2',region_name='us-east-1',aws_access_key_id=sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3])
response = ec2.delete_key_pair(KeyName=sys.argv[5])
print(response)