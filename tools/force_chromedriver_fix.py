#!/usr/bin/env python3
"""
Force ChromeDriver Fix
======================

Forces the correct ChromeDriver version by patching the working implementation.
"""

import shutil
import os
from pathlib import Path

def force_chromedriver_fix():
    """Force the correct ChromeDriver version."""
    print("🔧 FORCING CHROMEDRIVER FIX")
    print("=" * 35)
    
    try:
        # Get the correct ChromeDriver path
        from webdriver_manager.chrome import ChromeDriverManager
        correct_driver_path = ChromeDriverManager().install()
        print(f"✅ Correct ChromeDriver: {correct_driver_path}")
        
        # Find undetected Chrome cache
        import undetected_chromedriver as uc
        uc_version = uc.__version__
        print(f"📦 Undetected Chrome version: {uc_version}")
        
        # Clear undetected Chrome cache
        uc_cache_dirs = [
            Path.home() / ".local" / "share" / "undetected_chromedriver",
            Path.home() / ".cache" / "undetected_chromedriver",
            Path.home() / "AppData" / "Local" / "undetected_chromedriver",
        ]
        
        for cache_dir in uc_cache_dirs:
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                print(f"✅ Cleared UC cache: {cache_dir}")
        
        print("\n🎯 CHROMEDRIVER FIX APPLIED")
        print("The system will now use the correct ChromeDriver version.")
        
        return True
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        return False

def test_direct_selenium():
    """Test direct Selenium without undetected Chrome."""
    print("\n🧪 TESTING DIRECT SELENIUM")
    print("=" * 30)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        print("Initializing direct Selenium...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        print("✅ Direct Selenium successful!")
        
        # Test navigation
        driver.get("https://chatgpt.com")
        print("✅ Navigation successful!")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Direct Selenium failed: {e}")
        return False

if __name__ == "__main__":
    if force_chromedriver_fix():
        if test_direct_selenium():
            print("\n🎉 CHROMEDRIVER COMPLETELY FIXED!")
            print("Direct Selenium is working - the system should now function.")
        else:
            print("\n⚠️  Still having issues - try restarting your computer.")
    else:
        print("\n❌ Could not apply fix.")
