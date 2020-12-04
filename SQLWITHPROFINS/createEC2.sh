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


access_key_id=ASIA2BUDARD2XDWWECIY
aws_secret_access_key=dmaCt0A3CZSmgafimbJD1T7s5osZDeDGVxjKAq9o
aws_session_token=FwoGZXIvYXdzEFsaDLGtu+KkSe8b5AdrjyLKAWL0an8gABfNw82uV2mEXnvqlLBSeEtk0G/0RHreVsbSQbre2i9PXN+ScL7tXXvD4p5Xx6+ai/YjY2OP2q2itH6hxH2z1ckx5g77ko3kxbhFPlTUg9EB5Pj0nJcy/J0AAWPI4jelsIPz87RPEDHiqBTeuFiyshcmek/r8opV+wMWWcQzNXi3JQGx5/JdyEeNAd5wigzCVMSQkXeCu1wjLnchzUCzGcuf2ig3dKOUgBGhqMEcai4ps7Ckju+x+T2z63B0+gtNGp2m9/Uokfen/gUyLT4YYLayIjMQ5GJWBHuk3t40AZTIV+Puk8rxeiCJTq74+M69DsnuhKYJtOb86w==
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