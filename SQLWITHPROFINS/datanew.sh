echo masterip
echo $1
echo secondaryip
echo $2
echo slave1ip
echo $3
echo slave2ip
echo $4
echo $5
echo $6
echo $7
echo $8
echo $9
echo ${10}

export LC_ALL=C
#create new hadoop user
sudo adduser hadoop --gecos "" --disabled-password
#do config for hosts entering privateIP,Assigned DNS name
sudo tee /etc/hosts << EOF
127.0.0.1 localhost

${1} com.avg.master
${2} com.avg.slave0
${3} com.avg.slave1
${4} com.avg.slave2
${5} com.avg.slave3
${6} com.avg.slave4
${7} com.avg.slave5
${8} com.avg.slave6
${9} com.avg.slave7
${10} com.avg.slave8

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
EOF

#allow full access for User Hadoop
sudo sh -c 'echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-hadoop'
#change user to hadoop
sudo su hadoop
#set swapiness
sudo sysctl vm.swappiness=10


#key gen
sudo apt-get install -y ssh
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa