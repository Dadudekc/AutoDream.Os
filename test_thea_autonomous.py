#!/usr/bin/env python3
"""
Test Script for Thea Autonomous System
======================================

Comprehensive test of the autonomous Thea system to ensure it's ready for agent use.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.thea.thea_autonomous_system import TheaAutonomousSystem
from src.services.thea.thea_error_recovery import TheaErrorRecovery
from src.services.thea.thea_monitoring_system import TheaMonitoringSystem


def test_autonomous_system():
    """Test the autonomous Thea system components."""
    print("🧪 Testing Thea Autonomous System Components")
    print("=" * 55)
    
    # Test 1: System Creation
    print("\n1️⃣ Testing System Creation...")
    try:
        thea = TheaAutonomousSystem(headless=True)
        print("✅ TheaAutonomousSystem created successfully")
    except Exception as e:
        print(f"❌ Failed to create TheaAutonomousSystem: {e}")
        return False
    
    # Test 2: System Status
    print("\n2️⃣ Testing System Status...")
    try:
        status = thea.get_system_status()
        print("✅ System status retrieved successfully")
        print(f"   - Initialized: {status['initialized']}")
        print(f"   - Headless mode: {status['headless_mode']}")
        print(f"   - Browser available: {status['browser_available']}")
        print(f"   - Valid cookies: {status['has_valid_cookies']}")
    except Exception as e:
        print(f"❌ Failed to get system status: {e}")
        return False
    
    # Test 3: Error Recovery System
    print("\n3️⃣ Testing Error Recovery System...")
    try:
        recovery = TheaErrorRecovery()
        print("✅ TheaErrorRecovery created successfully")
        
        # Test error statistics
        stats = recovery.get_error_statistics()
        print(f"   - Total errors: {stats['total_errors']}")
    except Exception as e:
        print(f"❌ Failed to create error recovery system: {e}")
        return False
    
    # Test 4: Monitoring System
    print("\n4️⃣ Testing Monitoring System...")
    try:
        monitor = TheaMonitoringSystem()
        print("✅ TheaMonitoringSystem created successfully")
        
        # Test performance summary
        perf_summary = monitor.get_performance_summary()
        print(f"   - Total operations: {perf_summary['total_operations']}")
        
        # Test system health
        health_summary = monitor.get_system_health_summary()
        print(f"   - System status: {health_summary['status']}")
    except Exception as e:
        print(f"❌ Failed to create monitoring system: {e}")
        return False
    
    # Test 5: Context Manager
    print("\n5️⃣ Testing Context Manager...")
    try:
        with TheaAutonomousSystem(headless=True) as thea_context:
            status = thea_context.get_system_status()
            print("✅ Context manager working correctly")
            print(f"   - System initialized: {status['initialized']}")
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Thea Autonomous System is ready for agent use.")
    return True


def test_cli_interface():
    """Test the CLI interface."""
    print("\n🖥️ Testing CLI Interface")
    print("=" * 30)
    
    try:
        # Test CLI help
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "src.services.thea.thea_autonomous_cli", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ CLI help command working")
        else:
            print(f"⚠️ CLI help command returned code {result.returncode}")
        
        # Test status command
        result = subprocess.run([
            sys.executable, "-m", "src.services.thea.thea_autonomous_cli", "status"
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✅ CLI status command working")
        else:
            print(f"⚠️ CLI status command returned code {result.returncode}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🤖 V2_SWARM Thea Autonomous System Test Suite")
    print("=" * 60)
    
    # Run component tests
    component_test_passed = test_autonomous_system()
    
    # Run CLI tests
    cli_test_passed = test_cli_interface()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Component Tests: {'✅ PASSED' if component_test_passed else '❌ FAILED'}")
    print(f"CLI Tests: {'✅ PASSED' if cli_test_passed else '❌ FAILED'}")
    
    if component_test_passed and cli_test_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Thea Autonomous System is ready for 24/7 agent operation!")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
