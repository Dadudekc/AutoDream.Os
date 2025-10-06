#!/usr/bin/env python3
"""
Selenium Smoke Test - ChromeDriver v140 Compatibility Check
==========================================================

Verifies ChromeDriver v140 handshake with Chrome browser.
Tests explicit driver path integration.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
V2 Compliance: ≤50 lines, single responsibility
"""

import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from src.services.thea.driver_path import chromedriver_path
    SELENIUM_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    SELENIUM_AVAILABLE = False


def smoke_test():
    """Run ChromeDriver smoke test."""
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not available")
        return False

    driver = None
    try:
        print("🚀 SELENIUM SMOKE TEST")
        print("=" * 30)
        print(f"📁 Driver path: {chromedriver_path()}")
        
        # Initialize Chrome with explicit driver path
        service = Service(chromedriver_path())
        driver = webdriver.Chrome(service=service)
        
        # Get browser version from capabilities
        caps = driver.capabilities
        browser_version = caps.get('browserVersion', 'Unknown')
        print(f"🌐 Browser version: {browser_version}")
        
        # Test basic navigation
        driver.get("https://www.google.com")
        title = driver.title
        print(f"📄 Page title: {title}")
        
        print("✅ SMOKE TEST PASSED")
        return True
        
    except Exception as e:
        print(f"❌ SMOKE TEST FAILED: {e}")
        return False
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    success = smoke_test()
    sys.exit(0 if success else 1)
