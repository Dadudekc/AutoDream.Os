#!/usr/bin/env python3
"""
Thea Communication Manager - V2 Compliant Main Orchestrator
==========================================================

Main orchestration service for Thea communication system.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from ..authentication.thea_authentication_service import TheaAuthenticationService
from ..browser.thea_browser_service import TheaBrowserService
from ..config.thea_config import TheaConfig, get_thea_config
from ..messaging.thea_messaging_service import TheaMessagingService
from ..responses.thea_response_service import TheaResponseService


class TheaCommunicationManager:
    """Main orchestrator for Thea communication system."""

    def __init__(self, config: TheaConfig | None = None):
        self.config = config or get_thea_config()

        # Initialize services
        self.browser_service = TheaBrowserService(self.config)
        self.auth_service = TheaAuthenticationService(self.config)
        self.response_service = TheaResponseService(self.config, self.browser_service)
        self.messaging_service = TheaMessagingService(
            self.config, self.browser_service, self.response_service
        )

    def initialize(self) -> bool:

EXAMPLE USAGE:
==============

# Import the service
from src.services.thea.core.thea_communication_manager import Thea_Communication_ManagerService

# Initialize service
service = Thea_Communication_ManagerService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Thea_Communication_ManagerService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Initialize the Thea communication system."""
        print("🐝 V2_SWARM THEA COMMUNICATION SYSTEM")
        print("=" * 50)
        print("🎯 INITIALIZING COMPONENTS...")

        # Initialize browser
        if not self.browser_service.initialize_driver():
            print("❌ BROWSER INITIALIZATION FAILED")
            return False

        print("✅ SYSTEM INITIALIZATION COMPLETE")
        return True

    def run_communication_cycle(self, message: str | None = None) -> bool:
        """Run the complete send/receive communication cycle."""
        print("🐝 V2_SWARM THEA COMMUNICATION CYCLE")
        print("=" * 60)
        print("🎯 GOAL: Send prompt to Thea and receive response")
        print("👁️  USER WILL BE MY EYES THROUGHOUT THE PROCESS")
        print("=" * 60)

        # Default message if none provided
        if not message:
            message = """🌟 THEA COMMUNICATION TEST - V2_SWARM

Hello Thea! This is Agent-4 (Captain) testing the communication system.

Please acknowledge this test message and confirm you can see it.

Thank you!
🐝 WE ARE SWARM"""

        # Save the message for reference
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path = self.config.responses_dir / f"sent_message_{timestamp}.txt"
        with open(message_path, "w", encoding="utf-8") as f:
            f.write(message)
        print(f"💾 Message saved: {message_path}")

        print(f"📤 Message prepared: {len(message)} characters")
        print("Message preview:")
        print("-" * 30)
        print(message[:200] + "..." if len(message) > 200 else message)
        print("-" * 30)

        try:
            # Phase 1: Authentication
            print("\n🚀 STARTING PHASE 1: MESSAGE SENDING")
            if not self.auth_service.ensure_authenticated(self.browser_service):
                print("❌ PHASE 1 FAILED: Could not authenticate")
                return False

            print("\n✅ PHASE 1 COMPLETE: Authenticated with Thea")

            # Phase 2: Send Message
            status = self.messaging_service.send_message(message)
            if status.name != "SENT":
                print("❌ PHASE 1 FAILED: Could not send message")
                return False

            print("\n✅ PHASE 1 COMPLETE: Message sent to Thea")

            # Phase 2: Wait for Response (automated)
            print("\n⏳ PHASE 2: WAITING FOR THEA'S RESPONSE")
            print("=" * 50)

            # Use automated response detection
            response_ready = self.messaging_service.wait_for_response()

            if response_ready:
                print("✅ PHASE 2 COMPLETE: Thea's response detected")
            else:
                print("⚠️  PHASE 2: Manual confirmation used")

            # Phase 3: Capture Response
            print("\n🚀 STARTING PHASE 3: RESPONSE CAPTURE")
            screenshot_path = self.response_service.capture_response()
            if not screenshot_path:
                print("❌ PHASE 3 FAILED: Could not capture response")
                return False

            print("✅ PHASE 3 COMPLETE: Response captured")

            # Phase 4: Create analysis
            print("\n🚀 STARTING PHASE 4: ANALYSIS SETUP")
            template_path = self.create_response_analysis(screenshot_path)

            # Save session cookies
            self.auth_service.save_session_cookies(self.browser_service)

            # Success Summary
            self._print_success_summary(
                message, screenshot_path, template_path, message_path, timestamp
            )

            return True

        except Exception as e:
            print(f"\n💥 ERROR: {e}")
            return False
        finally:
            self.cleanup()

    def _print_success_summary(
        self,
        message: str,
        screenshot_path: Path,
        template_path: Path,
        message_path: Path,
        timestamp: str,
    ) -> None:
        """Print comprehensive success summary."""
        print("\n🎉 COMMUNICATION CYCLE COMPLETE!")
        print("=" * 50)
        print("✅ SUMMARY:")
        print(f"   📤 Message sent: {len(message)} characters")
        print(f"   💾 Message saved: {message_path}")
        print(f"   📸 Response captured: {screenshot_path}")
        print(
            f"   📋 Conversation log: {self.config.responses_dir}/conversation_log_{timestamp}.md"
        )
        print(f"   📝 Analysis template: {template_path}")
        print()
        print("🎯 NEXT STEPS:")
        print("   1. Review the conversation log for complete record")
        print("   2. Check the screenshot to see Thea's response")
        print("   3. Fill out the analysis template")
        print("   4. Let me know what Thea said!")
        print()
        print("🐝 WE ARE SWARM - COMMUNICATION SUCCESSFUL!")

    def create_response_analysis(self, screenshot_path):
        """Create analysis template for the captured response."""
        print("\n📝 CREATING RESPONSE ANALYSIS TEMPLATE")
        print("-" * 40)

        template_path = self.config.responses_dir / "response_analysis_template.md"

        template = f"""# Thea Response Analysis

**Captured:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Screenshot:** {screenshot_path}

## Captured Response
[View the screenshot at: {screenshot_path}]

## Thea's Response Content
[Copy Thea's response text here from the screenshot]

## Key Insights
- [Insight 1]
- [Insight 2]
- [Insight 3]

## Action Items
- [Action 1]
- [Action 2]
- [Action 3]

## Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

---
**Analysis completed by:** Agent-4 (Captain)
"""

        with open(template_path, "w") as f:
            f.write(template)
        print(f"✅ Analysis template created: {template_path}")

        return template_path

    def send_quick_message(self, message: str) -> bool:
        """Send a quick message without full cycle."""
        try:
            if not self.initialize():
                return False

            if not self.auth_service.ensure_authenticated(self.browser_service):
                return False

            status = self.messaging_service.send_message(message)
            return status.name == "SENT"

        except Exception as e:
            print(f"❌ Quick message failed: {e}")
            return False
        finally:
            self.cleanup()

    def get_status(self) -> dict[str, Any]:
        """Get current system status."""
        return {
            "browser_initialized": self.browser_service.driver is not None,
            "browser_mode": self.browser_service.mode.value,
            "selenium_available": self.browser_service._selenium_available,
            "cookies_available": self.auth_service.cookie_manager.has_valid_cookies(),
            "responses_dir": str(self.config.responses_dir),
            "logs_dir": str(self.config.logs_dir),
        }

    def cleanup(self) -> None:
        """Clean up all resources."""
        print("\n🧹 CLEANING UP RESOURCES...")
        self.browser_service.cleanup()
        print("✅ Cleanup complete")

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
