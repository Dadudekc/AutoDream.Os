#!/usr/bin/env python3
"""Analyze existing cookies to identify loading issues."""

import json
from pathlib import Path

def analyze_cookies():
    cookie_file = Path("data/thea_cookies.json")
    if not cookie_file.exists():
        print("❌ No cookie file found")
        return
    
    with open(cookie_file, "r") as f:
        cookies = json.load(f)
    
    print(f"🍪 Cookie Analysis: {len(cookies)} cookies found")
    print("=" * 40)
    
    for i, cookie in enumerate(cookies[:5]):  # Show first 5
        print(f"{i+1}. {cookie.get('name', 'unknown')}")
        print(f"   Domain: {cookie.get('domain', 'unknown')}")
        print(f"   Path: {cookie.get('path', 'unknown')}")
        print(f"   Secure: {cookie.get('secure', False)}")
        print(f"   HttpOnly: {cookie.get('httpOnly', False)}")
        print()
    
    # Check for common issues
    issues = []
    
    # Check domain format
    for cookie in cookies:
        domain = cookie.get('domain', '')
        if domain.startswith('.'):
            issues.append(f"Domain prefix issue: {domain}")
    
    # Check for session cookies
    session_cookies = [c for c in cookies if c.get('name', '').lower().find('session') != -1]
    if not session_cookies:
        issues.append("No session cookies found")
    
    if issues:
        print("⚠️  POTENTIAL ISSUES:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ Cookie structure looks good")

if __name__ == "__main__":
    analyze_cookies()
