from re import template
import boto3, yaml, json
import sys
# file must in the same dir as script
import json
from time import sleep
stack_name = 'DBPJT3'
template_file_location = "./cloudformation2.json"

# # read entire file as yaml
with open(template_file_location, 'r') as content_file:
    content = json.load(content_file)

# convert yaml to json string
# content = json.dumps(content)

content = json.dumps(content)
print(sys.argv[1])
# if use educate account
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= sys.argv[1],aws_secret_access_key=sys.argv[2],aws_session_token=sys.argv[3],region_name="us-east-1")
# Paid Account
# cloud_formation_client = boto3.client('cloudformation')
print("Creating {}".format(stack_name))
response = cloud_formation_client.create_stack(
    StackName=stack_name,
    Parameters=[{
        'KeyName':sys.argv[4]
    },
    ],
    TemplateBody=content
)
sleep(120)
print(response)