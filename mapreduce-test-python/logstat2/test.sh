#!/bin/sh
set -e

../../start.sh

HDFS="/usr/local/hadoop/bin/hdfs"
HADOOP="/usr/local/hadoop/bin/hadoop"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

$HDFS dfs -rm -r -f /logstat2/input/
/logstat2/output/ 2>/dev/null || true
$HDFS dfs -rm -r -f /logstat2/output/
$HDFS dfs -mkdir -p /logstat2/input/
$HDFS dfs -copyFromLocal ../../mapreduce-test-data/access.log /logstat2/input/

$HADOOP jar "$STREAMING_JAR" \
  -file ../../mapreduce-test-python/logstat2/mapper.py \
  -mapper ../../mapreduce-test-python/logstat2/mapper.py \
  -file ../../mapreduce-test-python/logstat2/reducer.py \
  -reducer ../../mapreduce-test-python/logstat2/reducer.py \
  -input /logstat2/input/* \
  -output /logstat2/output/

$HDFS dfs -cat /logstat2/output/part-00000

$HDFS dfs -rm -r -f /logstat2/input/
$HDFS dfs -rm -r -f /logstat2/output/

../../stop.sh
