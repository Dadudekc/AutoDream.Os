#!/usr/bin/env python3
"""
Concise Integration Testing Framework for Broadcast System
Tests core functionality within line limits
"""
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add services to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "services"))


class BroadcastIntegrationTester:
    """Concise integration tester for broadcast system"""

    def __init__(self):
        self.test_results = []
        self.system_instance = None

    def run_all_tests(self) -> bool:
        """Run complete integration test suite"""
        print("🧪 **BROADCAST SYSTEM INTEGRATION TEST SUITE**")
        print("=" * 60)

        tests = [
            ("System Import", self.test_system_import),
            ("Instance Creation", self.test_instance_creation),
            ("Agent Registry", self.test_agent_registry),
            ("Coordinate Loading", self.test_coordinate_loading),
            ("Message Queuing", self.test_message_queuing),
            ("Broadcast Functionality", self.test_broadcast_functionality),
            ("System Lifecycle", self.test_system_lifecycle),
        ]

        all_passed = True
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                result = test_func()
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}: {test_name}")
                self.test_results.append((test_name, result))
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"   ❌ ERROR: {test_name} - {e}")
                self.test_results.append((test_name, False))
                all_passed = False

        self.print_summary()
        return all_passed

    def test_system_import(self) -> bool:
        """Test system import"""
        try:
            from v1_v2_message_queue_system import V1V2MessageQueueSystem

            return True
        except ImportError:
            return False

    def test_instance_creation(self) -> bool:
        """Test instance creation"""
        try:
            from v1_v2_message_queue_system import V1V2MessageQueueSystem

            self.system_instance = V1V2MessageQueueSystem()
            return True
        except Exception:
            return False

    def test_agent_registry(self) -> bool:
        """Test agent registry"""
        if not self.system_instance:
            return False

        registry = self.system_instance.agent_registry
        return len(registry) == 8 and all(
            "coordinates" in agent_info for agent_info in registry.values()
        )

    def test_coordinate_loading(self) -> bool:
        """Test coordinate loading"""
        if not self.system_instance:
            return False

        coords = self.system_instance.config.get("agent_coordinates", {})
        if not coords:
            return False

        # Check if using calibrated vs default coordinates
        using_defaults = any(
            coords.get("x") in [400, 1200, 2000, 2800] and coords.get("y") in [300, 900]
            for coords in coords.values()
        )

        print(f"   📍 Coordinates loaded: {len(coords)} agents")
        print(f"   🎯 Using {'default' if using_defaults else 'calibrated'} coordinates")

        return True

    def test_message_queuing(self) -> bool:
        """Test message queuing"""
        if not self.system_instance:
            return False

        try:
            # Test single message
            msg_id = self.system_instance.send_message(
                "system", "agent_1", "Test message", "normal"
            )
            if not msg_id:
                return False

            # Test broadcast
            broadcast_ids = self.system_instance.send_message_to_all_agents(
                "system", "Broadcast test", "normal"
            )
            if not broadcast_ids or len(broadcast_ids) != 8:
                return False

            # Test high priority
            high_id = self.system_instance.send_high_priority_message(
                "system", "agent_1", "Urgent test"
            )
            if not high_id:
                return False

            return True
        except Exception:
            return False

    def test_broadcast_functionality(self) -> bool:
        """Test broadcast functionality"""
        if not self.system_instance:
            return False

        try:
            # Start system
            if not self.system_instance.start_system():
                return False

            # Send broadcast
            test_content = f"🧪 Integration test at {time.strftime('%H:%M:%S')}"
            message_ids = self.system_instance.send_message_to_all_agents(
                "system", test_content, "normal"
            )

            if len(message_ids) != 8:
                return False

            # Wait for processing
            time.sleep(1)

            # Check queue status
            queue_status = self.system_instance.get_queue_status()
            total_queued = queue_status.get("total_queued", 0)

            print(f"   📨 Broadcast sent: {len(message_ids)} messages")
            print(f"   📊 Queue status: {total_queued} remaining")

            # Stop system
            self.system_instance.stop_system()
            return True

        except Exception:
            return False

    def test_system_lifecycle(self) -> bool:
        """Test system lifecycle"""
        if not self.system_instance:
            return False

        try:
            # Health check
            health = self.system_instance.health_check()

            # Check if health check returns expected structure
            if not isinstance(health, dict) or "status" not in health:
                print(f"   ⚠️  Health check structure unexpected: {type(health)}")
                return False

            print(f"   🏥 Health status: {health.get('status', 'unknown')}")

            # Coordinate status check
            try:
                coord_status = self.system_instance.get_coordinate_status()
                if coord_status:
                    print("   ✅ Coordinate status check successful")
                else:
                    print("   ⚠️  Coordinate status check returned empty")
            except Exception as e:
                print(f"   ⚠️  Coordinate status check error: {e}")

            return True
            return True

        except Exception as e:
            print(f"   ❌ System lifecycle test error: {e}")
            return False

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 **TEST SUMMARY**")
        print("=" * 60)

        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)

        for test_name, result in self.test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name}")

        print(f"\n🎯 Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 **ALL TESTS PASSED! Broadcast system integration successful!**")
        else:
            print("⚠️  Some tests failed - review issues above")


def main():
    """Main test runner"""
    tester = BroadcastIntegrationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
