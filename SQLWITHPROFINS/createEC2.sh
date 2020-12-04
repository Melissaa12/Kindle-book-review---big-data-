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


access_key_id=ASIA2BUDARD2TJNZUGV3
aws_secret_access_key=VGZUaVqCNnmJ1d+HQylcirqhIKaTawPHoPVIrhzN
aws_session_token=FwoGZXIvYXdzEF8aDDD87m8TIRASW4rybCLKAW5E0xvQyX8XrbvDVRfaYtEOIb5XEWVYMatOOQHHYxaNnNWxku3eGAtBbqRXyKdfbHvyKlBahLa4U+ed5DhZlQb8P/NENAaWMgpvPAbF5Qtbr3UmMZXmdAPvdCco3l3quAhOGiUYRD87RiLj4uaWW4Ep77L/sGlNKmqFuzbZfOlUlilIqX0Kis23UWWKY6fgIRlbyS2fbEJqcCnJhS+b65H7+0gg5JmmFeHczrtrceCpLAN3UeNVXfaSzWoC2fzU1IgSYtoBvgTvdV8ouPOo/gUyLa1UnkIzIWgLcHIRgW/pFJOEW9I4pZqbm0NS1sRm3Xyq3wUUMWe37sJmDNl3/A==
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