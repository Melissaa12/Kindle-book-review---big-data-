sudo su hadoop
jps
cd
sudo tee -a .bashrc << EOF
export PATH=$PATH:/opt/spark-3.0.1-bin-hadoop3.2/bin
EOF
source ~/.bashrc
cd ..
cd ..
cd /opt/spark-3.0.1-bin-hadoop3.2/examples/jars
spark-submit --deploy-mode client --class org.apache.spark.examples.SparkPi spark-examples_2.12-3.0.1.jar 10