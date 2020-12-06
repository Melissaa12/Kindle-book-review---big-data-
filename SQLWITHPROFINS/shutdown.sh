sudo su hadoop
#shutting down both hadoop and spark cluster
/opt/spark-3.0.1-bin-hadoop3.2/sbin/start-all.sh
/opt/hadoop-3.3.0/sbin/stop-dfs.sh && /opt/hadoop-3.3.0/sbin/stop-yarn.sh