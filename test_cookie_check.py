#!/usr/bin/env python3
"""Quick cookie check"""
import json
from datetime import datetime

cookies = json.load(open('thea_cookies.json'))
print(f"Total cookies: {len(cookies)}")
print(f"\nCookie breakdown:")

current_time = datetime.now().timestamp()

for i, cookie in enumerate(cookies[:10], 1):
    name = cookie.get('name', 'unknown')
    domain = cookie.get('domain', 'unknown')
    expiry = cookie.get('expiry', None)
    
    if expiry:
        expired = expiry < current_time
        expiry_date = datetime.fromtimestamp(expiry).strftime('%Y-%m-%d')
        status = "EXPIRED" if expired else f"Valid until {expiry_date}"
    else:
        status = "No expiry (session cookie)"
    
    print(f"{i}. {name} | {domain} | {status}")

print(f"\n... and {len(cookies) - 10} more" if len(cookies) > 10 else "")



