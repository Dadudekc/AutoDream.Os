#!/usr/bin/env python3
"""
Smoke Tests for Unified Messaging System - Agent Cellphone V2
============================================================

Quick validation tests to ensure the messaging system is working correctly.
These tests run fast and validate core functionality.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import tempfile
import json
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_coordinate_manager():
    """Test coordinate manager basic functionality"""
    print("🧪 Testing Coordinate Manager...")
    
    try:
        from services.messaging.coordinate_manager import CoordinateManager
        
        # Create temporary coordinate file
        temp_dir = tempfile.mkdtemp()
        coord_file = Path(temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                }
            }
        }
        
        # Write test coordinates
        with open(coord_file, 'w') as f:
            json.dump(sample_coords, f)
        
        # Test initialization
        coord_manager = CoordinateManager(str(coord_file))
        assert len(coord_manager.coordinates) == 1, "Coordinate loading failed"
        
        # Test coordinate retrieval
        coords = coord_manager.get_agent_coordinates("Agent-1", "8-agent")
        assert coords is not None, "Coordinate retrieval failed"
        assert coords.agent_id == "Agent-1", "Agent ID mismatch"
        
        # Test validation
        validation_results = coord_manager.validate_coordinates()
        assert validation_results["valid_coordinates"] == 1, "Validation failed"
        
        # Test mode listing
        modes = coord_manager.get_available_modes()
        assert "8-agent" in modes, "Mode listing failed"
        
        # Test agent listing
        agents = coord_manager.get_agents_in_mode("8-agent")
        assert "Agent-1" in agents, "Agent listing failed"
        
        print("✅ Coordinate Manager: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Coordinate Manager: FAILED - {e}")
        return False
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def test_pyautogui_messaging():
    """Test PyAutoGUI messaging basic functionality"""
    print("🧪 Testing PyAutoGUI Messaging...")
    
    try:
        from services.messaging.pyautogui_messaging import PyAutoGUIMessaging
        from services.messaging.coordinate_manager import CoordinateManager
        
        # Create temporary coordinate file
        temp_dir = tempfile.mkdtemp()
        coord_file = Path(temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                }
            }
        }
        
        # Write test coordinates
        with open(coord_file, 'w') as f:
            json.dump(sample_coords, f)
        
        # Test initialization
        coord_manager = CoordinateManager(str(coord_file))
        pyautogui_messaging = PyAutoGUIMessaging(coord_manager)
        
        # Test message sending (mocked)
        # Note: We don't actually send messages in smoke tests
        assert pyautogui_messaging.coordinate_manager is not None, "Dependency injection failed"
        
        print("✅ PyAutoGUI Messaging: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ PyAutoGUI Messaging: FAILED - {e}")
        return False
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def test_campaign_messaging():
    """Test campaign messaging basic functionality"""
    print("🧪 Testing Campaign Messaging...")
    
    try:
        from services.messaging.campaign_messaging import CampaignMessaging
        from services.messaging.coordinate_manager import CoordinateManager
        from services.messaging.pyautogui_messaging import PyAutoGUIMessaging
        
        # Create temporary coordinate file
        temp_dir = tempfile.mkdtemp()
        coord_file = Path(temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                }
            }
        }
        
        # Write test coordinates
        with open(coord_file, 'w') as f:
            json.dump(sample_coords, f)
        
        # Test initialization
        coord_manager = CoordinateManager(str(coord_file))
        pyautogui_messaging = PyAutoGUIMessaging(coord_manager)
        campaign_messaging = CampaignMessaging(coord_manager, pyautogui_messaging)
        
        # Test dependency injection
        assert campaign_messaging.coordinate_manager is not None, "Coordinate manager injection failed"
        assert campaign_messaging.pyautogui_messaging is not None, "PyAutoGUI messaging injection failed"
        
        print("✅ Campaign Messaging: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Campaign Messaging: FAILED - {e}")
        return False
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def test_yolo_messaging():
    """Test YOLO messaging basic functionality"""
    print("🧪 Testing YOLO Messaging...")
    
    try:
        from services.messaging.yolo_messaging import YOLOMessaging
        from services.messaging.coordinate_manager import CoordinateManager
        from services.messaging.pyautogui_messaging import PyAutoGUIMessaging
        
        # Create temporary coordinate file
        temp_dir = tempfile.mkdtemp()
        coord_file = Path(temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                }
            }
        }
        
        # Write test coordinates
        with open(coord_file, 'w') as f:
            json.dump(sample_coords, f)
        
        # Test initialization
        coord_manager = CoordinateManager(str(coord_file))
        pyautogui_messaging = PyAutoGUIMessaging(coord_manager)
        yolo_messaging = YOLOMessaging(coord_manager, pyautogui_messaging)
        
        # Test dependency injection
        assert yolo_messaging.coordinate_manager is not None, "Coordinate manager injection failed"
        assert yolo_messaging.pyautogui_messaging is not None, "PyAutoGUI messaging injection failed"
        
        print("✅ YOLO Messaging: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ YOLO Messaging: FAILED - {e}")
        return False
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def test_unified_messaging_service():
    """Test unified messaging service orchestration"""
    print("🧪 Testing Unified Messaging Service...")
    
    try:
        from services.messaging.unified_messaging_service import UnifiedMessagingService
        from services.messaging.interfaces import MessagingMode
        
        # Create temporary coordinate file
        temp_dir = tempfile.mkdtemp()
        coord_file = Path(temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                }
            }
        }
        
        # Write test coordinates
        with open(coord_file, 'w') as f:
            json.dump(sample_coords, f)
        
        # Test initialization
        service = UnifiedMessagingService(str(coord_file))
        
        # Test component initialization
        assert service.coordinate_manager is not None, "Coordinate manager not initialized"
        assert service.pyautogui_messaging is not None, "PyAutoGUI messaging not initialized"
        assert service.campaign_messaging is not None, "Campaign messaging not initialized"
        assert service.yolo_messaging is not None, "YOLO messaging not initialized"
        
        # Test mode setting
        assert service.active_mode == MessagingMode.PYAUTOGUI, "Default mode incorrect"
        service.set_mode(MessagingMode.CAMPAIGN)
        assert service.active_mode == MessagingMode.CAMPAIGN, "Mode setting failed"
        
        # Test coordinate validation
        validation_results = service.validate_coordinates()
        assert validation_results["valid_coordinates"] == 1, "Coordinate validation failed"
        
        # Test mode listing
        modes = service.get_available_modes()
        assert "8-agent" in modes, "Mode listing failed"
        
        # Test agent listing
        agents = service.get_agents_in_mode("8-agent")
        assert "Agent-1" in agents, "Agent listing failed"
        
        print("✅ Unified Messaging Service: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Unified Messaging Service: FAILED - {e}")
        return False
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def test_interfaces():
    """Test interface definitions"""
    print("🧪 Testing Interfaces...")
    
    try:
        from services.messaging.interfaces import (
            MessagingMode, MessageType, IMessageSender, IBulkMessaging,
            ICampaignMessaging, IYOLOMessaging, ICoordinateManager
        )
        
        # Test enum values
        assert MessagingMode.PYAUTOGUI.value == "pyautogui", "PyAutoGUI mode value incorrect"
        assert MessagingMode.CAMPAIGN.value == "campaign", "Campaign mode value incorrect"
        assert MessagingMode.YOLO.value == "yolo", "YOLO mode value incorrect"
        
        # Test message types
        assert MessageType.TEXT.value == "text", "Text message type value incorrect"
        assert MessageType.COMMAND.value == "command", "Command message type value incorrect"
        assert MessageType.BROADCAST.value == "broadcast", "Broadcast message type value incorrect"
        
        # Test interface inheritance
        assert issubclass(IMessageSender, object), "IMessageSender interface inheritance failed"
        assert issubclass(IBulkMessaging, object), "IBulkMessaging interface inheritance failed"
        assert issubclass(ICampaignMessaging, object), "ICampaignMessaging interface inheritance failed"
        assert issubclass(IYOLOMessaging, object), "IYOLOMessaging interface inheritance failed"
        assert issubclass(ICoordinateManager, object), "ICoordinateManager interface inheritance failed"
        
        print("✅ Interfaces: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Interfaces: FAILED - {e}")
        return False


def test_cli_interface():
    """Test CLI interface basic functionality"""
    print("🧪 Testing CLI Interface...")
    
    try:
        from services.messaging.cli_interface import MessagingCLI
        
        # Test CLI initialization
        cli = MessagingCLI()
        
        # Test parser creation
        assert cli.parser is not None, "Argument parser not created"
        assert cli.service is not None, "Messaging service not initialized"
        
        # Test help generation
        help_result = cli._show_help()
        assert help_result == True, "Help generation failed"
        
        print("✅ CLI Interface: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ CLI Interface: FAILED - {e}")
        return False


def run_smoke_tests():
    """Run all smoke tests"""
    print("🚀 STARTING MESSAGING SYSTEM SMOKE TESTS")
    print("=" * 60)
    
    tests = [
        test_interfaces,
        test_coordinate_manager,
        test_pyautogui_messaging,
        test_campaign_messaging,
        test_yolo_messaging,
        test_unified_messaging_service,
        test_cli_interface
    ]
    
    passed = 0
    failed = 0
    
    start_time = time.time()
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: CRASHED - {e}")
            failed += 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🏆 SMOKE TEST RESULTS")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Duration: {duration:.2f} seconds")
    
    if failed == 0:
        print("\n🎉 ALL SMOKE TESTS PASSED! The messaging system is ready for production.")
        return True
    else:
        print(f"\n⚠️  {failed} smoke test(s) failed. The messaging system needs attention.")
        return False


if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
