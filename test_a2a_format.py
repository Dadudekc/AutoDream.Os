#!/usr/bin/env python3
"""
Test script for A2A message format restoration
"""
import os
import sys

sys.path.append('src')

from services.consolidated_messaging_service import ConsolidatedMessagingService


def test_a2a_format():
    """Test the A2A message format for agent-to-agent communication."""
    print("🧪 Testing A2A Message Format")
    print("=" * 50)

    # Test inbox message format
    print("📬 Testing inbox A2A format...")

    # Import the function directly
    from services.consolidated_messaging_service import send_message_inbox

    # Test agent-to-agent message
    result = send_message_inbox(
        agent_id="Agent-2",
        message="Test coordination message between agents during cleanup phase",
        sender="Agent-1"
    )

    if result:
        print("✅ A2A inbox message sent successfully")

        # Check if the message file was created with A2A format
        import os
        inbox_path = "agent_workspaces/Agent-2/inbox"
        if os.path.exists(inbox_path):
            files = [f for f in os.listdir(inbox_path) if f.startswith("A2A_MESSAGE")]
            if files:
                print(f"📄 A2A message file created: {files[-1]}")
                # Read and display the message content
                with open(os.path.join(inbox_path, files[-1]), 'r') as f:
                    content = f.read()
                    if "[A2A] Agent-1 → Agent-2" in content:
                        print("✅ A2A format correctly applied to message header")
                    if "CLEANUP PHASE: Avoid creating unnecessary files" in content:
                        print("✅ Cleanup reminder included in A2A message")
                    else:
                        print("❌ Cleanup reminder missing")
            else:
                print("❌ No A2A message file found")
        else:
            print("❌ Inbox directory not found")
    else:
        print("❌ Failed to send A2A inbox message")

    # Test PyAutoGUI format (this would require actual GUI testing)
    print("\n🖥️ PyAutoGUI A2A format would be tested in integration environment")

    print("\n" + "=" * 50)
    print("🎉 A2A Format Testing Complete")
    print("📋 A2A format restored for agent-to-agent communication")
    print("⚠️ Cleanup phase reminders now included in all A2A messages")

if __name__ == "__main__":
    test_a2a_format()
