#!/bin/bash
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

echo ssh into master instance
sudo chmod 600 $1
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}

# echo ssh into secondary instance
ssh -o StrictHostKeyChecking=no ubuntu@$4 -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
if [[ ${6} != "STOP" ]]; then
# echo ssh into slaves
    ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
    echo this is 8
    echo ${8}
    if [[ ${8} != "STOP" ]]; then 
        echo this is correct datanew
        ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
        if [[ ${10} != "STOP" ]]; then
            ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
            
            if [[ ${12} != "STOP" ]]; then
                ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
                
                if [[ ${14} != "STOP" ]]; then
                    ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}

                    if [[ ${16} != "STOP" ]]; then
                        ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
                        
                        if [[ ${18} != "STOP" ]]; then
                            ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
                            
                            if [[ ${20} != "STOP" ]]; then
                                ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./datanew.sh $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}
                                fi
                        fi
                    fi        
                fi
            fi
        fi
    fi
fi
# # this is to generate the ssh key pair
# ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./datanameonly.sh 

# #walkaround2
ssh ubuntu@$2 -i $1 \
"sudo cat /home/hadoop/.ssh/id_rsa.pub" \
| ssh ubuntu@$2 -i $1 \
"sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
ssh ubuntu@$2 -i $1 \
"sudo cat /home/hadoop/.ssh/id_rsa.pub" \
| ssh ubuntu@$4 -i $1 \
"sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"


if [[ ${6} != "STOP" ]]; then
# echo ssh into slaves
    ssh ubuntu@$2 -i $1 \
    "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
    | ssh ubuntu@$6 -i $1 \
    "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
    if [[ ${8} != "STOP" ]]; then
        echo this is correct share key 
        ssh ubuntu@$2 -i $1 \
        "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
        | ssh ubuntu@$8 -i $1 \
        "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
        if [[ ${10} != "STOP" ]]; then
            ssh ubuntu@$2 -i $1 \
            "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
            | ssh ubuntu@${10} -i $1 \
            "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
            if [[ ${12} != "STOP" ]]; then
                ssh ubuntu@$2 -i $1 \
                "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
                | ssh ubuntu@${12} -i $1 \
                "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
                if [[ ${14} != "STOP" ]]; then
                    ssh ubuntu@$2 -i $1 \
                    "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
                    | ssh ubuntu@${14} -i $1 \
                    "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"

                    if [[ ${16} != "STOP" ]]; then
                        ssh ubuntu@$2 -i $1 \
                        "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
                        | ssh ubuntu@${16} -i $1 \
                        "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
                        
                        if [[ ${18} != "STOP" ]]; then
                            ssh ubuntu@$2 -i $1 \
                            "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
                            | ssh ubuntu@${18} -i $1 \
                            "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
                            
                            if [[ ${20} != "STOP" ]]; then
                                ssh ubuntu@$2 -i $1 \
                            "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
                            | ssh ubuntu@${20} -i $1 \
                            "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"
                                fi
                        fi
                    fi        
                fi
            fi
        fi
    fi
fi

# ssh ubuntu@35.175.128.55 -i /Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem \
# "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
# | ssh ubuntu@35.175.128.55 -i /Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem \
# "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"

# ssh ubuntu@34.204.174.108 -i /Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem \
# "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
# | ssh ubuntu@3.227.249.64 -i /Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem \
# "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"

# ssh ubuntu@34.204.174.108 -i /Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem \
# "sudo cat /home/hadoop/.ssh/id_rsa.pub" \
# | ssh ubuntu@3.236.141.9 -i /Users/ryan/Desktop/DBProject/SQLWITHPROFINS/dbproject.pem \
# "sudo cat - | sudo tee -a /home/hadoop/.ssh/authorized_keys"


#setup java
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./datajava.sh 

# echo ssh into secondary instance
ssh -o StrictHostKeyChecking=no ubuntu@$4 -i $1 'bash -s' < ./datajava.sh 
if [[ ${6} != "STOP" ]]; then
# echo ssh into slaves
ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./datajava.sh
    if [[ ${8} != "STOP" ]]; then 
        echo this is correct datajava
        ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./datajava.sh 
        if [[ ${10} != "STOP" ]]; then
            ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./datajava.sh 
            
            if [[ ${12} != "STOP" ]]; then
                ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./datajava.sh 
                
                if [[ ${14} != "STOP" ]]; then
                    ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./datajava.sh 

                    if [[ ${16} != "STOP" ]]; then
                        ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./datajava.sh 
                        
                        if [[ ${18} != "STOP" ]]; then
                            ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./datajava.sh 
                            
                            if [[ ${20} != "STOP" ]]; then
                                ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./datajava.sh 
                                fi
                        fi
                    fi        
                fi
            fi
        fi
    fi
fi
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./hadoopinstall.sh 
ssh -o StrictHostKeyChecking=no ubuntu@$4 -i $1 'bash -s' < ./hadoopinstallother.sh 
if [[ ${6} != "STOP" ]]; then
# echo ssh into slaves
ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./hadoopinstallother.sh
    echo this is 9
    echo ${9}
    if [[ ${9} != "STOP" ]]; then
        echo this is correct datajava hadoopinstallother 
        ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./hadoopinstallother.sh
        if [[ ${11} != "STOP" ]]; then
            ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./hadoopinstallother.sh
            
            if [[ ${12} != "STOP" ]]; then
                ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./hadoopinstallother.sh
                
                if [[ ${14} != "STOP" ]]; then
                    ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./hadoopinstallother.sh

                    if [[ ${16} != "STOP" ]]; then
                        ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./hadoopinstallother.sh
                        
                        if [[ ${18} != "STOP" ]]; then
                            ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./hadoopinstallother.sh 
                            
                            if [[ ${20} != "STOP" ]]; then
                                ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./hadoopinstallother.sh
                                fi
                        fi
                    fi        
                fi
            fi
        fi
    fi
fi

ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./hadoopinstall2.sh 
ssh -o StrictHostKeyChecking=no ubuntu@$4 -i $1 'bash -s' < ./sparkother.sh 

# echo ssh into slaves

if [[ ${6} != "STOP" ]]; then 
    ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./sparkother.sh
    echo this is 9
    echo ${9}
    if [[ ${9} != "STOP" ]]; then
        echo this is correct datajava sparkother  
        ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./sparkother.sh 
        if [[ ${11} != "STOP" ]]; then
            ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./sparkother.sh 
            
            if [[ ${12} != "STOP" ]]; then
                ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./sparkother.sh 
                
                if [[ ${14} != "STOP" ]]; then
                    ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./sparkother.sh 

                    if [[ ${16} != "STOP" ]]; then
                        ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./sparkother.sh 
                        
                        if [[ ${18} != "STOP" ]]; then
                            ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./sparkother.sh  
                            
                            if [[ ${20} != "STOP" ]]; then
                                ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./sparkother.sh 
                                fi
                        fi
                    fi        
                fi
            fi
        fi
    fi
fi

ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./sparkrun.sh 
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./sparkrun2.sh 
# #copy the key pair to all the other nodes
# ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./datanameonly2.sh 
# echo this is the ip addr of the main node
# echo $2
# echo 'this is the public dns for the main node'
# echo $3
# echo this is the ip addr of the secondary node
# echo $4
# echo this is the public dns of the secondary node
# echo $5
# echo slaves ip array
# echo $6
# echo slaves dns array
# # # declare -a allip=($6 $8)
# # # for i in "${allip[@]}"
# # # do
# # #    echo "$i"
# # # done








# ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./data2.sh $1 $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}

# ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./data2slave.sh $1 $7
# if [[ ${8} != "STOP" ]]; then 
#     ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./data2slave.sh $1 $9
#     if [[ ${10} != "STOP" ]]; then
#         ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./data2slave.sh $1 ${11}
        
#         if [[ ${12} != "STOP" ]]; then
#             ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./data2slave.sh $1 ${13}
            
#             if [[ ${14} != "STOP" ]]; then
#                 ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./data2slave.sh $1 ${15}

#                 if [[ ${16} != "STOP" ]]; then
#                     ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./data2slave.sh $1 ${17}
                    
#                     if [[ ${18} != "STOP" ]]; then
#                         ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./data2slave.sh $1 ${19}
                        
#                         if [[ ${20} != "STOP" ]]; then
#                             ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./data2slave.sh $1 ${21}
#                             fi
#                     fi
#                 fi        
#             fi
#         fi
#     fi
# fi
# ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./data3.sh $1 $3
