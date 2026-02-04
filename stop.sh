#!/bin/sh
set -e

HADOOP_HOME="/usr/local/hadoop"
MAPRED="$HADOOP_HOME/bin/mapred"

# Stop JobHistory first (reduces YARN activity)
"$MAPRED" --daemon stop historyserver || true

# If your Hadoop build ignores this env var, it does no harm.
export HADOOP_STOP_TIMEOUT=30

# Stop YARN next
"$HADOOP_HOME/sbin/stop-yarn.sh" || true

# Stop HDFS last
"$HADOOP_HOME/sbin/stop-dfs.sh" || true
