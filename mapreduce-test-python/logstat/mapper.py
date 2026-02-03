#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# Typical access log begins with: "1.2.3.4 - - [date] "GET /path ..."
# Capture IP; keep the rest unused.
PAT = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?"\w+ (?P<subdir>.*?) ')

def main() -> int:
    for line in sys.stdin:
        m = PAT.search(line)
        if m:
            # Emit: ip \t 1
            print(f"{m.group('ip')}\t1")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
