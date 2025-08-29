#!/usr/bin/env python3
import json
import time

from src.utils.stability_improvements import stability_manager, safe_import

print("🧪 TEST_SYNC Demo for Enhanced 8-Agent Messaging System")
print("=" * 60)
print()
user_message = {
    "agent_id": "agent_1",
    "type": "test_sync",
    "content": "This is a synchronous test message",
    "timestamp": 1755726240.2626011,
}
print("📤 Original TEST_SYNC message from user:")
print(json.dumps(user_message, indent=2))
print()
print("✅ Message format validation:")
required_fields = ["agent_id", "type", "content", "timestamp"]
for field in required_fields:
    if field in user_message:
        print(f"   ✅ {field}: {user_message[field]}")
    else:
        print(f"   ❌ {field}: Missing")
print()
