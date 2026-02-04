#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta, timezone

METHODS = ["GET", "POST"]
PATHS = [
    "/activity.php",
    "/index.html",
    "/api/v1/login",
    "/api/v1/logout",
    "/weather/weather_data_new.php?city=Beijing",
    "/weather/weather_data_new.php?city=Shanghai",
    "/save_token.php?token=abc123&os=IOS&version=12.1.2&type=iPhone10,3",
    "/static/app.js",
    "/static/app.css",
    "/images/logo.png",
]
UAS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "curl/8.5.0",
]

STATUS_CODES = [200, 200, 200, 204, 301, 400, 401, 404, 500]  # biased toward 200


def rand_ipv4() -> str:
    # Avoid 0/255 in octets to look more “realistic”
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def apache_time(dt: datetime) -> str:
    # Example: 03/Feb/2026:12:34:56 +0000
    return dt.strftime("%d/%b/%Y:%H:%M:%S %z")


def gen_line(dt: datetime) -> str:
    ip = rand_ipv4()
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    status = random.choice(STATUS_CODES)
    size = random.randint(20, 5000)
    ua = random.choice(UAS)

    # Common-ish combined format (simplified, but matches your regex needs)
    # Note: Your mapper regexes look for: IP ... "WORD <something> "
    return (
        f'{ip} - - [{apache_time(dt)}] '
        f'"{method} {path} HTTP/1.1" "{status}" {size} '
        f'"-" "{ua}" "-"'
    )


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", type=int, default=2000, help="Number of log lines to generate")
    ap.add_argument("--hours", type=int, default=24, help="Span of hours to spread timestamps across")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    ap.add_argument("--out", default="access.log", help="Output filename")
    args = ap.parse_args()

    random.seed(args.seed)

    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=args.hours)

    with open(args.out, "w", encoding="utf-8") as f:
        for _ in range(args.lines):
            # random timestamp in [start, now]
            dt = start + timedelta(seconds=random.randint(0, args.hours * 3600))
            f.write(gen_line(dt) + "\n")

    print(f"Wrote {args.lines} lines to {args.out}")


if __name__ == "__main__":
    main()

# python3 gen_access_log.py --lines 5000 --hours 24 --out access.log
