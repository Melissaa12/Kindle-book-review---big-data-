import boto3
from boto3 import NullHandler
import json
def tweakStack(stack_name='DBPJT3'  , n = 0 ):

 template_file_location = "./finalcloud.json"
 #cloud_formation_client = boto3.client('cloudformation',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token,region_name="us-east-1")
 # # read entire file as yaml
 with open(template_file_location, 'r') as content_file:
     content = json.load(content_file)
 tempfile = open("./testsavenew.json" , 'w')
 tempVal  ={
             "Type": "AWS::EC2::Instance",
             "Properties": {
                 "ImageId": "ami-0f82752aa17ff8f5d",
                 "InstanceType": "t2.medium",
                 "SecurityGroups": [
                     {
                         "Ref": "DataSecurity"
                     }
                 ],
                 "KeyName": {
                     "Ref": "KeyName"
                 }
             }}
 tempOutput = {
             "Description": "Public IP of Dataserver",
             "Value": {
                 "Fn::GetAtt": [
                     "Slave2",
                     "PublicIp"
                 ]
             }
         }
 tempOutput2  ={
            "Description": "PrivateIP of Secondaryserver",
            "Value": {
                "Fn::GetAtt": [
                    "Slave0",
                    "PrivateIp"
                ]
            }
        }       
 #json.dump(template, newtemplate, indent=4)
  
 for i in range(0, n):
  content["Resources"]["Slave"+str(1+i)] = tempVal
  tempOutput["Value"]["Fn::GetAtt"][0] = "Slave"+str(1+i)
  tempOutput2["Value"]["Fn::GetAtt"][0] = "Slave"+str(1+i)
  content["Outputs"]["Slave"+str(1+i)+"IP"] = tempOutput
  content["Outputs"]["Slave"+str(1+i)+"PriIP"] = tempOutput2

 #content = json.dumps(content)
 


 json.dump(content, tempfile , indent=4)
 tempfile.close()