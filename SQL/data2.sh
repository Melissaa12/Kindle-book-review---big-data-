#!/bin/bash
#THIS IS FOR MASTER DATA SETUP2
echo before
echo slavenode1
echo $4
echo slavenode2
echo $5
echo slavenode3
echo $6
echo slavenode4
echo $7
echo masterdns
echo $2
# arr=("$@")
# for i in "${arr[@]}";
#     do
#         echo "$i"
#     done
# echo finish
sudo chmod 600 dbproject.pem
eval `ssh-agent`
ssh-add dbproject.pem
sleep 5
cd hadoop-3.3.0/etc/hadoop
echo scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$3:/home/ubuntu/hadoop-3.3.0/etc/hadoop
scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$3:/home/ubuntu/hadoop-3.3.0/etc/hadoop
scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$4:/home/ubuntu/hadoop-3.3.0/etc/hadoop

if [[ ${5} != "STOP" ]]; then 
    scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$5:/home/ubuntu/hadoop-3.3.0/etc/hadoop
    if [[ ${6} != "STOP" ]]; then
        scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$6:/home/ubuntu/hadoop-3.3.0/etc/hadoop        
        if [[ ${7} != "STOP" ]]; then
            scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$7:/home/ubuntu/hadoop-3.3.0/etc/hadoop
            if [[ ${8} != "STOP" ]]; then
                scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$8:/home/ubuntu/hadoop-3.3.0/etc/hadoop

                if [[ ${9} != "STOP" ]]; then
                    scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@$9:/home/ubuntu/hadoop-3.3.0/etc/hadoop
                    
                    if [[ ${10} != "STOP" ]]; then
                        scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@${10}:/home/ubuntu/hadoop-3.3.0/etc/hadoop
                        
                        if [[ ${11} != "STOP" ]]; then
                            scp -o StrictHostKeyChecking=no hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@${11}:/home/ubuntu/hadoop-3.3.0/etc/hadoop
                            fi
                    fi
                fi        
            fi
        fi
    fi
fi
# # do this for each of the slave nodes
# scp hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@<slavenodehostname>.compute-1.amazonaws.com:/home/ubuntu/hadoop-3.3.0/etc/hadoop

cd 
sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/masters << EOF
${2}
${3}
EOF



# # sudo tee $HADOOP_CONF/masters << EOF
# # ec2-3-90-89-241.compute-1.amazonaws.com
# # ec2-54-83-177-66.compute-1.amazonaws.com
# # EOF

# declare -a allip=($4 $5 $6 $7 $8 $9 ${10} ${11})
# for i in "${allip[@]}"
# do
#     if [[ $i == "STOP" ]]; then
        
#     fi
# done
sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/slaves << EOF
${4}
${5}
EOF

cd hadoop-3.3.0/etc/hadoop
scp masters slaves ubuntu@$3:/home/ubuntu/hadoop-3.3.0/etc/hadoop

# # sudo tee $HADOOP_CONF/slaves << EOF
# # ec2-18-209-164-190.compute-1.amazonaws.com
# # EOF

# http://ec2-3-91-228-245.compute-1.amazonaws.com:8088/cluster/scheduler