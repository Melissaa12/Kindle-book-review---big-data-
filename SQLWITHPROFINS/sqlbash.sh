echo $1
echo $2
echo ssh into instance
sudo chmod 600 $2
#ssh into SQL EC2 Instance and set up sql configuration
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2 'bash -s' < ./sql.sh $2
