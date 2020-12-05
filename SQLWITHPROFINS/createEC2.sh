# installing requirements 
pip install boto3
pip install pyyaml

# Prompting user for aws credentials
# echo enter your aws_access_key_id
# read access_key_id
# echo enter your aws_secret_access_key
# read aws_secret_access_key
# echo enter your aws_session_token
# read aws_session_token
# echo please enter your aws region
# read region



#Prompting user how many extra nodes they want, the fixed and default number is 1
echo 'how many extra datanodes do you want for the data analytics(there is already 1)'
read numberOfSlaves


access_key_id=ASIA2UVLEGX2IHAXOVF4
aws_secret_access_key=Wa+wtfXHFaPQ20PEijGOvgZji3kzdIR3OSFXZk7M
aws_session_token=FwoGZXIvYXdzEHcaDFkfbyCWngWsjfM5yyLSAU+NnJA89F4CdzeTES8LPXoOwrvwMbFx1nwEv0LUhaX5t9y3RdckLMGfeoPvEpd/yiNSPziHV5w4A8UJYnitg7XN1PlFiJvdjWkCO7E7maXcTuAddeyGlWEHWvE017NG3G0KXuC27yRAfOZS6S8VswpZCweX5dJ/zJapEk8EM7RzGvzrocOuQ7iTU8OfACG8egXs8hr60AN3zjUsRjk2xLaHRczAO0X+/p4eSicL6nHtLXLuG+vHNR/QrxlSmjeE2NLl4u4VhHz9Aj5caBERkyj3kyihna7+BTItd/k4LWWsQdpBDYa38YD9RcEF/VLwCGp1FWo6+pnIn52PropXd3jmvx9eJ8kZ
region = us-east-1
key_name=awskey
key_path=/Users/ryan/Desktop/DBProject/SQLWITHPROFINS/key.pem
echo "$access_key_id"
echo "$aws_secret_access_key"
echo "$aws_session_token"
echo "$region"

# sudo tee /etc/environment -a <<EOF
# ACCESS_KEY_ID=${access_key_id}
# AWS_SECRET_ACCESS_KEY=${aws_secret_access_key}
# AWS_SESSION_TOKEN=${aws_session_token}
# REGION=${region}
# EOF

echo $AWS_SESSION_TOKEN

source /etc/environment

python createEC2.py $access_key_id $aws_secret_access_key $aws_session_token $keyname $numberOfSlaves $region
pip install paramiko
python sshEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_path $key_name $numberOfSlaves