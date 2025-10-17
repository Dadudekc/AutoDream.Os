#!/usr/bin/env python3
"""
Thea Login Diagnostic - Debug Cookie Loading
=============================================

Diagnoses exactly what's happening during cookie loading and login.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.thea import TheaService


def diagnose_login():
    """Diagnose login issues with detailed logging."""
    
    print()
    print("=" * 80)
    print("🔍 THEA LOGIN DIAGNOSTIC")
    print("=" * 80)
    print()
    
    # Check cookies
    cookie_file = "thea_cookies.json"
    if not Path(cookie_file).exists():
        print(f"❌ Cookie file not found: {cookie_file}")
        return False
    
    with open(cookie_file) as f:
        cookies = json.load(f)
    
    print(f"📁 Cookie file: {cookie_file}")
    print(f"   Total cookies: {len(cookies)}")
    print()
    
    # Check expiry
    now = datetime.now().timestamp()
    expired = []
    valid = []
    
    for cookie in cookies:
        expiry = cookie.get("expiry", 0)
        if expiry == 0:
            valid.append(cookie)
        elif expiry > now:
            valid.append(cookie)
        else:
            expired.append(cookie)
    
    print(f"🍪 Cookie Status:")
    print(f"   Valid: {len(valid)}")
    print(f"   Expired: {len(expired)}")
    print()
    
    if len(expired) > len(valid):
        print("⚠️  WARNING: Most cookies are expired!")
        print("   You may need to run: python setup_thea_cookies.py")
        print()
    
    # Start browser test
    print("=" * 80)
    print("BROWSER TEST - WATCHING EACH STEP")
    print("=" * 80)
    print()
    
    try:
        thea = TheaService(cookie_file=cookie_file, headless=False)
        
        # Step 1: Start browser
        print("1️⃣  Starting browser...")
        if not thea.browser.start():
            print("   ❌ Failed to start browser")
            return False
        print("   ✅ Browser started")
        print()
        time.sleep(2)
        
        # Step 2: Navigate to domain
        print("2️⃣  Navigating to ChatGPT domain...")
        if not thea.browser.navigate_to_domain():
            print("   ❌ Failed to navigate")
            return False
        print("   ✅ On ChatGPT domain")
        print()
        time.sleep(3)  # Extra wait
        
        # Step 3: Check login BEFORE cookies
        print("3️⃣  Checking login status BEFORE loading cookies...")
        is_logged_in_before = thea.browser.is_logged_in()
        print(f"   Status: {'✅ Logged in' if is_logged_in_before else '❌ Not logged in'}")
        print()
        
        if is_logged_in_before:
            print("   ℹ️  Already logged in! Cookies may be working from browser cache.")
            print()
            return True
        
        # Step 4: Load cookies
        print("4️⃣  Loading cookies...")
        if thea.cookies.has_valid_cookies():
            success = thea.cookies.load_cookies(thea.browser.driver)
            if success:
                print("   ✅ Cookies loaded")
            else:
                print("   ❌ Cookie loading failed")
                return False
        else:
            print("   ❌ No valid cookies found")
            return False
        print()
        time.sleep(2)
        
        # Step 5: Refresh page (CRITICAL!)
        print("5️⃣  Refreshing page to apply cookies...")
        thea.browser.refresh()
        print("   ✅ Page refreshed")
        print()
        time.sleep(5)  # Extra wait after refresh
        
        # Step 6: Check login AFTER cookies
        print("6️⃣  Checking login status AFTER loading cookies...")
        is_logged_in_after = thea.browser.is_logged_in()
        print(f"   Status: {'✅ Logged in' if is_logged_in_after else '❌ Not logged in'}")
        print()
        
        if not is_logged_in_after:
            print("   ⚠️  Still not logged in after cookies!")
            print("   Checking page content...")
            print()
            
            # Get page title and URL for debugging
            title = thea.browser.driver.title
            url = thea.browser.driver.current_url
            
            print(f"   Page Title: {title}")
            print(f"   Current URL: {url}")
            print()
            
            # Check for visible textareas
            from selenium.webdriver.common.by import By
            textareas = thea.browser.driver.find_elements(By.TAG_NAME, "textarea")
            visible = [ta for ta in textareas if ta.is_displayed()]
            print(f"   Textareas found: {len(textareas)} total, {len(visible)} visible")
            print()
            
            # Check for buttons
            buttons = thea.browser.driver.find_elements(By.TAG_NAME, "button")
            button_texts = [btn.text for btn in buttons[:10] if btn.text]  # First 10
            print(f"   Buttons found: {len(buttons)}")
            if button_texts:
                print(f"   Sample buttons: {button_texts}")
            print()
        
        # Step 7: Navigate to Thea
        print("7️⃣  Navigating to Thea Manager...")
        if not thea.browser.navigate_to_thea():
            print("   ❌ Failed to navigate to Thea")
            return False
        print("   ✅ On Thea page")
        print()
        time.sleep(5)  # Extra wait
        
        # Step 8: Final login check
        print("8️⃣  Final login check on Thea page...")
        is_logged_in_final = thea.browser.is_logged_in()
        print(f"   Status: {'✅ Logged in' if is_logged_in_final else '❌ Not logged in'}")
        print()
        
        if is_logged_in_final:
            print("🎉 SUCCESS! Login with cookies works!")
            print()
            print("Press Enter to close browser and exit...")
            input()
            thea.cleanup()
            return True
        else:
            print("❌ FAILED! Cookies did not work.")
            print()
            print("Possible causes:")
            print("  1. Cookies are expired (check expiry above)")
            print("  2. Browser fingerprinting detection")
            print("  3. Need to regenerate cookies")
            print()
            print("Press Enter to close browser and exit...")
            input()
            thea.cleanup()
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = diagnose_login()
    sys.exit(0 if success else 1)

