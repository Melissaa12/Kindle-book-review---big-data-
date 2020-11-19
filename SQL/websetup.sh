echo $1
echo $2
echo ssh into instance
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2 'bash -s' < ./web.sh