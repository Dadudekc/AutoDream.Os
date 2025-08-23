#!/usr/bin/env python3
"""
AI Gaming Systems Test Framework
================================

Comprehensive testing framework for AI gaming systems core infrastructure.
Tests message queue, agent coordination, and system reliability before
integrating Dadudekc combat, economy, and NPC systems.
"""

from v1_v2_message_queue_system import V1V2MessageQueueSystem
import time
import threading
import random
import json
from datetime import datetime


class AIGamingSystemsTest:
    """AI Gaming Systems Test Framework"""

    def __init__(self):
        self.mq = None
        self.test_results = {}
        self.test_start_time = None

    def initialize_system(self):
        """Initialize the message queue system for testing"""
        print("🚀 Initializing AI Gaming Systems Test Framework...")

        try:
            self.mq = V1V2MessageQueueSystem()
            self.mq.start_system()
            print("✅ Message queue system initialized and started")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize system: {e}")
            return False

    def test_agent_registry(self):
        """Test agent registry functionality"""
        print("\n🔍 Testing Agent Registry...")

        try:
            # Check agent count
            agent_count = len(self.mq.agent_registry)
            expected_count = 5  # 5-agent mode

            if agent_count == expected_count:
                print(f"✅ Agent count: {agent_count}/{expected_count}")
                self.test_results["agent_registry"] = True
            else:
                print(f"❌ Agent count mismatch: {agent_count}/{expected_count}")
                self.test_results["agent_registry"] = False
                return False

            # Check agent coordinates
            for agent_id, info in self.mq.agent_registry.items():
                coords = info["coordinates"]
                if "x" in coords and "y" in coords:
                    print(f"✅ {agent_id}: x={coords['x']}, y={coords['y']}")
                else:
                    print(f"❌ {agent_id}: Missing coordinates")
                    self.test_results["agent_registry"] = False
                    return False

            return True

        except Exception as e:
            print(f"❌ Agent registry test failed: {e}")
            self.test_results["agent_registry"] = False
            return False

    def test_message_queuing(self):
        """Test message queuing system"""
        print("\n🔍 Testing Message Queuing System...")

        try:
            # Test normal priority message
            message_id = self.mq.send_message(
                sender_agent="TEST_SYSTEM",
                target_agent="agent_1",
                content="Test message for queuing system",
                priority="normal",
            )

            if message_id:
                print(f"✅ Normal priority message queued: {message_id}")
            else:
                print("❌ Failed to queue normal priority message")
                self.test_results["message_queuing"] = False
                return False

            # Test high priority message
            high_priority_id = self.mq.send_message(
                sender_agent="TEST_SYSTEM",
                target_agent="agent_2",
                content="HIGH PRIORITY TEST MESSAGE",
                priority="high",
            )

            if high_priority_id:
                print(f"✅ High priority message queued: {high_priority_id}")
            else:
                print("❌ Failed to queue high priority message")
                self.test_results["message_queuing"] = False
                return False

            # Check queue status
            status = self.mq.get_queue_status()
            print(
                f"✅ Queue status: Regular={status['regular_queue_size']}, High={status['high_priority_queue_size']}"
            )

            self.test_results["message_queuing"] = True
            return True

        except Exception as e:
            print(f"❌ Message queuing test failed: {e}")
            self.test_results["message_queuing"] = False
            return False

    def test_message_delivery(self):
        """Test message delivery to agents"""
        print("\n🔍 Testing Message Delivery...")

        try:
            # Send test message to agent_3
            test_message = (
                f"[TEST] AI Gaming Systems Test - {datetime.now().strftime('%H:%M:%S')}"
            )
            message_id = self.mq.send_message(
                sender_agent="TEST_SYSTEM",
                target_agent="agent_3",
                content=test_message,
                priority="high",
            )

            if not message_id:
                print("❌ Failed to send test message")
                self.test_results["message_delivery"] = False
                return False

            print(f"✅ Test message sent: {message_id}")

            # Wait for delivery
            print("⏳ Waiting for message delivery...")
            time.sleep(3)

            # Check delivery status
            if len(self.mq.message_history) > 0:
                latest_message = self.mq.message_history[-1]
                status = latest_message.get("status", "unknown")

                if "sent" in status or "high_priority_sent" in status:
                    print(f"✅ Message delivered successfully: {status}")
                    self.test_results["message_delivery"] = True
                    return True
                else:
                    print(f"❌ Message delivery failed: {status}")
                    self.test_results["message_delivery"] = False
                    return False
            else:
                print("❌ No message history found")
                self.test_results["message_delivery"] = False
                return False

        except Exception as e:
            print(f"❌ Message delivery test failed: {e}")
            self.test_results["message_delivery"] = False
            return False

    def test_broadcast_system(self):
        """Test broadcast message system"""
        print("\n🔍 Testing Broadcast System...")

        try:
            # Send broadcast to all agents
            broadcast_message = f"[BROADCAST] AI Gaming Systems Test - {datetime.now().strftime('%H:%M:%S')}"
            message_ids = self.mq.send_message_to_all_agents(
                sender_agent="TEST_SYSTEM", content=broadcast_message, priority="normal"
            )

            if len(message_ids) == 5:  # 5 agents
                print(f"✅ Broadcast sent to all {len(message_ids)} agents")
                print(f"🆔 Message IDs: {message_ids}")
            else:
                print(f"❌ Broadcast failed: {len(message_ids)}/5 agents")
                self.test_results["broadcast_system"] = False
                return False

            # Wait for processing
            print("⏳ Waiting for broadcast processing...")
            time.sleep(5)

            # Check broadcast status
            broadcast_messages = [
                msg
                for msg in self.mq.message_history[-len(message_ids) :]
                if msg.get("message", {}).get("sender_agent") == "TEST_SYSTEM"
            ]

            successful_deliveries = sum(
                1 for msg in broadcast_messages if "sent" in msg.get("status", "")
            )

            if successful_deliveries == 5:
                print(f"✅ All {successful_deliveries}/5 broadcast messages delivered")
                self.test_results["broadcast_system"] = True
                return True
            else:
                print(f"❌ Broadcast delivery incomplete: {successful_deliveries}/5")
                self.test_results["broadcast_system"] = False
                return False

        except Exception as e:
            print(f"❌ Broadcast system test failed: {e}")
            self.test_results["broadcast_system"] = False
            return False

    def test_high_priority_system(self):
        """Test high priority message system"""
        print("\n🔍 Testing High Priority System...")

        try:
            # Send multiple high priority messages
            high_priority_messages = [
                "🚨 URGENT: Combat system alert!",
                "🚨 URGENT: Economy system warning!",
                "🚨 URGENT: NPC interaction error!",
            ]

            message_ids = []
            for i, message in enumerate(high_priority_messages):
                msg_id = self.mq.send_high_priority_message(
                    sender_agent="TEST_SYSTEM",
                    target_agent=f"agent_{i+1}",
                    content=message,
                )
                if msg_id:
                    message_ids.append(msg_id)
                    print(f"✅ High priority message {i+1} queued: {msg_id}")
                else:
                    print(f"❌ Failed to queue high priority message {i+1}")
                    self.test_results["high_priority_system"] = False
                    return False

            # Wait for high priority processing
            print("⏳ Waiting for high priority message processing...")
            time.sleep(3)

            # Check high priority delivery
            high_priority_deliveries = [
                msg
                for msg in self.mq.message_history[-len(message_ids) :]
                if "high_priority" in msg.get("status", "")
            ]

            if len(high_priority_deliveries) == len(message_ids):
                print(
                    f"✅ All {len(high_priority_deliveries)} high priority messages processed"
                )
                self.test_results["high_priority_system"] = True
                return True
            else:
                print(
                    f"❌ High priority processing incomplete: {len(high_priority_deliveries)}/{len(message_ids)}"
                )
                self.test_results["high_priority_system"] = False
                return False

        except Exception as e:
            print(f"❌ High priority system test failed: {e}")
            self.test_results["high_priority_system"] = False
            return False

    def test_system_health(self):
        """Test overall system health"""
        print("\n🔍 Testing System Health...")

        try:
            # Get health status
            health_status = self.mq.health_check()

            if health_status["status"] == "healthy":
                print("✅ System health: HEALTHY")
            else:
                print(f"⚠️ System health: {health_status['status']}")

            # Check individual components
            checks = health_status.get("checks", {})

            for check_name, check_info in checks.items():
                status = check_info.get("status", "unknown")
                if status == "healthy":
                    print(f"✅ {check_name}: {status}")
                else:
                    print(f"❌ {check_name}: {status}")

            # Check queue status
            queue_status = self.mq.get_queue_status()
            print(
                f"✅ Queue status: Regular={queue_status['regular_queue_size']}, High={queue_status['high_priority_queue_size']}"
            )

            self.test_results["system_health"] = health_status["status"] == "healthy"
            return health_status["status"] == "healthy"

        except Exception as e:
            print(f"❌ System health test failed: {e}")
            self.test_results["system_health"] = False
            return False

    def run_complete_test_suite(self):
        """Run complete AI gaming systems test suite"""
        print("🚀 AI GAMING SYSTEMS TEST SUITE")
        print("=" * 50)
        print("Testing core infrastructure for Dadudekc integrations...")
        print()

        self.test_start_time = time.time()

        # Initialize system
        if not self.initialize_system():
            print("❌ System initialization failed - cannot proceed with tests")
            return False

        # Run all tests
        tests = [
            ("Agent Registry", self.test_agent_registry),
            ("Message Queuing", self.test_message_queuing),
            ("Message Delivery", self.test_message_delivery),
            ("Broadcast System", self.test_broadcast_system),
            ("High Priority System", self.test_high_priority_system),
            ("System Health", self.test_system_health),
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ {test_name} test failed")
            except Exception as e:
                print(f"❌ {test_name} test crashed: {e}")

        # Calculate test duration
        test_duration = time.time() - self.test_start_time

        # Print results
        print("\n" + "=" * 50)
        print("📊 AI GAMING SYSTEMS TEST RESULTS")
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        print(f"⏱️ Test duration: {test_duration:.2f} seconds")

        if passed == total:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Core infrastructure is ready for Dadudekc integrations")
            print("✅ Ready to proceed with combat, economy, and NPC systems")
        else:
            print("\n⚠️ SOME TESTS FAILED!")
            print("❌ Core infrastructure needs attention before Dadudekc integrations")

        # Cleanup
        if self.mq:
            self.mq.stop_system()
            print("✅ System stopped")

        return passed == total


def main():
    """Main test execution"""
    try:
        test_suite = AIGamingSystemsTest()
        success = test_suite.run_complete_test_suite()

        if success:
            print("\n🚀 READY FOR DADUDEKC INTEGRATIONS!")
            print("Next steps:")
            print("1. Integrate Dadudekc combat system enhancements")
            print("2. Integrate Dadudekc economy and market systems")
            print("3. Integrate Dadudekc NPC interaction systems")
        else:
            print("\n❌ CORE INFRASTRUCTURE ISSUES DETECTED")
            print("Please resolve test failures before proceeding with integrations")

        return success

    except KeyboardInterrupt:
        print("\n🛑 Test suite interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test suite crashed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
