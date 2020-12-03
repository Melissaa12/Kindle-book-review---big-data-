echo webip
echo $1
echo pemkey
echo $2
echo mongodbip
echo $3
echo mysqlip
echo $4
echo masternodeip
echo $5
echo ssh into instance
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2 'bash -s' < ./web.sh $1 $3 $4 $5