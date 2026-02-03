#!/bin/sh
set -e

HADOOP_HOME="/usr/local/hadoop"
HDFS="$HADOOP_HOME/bin/hdfs"
MAPRED="$HADOOP_HOME/bin/mapred"

# Start HDFS
"$HADOOP_HOME/sbin/start-dfs.sh"

# Start YARN
"$HADOOP_HOME/sbin/start-yarn.sh"

# Start MapReduce JobHistory Server 
"$MAPRED" --daemon start historyserver

# Leave safemode if needed (safe to run even if already out of safemode)
"$HDFS" dfsadmin -safemode leave || true

