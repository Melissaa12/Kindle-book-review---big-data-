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


# access_key_id=ASIA2UVLEGX2IHAXOVF4
# aws_secret_access_key=Wa+wtfXHFaPQ20PEijGOvgZji3kzdIR3OSFXZk7M
# aws_session_token=FwoGZXIvYXdzEHcaDFkfbyCWngWsjfM5yyLSAU+NnJA89F4CdzeTES8LPXoOwrvwMbFx1nwEv0LUhaX5t9y3RdckLMGfeoPvEpd/yiNSPziHV5w4A8UJYnitg7XN1PlFiJvdjWkCO7E7maXcTuAddeyGlWEHWvE017NG3G0KXuC27yRAfOZS6S8VswpZCweX5dJ/zJapEk8EM7RzGvzrocOuQ7iTU8OfACG8egXs8hr60AN3zjUsRjk2xLaHRczAO0X+/p4eSicL6nHtLXLuG+vHNR/QrxlSmjeE2NLl4u4VhHz9Aj5caBERkyj3kyihna7+BTItd/k4LWWsQdpBDYa38YD9RcEF/VLwCGp1FWo6+pnIn52PropXd3jmvx9eJ8kZ
# region=us-east-1

echo $key_name
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
source /etc/environment
echo $AWS_SESSION_TOKEN
echo $KEYNAME



# installing requirements 
export LC_ALL=C
pip3 install boto3
pip3 install pyyaml
yes Y|sudo apt install python-pip3
pip3 install --upgrade pip
pip3 install paramiko
#calling python script that creates all the EC2 instances based on cloudformation
python3 createEC2.py $access_key_id $aws_secret_access_key $aws_session_token $numberOfSlaves ${region}

#calling python script to get outputs from EC2 and start configuration for all servers
python3 sshEC2.py $access_key_id $aws_secret_access_key $aws_session_token $numberOfSlaves ${region}