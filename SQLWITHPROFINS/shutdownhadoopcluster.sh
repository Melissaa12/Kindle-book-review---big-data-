echo ${MASTERIP}
ssh -o StrictHostKeyChecking=no ubuntu@${MASTERIP} -i key.pem 'bash -s' < ./shutdown.sh
