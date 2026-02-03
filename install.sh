#!/bin/sh
set -e

BASE_DIR="/mapreduce-test"
HADOOP_HOME="/usr/local/hadoop"
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes -o ConnectTimeout=10"

cd "$BASE_DIR"

# Configure manager locally first
python3 "$BASE_DIR/setup.py" --role manager

# Build worker IP list (strip CRLF, trim, drop '-', blanks, comments)
WORKER_IPS=$(
  sed 's/\r$//' "$BASE_DIR/workers" \
  | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
  | grep -Ev '^(#|$|-)$'
)

echo "Workers:"
printf '%s\n' $WORKER_IPS

copy_payload() {
  ip="$1"
  ssh $SSH_OPTS root@"$ip" "rm -rf $BASE_DIR && mkdir -p $BASE_DIR"
  scp $SSH_OPTS "$BASE_DIR/setup.py"  root@"$ip":"$BASE_DIR/"
  scp $SSH_OPTS "$BASE_DIR/manager"   root@"$ip":"$BASE_DIR/"
  scp $SSH_OPTS "$BASE_DIR/workers"   root@"$ip":"$BASE_DIR/"
}

for ip in $WORKER_IPS; do
  echo "==== Worker $ip ===="
  copy_payload "$ip"
  ssh $SSH_OPTS root@"$ip" "cd $BASE_DIR && python3 setup.py --role worker"
  echo "[OK] $ip"
done

echo "Done."
