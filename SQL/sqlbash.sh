echo $1
echo $2
echo ssh into instance
# ssh ubuntu@$1 -i  -o StrictHostKeyChecking=no
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2 'bash -s' < ./sql.sh $2
