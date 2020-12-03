echo masterip
echo $1
echo secondaryip
echo $2
echo slave1ip
echo $3
echo slave2ip
echo $4

export LC_ALL=C
sudo adduser hadoop --gecos "" --disabled-password

sudo tee /etc/hosts << EOF
127.0.0.1 localhost

${1} com.avg.master
${2} com.avg.secondary
${3} com.avg.slave1
${4} com.avg.slave2

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
EOF

sudo sh -c 'echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-hadoop'
sudo su hadoop
sudo sysctl vm.swappiness=10


echo this is to setup key
sudo apt-get install -y ssh
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa