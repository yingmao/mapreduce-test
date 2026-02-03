import argparse
import ipaddress
from pathlib import Path

HADOOP_CONF_DIR = Path("/usr/local/hadoop/etc/hadoop")
BASE_DIR = Path("/mapreduce-test")

MANAGER_FILE = BASE_DIR / "manager"
WORKERS_FILE = BASE_DIR / "workers"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"Finished Config: {path.name}")


def read_manager_ip() -> str:
    mip = MANAGER_FILE.read_text(encoding="utf-8", errors="replace").strip()
    ipaddress.ip_address(mip)
    return mip


def read_worker_ips() -> list[str]:
    text = WORKERS_FILE.read_bytes().decode("utf-8", errors="replace")
    ips: list[str] = []
    for line in text.splitlines():
        s = line.replace("\ufeff", "").replace("\u00a0", " ").replace("\r", "").strip()
        if not s or s == "-" or s.startswith("#"):
            continue
        try:
            ipaddress.ip_address(s)
            ips.append(s)
        except ValueError:
            print(f"[WARN] Ignoring non-IP line in workers: {s!r}")
    return ips


def make_mapred_site() -> str:
    # Minimal, clean mapred-site.xml for YARN
    return """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>

  <!-- Ensure MapReduce AM and tasks see HADOOP_MAPRED_HOME -->
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>
  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>
  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>
</configuration>
"""


def make_yarn_site(mip: str) -> str:
    # YARN + shuffle + JobHistory endpoints (JobHistory server itself is separate daemon)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>{mip}</value>
  </property>

  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>

  <property>
    <name>yarn.resourcemanager.webapp.address</name>
    <value>0.0.0.0:8088</value>
  </property>

  <!-- MapReduce JobHistory UI/IPC endpoints -->
  <property>
    <name>mapreduce.jobhistory.address</name>
    <value>{mip}:10020</value>
  </property>
  <property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>0.0.0.0:19888</value>
  </property>
</configuration>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True, choices=["manager", "worker"])
    args = ap.parse_args()

    mip = read_manager_ip()
    workers = read_worker_ips()

    print(f"Role: {args.role}")
    print(f"Manager IP: {mip}")
    print(f"Workers: {workers}")

    # Write configs used by both manager and workers
    write_file(HADOOP_CONF_DIR / "mapred-site.xml", make_mapred_site())
    write_file(HADOOP_CONF_DIR / "yarn-site.xml", make_yarn_site(mip))

    # (Optional) Keep Hadoop workers list consistent too
    (HADOOP_CONF_DIR / "workers").write_text("\n".join(workers) + ("\n" if workers else ""))

    print("Finished MapReduce/YARN configuration.")


if __name__ == "__main__":
    main()
