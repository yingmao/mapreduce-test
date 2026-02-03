#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# Extract IP and hour from common access.log timestamps like: [10/Oct/2000:13:55:36 -0700]
# Your original pattern used '.' which matches any char; here we escape dots for real IPs.
PAT = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\d{4}:(?P<hour>\d{2}):\d{2}.*? ')

def main() -> int:
    for line in sys.stdin:
        m = PAT.search(line)
        if m:
            key = f"[{m.group('hour')}:00]{m.group('ip')}"
            print(f"{key}\t1")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
