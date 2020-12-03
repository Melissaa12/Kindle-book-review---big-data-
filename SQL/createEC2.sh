pip install boto3
pip install pyyaml
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
echo 'how many slave nodes do you want for the data analytics'
read numberOfSlaves
access_key_id=ASIA2BUDARD24NSCPNXX
aws_secret_access_key=YOkvdmhkCrzzVfTAfFXqY5hvL8B+PMK95U18E+OL
aws_session_token=FwoGZXIvYXdzEBIaDOerOKWQz2FiLGsQWCLKAUZGOH7TQ+LlsQqpsEGHKC7EuO58WF/ErzatdpV/55leR4eONcFr3359ZXx1OFr4dV6S2oWy1sYAfTVFzW0rniB9pUrS/np+eP2h7d+AAl2Yx/iFMASuGo26aaEwa0wrUlYM2MX/1zoahw9xkRJGhEZ5Kb0N2qC0njUD4SGBQNCkFsQLz6X682u+4cXgTZYSRYkDRjmhlCe3WdUui74ziB5luAym3lzm+KOVkt/eoQVX3zytCm58hasODkaDH6yCNevWEaORXxDIfW8oyfqX/gUyLbnyiWjHjJ98R4nSdk7sNaAqdQV973UAh12NCbZVhKL4QAGjamAY27xNdkdliQ==
key_name=dbproject
key_path=/Users/ryan/Desktop/DBProject/SQL/dbproject.pem
echo "$access_key_id"
echo "$aws_secret_access_key"
echo "$aws_session_token"
echo "$key_name"
echo "$key_path"
python createEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_name $numberOfSlaves
pip install paramiko
python sshEC2.py $access_key_id $aws_secret_access_key $aws_session_token $key_path $key_name $numberOfSlaves