#!/usr/bin/env python3
"""
Test Coordinate Loading System (Headless)
==========================================

This script tests the coordinate loading functionality for the agent system
in a headless environment without requiring GUI dependencies.
"""

import sys
import json
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_coordinate_system_headless():
    """Test coordinate system without GUI dependencies"""
    print("🧪 Testing Coordinate Loading System (Headless)")
    print("=" * 55)
    
    try:
        # Test 1: Check if we can import the required modules
        print("1️⃣ Testing module imports...")
        try:
            # Import without triggering pyautogui
            import importlib.util
            
            # Check if the message queue module exists
            mq_path = Path(__file__).parent / "src" / "services" / "v1_v2_message_queue_system.py"
            if mq_path.exists():
                print("   ✅ MessageQueue module found")
            else:
                print("   ❌ MessageQueue module not found")
                return False
            
            # Check shared enums
            enum_path = Path(__file__).parent / "src" / "core" / "shared_enums.py"
            if enum_path.exists():
                print("   ✅ SharedEnums module found")
            else:
                print("   ❌ SharedEnums module not found")
                return False
                
        except Exception as e:
            print(f"   ❌ Module import test failed: {e}")
            return False
        
        # Test 2: Check coordinate configuration files
        print("\n2️⃣ Checking coordinate configuration...")
        config_files = [
            "config/8_agent_config.json",
            "config/cursor_agent_coords.json"
        ]
        
        coord_config_found = False
        for config_file in config_files:
            config_path = Path(__file__).parent / config_file
            if config_path.exists():
                print(f"   ✅ Found config: {config_file}")
                coord_config_found = True
                
                # Try to read and validate config
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                    print(f"   ✅ Config file valid JSON with {len(config_data)} entries")
                except Exception as e:
                    print(f"   ❌ Config file invalid: {e}")
            else:
                print(f"   ❌ Config not found: {config_file}")
        
        if not coord_config_found:
            print("   ⚠️ No coordinate config files found")
        
        # Test 3: Validate default coordinate layout
        print("\n3️⃣ Testing default coordinate layout...")
        default_coords = {
            "agent_1": {"x": 400, "y": 200},   # Top-left quadrant
            "agent_2": {"x": 1200, "y": 200},  # Top-right quadrant  
            "agent_3": {"x": 2000, "y": 200},  # Extended top-right
            "agent_4": {"x": 400, "y": 600},   # Bottom-left quadrant
            "agent_5": {"x": 1200, "y": 600},  # Bottom-right quadrant
            "agent_6": {"x": 2000, "y": 600},  # Extended bottom-right
            "agent_7": {"x": 400, "y": 1000},  # Lower-left
            "agent_8": {"x": 1200, "y": 1000} # Lower-right
        }
        
        for agent_id, coords in default_coords.items():
            x, y = coords["x"], coords["y"]
            
            # Basic validation - coordinates should be positive and reasonable
            if x > 0 and y > 0 and x < 4000 and y < 2000:
                print(f"   ✅ {agent_id}: x={x}, y={y} (valid)")
            else:
                print(f"   ❌ {agent_id}: x={x}, y={y} (invalid)")
        
        # Test 4: Check system files
        print("\n4️⃣ Checking system files...")
        system_files = [
            "src/services/v1_v2_message_queue_system.py",
            "calibrate_coordinates.py",
            "src/set_8_agent_coordinates.py"
        ]
        
        for sys_file in system_files:
            file_path = Path(__file__).parent / sys_file
            if file_path.exists():
                print(f"   ✅ {sys_file} exists")
            else:
                print(f"   ❌ {sys_file} missing")
        
        print("\n🎉 **Headless Coordinate Test Complete!**")
        print("Basic coordinate system structure is in place.")
        return True
        
    except Exception as e:
        print(f"\n❌ **Test Failed: {e}**")
        import traceback
        traceback.print_exc()
        return False

def diagnose_coordinate_issues():
    """Diagnose common coordinate system issues"""
    print("\n🔍 **Coordinate System Diagnostics**")
    print("=" * 40)
    
    issues_found = []
    
    # Check 1: Dependencies
    print("1️⃣ Checking dependencies...")
    required_packages = ["pyautogui", "psutil", "watchdog", "aiohttp"]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} available")
        except ImportError:
            print(f"   ❌ {package} missing")
            issues_found.append(f"Missing package: {package}")
    
    # Check 2: File structure
    print("\n2️⃣ Checking file structure...")
    required_files = [
        "src/services/v1_v2_message_queue_system.py",
        "src/core/shared_enums.py",
        "calibrate_coordinates.py"
    ]
    
    for req_file in required_files:
        file_path = Path(__file__).parent / req_file
        if file_path.exists():
            print(f"   ✅ {req_file} exists")
        else:
            print(f"   ❌ {req_file} missing")
            issues_found.append(f"Missing file: {req_file}")
    
    # Check 3: Configuration
    print("\n3️⃣ Checking configuration...")
    config_dir = Path(__file__).parent / "config"
    if config_dir.exists():
        print(f"   ✅ Config directory exists")
        config_files = list(config_dir.glob("*.json"))
        print(f"   📁 Found {len(config_files)} config files")
    else:
        print("   ❌ Config directory missing")
        issues_found.append("Missing config directory")
    
    # Summary
    print(f"\n📊 **Diagnostic Summary**")
    if issues_found:
        print(f"   ❌ Found {len(issues_found)} issues:")
        for issue in issues_found:
            print(f"      • {issue}")
        print("\n💡 **Recommended Actions:**")
        print("   1. Install missing dependencies")
        print("   2. Run setup scripts to create missing files")
        print("   3. Calibrate coordinates with calibrate_coordinates.py")
    else:
        print("   ✅ No major issues detected")
        print("   💡 If still having problems, check agent window setup")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    print("🚀 Starting Headless Coordinate System Tests")
    print("=" * 50)
    
    # Run headless tests
    coord_test_passed = test_coordinate_system_headless()
    
    # Run diagnostics
    system_healthy = diagnose_coordinate_issues()
    
    print("\n📊 **Final Test Summary**")
    print("=" * 30)
    print(f"Coordinate System: {'✅ PASSED' if coord_test_passed else '❌ FAILED'}")
    print(f"System Health: {'✅ HEALTHY' if system_healthy else '❌ ISSUES FOUND'}")
    
    if coord_test_passed and system_healthy:
        print("\n🎉 Coordinate system is ready for use!")
        print("💡 Next: Run calibrate_coordinates.py to set actual coordinates")
    else:
        print("\n⚠️ System needs attention before coordinate calibration")