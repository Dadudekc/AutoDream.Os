#!/usr/bin/env python3
"""
Login Helper Script
===================

Simple script to help you log into ChatGPT/Thea and then test the system.
This opens a browser, lets you log in manually, then tests the automation.

Usage:
    python login_helper.py
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def login_helper():
    """Help user log in and test the system."""
    
    print("🔐 Login Helper for Thea Automation")
    print("=" * 40)
    
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
        print(f"🌐 Opening: {thea_url}")
        
        # Navigate to Thea
        driver.get(thea_url)
        
        print("\n🔐 LOGIN INSTRUCTIONS:")
        print("-" * 25)
        print("1. The browser window should now be open")
        print("2. If you see a login page, log in with your ChatGPT credentials")
        print("3. Navigate to the Thea Manager GPT if needed")
        print("4. Make sure you can see the message input area")
        print("5. Look for a text area or input field where you can type messages")
        
        input("\n🎯 Press Enter AFTER you have logged in and can see the Thea interface...")
        
        # Check if we can find the input field
        print("\n🔍 Checking for input field...")
        
        input_selectors = [
            "#prompt-textarea",
            "textarea[data-testid*='prompt']",
            "textarea[placeholder*='Message']",
            "textarea",
            "[contenteditable='true']",
        ]
        
        input_found = False
        for selector in input_selectors:
            try:
                element = driver.find_element("css selector", selector)
                if element and element.is_displayed():
                    print(f"✅ Found input field with selector: {selector}")
                    input_found = True
                    break
            except:
                continue
        
        if not input_found:
            print("⚠️  Could not find input field automatically")
            print("💡 Please manually check if you can see a text input area")
            print("💡 The system will still try to work")
        
        # Test sending a message
        print("\n🧪 Testing message sending...")
        
        test_message = "Agent-4 login test - can you see this message?"
        
        try:
            # Try to find and use the input field
            for selector in input_selectors:
                try:
                    element = driver.find_element("css selector", selector)
                    if element and element.is_displayed():
                        element.clear()
                        element.send_keys(test_message)
                        print(f"✅ Message sent using selector: {selector}")
                        
                        # Try to submit (look for send button or press Enter)
                        from selenium.webdriver.common.keys import Keys
                        element.send_keys(Keys.RETURN)
                        print("✅ Message submitted")
                        break
                except:
                    continue
        except Exception as e:
            print(f"⚠️  Could not send test message: {e}")
        
        print("\n🎉 LOGIN HELPER COMPLETE!")
        print("-" * 30)
        print("✅ Browser is open and ready")
        print("✅ You should be logged in")
        print("💡 You can now test the automation system")
        print("💡 Run: python thea_autonomous.py send 'your test message'")
        print("💡 The browser window will stay open for testing")
        
        # Keep browser open
        print("\n⏳ Browser will stay open for 60 seconds for testing...")
        print("💡 You can close it manually or wait for auto-close")
        
        time.sleep(60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        if driver:
            print("\n🔚 Closing browser...")
            driver.quit()

def main():
    """Main function."""
    print("🔐 Thea Login Helper")
    print("=" * 25)
    print("This script will help you log into ChatGPT/Thea and test the automation.")
    print()
    
    proceed = input("Continue? (y/n): ").lower().strip()
    if proceed != 'y':
        print("❌ Cancelled")
        return
    
    login_helper()

if __name__ == "__main__":
    main()
