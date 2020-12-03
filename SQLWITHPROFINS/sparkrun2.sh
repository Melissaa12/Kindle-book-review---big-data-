sudo su hadoop
jps
cd
sudo tee -a .bashrc << EOF
export PATH=$PATH:/opt/spark-3.0.1-bin-hadoop3.2/bin
export PATH=$PATH:/opt/hadoop-3.3.0/bin
EOF
wget https://istd50043.github.io/assets/scripts/get_data.sh
chmod +x get_data.sh
./get_data.sh
hdfs dfs -mkdir -p /project
hdfs dfs -put kindle_reviews.csv /project/
hdfs dfs -put meta_Kindle_Store.json /project/
source ~/.bashrc
cd ..
cd ..
cd /opt/spark-3.0.1-bin-hadoop3.2/examples/jars
spark-submit --deploy-mode client --class org.apache.spark.examples.SparkPi spark-examples_2.12-3.0.1.jar 10