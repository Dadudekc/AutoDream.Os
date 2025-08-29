import os
import sys

        from ml_robot_bridge import MLRobotBridge
        from ml_robot_bridge import MLRobotBridge, create_ml_robot_bridge, validate_ml_robot_integration
        from unittest.mock import Mock

#!/usr/bin/env python3
"""
Simple ML Robot Integration Test - Agent Cellphone V2
====================================================

Quick verification that ML robot integration works properly.
"""


# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def test_ml_robot_bridge_import():
    """Test that ML robot bridge can be imported."""
    try:
        print("✅ ML Robot Bridge import successful")
        return True
    except ImportError as e:
        print(f"❌ ML Robot Bridge import failed: {e}")
        return False

def test_ml_robot_bridge_creation():
    """Test that ML robot bridge can be created."""
    try:
        
        # Create mock coordinate manager
        mock_coord_manager = Mock()
        mock_coord_manager.get_agent_count.return_value = 8
        
        # Create bridge
        bridge = MLRobotBridge(mock_coord_manager)
        print("✅ ML Robot Bridge creation successful")
        return True
    except Exception as e:
        print(f"❌ ML Robot Bridge creation failed: {e}")
        return False

def test_integration_status():
    """Test that integration status can be retrieved."""
    try:
        
        # Create mock coordinate manager
        mock_coord_manager = Mock()
        mock_coord_manager.get_agent_count.return_value = 8
        
        # Create bridge and get status
        bridge = MLRobotBridge(mock_coord_manager)
        status = bridge.get_integration_status()
        
        # Verify status structure
        required_keys = ["coordinate_manager", "messaging_system", "agent_coordinator", "ml_robot_systems"]
        for key in required_keys:
            if key not in status:
                print(f"❌ Missing status key: {key}")
                return False
        
        print("✅ Integration status retrieval successful")
        return True
    except Exception as e:
        print(f"❌ Integration status test failed: {e}")
        return False

def test_compliance_validation():
    """Test that compliance validation works."""
    try:
        
        # Create mock coordinate manager
        mock_coord_manager = Mock()
        mock_coord_manager.get_agent_count.return_value = 8
        
        # Create bridge and validate compliance
        bridge = MLRobotBridge(mock_coord_manager)
        compliance = bridge.validate_integration_compliance()
        
        # Verify compliance structure
        if "overall_score" not in compliance:
            print("❌ Missing compliance score")
            return False
        
        if compliance["overall_score"] != 100.0:
            print(f"❌ Compliance score not 100%: {compliance['overall_score']}")
            return False
        
        print("✅ Compliance validation successful")
        return True
    except Exception as e:
        print(f"❌ Compliance validation test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🤖 ML Robot Integration Test - Agent Cellphone V2")
    print("=" * 50)
    
    tests = [
        test_ml_robot_bridge_import,
        test_ml_robot_bridge_creation,
        test_integration_status,
        test_compliance_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ML Robot integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the integration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
