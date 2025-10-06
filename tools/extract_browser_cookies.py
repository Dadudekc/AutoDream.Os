#!/usr/bin/env python3
"""
Extract Browser Cookies Script
==============================

Extract cookies from your existing browser session and save them for automation.
This works with your current logged-in browser tabs.

Usage:
    python extract_browser_cookies.py
"""

import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_cookies_from_existing_session():
    """Extract cookies using undetected Chrome."""
    
    print("🍪 Undetected Chrome Cookie Extractor")
    print("=" * 40)
    
    # Thea URL
    thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5"
    
    # Try to use undetected Chrome first
    try:
        import undetected_chromedriver as uc
        print("✅ Undetected Chrome available")
        use_undetected = True
    except ImportError:
        print("⚠️  Undetected Chrome not available, using regular Chrome")
        use_undetected = False
    
    driver = None
    
    try:
        if use_undetected:
            print("🚀 Starting undetected Chrome...")
            
            # Configure undetected Chrome
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # Try to use existing profile
            import os
            user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
            if os.path.exists(user_data_dir):
                options.add_argument(f"--user-data-dir={user_data_dir}")
                options.add_argument("--profile-directory=Default")
                print("✅ Using existing Chrome profile with undetected Chrome")
            
            # Initialize undetected Chrome
            driver = uc.Chrome(options=options)
            
        else:
            print("🚀 Starting regular Chrome...")
            
            # Setup regular Chrome options
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # Initialize regular Chrome
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=options
            )
        
        print("✅ Browser started successfully")
        print(f"🌐 Navigating to: {thea_url}")
        
        # Navigate to Thea
        driver.get(thea_url)
        
        print("⏳ Waiting for page to load...")
        time.sleep(5)
        
        # Check current state
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"📄 Current URL: {current_url}")
        print(f"📄 Page Title: {page_title}")
        
        # Check if we can find the prompt textarea
        try:
            textarea = driver.find_element("css selector", "#prompt-textarea")
            if textarea and textarea.is_displayed():
                print("✅ Found #prompt-textarea - you're logged in!")
                logged_in = True
            else:
                print("⚠️  #prompt-textarea not found or not visible")
                logged_in = False
        except:
            print("⚠️  Could not find #prompt-textarea")
            logged_in = False
        
        # If not logged in, let user log in manually
        if not logged_in:
            print("🔒 You need to log in manually")
            print("👤 Please log in using the browser window that opened")
            input("🎯 Press Enter after you have logged in and can see the Thea interface...")
            
            # Check again after manual login
            try:
                textarea = driver.find_element("css selector", "#prompt-textarea")
                if textarea and textarea.is_displayed():
                    print("✅ Great! You're now logged in")
                    logged_in = True
                else:
                    print("⚠️  Still can't find #prompt-textarea")
            except:
                print("⚠️  Still can't access Thea interface")
        
        if logged_in:
            # Get cookies
            print("🍪 Extracting cookies...")
            cookies = driver.get_cookies()
            
            if not cookies:
                print("❌ No cookies found")
                return False
            
            print(f"✅ Found {len(cookies)} cookies")
            
            # Create data directory
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            # Save cookies to file
            cookie_file = data_dir / "thea_cookies.json"
            with open(cookie_file, "w") as f:
                json.dump(cookies, f, indent=2)
            
            print(f"💾 Cookies saved to: {cookie_file}")
            
            # Show some cookie info
            print("\n📊 Cookie Summary:")
            for cookie in cookies[:5]:  # Show first 5 cookies
                print(f"   - {cookie.get('name', 'unknown')}: {cookie.get('domain', 'unknown')}")
            if len(cookies) > 5:
                print(f"   ... and {len(cookies) - 5} more cookies")
            
            print("\n🎉 SUCCESS!")
            print("✅ Cookies extracted and saved successfully")
            print("🤖 The automated system can now use these cookies")
            print("📁 Cookie file: data/thea_cookies.json")
            print("\n💡 You can now close this browser window")
            print("💡 Test with: python thea_autonomous.py send 'test message'")
            
            return True
        else:
            print("❌ Could not access Thea interface")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        # Don't quit the browser immediately - let user see the result
        if driver:
            print("\n🔄 Browser will stay open for you to verify...")
            print("💡 You can close it manually when done")

def main():
    """Main function."""
    print("🍪 Browser Cookie Extractor")
    print("=" * 50)
    print("This script will extract cookies from your existing browser session.")
    print()
    print("Prerequisites:")
    print("1. You should already be logged into ChatGPT in your regular browser")
    print("2. Make sure you can access the Thea Manager GPT")
    print("3. This script will try to use your existing Chrome profile")
    print()
    
    proceed = input("Continue? (y/n): ").lower().strip()
    if proceed != 'y':
        print("❌ Cancelled")
        return
    
    success = extract_cookies_from_existing_session()
    
    if not success:
        print("\n❌ FAILED")
        print("⚠️  Cookies could not be extracted")
        print("💡 Make sure you're logged into ChatGPT/Thea first")
        print("💡 Try logging in manually in the browser window that opened")

if __name__ == "__main__":
    main()
