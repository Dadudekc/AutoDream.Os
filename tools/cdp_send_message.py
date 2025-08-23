#!/usr/bin/env python3
import sys, json, urllib.request
from urllib.error import URLError

CDP_PORT = 9222
LIST_URL = f"http://127.0.0.1:{CDP_PORT}/json"


def test_cdp_connection():
    try:
        with urllib.request.urlopen(LIST_URL, timeout=2.5) as r:
            targets = json.loads(r.read().decode("utf-8"))
            print(f"CDP Connection Successful! Found {len(targets)} targets:")
            for t in targets:
                title = t.get("title", "Unknown")
                type_info = t.get("type", "Unknown")
                print(f"  - {title} ({type_info})")
            return True
    except URLError:
        print(
            "CDP Connection Failed: Cursor not running with --remote-debugging-port=9222"
        )
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: cdp_send_message.py "Your message here"')
        sys.exit(1)

    message = sys.argv[1]
    print(f"Testing CDP Messenger with message: {message}")

    if test_cdp_connection():
        print("CDP Messenger ready for use!")
    else:
        print("Please launch Cursor with CDP debugging enabled first.")
