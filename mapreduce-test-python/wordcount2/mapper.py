#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def main() -> int:
    for line in sys.stdin:
        words = line.strip().split()
        # emit bigrams: (w0 w1), (w1 w2), ...
        for i in range(1, len(words)):
            print(f"{words[i-1]} {words[i]}\t1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
