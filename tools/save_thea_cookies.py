#!/usr/bin/env python3
"""
Save Thea Cookies Script
========================

Simple script to save cookies from an already logged-in browser session.
This allows the automated system to reuse your existing login.

Usage:
    python save_thea_cookies.py

Instructions:
1. Make sure you're already logged into ChatGPT/Thea in your browser
2. Run this script
3. It will open a browser, navigate to Thea, and save your cookies
4. The automated system will then use these cookies for future sessions
"""

import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_thea_cookies():
    """Save cookies from current browser session."""
    
    print("🍪 Thea Cookie Saver")
    print("=" * 30)
    
    # Thea URL
    thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5"
    
    # Setup Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = None
    
    try:
        print("🚀 Starting browser...")
        
        # Initialize Chrome driver with webdriver_manager
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
        
        # Check if we're logged in
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"📄 Current URL: {current_url}")
        print(f"📄 Page Title: {page_title}")
        
        # Look for login indicators
        try:
            # Check for login page elements
            login_elements = driver.find_elements("xpath", "//button[contains(text(), 'Log in')]")
            if login_elements:
                print("🔒 Login page detected - you need to log in manually")
                print("👤 Please log in manually in the browser window that opened")
                input("🎯 Press Enter after you have logged in...")
                
                # Refresh to get the logged-in state
                driver.refresh()
                time.sleep(3)
        except:
            pass
        
        # Get cookies
        print("🍪 Extracting cookies...")
        cookies = driver.get_cookies()
        
        if not cookies:
            print("❌ No cookies found - you may not be logged in")
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
        
        # Test cookie loading
        print("🧪 Testing cookie loading...")
        driver.delete_all_cookies()
        
        # Load cookies back
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"⚠️  Warning: Could not add cookie {cookie.get('name', 'unknown')}: {e}")
        
        # Refresh to test
        driver.refresh()
        time.sleep(3)
        
        # Check if still logged in
        final_url = driver.current_url
        print(f"🔍 Final URL after cookie reload: {final_url}")
        
        if "login" not in final_url.lower() and "auth" not in final_url.lower():
            print("✅ Cookie test successful - you should still be logged in")
            return True
        else:
            print("❌ Cookie test failed - you may need to log in again")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if driver:
            print("🔄 Closing browser...")
            driver.quit()
            print("✅ Browser closed")

def main():
    """Main function."""
    print("🍪 Thea Cookie Saver")
    print("=" * 50)
    print("This script will save your Thea/ChatGPT cookies for automated use.")
    print()
    print("Prerequisites:")
    print("1. You should already be logged into ChatGPT in your regular browser")
    print("2. Make sure you can access the Thea Manager GPT")
    print()
    
    proceed = input("Continue? (y/n): ").lower().strip()
    if proceed != 'y':
        print("❌ Cancelled")
        return
    
    success = save_thea_cookies()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("✅ Cookies saved successfully")
        print("🤖 The automated system can now use these cookies")
        print("📁 Cookie file: data/thea_cookies.json")
    else:
        print("\n❌ FAILED")
        print("⚠️  Cookies could not be saved or tested")
        print("💡 Make sure you're logged into ChatGPT/Thea first")

if __name__ == "__main__":
    main()
