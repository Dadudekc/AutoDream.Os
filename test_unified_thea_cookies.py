#!/usr/bin/env python3
"""
Quick test of unified Thea cookie loading
==========================================

Tests the fixed cookie loading pattern.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.thea import TheaService

def test_cookie_loading():
    """Test cookie loading with the unified service."""
    
    print()
    print("=" * 70)
    print("🔍 UNIFIED THEA SERVICE - COOKIE LOADING TEST")
    print("=" * 70)
    print()
    
    # Check which cookie files exist
    cookie_files = [
        "thea_cookies.json",
        "src/services/thea/thea_cookies.json",
        "data/thea_cookies.json"
    ]
    
    print("📁 Cookie files found:")
    for cf in cookie_files:
        if Path(cf).exists():
            size = Path(cf).stat().st_size
            print(f"  ✅ {cf} ({size} bytes)")
        else:
            print(f"  ❌ {cf} (not found)")
    print()
    
    # Test with root cookie file (most likely location)
    cookie_file = "thea_cookies.json"
    
    if not Path(cookie_file).exists():
        print(f"❌ Cookie file '{cookie_file}' not found!")
        print("💡 Run setup_thea_cookies.py first to create cookies")
        return False
    
    print(f"🧪 Testing with cookie file: {cookie_file}")
    print()
    
    try:
        # Create service
        print("1️⃣  Creating Thea service...")
        thea = TheaService(cookie_file=cookie_file, headless=False)
        print("   ✅ Service created")
        print()
        
        # Test login
        print("2️⃣  Testing login with cookies...")
        print("   (Watch browser window for cookie loading)")
        print()
        
        success = thea.ensure_login()
        
        print()
        print("=" * 70)
        print("📊 RESULT")
        print("=" * 70)
        
        if success:
            print("✅ LOGIN SUCCESSFUL!")
            print()
            print("Cookie loading pattern working:")
            print("  1. Navigate to domain ✅")
            print("  2. Load cookies ✅")
            print("  3. Refresh page ✅")
            print("  4. Navigate to Thea ✅")
            print()
        else:
            print("❌ LOGIN FAILED!")
            print()
            print("Possible issues:")
            print("  - Cookies expired")
            print("  - Cookie format incorrect")
            print("  - Browser detection blocked")
            print()
        
        # Cleanup
        thea.cleanup()
        
        return success
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cookie_loading()
    
    print()
    if success:
        print("🎉 TEST PASSED - Cookie loading works!")
    else:
        print("⚠️  TEST FAILED - Check errors above")
    print()
    print("🐝 WE ARE SWARM")
    print()
    
    sys.exit(0 if success else 1)

