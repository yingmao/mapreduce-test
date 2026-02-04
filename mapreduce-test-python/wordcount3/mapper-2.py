#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue

        word, freq = parts
        # emit "frequency \t word"
        print(f"{freq}\t{word}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
