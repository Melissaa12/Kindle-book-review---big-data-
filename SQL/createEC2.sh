pip install boto3
pip install pyyaml
echo enter your aws_access_key_id
read access_key_id
echo enter your aws_secret_access_key
read aws_secret_access_key
echo enter your aws_session_token
read aws_session_token
echo please enter your aws keyname
read key_name
echo enter your path to your key
read key_path
echo credentials
echo "$access_key_id"
echo "$aws_secret_access_key"
echo "$aws_session_token"
echo "$key_name"
echo "$key_path"
python createEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_name
pip install paramiko
python sshEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_path $key_name