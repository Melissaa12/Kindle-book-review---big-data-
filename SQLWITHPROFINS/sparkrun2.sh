#!/bin/bash
sudo su hadoop
jps
cd
sudo apt-get -y install zip unzip
sudo tee -a .bashrc << EOF
export PATH=\$PATH:/opt/spark-3.0.1-bin-hadoop3.2/bin
export PATH=\$PATH:/opt/hadoop-3.3.0/bin
export PATH=\$PATH:/opt/hadoop-3.3.0/sbin
EOF
source ~/.bashrc
sudo git clone https://ryangen97:Sherene31071997@github.com/ryangen97/DBProject.git 
wget https://istd50043.github.io/assets/scripts/get_data.sh
chmod +x get_data.sh
./get_data.sh
sudo su hadoop
which hdfs
/opt/hadoop-3.3.0/bin/hdfs dfs -mkdir -p /project
/opt/hadoop-3.3.0/bin/hdfs dfs -put kindle_reviews.csv /project/
/opt/hadoop-3.3.0/bin/hdfs dfs -put meta_Kindle_Store.json /project/
cd DBProject
/opt/hadoop-3.3.0/bin/hdfs dfs -put data/mongo_price_asin.csv /project/
cd ..
cd ..
cd ..
cd /opt/spark-3.0.1-bin-hadoop3.2/examples/jars
/opt/spark-3.0.1-bin-hadoop3.2/bin/spark-submit --deploy-mode client --class org.apache.spark.examples.SparkPi spark-examples_2.12-3.0.1.jar 10
