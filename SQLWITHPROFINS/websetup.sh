echo $1
echo $2
echo $3
echo ssh into instance
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2 'bash -s' < ./web.sh $1 $3 $4