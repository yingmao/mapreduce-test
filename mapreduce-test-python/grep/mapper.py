#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("Pattern not found", file=sys.stderr)
        return 1

    pat = re.compile(sys.argv[1])

    for line in sys.stdin:
        if pat.search(line):
            # key \t value
            print("input\t1")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
