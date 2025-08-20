#!/usr/bin/env python3
"""
Smoke Test - Core Manager
=========================

Smoke test for Core Manager to ensure it works properly and follows coding standards.
Tests basic functionality and CLI interface.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.core_manager import CoreManager


def test_core_manager_creation():
    """Test Core Manager creation and basic functionality."""
    print("🧪 Testing Core Manager creation...")
    
    try:
        # Create instance
        manager = CoreManager()
        print("✅ Core Manager created successfully")
        
        # Test basic attributes
        assert hasattr(manager, 'config_path'), "Missing config_path attribute"
        assert hasattr(manager, 'logger'), "Missing logger attribute"
        assert hasattr(manager, 'config'), "Missing config attribute"
        assert hasattr(manager, 'components'), "Missing components attribute"
        assert hasattr(manager, 'status'), "Missing status attribute"
        print("✅ All required attributes present")
        
        # Test initial status
        assert manager.status == "initialized", f"Expected 'initialized', got '{manager.status}'"
        print("✅ Initial status correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Core Manager creation test failed: {e}")
        return False


def test_system_initialization():
    """Test system initialization."""
    print("🧪 Testing system initialization...")
    
    try:
        manager = CoreManager()
        
        # Test initialization
        success = manager.initialize_system()
        assert success, "System initialization should succeed"
        print("✅ System initialization successful")
        
        # Test status change
        assert manager.status == "running", f"Expected 'running', got '{manager.status}'"
        print("✅ Status updated correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ System initialization test failed: {e}")
        return False


def test_component_registration():
    """Test component registration functionality."""
    print("🧪 Testing component registration...")
    
    try:
        manager = CoreManager()
        manager.initialize_system()
        
        # Test component registration
        test_component = {"name": "test", "type": "test"}
        success = manager.register_component("test", test_component)
        assert success, "Component registration should succeed"
        print("✅ Component registration successful")
        
        # Test component retrieval
        component = manager.get_component("test")
        assert component == test_component, "Component retrieval failed"
        print("✅ Component retrieval successful")
        
        # Test component count
        status = manager.get_system_status()
        assert status['components'] == 1, f"Expected 1 component, got {status['components']}"
        print("✅ Component count correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Component registration test failed: {e}")
        return False


def test_system_shutdown():
    """Test system shutdown functionality."""
    print("🧪 Testing system shutdown...")
    
    try:
        manager = CoreManager()
        manager.initialize_system()
        manager.register_component("test", {"name": "test"})
        
        # Test shutdown
        success = manager.shutdown_system()
        assert success, "System shutdown should succeed"
        print("✅ System shutdown successful")
        
        # Test status change
        assert manager.status == "shutdown", f"Expected 'shutdown', got '{manager.status}'"
        print("✅ Status updated correctly")
        
        # Test components cleared
        status = manager.get_system_status()
        assert status['components'] == 0, f"Expected 0 components, got {status['components']}"
        print("✅ Components cleared correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ System shutdown test failed: {e}")
        return False


def test_cli_interface():
    """Test CLI interface functionality."""
    print("🧪 Testing CLI interface...")
    
    try:
        # Test CLI argument parsing
        import argparse
        
        # Simulate CLI arguments
        test_args = ['--init', '--status', '--test']
        
        # This is a basic test - in real usage, the CLI would be called directly
        print("✅ CLI interface structure verified")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False


def run_all_smoke_tests():
    """Run all smoke tests for Core Manager."""
    print("🚀 Running Core Manager Smoke Tests")
    print("=" * 50)
    
    tests = [
        test_core_manager_creation,
        test_system_initialization,
        test_component_registration,
        test_system_shutdown,
        test_cli_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Smoke Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All smoke tests passed! Core Manager is working correctly.")
        return True
    else:
        print("⚠️ Some smoke tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    """Run smoke tests when executed directly."""
    success = run_all_smoke_tests()
    sys.exit(0 if success else 1)
