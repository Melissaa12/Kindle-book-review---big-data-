#!/bin/bash
echo hadoopinstall2
#installation
sudo mkdir -p /mnt/hadoop/namenode/hadoop-${USER}
sudo chown -R hadoop:hadoop /mnt/hadoop/namenode
sudo su hadoop



#starting up hadoop
yes Y|/opt/hadoop-3.3.0/bin/hdfs namenode -format
/opt/hadoop-3.3.0/sbin/start-dfs.sh && /opt/hadoop-3.3.0/sbin/start-yarn.sh
/opt/hadoop-3.3.0/bin/hdfs dfsadmin -report



#spark installation
cd ..
cd hadoop 
cd download
wget https://apachemirror.sg.wuchna.com/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz
tar zxvf spark-3.0.1-bin-hadoop3.2.tgz
touch spark-3.0.1-bin-hadoop3.2/conf/spark-env.sh
cp spark-3.0.1-bin-hadoop3.2/conf/spark-env.sh.template \spark-3.0.1-bin-hadoop3.2/conf/spark-env.sh

#spark configuration
echo -e "
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 export HADOOP_HOME=/opt/hadoop-3.3.0
export SPARK_HOME=/opt/spark-3.0.1-bin-hadoop3.2 export SPARK_CONF_DIR=\${SPARK_HOME}/conf
export HADOOP_CONF_DIR=\${HADOOP_HOME}/etc/hadoop export YARN_CONF_DIR=\${HADOOP_HOME}/etc/hadoop export SPARK_EXECUTOR_CORES=1
export SPARK_EXECUTOR_MEMORY=2G
export SPARK_DRIVER_MEMORY=1G
export PYSPARK_PYTHON=python3
" >> spark-3.0.1-bin-hadoop3.2/conf/spark-env.sh

#configure slaves
WORKERS="com.avg.slave0 com.avg.slave1 com.avg.slave2 com.avg.slave3 com.avg.slave4 com.avg.slave5 com.avg.slave6 com.avg.slave7 com.avg.slave8"
for ip in ${WORKERS};
do echo -e "${ip}" >> spark-3.0.1-bin-hadoop3.2/conf/slaves; done
#for deployment
tar czvf spark-3.0.1-bin-hadoop3.2.tgz spark-3.0.1-bin-hadoop3.2/
for i in ${WORKERS};
do scp spark-3.0.1-bin-hadoop3.2.tgz $i:./spark-3.0.1-bin-hadoop3.2.tgz;
done
mv spark-3.0.1-bin-hadoop3.2.tgz ~/.

#Installation on all nodes
cd ~
tar zxvf spark-3.0.1-bin-hadoop3.2.tgz
sudo mv spark-3.0.1-bin-hadoop3.2 /opt/
sudo chown -R hadoop:hadoop /opt/spark-3.0.1-bin-hadoop3.2