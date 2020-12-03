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
# echo please enter your aws keyname
# read key_name
# echo enter your path to your key
# read key_path
# echo credentials

#Prompting user how many extra nodes they want, the fixed and default number is 1
echo 'how many extra datanodes do you want for the data analytics(there is already 1)'
read numberOfSlaves


access_key_id=ASIA2BUDARD26VL3OBRH
aws_secret_access_key=Wkkr7xE940Hf80awxKnHZTIERezBt/ZKja/f9BG6
aws_session_token=FwoGZXIvYXdzEEcaDNiPWRqY5RCky0XbaiLKAVj7nQmfbxcu4Sj+O62vv+ZB2Ged3GVeGvRTAjNRFPArfAGV4RQVXLZ3fTw7Y65v8THPyTD+PhXxgvYpwikJlHznzFpHuMbs66vX2/z+gXR+FrjdE2tKS8EtXbPdRfAPVYcNHPlJwmdrqispcgQugG/vf/jT+UY8Ft1sWm/hYLng8JyGW/JMqI3FAnbxABMagN5DLZqBqQWw2NQGE3n1J9UrSnxRCjpZPqmnM3DEhvXw+7co66hh/jj69C+RTCunnkisAocP22ThdrEoiMyj/gUyLTrtyjpOLDbL84T73eOSZfr7Z6d7ha2f9gm1JpMyqVlp6I8sgb0ZiQpkssGwuA==
key_name=dbproject
key_path=/Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem

echo "$access_key_id"
echo "$aws_secret_access_key"
echo "$aws_session_token"
echo "$key_name"
echo "$key_path"


python createEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_name $numberOfSlaves
pip install paramiko
python sshEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_path $key_name $numberOfSlaves