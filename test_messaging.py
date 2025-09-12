#!/usr/bin/env python3
"""
Test script to verify MessagingGateway functionality
"""
import asyncio
import sys
import os

sys.path.append("src")

from integration.messaging_gateway import MessagingGateway


async def test_message():
    print("🔧 Testing MessagingGateway...")
    print("=" * 50)

    try:
        # Initialize gateway
        gateway = MessagingGateway()
        print("✅ MessagingGateway initialized successfully")

        # Send test message to Agent-4
        print("📨 Sending test message to Agent-4...")

        result = await gateway.send(
            agent_key="Agent-4",
            message="SYSTEM TEST: This is a test message to verify messaging functionality after recent fixes",
            meta={
                "source": "system_test",
                "message_type": "general_to_agent",
                "author_tag": "SystemTest-Agent4",
            },
        )

        print("✅ Message sent successfully!")
        print("-" * 30)
        print(f'Status: {result.get("status")}')
        print(f'Agent: {result.get("agent")}')
        print(f'Backend: {result.get("backend")}')
        print(f'Request ID: {result.get("request_id")}')
        print(f'Timestamp: {result.get("timestamp")}')

        if result.get("status") == "sent":
            print("🎉 MESSAGING SYSTEM IS OPERATIONAL!")
        else:
            print("⚠️  Message status indicates potential issue")

        return result

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("🚀 Starting MessagingGateway Test")
    result = asyncio.run(test_message())
    print("=" * 50)
    print("🏁 Test completed")
