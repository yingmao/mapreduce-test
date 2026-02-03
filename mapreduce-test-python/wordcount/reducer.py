#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main() -> int:
    current_word = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue

        word, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if word == current_word:
            current_count += count
        else:
            if current_word is not None:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    if current_word is not None:
        print(f"{current_word}\t{current_count}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

