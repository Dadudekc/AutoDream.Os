#!/usr/bin/env python3
"""
THEA Clean Start - Fresh Authentication Test
============================================

Clean start for THEA authentication without placeholder conversations.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def clean_thea_test():
    """Test THEA with clean authentication."""
    print("🧹 THEA CLEAN START TEST")
    print("=" * 50)
    print("Starting fresh - no cookies, no placeholder conversations")
    print("=" * 50)

    try:
        from src.services.thea.thea_autonomous_system import send_thea_message_autonomous

        print("🚀 Testing THEA with clean authentication...")
        print("This will:")
        print("1. Launch browser to ChatGPT")
        print("2. Navigate to ChatGPT (not placeholder conversation)")
        print("3. Attempt to send a message")
        print("4. Show you what happens")
        print("=" * 50)

        test_message = "Commander Thea, this is General Agent-4. Clean authentication test - can you see this message?"

        print(f"📤 Sending test message: {test_message}")
        print("🌐 Browser will open in visible mode...")

        response = send_thea_message_autonomous(test_message, headless=False)

        if response:
            print("\n✅ SUCCESS! THEA is working!")
            print(f"📋 Response received: {len(response)} characters")
            print("🎉 Authentication is working properly!")
        else:
            print("\n❌ FAILED: No response received")
            print("🔍 This means authentication still needs to be fixed")

        print("\n" + "=" * 50)
        print("📝 WHAT TO DO NEXT")
        print("=" * 50)

        if response:
            print("✅ THEA is working! You can now use it for:")
            print("   - Strategic consultations")
            print("   - Status reports")
            print("   - Emergency consultations")
        else:
            print("❌ Authentication still not working. You may need to:")
            print("   1. Log in to ChatGPT manually in the browser")
            print("   2. Let THEA save the cookies")
            print("   3. Test again")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("This might indicate a deeper issue with THEA setup")


if __name__ == "__main__":
    clean_thea_test()
