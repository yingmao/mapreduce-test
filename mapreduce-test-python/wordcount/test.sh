#!/bin/sh
set -e

../../start.sh

HDFS="/usr/local/hadoop/bin/hdfs"
HADOOP="/usr/local/hadoop/bin/hadoop"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

$HDFS dfs -rm -r -f /wordcount/input/
$HDFS dfs -rm -r -f /wordcount/output/
$HDFS dfs -mkdir -p /wordcount/input/
$HDFS dfs -copyFromLocal ../../mapreduce-test-data/test.txt /wordcount/input/

$HADOOP jar "$STREAMING_JAR" \
  -file ../../mapreduce-test-python/wordcount/mapper.py \
  -mapper ../../mapreduce-test-python/wordcount/mapper.py \
  -file ../../mapreduce-test-python/wordcount/reducer.py \
  -reducer ../../mapreduce-test-python/wordcount/reducer.py \
  -input /wordcount/input/* \
  -output /wordcount/output/

$HDFS dfs -cat /wordcount/output/part-00000

$HDFS dfs -rm -r -f /wordcount/input/
$HDFS dfs -rm -r -f /wordcount/output/

../../stop.sh
