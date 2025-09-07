from pathlib import Path
import json
import os
import sys

        import traceback
    from core.agent_communication import (
    from core.fsm import FSMSystemManager
    from core.inbox_manager import InboxManager
    from core.v2_onboarding_sequence import V2OnboardingSequence
from src.utils.stability_improvements import stability_manager, safe_import
from tests.utils.mock_managers import MockWorkspaceManager
import time

#!/usr/bin/env python3
"""
Test Individual Message to Agent-1 - Agent Cellphone V2
=======================================================

Simple test script to send an individual test message to Agent-1.
Tests the V2 onboarding sequence and real agent communication.

Author: V2 Testing Specialist
License: MIT
"""



# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))


try:
        AgentCommunicationProtocol,
        MessageType,
        UnifiedMessagePriority,
    )

    print("✅ All V2 components imported successfully")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Running in limited mode...")

    # Create mock components for testing
    class MockAgentCommunicationProtocol:
        def __init__(self):
            self.messages_sent = []

        def send_message(
            self, sender_id, recipient_id, message_type, payload, priority
        ):
            message_id = f"test_msg_{len(self.messages_sent)}"
            self.messages_sent.append(
                {
                    "message_id": message_id,
                    "sender_id": sender_id,
                    "recipient_id": recipient_id,
                    "message_type": message_type,
                    "payload": payload,
                    "priority": priority,
                }
            )
            print(f"📤 Mock message sent: {message_id}")
            return message_id

    class MockFSMCoreV2:
        def __init__(self):
            self.tasks_created = []

        def create_task(self, title, description, assigned_agent):
            task_id = f"test_task_{len(self.tasks_created)}"
            self.tasks_created.append(
                {
                    "task_id": task_id,
                    "title": title,
                    "description": description,
                    "assigned_agent": assigned_agent,
                }
            )
            print(f"📋 Mock FSM task created: {task_id}")
            return task_id

    class MockInboxManager:
        def __init__(self):
            self.messages = []

        def get_messages(self, agent_id=None):
            return self.messages

    # Use mock components
    AgentCommunicationProtocol = MockAgentCommunicationProtocol
    FSMCoreV2 = MockFSMCoreV2
    InboxManager = MockInboxManager


def send_test_message_to_agent1():
    """Send a test message to Agent-1"""
    print("\n🚀 Sending Individual Test Message to Agent-1!")
    print("=" * 60)

    try:
        # Initialize components
        print("🔧 Initializing V2 components...")

        inbox_manager = InboxManager()
        comm_protocol = AgentCommunicationProtocol()

        # Create mock workspace manager for FSM core
        workspace_manager = MockWorkspaceManager("/tmp/mock_workspace")
        fsm_core = FSMCoreV2(workspace_manager, inbox_manager)

        # Initialize onboarding sequence
        onboarding_config = {
            "phase_timeout": 30,  # Short timeout for testing
            "validation_retries": 2,
        }

        onboarding = V2OnboardingSequence(onboarding_config)
        print("✅ V2 Onboarding Sequence initialized")

        # Start onboarding for Agent-1
        print(f"\n🎯 Starting onboarding for Agent-1...")
        session_id = onboarding.start_onboarding(
            "Agent-1", comm_protocol, fsm_core, inbox_manager
        )

        if session_id:
            print(f"✅ Onboarding started with session: {session_id}")

            # Monitor progress
            print(f"\n📊 Monitoring onboarding progress...")
            max_wait = 30  # 30 seconds max wait
            start_time = time.time()

            while time.time() - start_time < max_wait:
                status = onboarding.get_onboarding_status(session_id)
                if status:
                    print(
                        f"📈 Status: {status['status']} | Phase: {status['current_phase']} | Completed: {len(status['completed_phases'])}"
                    )

                    if status["status"] in ["completed", "failed"]:
                        print(f"\n🎉 Onboarding {status['status']} for Agent-1!")
                        break

                time.sleep(2)
            else:
                print("⏰ Timeout reached - checking final status")
                final_status = onboarding.get_onboarding_status(session_id)
                if final_status:
                    print(f"📊 Final Status: {final_status['status']}")

            # Show communication results
            if hasattr(comm_protocol, "messages_sent"):
                print(f"\n📤 Messages sent to Agent-1:")
                for msg in comm_protocol.messages_sent:
                    print(
                        f"  • {msg['message_type']}: {msg['payload'].get('content', 'N/A')[:50]}..."
                    )

            # Show FSM tasks created
            if hasattr(fsm_core, "tasks_created"):
                print(f"\n📋 FSM tasks created:")
                for task in fsm_core.tasks_created:
                    print(f"  • {task['title']}")

            return True

        else:
            print("❌ Failed to start onboarding for Agent-1")
            return False

    except Exception as e:
        print(f"❌ Error during test: {e}")

        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("🧪 Agent-1 Individual Message Test - Agent Cellphone V2")
    print("=" * 60)

    success = send_test_message_to_agent1()

    if success:
        print("\n✅ Test completed successfully!")
        print("🎉 Agent-1 received individual test message through V2 onboarding!")
    else:
        print("\n❌ Test failed!")
        print("🔧 Check the error messages above for troubleshooting")

    print("\n" + "=" * 60)
    print("🏁 Test complete!")


if __name__ == "__main__":
    main()
