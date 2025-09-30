#!/usr/bin/env python3
"""
Consolidated Messaging Service - Utils
=====================================

Utility functions for message formatting, validation, and sending.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import logging
import time
from typing import Tuple

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
    def format_a2a_message(from_agent: str, to_agent: str, content: str, priority: str) -> str:
        """Format A2A message with proper headers."""
        priority_indicator = "🚨 " if priority.upper() == "URGENT" else ""

        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority.upper()}
Tags: GENERAL
-------------------------------------------------------------
{content}
{MessageFormatter.get_quality_guidelines()}
============================================================
-------------------------------------------------------------"""

    @staticmethod
    def get_quality_guidelines() -> str:
        """Get concise quality guidelines reminder for all agent communications."""
        return """🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'"""


class MessageValidator:
    """Validate message content before sending."""

    def __init__(self, enhanced_validator=None):
        """Initialize message validator."""
        self.enhanced_validator = enhanced_validator

    def validate_before_paste(self, text: str) -> Tuple[bool, str]:
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


class AgentOnboarder:
    """Handle agent onboarding operations."""

    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize agent onboarder."""
        self.coord_path = coord_path

    def get_agent_default_role(self, agent_id: str) -> str:
        """Get agent's default role from capabilities."""
        try:
            with open("config/agent_capabilities.json") as f:
                capabilities = json.load(f)

            if agent_id in capabilities["agents"]:
                default_roles = capabilities["agents"][agent_id]["default_roles"]
                return default_roles[0] if default_roles else "TASK_EXECUTOR"
            return "TASK_EXECUTOR"
        except:
            return "TASK_EXECUTOR"

    def create_onboarding_message(self, agent_id: str, default_role: str) -> str:
        """Create comprehensive onboarding message with role assignment and tool discovery."""
        return f"""🔔 HARD ONBOARD SEQUENCE INITIATED
============================================================
🤖 AGENT: {agent_id}
🎭 DEFAULT ROLE: {default_role}
📋 STATUS: ACTIVATING
============================================================

📖 IMMEDIATE ACTIONS REQUIRED:
1. Review AGENTS.md for complete system overview
2. Understand your role: {default_role}
3. Initialize agent workspace and inbox
4. Load role-specific protocols from config/protocols/
5. Discover and integrate available tools
6. Begin autonomous workflow cycle

🎯 COORDINATION PROTOCOL:
- Monitor inbox for role assignments from Captain Agent-4
- Execute General Cycle: CHECK_INBOX → EVALUATE_TASKS → EXECUTE_ROLE → QUALITY_GATES → CYCLE_DONE
- Maintain V2 compliance standards (≤400 lines, proper structure)
- Use PyAutoGUI messaging for agent coordination

📊 AVAILABLE ROLES (25 total):
Core: CAPTAIN, SSOT_MANAGER, COORDINATOR
Technical: INTEGRATION_SPECIALIST, ARCHITECTURE_SPECIALIST, INFRASTRUCTURE_SPECIALIST, WEB_DEVELOPER, DATA_ANALYST, QUALITY_ASSURANCE, PERFORMANCE_DETECTIVE, SECURITY_INSPECTOR, INTEGRATION_EXPLORER, FINANCIAL_ANALYST, TRADING_STRATEGIST, RISK_MANAGER, PORTFOLIO_OPTIMIZER, COMPLIANCE_AUDITOR
Operational: TASK_EXECUTOR, RESEARCHER, TROUBLESHOOTER, OPTIMIZER, DEVLOG_STORYTELLER, CODE_ARCHAEOLOGIST, DOCUMENTATION_ARCHITECT, MARKET_RESEARCHER

🛠️ TOOL DISCOVERY PROTOCOL:
1. Core Communication: src/services/consolidated_messaging_service.py
2. Captain Tools: tools/captain_cli.py, tools/captain_directive_manager.py
3. Analysis Tools: tools/analysis_cli.py, tools/overengineering_detector.py
4. Workflow Tools: tools/agent_workflow_manager.py, tools/simple_workflow_automation.py
5. Static Analysis: tools/static_analysis/ (code_quality_analyzer.py, dependency_scanner.py, security_scanner.py)
6. Protocol Tools: tools/protocol_compliance_checker.py, tools/protocol_governance_system.py
7. DevOps Tools: scripts/deployment_dashboard.py, tools/performance_detective_cli.py
8. Specialized Tools: tools/financial_analyst_cli.py, tools/trading_strategist_cli.py, tools/risk_manager_cli.py
9. THEA Integration: src/services/thea/ (strategic_consultation_cli.py, thea_autonomous_system.py)
10. Alerting Tools: tools/intelligent_alerting_cli.py, tools/predictive_analytics_cli.py

🔧 TOOL INTEGRATION IN GENERAL CYCLE:
- PHASE 1 (CHECK_INBOX): Use messaging tools, check tool status
- PHASE 2 (EVALUATE_TASKS): Use analysis tools, workflow tools
- PHASE 3 (EXECUTE_ROLE): Use role-specific tools, specialized tools
- PHASE 4 (QUALITY_GATES): Use quality tools, static analysis tools
- PHASE 5 (CYCLE_DONE): Use reporting tools, update tool status

📚 REQUIRED READING FOR TOOL DISCOVERY:
- AGENTS.md (complete tool integration in General Cycle)
- tools/ directory (all available CLI tools)
- src/services/ directory (all available services)
- config/protocols/ (role-specific tool protocols)

🚀 BEGIN ONBOARDING PROTOCOLS
============================================================
🐝 WE ARE SWARM - {agent_id} Activation Complete"""


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
