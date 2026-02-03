#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main() -> int:
    counts = {}

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue

        key, num_str = parts
        try:
            num = int(num_str)
        except ValueError:
            continue

        counts[key] = counts.get(key, 0) + num

    for key in sorted(counts):
        print(f"{key}\t{counts[key]}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
