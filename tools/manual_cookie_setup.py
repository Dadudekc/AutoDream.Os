#!/usr/bin/env python3
"""
Manual Cookie Setup Script
==========================

Simple script to manually set up cookies for Thea automation.
If the automatic cookie extraction doesn't work, use this.

Usage:
    python manual_cookie_setup.py
"""

import json
from pathlib import Path

def manual_cookie_setup():
    """Manual cookie setup with user guidance."""
    
    print("🍪 Manual Cookie Setup")
    print("=" * 30)
    print()
    print("If the automatic cookie extraction isn't working, here's how to manually set up cookies:")
    print()
    print("METHOD 1: Browser Developer Tools")
    print("-" * 35)
    print("1. Open Chrome and go to: https://chatgpt.com")
    print("2. Make sure you're logged in")
    print("3. Press F12 to open Developer Tools")
    print("4. Go to the 'Application' tab")
    print("5. In the left sidebar, expand 'Storage' > 'Cookies'")
    print("6. Click on 'https://chatgpt.com'")
    print("7. Right-click on any cookie and select 'Copy' > 'Copy as cURL'")
    print("8. Or manually copy cookie names and values")
    print()
    
    print("METHOD 2: Export from Browser")
    print("-" * 30)
    print("1. Install a cookie export extension like 'Get cookies.txt'")
    print("2. Export cookies from chatgpt.com")
    print("3. Convert to JSON format")
    print()
    
    print("METHOD 3: Use Browser Profile")
    print("-" * 25)
    print("1. Close all Chrome windows")
    print("2. Start Chrome with: chrome.exe --user-data-dir=./chrome-profile")
    print("3. Log into ChatGPT in this new profile")
    print("4. Run the cookie extractor again")
    print()
    
    # Ask if user wants to try a simple test
    print("QUICK TEST")
    print("-" * 10)
    print("Let's test if the automation system works without cookies first...")
    
    test = input("Test the system without cookies? (y/n): ").lower().strip()
    if test == 'y':
        print("\n🧪 Testing system without cookies...")
        print("Run this command:")
        print("python thea_autonomous.py send 'test message without cookies'")
        print()
        print("This will open a browser and you can log in manually.")
        print("The system will then try to send the message.")
    
    print("\n💡 TROUBLESHOOTING TIPS:")
    print("-" * 25)
    print("1. Make sure you're logged into ChatGPT in your regular browser")
    print("2. Try accessing the Thea Manager GPT directly:")
    print("   https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5")
    print("3. If you see a login page, log in first")
    print("4. Then try the cookie extraction again")
    print("5. The system will work even without cookies - it will just open a browser for you to log in")

def create_minimal_cookies():
    """Create a minimal cookie file for testing."""
    
    print("\n🔧 Creating minimal cookie file for testing...")
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create minimal cookie file
    cookie_file = data_dir / "thea_cookies.json"
    
    # Minimal cookies structure (will be replaced by real cookies)
    minimal_cookies = [
        {
            "name": "session_token",
            "value": "placeholder_session_token",
            "domain": "chatgpt.com",
            "path": "/",
            "secure": True,
            "httpOnly": True
        }
    ]
    
    with open(cookie_file, "w") as f:
        json.dump(minimal_cookies, f, indent=2)
    
    print(f"✅ Created minimal cookie file: {cookie_file}")
    print("⚠️  This is just a placeholder - you'll need real cookies for automation")

def main():
    """Main function."""
    manual_cookie_setup()
    
    # Ask if user wants to create minimal cookies
    minimal = input("\nCreate minimal cookie file for testing? (y/n): ").lower().strip()
    if minimal == 'y':
        create_minimal_cookies()

if __name__ == "__main__":
    main()
