#!/bin/sh
set -e

../../start.sh

HDFS="/usr/local/hadoop/bin/hdfs"
HADOOP="/usr/local/hadoop/bin/hadoop"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

# Clean
$HDFS dfs -rm -r -f /wordcount3/input/  || true
$HDFS dfs -rm -r -f /wordcount3/output/ || true
$HDFS dfs -rm -r -f /wordcount3-2/output/ || true

# Input
$HDFS dfs -mkdir -p /wordcount3/input/
$HDFS dfs -copyFromLocal ../../mapreduce-test-data/test.txt /wordcount3/input/

# Stage 1
$HADOOP jar "$STREAMING_JAR" \
  -files ../../mapreduce-test-python/wordcount3/mapper-1.py,../../mapreduce-test-python/wordcount3/reducer-1.py \
  -mapper ../../mapreduce-test-python/wordcount3/mapper-1.py \
  -reducer ../../mapreduce-test-python/wordcount3/reducer-1.py \
  -input /wordcount3/input/* \
  -output /wordcount3/output/

# Stage 2
$HADOOP jar "$STREAMING_JAR" \
  -files ../../mapreduce-test-python/wordcount3/mapper-2.py,../../mapreduce-test-python/wordcount3/reducer-2.py \
  -mapper ../../mapreduce-test-python/wordcount3/mapper-2.py \
  -reducer ../../mapreduce-test-python/wordcount3/reducer-2.py \
  -input /wordcount3/output/* \
  -output /wordcount3-2/output/

$HDFS dfs -cat /wordcount3-2/output/part-00000 | tail -10

# Clean up
$HDFS dfs -rm -r -f /wordcount3/input/
$HDFS dfs -rm -r -f /wordcount3/output/
$HDFS dfs -rm -r -f /wordcount3-2/output/

../../stop.sh
