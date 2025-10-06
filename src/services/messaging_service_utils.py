#!/usr/bin/env python3
"""
Consolidated Messaging Service - Utils
=====================================

Utility functions for message formatting, validation, and sending.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import logging
import time

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class MessageFormatter:
    """Format A2A messages with proper headers and guidelines."""

    @staticmethod
    def format_a2a_message(from_agent: str, to_agent: str, content: str, priority: str, compact: bool = False) -> str:
        """Format A2A message with proper headers."""
        priority_indicator = "🚨 " if priority.upper() == "URGENT" else ""

        if compact:
            guidelines = MessageFormatter.get_compact_guidelines()
        else:
            guidelines = MessageFormatter.get_quality_guidelines()

        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority.upper()}
Tags: GENERAL
-------------------------------------------------------------
{content}
{guidelines}
============================================================
-------------------------------------------------------------"""

    @staticmethod
    def get_quality_guidelines() -> str:
        """Get comprehensive tool reminders for all agent communications."""
        return """🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
============================================================
🗃️ DATABASE INTEGRATION REMINDERS:
🧠 Swarm Brain: from swarm_brain import Retriever; r = Retriever(); r.search("query", k=5)
🔧 Unified DB: import sqlite3; conn = sqlite3.connect("unified.db")
🧠 Vector DB: from src.services.vector_database import VectorDatabaseIntegration
🤖 ML Model: Automated SSOT violation prevention via PredictiveSSOTEngine
============================================================
🔄 DYNAMIC TOOL DISCOVERY:
📁 Scan Tools: python tools/scan_tools.py
🔍 Find Tools: python tools/find_tool.py --query "need"
📊 Project Analysis: python tools/run_project_scan.py
🎯 Captain Tools: python tools/captain_cli.py
📈 Analysis Tools: python tools/analysis_cli.py
============================================================
🚀 MESSAGING & COORDINATION:
📨 Messaging Service: src/services/messaging_service.py
🤖 Discord Bot: python run_discord_messaging.py
📋 Captain Directives: tools/captain_directive_manager.py
🔄 Workflow Manager: tools/agent_workflow_manager.py
============================================================
💡 REMEMBER: Query databases every cycle phase for patterns, tasks, and knowledge!"""

    @staticmethod
    def get_compact_guidelines() -> str:
        """Get compact tool reminders for space-limited communications."""
        return """🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
🗃️ DATABASES: Swarm Brain (r.search), Unified (sqlite3), Vector (VectorDatabaseIntegration)
🔄 TOOLS: Scan (scan_tools.py), Find (find_tool.py), Project (run_project_scan.py)
🚀 MESSAGING: messaging_service.py, Discord (run_discord_messaging.py)
💡 REMEMBER: Query databases every cycle phase for patterns and knowledge!"""


class MessageValidator:
    """Validate message content before sending."""

    def __init__(self, enhanced_validator=None):
        """Initialize message validator."""
        self.enhanced_validator = enhanced_validator

    def validate_before_paste(self, text: str) -> tuple[bool, str]:
        """Validate message content before pasting with enhanced validation."""
        try:
            # Use enhanced validator if available
            if self.enhanced_validator:
                validation_result = self.enhanced_validator.validate_and_prepare_for_paste(text)
                if validation_result["ready_for_paste"]:
                    return True, "Enhanced validation passed"
                else:
                    recommendations = validation_result.get("recommendations", [])
                    return False, f"Enhanced validation failed: {'; '.join(recommendations)}"

            # Fallback to basic validation
            if "[A2A] MESSAGE" not in text:
                return False, "Message missing A2A format"

            if "📤 FROM:" not in text:
                return False, "Message missing FROM field"

            if "📥 TO:" not in text:
                return False, "Message missing TO field"

            if len(text) > 10000:
                return False, "Message too long for clipboard"

            problematic_chars = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05"]
            for char in problematic_chars:
                if char in text:
                    return False, f"Message contains problematic character: {repr(char)}"

            logger.info("✅ Basic message validation passed")
            return True, "Basic message validation successful"

        except Exception as e:
            logger.error(f"Message validation failed: {e}")
            return False, f"Validation error: {e}"


class MessageSender:
    """Send messages via PyAutoGUI with validation."""

    def __init__(self, enhanced_handler=None, enhanced_validator=None):
        """Initialize message sender."""
        self.enhanced_handler = enhanced_handler
        self.validator = MessageValidator(enhanced_validator)

    def paste_to_coords(self, coords: tuple[int, int], text: str) -> bool:
        """Paste text to coordinates and press Enter to send using PyAutoGUI with validation."""
        if not pyautogui or not pyperclip:
            logger.error("PyAutoGUI or pyperclip not available")
            return False

        # Use enhanced handler if available
        if self.enhanced_handler:
            try:
                success = self.enhanced_handler.send_message_to_agent_with_validation(
                    list(coords), text, use_paste=True, create_new_tab=False
                )
                if success:
                    logger.info("✅ Message sent successfully via enhanced handler")
                    return True
                else:
                    logger.warning("⚠️ Enhanced handler failed, falling back to basic method")
            except Exception as e:
                logger.warning(f"⚠️ Enhanced handler error: {e}, falling back to basic method")

        # Fallback to basic validation and paste
        is_valid, validation_msg = self.validator.validate_before_paste(text)
        if not is_valid:
            logger.error(f"❌ Message validation failed: {validation_msg}")
            logger.error(f"Message content preview: {text[:200]}...")
            return False

        logger.info(f"✅ Message validation passed: {validation_msg}")

        try:
            # Save current clipboard
            original_clipboard = pyperclip.paste()

            # Set new clipboard content
            pyperclip.copy(text)

            # Click at coordinates to focus
            pyautogui.click(coords[0], coords[1])
            time.sleep(0.3)

            # Ensure we have focus by clicking again
            pyautogui.click(coords[0], coords[1])

            # Paste
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)

            # Press Enter to send the message
            pyautogui.press("enter")
            time.sleep(0.1)

            # Only restore clipboard if not problematic
            if (
                len(original_clipboard) < 1000
                and not any(
                    lang in original_clipboard.lower()
                    for lang in ["soy ", "cuando ", "primero", "segundo", "tercero"]
                )
                and not original_clipboard.startswith("Soy Claudia")
            ):
                pyperclip.copy(original_clipboard)
            else:
                pyperclip.copy("")

            logger.info("✅ Message pasted and sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to paste and send to coordinates: {e}")
            return False


# Import canonical AgentHardOnboarder as AgentOnboarder for backward compatibility
from src.services.agent_hard_onboarding import AgentHardOnboarder as AgentOnboarder


def create_message_formatter() -> MessageFormatter:
    """Factory function to create message formatter."""
    return MessageFormatter()


def create_message_validator(enhanced_validator=None) -> MessageValidator:
    """Factory function to create message validator."""
    return MessageValidator(enhanced_validator)


def create_message_sender(enhanced_handler=None, enhanced_validator=None) -> MessageSender:
    """Factory function to create message sender."""
    return MessageSender(enhanced_handler, enhanced_validator)


def create_agent_onboarder(coord_path: str = "config/coordinates.json") -> AgentOnboarder:
    """Factory function to create agent onboarder."""
    return AgentOnboarder(coord_path)
