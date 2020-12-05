echo this is the latest version
echo this is the pem
echo $1
echo this is the ip addr of the main node
echo $2
echo 'this is the private ip for the main node'
echo $3
echo this is the ip addr of the slave0
echo $4
echo this is the private ip of the slave1
echo $5
echo slaves ip array
echo $6
echo $7
echo slaves dns array
echo ${8}
echo ${9}
echo ${10}
#adding a new node
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./shutdownhadoopcluster.sh 

ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./edithostsfile.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}

ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}