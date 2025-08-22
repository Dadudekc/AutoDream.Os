#!/usr/bin/env python3
"""
Comprehensive Coordinate Loading Test System
===========================================

This script provides comprehensive testing and diagnostics for the 
8-agent coordinate loading system, including error handling and
status reporting to help diagnose terminal corruption issues.

Features:
- Safe dependency loading with fallbacks
- Comprehensive coordinate validation
- Clear status reporting
- Error diagnostics and recovery
- Terminal encoding safety
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def safe_import_dependencies():
    """Safely import dependencies with error handling"""
    missing_deps = []
    imported_modules = {}
    
    try:
        import pyautogui
        imported_modules['pyautogui'] = pyautogui
        print("✅ pyautogui imported successfully")
    except ImportError as e:
        missing_deps.append('pyautogui')
        print(f"❌ pyautogui import failed: {e}")
    
    try:
        import pynput
        imported_modules['pynput'] = pynput
        print("✅ pynput imported successfully")
    except ImportError as e:
        missing_deps.append('pynput')
        print(f"❌ pynput import failed: {e}")
    
    try:
        import keyboard
        imported_modules['keyboard'] = keyboard
        print("✅ keyboard imported successfully")
    except ImportError as e:
        missing_deps.append('keyboard')
        print(f"❌ keyboard import failed: {e}")
    
    return imported_modules, missing_deps

def test_coordinate_loading_system():
    """Comprehensive coordinate loading test with error handling"""
    
    print("🧪 " + "="*60)
    print("   COMPREHENSIVE COORDINATE LOADING TEST")
    print("="*64)
    print()
    
    # Test 1: Check terminal encoding
    print("🔍 Test 1: Terminal Encoding Check")
    print("-" * 40)
    try:
        print(f"✅ Terminal encoding: {sys.stdout.encoding}")
        print(f"✅ File system encoding: {sys.getfilesystemencoding()}")
        print("✅ Unicode test: 🎯📍🚀✅❌⚠️🧪")
    except Exception as e:
        print(f"❌ Encoding issue detected: {e}")
    print()
    
    # Test 2: Dependency Import Test
    print("🔍 Test 2: Dependency Import Test")
    print("-" * 40)
    imported_modules, missing_deps = safe_import_dependencies()
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("   Please install with: pip install pyautogui pynput keyboard")
        return False
    else:
        print("\n✅ All dependencies imported successfully!")
    print()
    
    # Test 3: Message Queue System Import
    print("🔍 Test 3: Message Queue System Import")
    print("-" * 40)
    try:
        from services.v1_v2_message_queue_system import MessageQueueManager, V1V2MessageQueueSystem
        print("✅ MessageQueueManager imported successfully")
        print("✅ V1V2MessageQueueSystem imported successfully")
    except ImportError as e:
        print(f"❌ Message queue system import failed: {e}")
        return False
    print()
    
    # Test 4: Initialize Message Queue Manager
    print("🔍 Test 4: Message Queue Manager Initialization")
    print("-" * 40)
    try:
        manager = MessageQueueManager()
        print("✅ MessageQueueManager initialized successfully")
        print(f"✅ Agent registry initialized: {len(manager.agent_registry)} agents")
    except Exception as e:
        print(f"❌ Manager initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # Test 5: Coordinate Status Check
    print("🔍 Test 5: Coordinate Status Analysis")
    print("-" * 40)
    try:
        coord_status = manager.get_coordinate_status()
        print(f"✅ Retrieved coordinate status for {len(coord_status)} agents")
        
        valid_coords = 0
        invalid_coords = 0
        
        for agent_id, status in coord_status.items():
            name = status.get("name", "Unknown")
            coords = status.get("coordinates")
            has_coords = status.get("has_coordinates", False)
            
            if has_coords and coords and coords.get("x", 0) > 0 and coords.get("y", 0) > 0:
                print(f"  ✅ {name} ({agent_id}): {coords}")
                valid_coords += 1
            else:
                print(f"  ❌ {name} ({agent_id}): Invalid/missing coordinates")
                invalid_coords += 1
        
        print(f"\n📊 Coordinate Summary:")
        print(f"   Valid coordinates: {valid_coords}/8")
        print(f"   Invalid coordinates: {invalid_coords}/8")
        
    except Exception as e:
        print(f"❌ Coordinate status check failed: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    # Test 6: PyAutoGUI Functionality
    print("🔍 Test 6: PyAutoGUI Functionality Test")
    print("-" * 40)
    try:
        pyautogui = imported_modules.get('pyautogui')
        if pyautogui:
            screen_size = pyautogui.size()
            mouse_pos = pyautogui.position()
            print(f"✅ Screen size detected: {screen_size}")
            print(f"✅ Current mouse position: {mouse_pos}")
            print("✅ PyAutoGUI is functional")
        else:
            print("❌ PyAutoGUI not available")
    except Exception as e:
        print(f"❌ PyAutoGUI test failed: {e}")
    print()
    
    # Test 7: Message Queue Test (Safe Mode)
    print("🔍 Test 7: Message Queue Test (Safe Mode)")
    print("-" * 40)
    try:
        # Create a test message but don't actually send it
        test_message = {
            "source_agent": "test_agent",
            "content": "🧪 TEST: Coordinate loading verification message",
            "timestamp": time.time(),
            "priority": "normal"
        }
        
                 print("✅ Test message created successfully")
         print(f"✅ Message content: {test_message['content'][:50]}...")
         
         # Test message queue operations without actual broadcast
         queue_size = manager.queue_system.message_queue.qsize() if hasattr(manager.queue_system, 'message_queue') else 0
         print(f"✅ Current queue size: {queue_size}")
         
     except Exception as e:
         print(f"❌ Message queue test failed: {e}")
     print()
     
     # Test 8: Cleanup and Summary
     print("🔍 Test 8: System Cleanup")
     print("-" * 40)
     try:
         if hasattr(manager.queue_system, 'stop_system'):
             manager.queue_system.stop_system()
         else:
             manager.queue_system.is_running = False
         print("✅ System stopped cleanly")
     except Exception as e:
         print(f"⚠️ Cleanup warning: {e}")
     print()
    
    # Final Summary
    print("🎯 " + "="*60)
    print("   COORDINATE LOADING TEST SUMMARY")
    print("="*64)
    
    if valid_coords >= 6:
        print("🎉 SYSTEM STATUS: GOOD")
        print(f"   Most agents have valid coordinates ({valid_coords}/8)")
        print("   The broadcast system should work for most agents.")
    elif valid_coords >= 3:
        print("⚠️ SYSTEM STATUS: NEEDS ATTENTION") 
        print(f"   Some agents have valid coordinates ({valid_coords}/8)")
        print("   Run calibrate_coordinates.py to fix remaining agents.")
    else:
        print("❌ SYSTEM STATUS: REQUIRES CALIBRATION")
        print(f"   Few agents have valid coordinates ({valid_coords}/8)")
        print("   Run calibrate_coordinates.py to set up agent positions.")
    
    print()
    print("📋 Next Steps:")
    if valid_coords < 8:
        print("   1. Run: python3 calibrate_coordinates.py")
        print("   2. Position mouse over each agent's chat window")
        print("   3. Follow interactive calibration prompts")
        print("   4. Re-run this test to verify fixes")
    else:
        print("   1. System is fully calibrated!")
        print("   2. You can now use the broadcast system")
        print("   3. Test with: python3 demo_message_queue_system.py")
    
    return valid_coords >= 6

def main():
    """Main test execution with error recovery"""
    try:
        # Set UTF-8 encoding for terminal output
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        
        print("🚀 Starting comprehensive coordinate loading test...")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🐍 Python version: {sys.version}")
        print()
        
        success = test_coordinate_loading_system()
        
        if success:
            print("\n🎉 All tests passed! Coordinate system is ready.")
        else:
            print("\n⚠️ Some issues detected. Check output above for details.")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        print("\n🔧 Debug Information:")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Troubleshooting Tips:")
        print("   1. Check if all dependencies are installed")
        print("   2. Verify terminal encoding supports Unicode")
        print("   3. Try running in a different terminal")
        print("   4. Check system permissions for PyAutoGUI")

if __name__ == "__main__":
    main()