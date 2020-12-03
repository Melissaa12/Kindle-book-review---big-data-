#remember to pass the aws dns name here to change the hostname
sudo hostname $2
sudo tee /etc/hosts << EOF
${2} ${3}

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
EOF

# sudo tee /etc/hosts << EOF
# 3.236.16.254 ec2-3-236-16-254.compute-1.amazonaws.com

# # The following lines are desirable for IPv6 capable hosts
# ::1 ip6-localhost ip6-loopback
# fe00::0 ip6-localnet
# ff00::0 ip6-mcastprefix
# ff02::1 ip6-allnodes
# ff02::2 ip6-allrouters
# ff02::3 ip6-allhosts
# EOF

sudo apt-get update

#Installing java 
yes "" | sudo add-apt-repository ppa:webupd8team/java
yes Y|sudo apt-get update
yes Y|sudo apt install openjdk-8-jdk

#Installing hadoop
wget https://apachemirror.sg.wuchna.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
echo prev here
tar -xzvf hadoop-3.3.0.tar.gz

#change config file for .bashrc
echo changing config file here
cd
sudo tee .bashrc << EOF
export HADOOP_CONF=/home/ubuntu/hadoop-3.3.0/etc/hadoop
export HADOOP_PREFIX=/home/ubuntu/hadoop-3.3.0
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# Add Hadoop bin/ directory to path
export PATH="\$PATH":/home/ubuntu/hadoop-3.3.0/bin
export PATH="\$PATH":/home/ubuntu/hadoop-3.3.0/sbin
EOF
source ~/.bashrc
chmod 644 .ssh/authorized_keys



#gitclone repo to get the pem key
git clone https://ryangen97:Sherene31071997@github.com/ryangen97/DBProject.git
cd DBProject
cd SQL
#move the pem key to the main dir
mv dbproject.pem ~/


cd
sudo chmod 400 dbproject.pem
eval `ssh-agent`
ssh-add dbproject.pem

echo adding at hadoopenvsh
cd
sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/hadoop-env.sh << EOF
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
EOF

echo adding at hadoopcoresite
sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/core-site.xml << EOF
<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://${3}:8020</value>
</property>

<property>
<name>hadoop.tmp.dir</name>
<value>/home/ubuntu/hdfstmp</value>
</property>

</configuration>
EOF

cd
mkdir hdfstmp


# sudo tee $HADOOP_CONF/hdfs-site.xml << EOF
# <configuration>
# <property>
# <name>dfs.replication</name>
# <value>2</value>
# </property>
# <property>
# <name>dfs.permissions</name>
# <value>false</value>
# </property>
# </configuration>
# EOF


# This is what mel suggested might fix
# sudo tee $HADOOP_CONF/hdfs-site.xml << EOF
# <configuration>
#    <property>
#        <name>dfs.webhdfs.enabled</name>
#        <value>false</value>
#    </property>
#    <property>
#        <name>dfs.replication</name>
#        <value>2</value>
#    </property>
#    <property>
#        <name>dfs.namenode.name.dir</name>
#        <value>ec2-3-90-89-241.compute-1.amazonaws.com</value>
#    </property>
#    <property>
#        <name>dfs.datanode.data.dir</name>
#        <value>ec2-54-83-177-66.compute-1.amazonaws.com</value>
#    </property>
# </configuration>
# EOF


sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/hdfs-site.xml << EOF
<configuration>
   <property>
       <name>dfs.webhdfs.enabled</name>
       <value>false</value>
   </property>
   <property>
       <name>dfs.replication</name>
       <value>2</value>
   </property>
</configuration>
EOF

sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/mapred-site.xml << EOF
<configuration>
<property>
<name>mapred.job.tracker</name>
<value>hdfs://${3}:8021</value>
</property>
</configuration>
EOF









