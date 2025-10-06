#!/usr/bin/env python3
"""
ChromeDriver Version Fixer
==========================

Fixes ChromeDriver version mismatch issues by forcing the correct version.
"""

import subprocess
import sys

def fix_chromedriver():
    """Fix ChromeDriver version mismatch."""
    print("🔧 CHROMEDRIVER VERSION FIXER")
    print("=" * 40)
    
    print("Current issue: ChromeDriver 141 vs Chrome 140")
    print("Solution: Force ChromeDriver to use correct version")
    
    try:
        # Method 1: Update undetected-chromedriver
        print("\n1. Updating undetected-chromedriver...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "undetected-chromedriver"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ undetected-chromedriver updated")
        else:
            print(f"⚠️  Update failed: {result.stderr}")
        
        # Method 2: Clear webdriver cache
        print("\n2. Clearing webdriver cache...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            import shutil
            import os
            
            # Clear the cache directory
            cache_dir = os.path.expanduser("~/.wdm")
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                print("✅ Webdriver cache cleared")
            else:
                print("ℹ️  No webdriver cache found")
        except Exception as e:
            print(f"⚠️  Cache clear failed: {e}")
        
        # Method 3: Force download correct version
        print("\n3. Forcing download of correct ChromeDriver...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            # This will download the correct version
            driver_path = ChromeDriverManager().install()
            print(f"✅ ChromeDriver downloaded: {driver_path}")
            
        except Exception as e:
            print(f"⚠️  Force download failed: {e}")
        
        print("\n🎯 RECOMMENDATIONS:")
        print("1. Restart your browser completely")
        print("2. Close all Chrome processes in Task Manager")
        print("3. Try running the test again")
        print("4. If still failing, try: pip install --upgrade selenium")
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")

def test_fix():
    """Test if the fix worked."""
    print("\n🧪 TESTING FIX")
    print("=" * 20)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("Testing ChromeDriver initialization...")
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        
        print("✅ ChromeDriver test successful!")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

if __name__ == "__main__":
    fix_chromedriver()
    
    if test_fix():
        print("\n🎉 CHROMEDRIVER FIX SUCCESSFUL!")
        print("You can now run the Thea automation.")
    else:
        print("\n⚠️  CHROMEDRIVER STILL HAS ISSUES")
        print("Try manually updating Chrome or using a different approach.")
