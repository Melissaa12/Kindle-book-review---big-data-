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
# if use educate account
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id= 'ASIA2BUDARD22DHUBG6D',aws_secret_access_key='+0gCx/AfGyQX3DPaLena70uI+Bnsm7iefsVibzX+',aws_session_token='FwoGZXIvYXdzEIj//////////wEaDOaV+b60Ph25kaj6SSLKAWZ5pVGH2svCZoxQsNP3gIYIVS2NscFfmgDRHl8QBGkHuVHUcVUesaWahyIM1LbBrQZB1cdWOFq9tn6CIUqS1+uaEMduEA3T1padkKw1G9jw/JfGizlCYDp+S+FMgEJYE1NoI9jtblOY259+W51hcPjYYP9/uz4Bi2Ymp31PKSdnRuy+1y7ozIY569RbLPKq2nkvgh6lgqBG8bE9DojK/Ib7SO1iD5I6gPIVtc0nmX6meC/eo3E00R8i4vSdGZbAOO96JvhqDvzegZMoi8r5/QUyLb8UnNaHb3gBe0v20UjXtNBNIDdQFkAVHW+FmgOKzUWFMkk3Voos5pvIARikVA==',region_name="us-east-1")

response = cloud_formation_client.delete_stack(
    StackName=stack_name,
)

