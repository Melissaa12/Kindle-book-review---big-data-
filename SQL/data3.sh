hadoop namenode -format
eval `ssh-agent`
ssh-add dbproject.pem
cd /home/ubuntu/hadoop-3.3.0/etc/hadoop
start-all.sh
hdfs dfsadmin -report


cd
cd hadoop-3.3.0/share/hadoop/mapreduce
hadoop jar hadoop-mapreduce-examples-3.3.0.jar pi 10 1000000
cd

cd hadoop-3.3.0/
wget https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz
tar -xvf spark-3.0.1-bin-hadoop3.2.tgz
mv spark-3.0.1-bin-hadoop3.2.tgz spark
cd
sudo tee -a .bashrc << EOF
export HADOOP_CONF_DIR=/home/ubuntu/hadoop-3.3.0/etc/hadoop
export SPARK_HOME=/home/ubuntu/hadoop-3.3.0/spark-3.0.1-bin-hadoop3.2
export PATH="\$PATH":/home/ubuntu/hadoop-3.3.0/spark-3.0.1-bin-hadoop3.2/bin
export LD_LIBRARY_PATH=/home/ubuntu/hadoop-3.3.0/lib/native:"\$LD_LIBRARY_PATH"
EOF
source ~/.bashrc    
sudo tee /home/ubuntu/hadoop-3.3.0/spark-3.0.1-bin-hadoop3.2/conf/spark-defaults.conf << EOF

spark.master yarn
spark.driver.memory 512m
spark.yarn.am.memory 512m
spark.executor.memory 512m  

EOF
source ~/.bashrc  

spark-submit --deploy-mode client --class org.apache.spark.examples.SparkPi /home/ubuntu/hadoop-3.3.0/spark-3.0.1-bin-hadoop3.2/examples/jars/spark-examples_2.12-3.0.1.jar 10
