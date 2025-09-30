#!/usr/bin/env python3
"""
THEA Manual Login Helper - Guide for Manual Authentication
=========================================================

This script will launch ChatGPT and guide you through manual login
so THEA can save proper authentication cookies.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def manual_login_helper():
    """Guide user through manual login process."""
    print("🔐 THEA MANUAL LOGIN HELPER")
    print("=" * 50)
    print("This will help you log in to ChatGPT manually so THEA can work properly.")
    print("=" * 50)

    try:
        from src.services.thea.thea_autonomous_system import TheaAutonomousSystem

        print("🚀 Launching ChatGPT in visible mode...")
        system = TheaAutonomousSystem(headless=False)

        # Get the browser manager
        browser_manager = system.browser_manager
        driver = browser_manager.initialize_driver()

        if not driver:
            print("❌ Failed to initialize browser")
            return

        print("🌐 Navigating to ChatGPT...")
        driver.get("https://chatgpt.com")

        print("\n" + "=" * 50)
        print("🔐 MANUAL LOGIN INSTRUCTIONS")
        print("=" * 50)
        print("1. ✅ Browser opened to ChatGPT")
        print("2. 🔐 Log in to ChatGPT using your preferred method:")
        print("   - Google account")
        print("   - Microsoft account")
        print("   - Apple account")
        print("   - Email/password")
        print("3. ✅ Wait for ChatGPT interface to fully load")
        print("4. ✅ Verify you can see the chat interface")
        print("5. ✅ Press Enter here when login is complete")
        print("=" * 50)

        input("\nPress Enter when you've completed login...")

        print("\n🔍 Verifying login status...")

        # Check if login was successful
        page_source = driver.page_source.lower()

        if "new chat" in page_source and "log in" not in page_source:
            print("✅ LOGIN SUCCESSFUL!")
            print("🔍 Saving authentication cookies...")

            # Save cookies
            cookie_manager = system.cookie_manager
            success = cookie_manager.save_cookies(driver)

            if success:
                print("✅ Authentication cookies saved successfully!")
                print("🎉 THEA is now ready for autonomous operation!")
            else:
                print("⚠️  Cookie saving had issues, but login appears successful")

        else:
            print("⚠️  Login status unclear - please verify you're logged in")

        print("\n" + "=" * 50)
        print("🧪 TESTING THEA AFTER LOGIN")
        print("=" * 50)
        print("Let's test if THEA can now send messages properly...")

        test_message = "Commander Thea, this is General Agent-4. Authentication test complete. Please confirm you can see this message."

        print(f"📤 Sending test message: {test_message[:50]}...")

        # Test THEA message sending
        response = system.send_message_autonomous(test_message)

        if response:
            print("✅ SUCCESS! THEA is working properly!")
            print(f"📋 Response received: {len(response)} characters")
            print("🎉 THEA authentication is now complete!")
        else:
            print("⚠️  THEA test failed - may need additional troubleshooting")

        print("\n" + "=" * 50)
        print("📝 NEXT STEPS")
        print("=" * 50)
        print("1. ✅ THEA authentication should now work")
        print("2. 🚀 You can use THEA for strategic consultations")
        print("3. 🔄 THEA will maintain authentication automatically")
        print(
            "4. 📊 Test with: python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance"
        )

        input("\nPress Enter to close browser...")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        try:
            if "driver" in locals():
                driver.quit()
                print("✅ Browser closed")
        except:
            pass


if __name__ == "__main__":
    manual_login_helper()
