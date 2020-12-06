#!/bin/bash


# Prompting user for aws credentials
echo enter your aws_access_key_id
read access_key_id
echo enter your aws_secret_access_key
read aws_secret_access_key
echo enter your aws_session_token
read aws_session_token
echo please enter your aws region
read region

#Prompting user how many extra nodes they want, the fixed and default number is 1
echo 'how many extra datanodes do you want for the data analytics(there is already 1)'
read numberOfSlaves

echo "$access_key_id"
echo "$aws_secret_access_key"
echo "$aws_session_token"
echo "$region"

#saving user credentials as envornmental variables to retrieve for later
sudo tee /etc/environment -a <<EOF
ACCESS_KEY_ID=${access_key_id}
AWS_SECRET_ACCESS_KEY=${aws_secret_access_key}
AWS_SESSION_TOKEN=${aws_session_token}
REGION=${region}
EOF
# source /etc/environment
echo $AWS_SESSION_TOKEN

#calling python script that creates all the EC2 instances based on cloudformation
python3 createEC2.py $access_key_id $aws_secret_access_key $aws_session_token $numberOfSlaves ${region}

#calling python script to get outputs from EC2 and start configuration for all servers
python3 sshEC2.py $access_key_id $aws_secret_access_key $aws_session_token $numberOfSlaves ${region}