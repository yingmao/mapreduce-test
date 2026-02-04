#!/bin/sh
set -e

../../start.sh

HDFS="/usr/local/hadoop/bin/hdfs"
HADOOP="/usr/local/hadoop/bin/hadoop"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

$HDFS dfs -rm -r -f /wordcount2/input/
$HDFS dfs -rm -r -f /wordcount2/output/
$HDFS dfs -mkdir -p /wordcount2/input/
$HDFS dfs -copyFromLocal ../../mapreduce-test-data/test.txt /wordcount2/input/

$HADOOP jar "$STREAMING_JAR" \
  -files ../../mapreduce-test-python/wordcount2/mapper.py,../../mapreduce-test-python/wordcount2/reducer.py \
  -mapper ../../mapreduce-test-python/wordcount2/mapper.py \
  -reducer ../../mapreduce-test-python/wordcount2/reducer.py \
  -input /wordcount2/input/* \
  -output /wordcount2/output/

$HDFS dfs -cat /wordcount2/output/part-00000 | tail -100

$HDFS dfs -rm -r -f /wordcount2/input/
$HDFS dfs -rm -r -f /wordcount2/output/

../../stop.sh
