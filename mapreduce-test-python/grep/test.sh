#!/bin/sh
set -e

base_dir=$(cd "$(dirname "$0")"; pwd)

../../start.sh

/usr/local/hadoop/bin/hdfs dfs -rm -r -f /grep/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r -f /grep/output/
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /grep/input/
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal ../../mapreduce-test-data/test.txt /grep/input/

STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

# Option A: rely on shebang + executable bit
# chmod +x ../../mapreduce-test-python/grep/mapper.py ../../mapreduce-test-python/grep/reducer.py

/usr/local/hadoop/bin/hadoop jar "$STREAMING_JAR" \
  -file ../../mapreduce-test-python/grep/mapper.py \
  -mapper "../../mapreduce-test-python/grep/mapper.py world" \
  -file ../../mapreduce-test-python/grep/reducer.py \
  -reducer ../../mapreduce-test-python/grep/reducer.py \
  -input /grep/input/* \
  -output /grep/output/

/usr/local/hadoop/bin/hdfs dfs -cat /grep/output/part-00000

/usr/local/hadoop/bin/hdfs dfs -rm -r -f /grep/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r -f /grep/output/

../../stop.sh
