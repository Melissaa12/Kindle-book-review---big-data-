#remember to pass the aws dns name here to change the hostname
sudo hostname $1
sudo apt-get update

yes "" | sudo add-apt-repository ppa:webupd8team/java
yes Y|sudo apt-get update
yes Y|sudo apt install openjdk-8-jdk

wget https://apachemirror.sg.wuchna.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar -xzvf hadoop-3.3.0.tar.gz

cd
sudo tee .bashrc << EOF
export HADOOP_CONF=/home/ubuntu/hadoop-3.3.0/etc/hadoop
export HADOOP_PREFIX=/home/ubuntu/hadoop-3.3.0
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# Add Hadoop bin/ directory to path
export PATH=$PATH:$HADOOP_PREFIX/bin
export PATH=$PATH:$HADOOP_PREFIX/sbin
EOF

git clone https://ryangen97:Sherene31071997@github.com/ryangen97/DBProject.git
chmod 644 .ssh/authorized_keys
cd DBProject
cd SQL
mv dbproject.pem ~/
# pemkey
cd
sudo chmod 400 dbproject.pem
eval `ssh-agent`
ssh-add dbproject.pem

sudo tee $HADOOP_CONF/hadoop-env.sh << EOF
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
EOF
sudo tee $HADOOP_CONF/core-site.xml << EOF
<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://${1}:8020</value>
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

sudo tee $HADOOP_CONF/hdfs-site.xml << EOF
<configuration>
   <property>
       <name>dfs.webhdfs.enabled</name>
       <value>false</value>
   </property>
   <property>
       <name>dfs.replication</name>
       <value>2</value>
   </property>
   <property>
       <name>dfs.namenode.name.dir</name>
       <value>ec2-3-90-89-241.compute-1.amazonaws.com</value>
   </property>
   <property>
       <name>dfs.datanode.data.dir</name>
       <value>ec2-54-83-177-66.compute-1.amazonaws.com</value>
   </property>
</configuration>
EOF

sudo tee $HADOOP_CONF/hdfs-site.xml << EOF
<configuration>
<property>
<name>mapred.job.tracker</name>
<value>hdfs://${1}:8021</value>
</property>
</configuration>
EOF

# do this for each of the slave nodes
scp hadoop-env.sh core-site.xml hdfs-site.xml mapred-site.xml ubuntu@<slavenodehostname>.compute-1.amazonaws.com:/home/ubuntu/hadoop-3.3.0/etc/hadoop


sudo tee $HADOOP_CONF/masters << EOF
<hostnameformaster>
<hostnameforsecondary>
EOF



# sudo tee $HADOOP_CONF/masters << EOF
# ec2-3-90-89-241.compute-1.amazonaws.com
# ec2-54-83-177-66.compute-1.amazonaws.com
# EOF

sudo tee $HADOOP_CONF/slaves << EOF
<hostnameforslaves>
EOF


# sudo tee $HADOOP_CONF/slaves << EOF
# ec2-18-209-164-190.compute-1.amazonaws.com
# EOF