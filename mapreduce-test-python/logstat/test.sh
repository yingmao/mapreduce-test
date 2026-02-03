#!/bin/sh
set -e

../../start.sh

HDFS="/usr/local/hadoop/bin/hdfs"
HADOOP="/usr/local/hadoop/bin/hadoop"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

$HDFS dfs -rm -r -f /logstat/input/
$HDFS dfs -rm -r -f /logstat/output/
$HDFS dfs -mkdir -p /logstat/input/
$HDFS dfs -copyFromLocal ../../mapreduce-test-data/access.log /logstat/input/

# If mapper/reducer are executable with the python3 shebang, this is enough.
# Otherwise, change -mapper/-reducer to "python3 ...".
$HADOOP jar "$STREAMING_JAR" \
  -file ../../mapreduce-test-python/logstat/mapper.py \
  -mapper ../../mapreduce-test-python/logstat/mapper.py \
  -file ../../mapreduce-test-python/logstat/reducer.py \
  -reducer ../../mapreduce-test-python/logstat/reducer.py \
  -input /logstat/input/* \
  -output /logstat/output/

$HDFS dfs -cat /logstat/output/part-00000

$HDFS dfs -rm -r -f /logstat/input/
$HDFS dfs -rm -r -f /logstat/output/

../../stop.sh
