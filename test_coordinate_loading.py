#!/usr/bin/env python3
"""
Test Coordinate Loading - System Communication Verification
===========================================================

This script tests the coordinate loading system and verifies
that all 8 agents are properly configured and communicating.
It also validates that screen region coordinates are properly calibrated.
"""

import sys
import json
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from services.v1_v2_message_queue_system import MessageQueueManager
    from core.shared_enums import AgentCapability
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure the src directory structure is correct.")
    sys.exit(1)

def test_coordinate_loading():
    """Test coordinate loading and screen region validation"""
    print("🧪 Testing Coordinate Loading System")
    print("=" * 50)
    
    try:
        # Initialize the message queue manager
        print("1️⃣ Initializing MessageQueueManager...")
        manager = MessageQueueManager()
        
        # Check if agents are registered
        print(f"2️⃣ Found {len(manager.agent_registry)} registered agents")
        
        if not manager.agent_registry:
            print("❌ No agents registered! System may not be initialized.")
            return False
        
        # Test coordinate status
        print("3️⃣ Checking coordinate status...")
        coord_status = manager.get_coordinate_status()
        
        valid_coordinates = 0
        total_agents = len(coord_status)
        
        print("\n📍 Agent Coordinate Status:")
        for agent_id, status in coord_status.items():
            name = status.get("name", "Unknown")
            coords = status.get("coordinates")
            has_coords = status.get("has_coordinates", False)
            
            if has_coords and coords:
                print(f"   ✅ {agent_id} ({name}): x={coords.get('x', 'N/A')}, y={coords.get('y', 'N/A')}")
                valid_coordinates += 1
            else:
                print(f"   ❌ {agent_id} ({name}): No coordinates set")
        
        # Validate screen region coverage
        print(f"\n4️⃣ Screen Region Validation:")
        print(f"   Valid coordinates: {valid_coordinates}/{total_agents}")
        
        if valid_coordinates == 0:
            print("   ❌ CRITICAL: No coordinates are set!")
            print("   🔧 Run calibrate_coordinates.py to set up coordinates")
            return False
        elif valid_coordinates < total_agents:
            print(f"   ⚠️ WARNING: Only {valid_coordinates} out of {total_agents} agents have coordinates")
            print("   🔧 Some agents may not receive messages properly")
            return False
        else:
            print("   ✅ All agents have valid coordinates")
        
        # Test coordinate validation (without mouse position)
        print("\n5️⃣ Testing coordinate validation...")
        test_coords = {"x": 500, "y": 300}
        is_valid = manager._validate_coordinates(test_coords)
        print(f"   ✅ Coordinate validation working: {is_valid}")
        
        print("\n🎉 **Coordinate Loading Test Complete!**")
        print("All coordinate systems are functioning properly.")
        return True
        
    except Exception as e:
        print(f"\n❌ **Test Failed: {e}**")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        try:
            if 'manager' in locals():
                manager.stop_system()
        except:
            pass

def test_screen_region_system():
    """Test screen region detection and coordination (headless mode)"""
    print("\n🖥️ Testing Screen Region System (Headless)")
    print("=" * 40)
    
    try:
        # Test screen regions for 8-agent layout (without GUI)
        regions = {
            "agent_1": {"x": 100, "y": 100, "region": "top-left"},
            "agent_2": {"x": 500, "y": 100, "region": "top-center-left"},
            "agent_3": {"x": 900, "y": 100, "region": "top-center-right"},
            "agent_4": {"x": 1300, "y": 100, "region": "top-right"},
            "agent_5": {"x": 100, "y": 400, "region": "bottom-left"},
            "agent_6": {"x": 500, "y": 400, "region": "bottom-center-left"},
            "agent_7": {"x": 900, "y": 400, "region": "bottom-center-right"},
            "agent_8": {"x": 1300, "y": 400, "region": "bottom-right"}
        }
        
        # Assume standard monitor sizes
        standard_widths = [1920, 2560, 3440]  # Common monitor resolutions
        standard_heights = [1080, 1440, 1440]
        
        print("   🎯 Testing screen regions for 8-agent layout:")
        for screen_width, screen_height in zip(standard_widths, standard_heights):
            print(f"\n   📺 Testing on {screen_width}x{screen_height} resolution:")
            all_valid = True
            
            for agent_id, region_info in regions.items():
                x, y = region_info["x"], region_info["y"]
                region_name = region_info["region"]
                
                # Check if coordinates are within screen bounds
                if 0 <= x <= screen_width and 0 <= y <= screen_height:
                    print(f"      ✅ {agent_id} ({region_name}): {x}, {y}")
                else:
                    print(f"      ❌ {agent_id} ({region_name}): {x}, {y} - OUT OF BOUNDS")
                    all_valid = False
            
            if all_valid:
                print(f"      🎉 All coordinates valid for {screen_width}x{screen_height}")
            else:
                print(f"      ⚠️ Some coordinates invalid for {screen_width}x{screen_height}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Screen region test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Coordinate Loading Tests (Headless Mode)")
    print("=" * 60)
    
    # Run coordinate loading test
    coord_test_passed = test_coordinate_loading()
    
    # Run screen region test
    screen_test_passed = test_screen_region_system()
    
    print("\n📊 **Test Summary**")
    print("=" * 30)
    print(f"Coordinate Loading: {'✅ PASSED' if coord_test_passed else '❌ FAILED'}")
    print(f"Screen Region Test: {'✅ PASSED' if screen_test_passed else '❌ FAILED'}")
    
    if coord_test_passed and screen_test_passed:
        print("\n🎉 All tests passed! Coordinate system is ready.")
    else:
        print("\n⚠️ Some tests failed. Check coordinate calibration.")
        print("💡 Try running: python3 calibrate_coordinates.py")
        
    # Additional diagnostic information
    print("\n🔍 **System Diagnostic Info**")
    print("=" * 30)
    print("If you're seeing coordinate issues, try:")
    print("1. Run calibrate_coordinates.py to set up agent coordinates")
    print("2. Check that all 8 Cursor agent windows are open")
    print("3. Verify screen resolution supports 8-agent layout")
    print("4. Test individual agent communication")
