#!/usr/bin/env python3
"""
THEA Selector Debugger - Visual Interface Inspector
==================================================

Launches THEA browser in visible mode for manual selector inspection.
Allows human eyes to identify current ChatGPT interface elements.

Usage:
    python thea_selector_debugger.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.thea.thea_autonomous_system import TheaAutonomousSystem


def debug_selectors():
    """Launch THEA browser in visible mode for selector debugging."""
    print("🔍 THEA SELECTOR DEBUGGER")
    print("=" * 50)
    print("Launching browser in VISIBLE mode for selector inspection...")
    print("You can now inspect the ChatGPT interface elements.")
    print("Look for the message input field and note its selectors.")
    print("=" * 50)

    try:
        # Initialize THEA system in visible mode
        system = TheaAutonomousSystem()

        # Launch browser in visible mode (not headless)
        print("🚀 Initializing browser...")
        driver = system._initialize_browser(headless=False)

        if driver:
            print("✅ Browser launched successfully!")
            print("🌐 Navigating to ChatGPT...")
            driver.get("https://chatgpt.com")

            print("\n" + "=" * 50)
            print("🔍 SELECTOR DEBUGGING INSTRUCTIONS:")
            print("=" * 50)
            print("1. Look at the ChatGPT interface")
            print("2. Find the message input field")
            print("3. Right-click on the input field")
            print("4. Select 'Inspect Element'")
            print("5. Note the element's attributes:")
            print("   - id")
            print("   - class")
            print("   - data-testid")
            print("   - role")
            print("   - contenteditable")
            print("6. Press Enter when you've noted the selectors")
            print("=" * 50)

            input("\nPress Enter when you've inspected the interface...")

            print("\n🔍 Testing current selectors...")

            # Test current selectors
            current_selectors = [
                "#prompt-textarea > p",
                "p[data-placeholder='Ask anything']",
                "p[class*='placeholder']",
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                "#prompt-textarea",
                "textarea[placeholder*='Send a message']",
                "textarea[data-testid='prompt-textarea']",
                "div[contenteditable='true'][role='textbox']",
                "textarea",
                "[contenteditable='true']",
                "div[data-testid='conversation-composer-input'] textarea",
                "div[data-testid='conversation-composer-input'] div[contenteditable='true']",
            ]

            for i, selector in enumerate(current_selectors, 1):
                try:
                    elements = driver.find_elements("css selector", selector)
                    if elements:
                        print(f"✅ Selector {i}: '{selector}' - Found {len(elements)} element(s)")
                        for j, element in enumerate(elements):
                            try:
                                print(
                                    f"   Element {j+1}: tag='{element.tag_name}', visible={element.is_displayed()}, enabled={element.is_enabled()}"
                                )
                            except:
                                print(f"   Element {j+1}: Found but couldn't inspect")
                    else:
                        print(f"❌ Selector {i}: '{selector}' - No elements found")
                except Exception as e:
                    print(f"⚠️  Selector {i}: '{selector}' - Error: {e}")

            print("\n" + "=" * 50)
            print("📝 NEXT STEPS:")
            print("=" * 50)
            print("1. If you found working selectors, provide them")
            print("2. If no selectors worked, describe the input field")
            print("3. We'll update the THEA system with new selectors")
            print("=" * 50)

            input("\nPress Enter to close browser...")

        else:
            print("❌ Failed to initialize browser")

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
    debug_selectors()
