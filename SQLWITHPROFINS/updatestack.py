import boto3
from boto3 import NullHandler
import json
import sys
import copy
# you need the cloud_formation_client for this?
# why is there a tempfile close below?
cloud_formation_client = boto3.client('cloudformation',aws_access_key_id=sys.argv[2],aws_secret_access_key=sys.argv[3],aws_session_token=sys.argv[4],region_name=sys.argv[5])
def updateStack(stack_name='DBPJT3' , n =1,keyname='dbproject'):
 newtemplate = open("finalcloud.json" , 'w')


 template = cloud_formation_client.get_template(StackName=stack_name,TemplateStage='Processed')
 #json.dump(template,newtemplate, indent=4)
 print(template["TemplateBody"].keys() )
 template  = template["TemplateBody"]

 #tempfile = open("./newtemplate.json" , 'w')
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
  template["Resources"]["Slave"+str(1+i)] = tempVal
  tempOutput["Value"]["Fn::GetAtt"][0] = "Slave"+str(1+i)
  tempOutput2["Value"]["Fn::GetAtt"][0] = "Slave"+str(1+i)
  template["Outputs"]["Slave"+str(1+i)+"IP"] = copy.deepcopy(tempOutput)
  template["Outputs"]["Slave"+str(1+i)+"PriIP"] = copy.deepcopy(tempOutput2)

 json.dump(template, newtemplate , indent=4)
 tempfile.close() 

 response = cloud_formation_client.update_stack(
     StackName=stack_name,
     Parameters=[{
         'ParameterKey':"KeyName",
         'ParameterValue':'newawskey'
     },],
     TemplateBody=json.dumps(template)
     )
 return response
print('hi')
updateStack('DBPJT3',int(sys.argv[1]),'dbproject')