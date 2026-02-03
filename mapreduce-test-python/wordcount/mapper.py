#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main() -> int:
    for line in sys.stdin:
        for word in line.strip().split():
            print(f"{word}\t1")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
