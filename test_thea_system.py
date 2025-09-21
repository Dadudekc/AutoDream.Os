#!/usr/bin/env python3
"""
Thea System Test - V2 Compliant Test Script
===========================================

Test script for the refactored Thea communication system.
Verifies all components are working correctly and V2 compliant.

Usage:
    python test_thea_system.py
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported correctly."""
    print("🧪 TESTING IMPORTS")
    print("=" * 30)
    
    try:
        # Test core imports
        from src.services.thea.thea_communication_core import TheaCommunicationCore
        print("✅ TheaCommunicationCore imported successfully")
        
        from src.services.thea.thea_communication_interface import TheaCommunicationInterface
        print("✅ TheaCommunicationInterface imported successfully")
        
        from src.services.thea.thea_browser_manager import TheaBrowserManager
        print("✅ TheaBrowserManager imported successfully")
        
        from src.services.thea.thea_cookie_manager import TheaCookieManager
        print("✅ TheaCookieManager imported successfully")
        
        from src.services.thea.thea_login_detector import TheaLoginDetector
        print("✅ TheaLoginDetector imported successfully")
        
        from src.services.thea.thea_login_handler_refactored import TheaLoginHandler
        print("✅ TheaLoginHandler imported successfully")
        
        # Test module-level imports
        from src.services.thea import (
            TheaCommunicationInterface,
            TheaCommunicationCore,
            TheaBrowserManager,
            TheaCookieManager,
            TheaLoginDetector,
            TheaLoginHandler
        )
        print("✅ Module-level imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_v2_compliance():
    """Test that all files are V2 compliant (≤400 lines)."""
    print("\n📏 TESTING V2 COMPLIANCE")
    print("=" * 30)
    
    thea_files = [
        "src/services/thea/thea_communication_core.py",
        "src/services/thea/thea_communication_interface.py",
        "src/services/thea/thea_browser_manager.py",
        "src/services/thea/thea_cookie_manager.py",
        "src/services/thea/thea_login_detector.py",
        "src/services/thea/thea_login_handler_refactored.py",
        "src/services/thea/__init__.py"
    ]
    
    all_compliant = True
    
    for file_path in thea_files:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            
            if lines <= 400:
                print(f"✅ {file_path}: {lines} lines (V2 compliant)")
            else:
                print(f"❌ {file_path}: {lines} lines (V2 VIOLATION)")
                all_compliant = False
        else:
            print(f"⚠️  {file_path}: File not found")
            all_compliant = False
    
    return all_compliant

def test_original_files():
    """Test that original files are still present and check their line counts."""
    print("\n📋 TESTING ORIGINAL FILES")
    print("=" * 30)
    
    original_files = [
        "simple_thea_communication.py",
        "response_detector.py", 
        "thea_login_handler.py",
        "setup_thea_cookies.py"
    ]
    
    for file_path in original_files:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            
            if lines <= 400:
                print(f"✅ {file_path}: {lines} lines (V2 compliant)")
            else:
                print(f"⚠️  {file_path}: {lines} lines (V2 VIOLATION - needs refactoring)")
        else:
            print(f"❌ {file_path}: File not found")

def test_functionality():
    """Test basic functionality of the refactored system."""
    print("\n🔧 TESTING FUNCTIONALITY")
    print("=" * 30)
    
    try:
        from src.services.thea import TheaCommunicationInterface, TheaBrowserManager, TheaCookieManager, TheaLoginDetector
        
        # Test instantiation
        comm = TheaCommunicationInterface()
        print("✅ TheaCommunicationInterface instantiated")
        
        browser_manager = TheaBrowserManager()
        print("✅ TheaBrowserManager instantiated")
        
        cookie_manager = TheaCookieManager()
        print("✅ TheaCookieManager instantiated")
        
        login_detector = TheaLoginDetector()
        print("✅ TheaLoginDetector instantiated")
        
        # Test convenience functions
        from src.services.thea import create_cookie_manager, create_login_detector
        cookie_manager2 = create_cookie_manager()
        login_detector2 = create_login_detector()
        print("✅ Convenience functions working")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🐝 V2_SWARM THEA SYSTEM TEST")
    print("=" * 50)
    print("Testing refactored Thea communication system for V2 compliance")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("V2 Compliance Test", test_v2_compliance),
        ("Original Files Test", test_original_files),
        ("Functionality Test", test_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Thea system is V2 compliant and ready for use")
        return True
    else:
        print("⚠️  Some tests failed - check the output above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
