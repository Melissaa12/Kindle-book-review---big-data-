import boto3
from boto3 import NullHandler
import json
import copy
def tweakStack(stack_name='DBPJT3'  , n = 0 ):

 template_file_location = "./finalcloud.json"
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
  
 for i in range(0, n):
  content["Resources"]["Slave"+str(1+i)] = tempVal
  tempOutput["Value"]["Fn::GetAtt"][0] = "Slave"+str(1+i)
  tempOutput2["Value"]["Fn::GetAtt"][0] = "Slave"+str(1+i)
  content["Outputs"]["Slave"+str(1+i)+"IP"] = copy.deepcopy(tempOutput)
  content["Outputs"]["Slave"+str(1+i)+"PriIP"] = copy.deepcopy(tempOutput2)
 


 json.dump(content, tempfile , indent=4)
 tempfile.close()