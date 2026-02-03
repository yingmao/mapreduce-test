#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def main() -> int:
    counts = {}

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue

        word, num_str = parts
        try:
            num = int(num_str)
        except ValueError:
            continue

        counts[word] = counts.get(word, 0) + num

    for word in sorted(counts):
        print(f"{word}\t{counts[word]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
