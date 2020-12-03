#!/bin/bash
echo this is the pem
echo $1
echo this is the ip addr of the main node
echo $2
echo 'this is the public dns for the main node'
echo $3
echo this is the ip addr of the secondary node
echo $4
echo this is the public dns of the secondary node
echo $5
echo slaves ip array
echo $6
echo slaves dns array
echo $7
echo $8
echo $9
echo ${10}
echo ssh into master instance
sudo chmod 600 $1
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./data.sh $1 $2 $3

# echo ssh into secondary instance
ssh -o StrictHostKeyChecking=no ubuntu@$4 -i $1 'bash -s' < ./data.sh $1 $4 $5

# echo ssh into slaves
ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./data.sh $1 $6 $7
if [[ ${8} != "STOP" ]]; then 
    ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./data.sh $1 $8 $9 
    if [[ ${10} != "STOP" ]]; then
        ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./data.sh $1 ${10} ${11}
        
        if [[ ${12} != "STOP" ]]; then
            ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./data.sh $1 ${12} ${13}
            
            if [[ ${14} != "STOP" ]]; then
                ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./data.sh $1 ${14} ${15}

                if [[ ${16} != "STOP" ]]; then
                    ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./data.sh $1 ${16} ${17}
                    
                    if [[ ${18} != "STOP" ]]; then
                        ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./data.sh $1 ${18} ${19}
                        
                        if [[ ${20} != "STOP" ]]; then
                            ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./data.sh $1 ${20} ${21}
                            fi
                    fi
                fi        
            fi
        fi
    fi
fi
echo this is the ip addr of the main node
echo $2
echo 'this is the public dns for the main node'
echo $3
echo this is the ip addr of the secondary node
echo $4
echo this is the public dns of the secondary node
echo $5
echo slaves ip array
echo $6
echo slaves dns array
# # declare -a allip=($6 $8)
# # for i in "${allip[@]}"
# # do
# #    echo "$i"
# # done








ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./data2.sh $1 $3 $5 $7 $9 ${11} ${13} ${15} ${17} ${19} ${21}

ssh -o StrictHostKeyChecking=no ubuntu@$6 -i $1 'bash -s' < ./data2slave.sh $1 $7
if [[ ${8} != "STOP" ]]; then 
    ssh -o StrictHostKeyChecking=no ubuntu@$8 -i $1 'bash -s' < ./data2slave.sh $1 $9
    if [[ ${10} != "STOP" ]]; then
        ssh -o StrictHostKeyChecking=no ubuntu@${10} -i $1 'bash -s' < ./data2slave.sh $1 ${11}
        
        if [[ ${12} != "STOP" ]]; then
            ssh -o StrictHostKeyChecking=no ubuntu@${12} -i $1 'bash -s' < ./data2slave.sh $1 ${13}
            
            if [[ ${14} != "STOP" ]]; then
                ssh -o StrictHostKeyChecking=no ubuntu@${14} -i $1 'bash -s' < ./data2slave.sh $1 ${15}

                if [[ ${16} != "STOP" ]]; then
                    ssh -o StrictHostKeyChecking=no ubuntu@${16} -i $1 'bash -s' < ./data2slave.sh $1 ${17}
                    
                    if [[ ${18} != "STOP" ]]; then
                        ssh -o StrictHostKeyChecking=no ubuntu@${18} -i $1 'bash -s' < ./data2slave.sh $1 ${19}
                        
                        if [[ ${20} != "STOP" ]]; then
                            ssh -o StrictHostKeyChecking=no ubuntu@${20} -i $1 'bash -s' < ./data2slave.sh $1 ${21}
                            fi
                    fi
                fi        
            fi
        fi
    fi
fi
ssh -o StrictHostKeyChecking=no ubuntu@$2 -i $1 'bash -s' < ./data3.sh $1 $3
