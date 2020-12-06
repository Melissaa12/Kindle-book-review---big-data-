#!/bin/bash
echo hadoopinstallother
sudo su hadoop
cd ..
cd hadoop
#installation of hadoop
tar zxvf hadoop-3.3.0.tgz
sudo mv hadoop-3.3.0 /opt/
sudo mkdir -p /mnt/hadoop/datanode/
sudo chown -R hadoop:hadoop /mnt/hadoop/datanode/