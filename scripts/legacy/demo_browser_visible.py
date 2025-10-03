#!/usr/bin/env python3
"""
Demo Browser Visible - Simple Chrome Browser Demo
================================================

Simple demonstration of opening Chrome browser in visible mode
to show Thea interface without full automation.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def demo_browser():
    """Demo opening Chrome browser to Thea interface."""
    print("🚀 Opening Chrome Browser to Thea Interface")
    print("=" * 50)
    
    try:
        # Configure Chrome options for visible mode
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        
        # Try to use existing ChromeDriver first
        try:
            print("🔧 Attempting to use existing ChromeDriver...")
            driver = webdriver.Chrome(options=chrome_options)
            print("✅ Using existing ChromeDriver")
        except Exception as e:
            print(f"⚠️  Existing ChromeDriver failed: {e}")
            print("🔧 Attempting to download compatible ChromeDriver...")
            
            # Try with webdriver-manager
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ ChromeDriver downloaded and initialized")
            except Exception as e2:
                print(f"❌ ChromeDriver download failed: {e2}")
                print("💡 Please manually update ChromeDriver or free up disk space")
                return False
        
        # Navigate to Thea interface
        thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        print(f"🌐 Navigating to Thea interface: {thea_url}")
        driver.get(thea_url)
        
        print("✅ Browser opened successfully!")
        print("👀 You should now see the Thea interface in the browser window")
        print("⏳ Browser will stay open for 30 seconds...")
        
        # Keep browser open for demonstration
        time.sleep(30)
        
        print("🧹 Closing browser...")
        driver.quit()
        print("✅ Demo complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

if __name__ == "__main__":
    success = demo_browser()
    if success:
        print("\n🎯 Thea interface is accessible and browser automation is working!")
    else:
        print("\n⚠️  Browser demo encountered issues - check disk space and ChromeDriver compatibility")
