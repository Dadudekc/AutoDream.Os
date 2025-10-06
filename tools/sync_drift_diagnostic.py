#!/usr/bin/env python3
"""
Sync Drift Diagnostic Tool
==========================

Quick diagnostic to identify cookie authentication pipeline issues.
Checks browser environment, cookie accessibility, and agent-THEA handshake.
"""

import json
import os
import sys
from pathlib import Path

def check_browser_environment():
    """Check browser environment and cookie accessibility."""
    print("🔍 BROWSER ENVIRONMENT CHECK")
    print("=" * 40)
    
    # Check if we can import browser automation libraries
    try:
        import undetected_chromedriver as uc
        print("✅ Undetected Chrome: Available")
    except ImportError:
        print("❌ Undetected Chrome: Not available")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ Selenium + webdriver_manager: Available")
    except ImportError:
        print("❌ Selenium + webdriver_manager: Not available")
    
    # Check Chrome installation
    try:
        import webbrowser
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Chrome found: {path}")
                chrome_found = True
                break
        
        if not chrome_found:
            print("⚠️  Chrome executable not found in standard locations")
            
    except Exception as e:
        print(f"❌ Chrome check failed: {e}")

def check_cookie_files():
    """Check existing cookie files and data directory."""
    print("\n🍪 COOKIE FILES CHECK")
    print("=" * 30)
    
    # Check data directory
    data_dir = Path("data")
    if data_dir.exists():
        print("✅ Data directory exists")
        
        # Check cookie files
        cookie_file = data_dir / "thea_cookies.json"
        if cookie_file.exists():
            try:
                with open(cookie_file, "r") as f:
                    cookies = json.load(f)
                print(f"✅ Cookie file exists: {len(cookies)} cookies")
                
                # Check cookie structure
                if cookies and len(cookies) > 0:
                    sample_cookie = cookies[0]
                    required_fields = ['name', 'value', 'domain']
                    missing_fields = [field for field in required_fields if field not in sample_cookie]
                    
                    if not missing_fields:
                        print("✅ Cookie structure: Valid")
                    else:
                        print(f"⚠️  Cookie structure: Missing fields {missing_fields}")
                else:
                    print("⚠️  Cookie file: Empty")
                    
            except Exception as e:
                print(f"❌ Cookie file: Corrupted ({e})")
        else:
            print("❌ Cookie file: Not found")
    else:
        print("❌ Data directory: Not found")

def check_agent_environment():
    """Check agent environment and workspace configuration."""
    print("\n🤖 AGENT ENVIRONMENT CHECK")
    print("=" * 35)
    
    # Check current working directory
    cwd = os.getcwd()
    print(f"📁 Working directory: {cwd}")
    
    # Check if we're in the right project
    if "Agent_Cellphone_V2_Repository" in cwd:
        print("✅ Project namespace: Correct")
    else:
        print("⚠️  Project namespace: May be incorrect")
    
    # Check Python path
    python_path = sys.executable
    print(f"🐍 Python path: {python_path}")
    
    # Check environment variables
    env_vars = ['PATH', 'PYTHONPATH', 'USERPROFILE']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        if var == 'PATH':
            print(f"🔧 {var}: {len(value.split(';'))} entries")
        else:
            print(f"🔧 {var}: {value[:50]}..." if len(value) > 50 else f"🔧 {var}: {value}")

def check_thea_url_accessibility():
    """Check THEA URL accessibility and configuration."""
    print("\n🌐 THEA URL ACCESSIBILITY CHECK")
    print("=" * 40)
    
    thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5"
    print(f"🎯 Target URL: {thea_url}")
    
    # Check if URL is accessible
    try:
        import urllib.request
        import urllib.error
        
        # Try to access the URL (without following redirects)
        req = urllib.request.Request(thea_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            print(f"✅ URL accessibility: HTTP {status_code}")
            
            # Check if we're redirected to login
            final_url = response.geturl()
            if final_url != thea_url:
                print(f"🔄 Redirected to: {final_url}")
                if "login" in final_url.lower() or "auth" in final_url.lower():
                    print("⚠️  Redirected to login page - authentication required")
            else:
                print("✅ No redirect detected")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def generate_fix_recommendations():
    """Generate specific fix recommendations based on findings."""
    print("\n🔧 FIX RECOMMENDATIONS")
    print("=" * 30)
    
    print("1. 🍪 Cookie Setup:")
    print("   - Run: python extract_browser_cookies.py")
    print("   - Or: python save_thea_cookies.py")
    print("   - Ensure you're logged into ChatGPT in your browser first")
    
    print("\n2. 🌐 Browser Configuration:")
    print("   - Enable 3rd-party cookies in Chrome settings")
    print("   - Disable incognito/private mode")
    print("   - Clear browser cache and cookies")
    print("   - Try: chrome://settings/cookies")
    
    print("\n3. 🔧 Environment Fixes:")
    print("   - Ensure you're in the correct project directory")
    print("   - Update Chrome to latest version")
    print("   - Restart browser after cookie changes")
    
    print("\n4. 🧪 Testing:")
    print("   - Test with: python login_helper.py")
    print("   - Then: python thea_autonomous.py send 'test'")

def main():
    """Run complete diagnostic."""
    print("🚨 SYNC DRIFT DIAGNOSTIC")
    print("=" * 50)
    print("Diagnosing cookie authentication pipeline issues...")
    print()
    
    check_browser_environment()
    check_cookie_files()
    check_agent_environment()
    check_thea_url_accessibility()
    generate_fix_recommendations()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Address any ❌ errors above")
    print("2. Run cookie extraction if needed")
    print("3. Test with login_helper.py")
    print("4. Verify agent-THEA handshake")

if __name__ == "__main__":
    main()
