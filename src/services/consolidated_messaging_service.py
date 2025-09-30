#!/usr/bin/env python3
"""
Consolidated Messaging Service - SSOT for All Messaging
=======================================================

Single Source of Truth messaging service that consolidates all messaging functionality.
Handles core messaging, status monitoring, onboarding, and enhanced features.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.append(str(project_root))


# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

# Import enhanced validation components
try:
    from src.services.messaging.enhanced_message_validator import EnhancedMessageValidator
    from src.services.messaging.enhanced_pyautogui_handler import EnhancedPyAutoGUIHandler
    ENHANCED_VALIDATION_AVAILABLE = True
except Exception as e:
    EnhancedMessageValidator = None
    EnhancedPyAutoGUIHandler = None
    ENHANCED_VALIDATION_AVAILABLE = False
    logging.warning(f"Enhanced validation import failed: {e}")

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService:
    """Consolidated messaging service - SSOT for all messaging."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize consolidated messaging service - SSOT for all messaging."""
        self.coord_path = coord_path
        self.agent_data = self._load_coordinates()

        # Add enhanced functionality
        self.auto_devlog_enabled = True
        self.response_protocol_enabled = True
        self.coordination_requests = {}  # Track coordination requests

    def _load_coordinates(self) -> dict:
        """Load agent coordinates from JSON file."""
        try:
            with open(self.coord_path) as f:
                data = json.load(f)
            return data.get("agents", {})
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}

    def track_coordination_request(self, from_agent: str, to_agent: str, message: str) -> None:
        """Track coordination requests for protocol compliance."""
        request_id = f"{from_agent}_{to_agent}_{int(time.time())}"
        self.coordination_requests[request_id] = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "message": message,
            "timestamp": time.time(),
            "acknowledged": False,
            "responded": False,
            "completed": False,
        }
        logger.info(f"Coordination request tracked: {request_id}")

    def check_response_protocol(self) -> dict[str, list[str]]:
        """Check for protocol violations."""
        violations = {"overdue": [], "unacknowledged": [], "incomplete": []}
        current_time = time.time()

        for request_id, request in self.coordination_requests.items():
            # Check for overdue responses (>2 agent cycles = ~10 minutes)
            if current_time - request["timestamp"] > 600 and not request["acknowledged"]:
                violations["overdue"].append(request_id)

            # Check for unacknowledged requests (>1 agent cycle = ~5 minutes)
            if current_time - request["timestamp"] > 300 and not request["acknowledged"]:
                violations["unacknowledged"].append(request_id)

            # Check for incomplete responses (>1 hour without completion)
            if current_time - request["timestamp"] > 3600 and not request["completed"]:
                violations["incomplete"].append(request_id)

        return violations

    def send_message(
        self, agent_id: str, message: str, from_agent: str = None, priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent via PyAutoGUI automation."""
        if from_agent is None:
            logger.error("from_agent is required - agents must specify their own ID")
            return False

        if not self._is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} is inactive, message not sent")
            return False

        # Track coordination requests for protocol compliance
        if "coordinate" in message.lower() or "coordination" in message.lower():
            self.track_coordination_request(from_agent, agent_id, message)

        try:
            # Get agent coordinates
            if agent_id not in self.agent_data:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            coords = self.agent_data[agent_id]["chat_input_coordinates"]
            if not isinstance(coords, list) or len(coords) < 2:
                logger.error(f"Invalid coordinates for agent {agent_id}: {coords}")
                return False

            # Format A2A message
            formatted_message = self._format_a2a_message(from_agent, agent_id, message, priority)

            # Send via PyAutoGUI
            success = self._paste_to_coords(coords, formatted_message)

            # Auto-create devlog if enabled with improved messaging
            if success and self.auto_devlog_enabled:
                try:
                    # Import the agent devlog posting service (local file storage only)
                    import asyncio

                    from .agent_devlog_posting import AgentDevlogPoster

                    # Create devlog poster
                    poster = AgentDevlogPoster()

                    # Post devlog asynchronously to local storage
                    asyncio.create_task(
                        poster.post_devlog(
                            agent_flag=from_agent,
                            action=f"Message sent to {agent_id}",
                            status="completed",
                            details=f"Message from {from_agent}: {message[:200]}...",
                        )
                    )

                    logger.info(f"✅ Auto devlog created in local storage for {agent_id}")

                except Exception as e:
                    logger.warning(f"Failed to create auto devlog: {e}")

            if success:
                logger.info(f"Message sent to {agent_id} from {from_agent}")
            else:
                logger.error(f"Failed to send message to {agent_id}")

            return success

        except Exception as e:
            logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    def broadcast_message(
        self, message: str, from_agent: str = None, priority: str = "NORMAL"
    ) -> dict[str, bool]:
        """Send message to all active agents."""
        if from_agent is None:
            logger.error("from_agent is required - agents must specify their own ID")
            return {}

        results = {}

        for agent_id in self.agent_data.keys():
            if self._is_agent_active(agent_id):
                results[agent_id] = self.send_message(agent_id, message, from_agent, priority)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")

        return results

    def _is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        return agent_id in self.agent_data and self.agent_data[agent_id].get("active", True)

    def _format_a2a_message(
        self, from_agent: str, to_agent: str, content: str, priority: str
    ) -> str:
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
{self._get_quality_guidelines()}
============================================================
-------------------------------------------------------------"""

    def _get_quality_guidelines(self) -> str:
        """Get concise quality guidelines reminder for all agent communications."""
        return """🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'"""

    def _validate_message_before_paste(self, text: str) -> tuple[bool, str]:
        """Validate message content before pasting."""
        try:
            # Check if message contains required A2A format
            if "[A2A] MESSAGE" not in text:
                return False, "Message missing A2A format"

            # Check if message contains FROM field
            if "📤 FROM:" not in text:
                return False, "Message missing FROM field"

            # Check if message contains TO field
            if "📥 TO:" not in text:
                return False, "Message missing TO field"

            # Check message length (not too long for clipboard)
            if len(text) > 10000:
                return False, "Message too long for clipboard"

            # Check for problematic characters that might break pasting
            problematic_chars = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05"]
            for char in problematic_chars:
                if char in text:
                    return False, f"Message contains problematic character: {repr(char)}"

            logger.info("✅ Message validation passed")
            return True, "Message validation successful"

        except Exception as e:
            logger.error(f"Message validation failed: {e}")
            return False, f"Validation error: {e}"

    def _paste_to_coords(self, coords: tuple[int, int], text: str) -> bool:
        """Paste text to coordinates and press Enter to send using PyAutoGUI with validation."""
        if not pyautogui or not pyperclip:
            logger.error("PyAutoGUI or pyperclip not available")
            return False

        # Validate message before pasting
        is_valid, validation_msg = self._validate_message_before_paste(text)
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

            # Longer delay to ensure focus
            time.sleep(0.3)

            # Ensure we have focus by clicking again
            pyautogui.click(coords[0], coords[1])

            # Paste
            pyautogui.hotkey("ctrl", "v")

            # Wait for paste to complete
            time.sleep(0.2)

            # Small delay after paste
            time.sleep(0.2)

            # Press Enter to send the message
            pyautogui.press("enter")

            # Small delay after sending
            time.sleep(0.1)

            # Only restore original clipboard if it's not problematic content
            # Skip restoration if original clipboard contains foreign language or spam content
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
                # Clear clipboard to prevent spam content restoration
                pyperclip.copy("")

            logger.info("✅ Message pasted and sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to paste and send to coordinates: {e}")
            return False

    def stall_agent(self, agent_id: str, reason: str = None) -> bool:
        """
        Stall an agent by sending Ctrl+Shift+Backspace to their chat input.

        QUEUE BEHAVIOR:
        - Stops agent's current operations immediately
        - Any cued messages remain in the queue (not lost)
        - New messages sent to stalled agent go to top of queue
        - Agent will process queued messages when unstalled

        To resume: Use unstall_agent() which sends Ctrl+Enter to deliver
        the next pending message in the cue.

        Args:
            agent_id: The agent to stall
            reason: Optional reason for stalling (for logging)

        Returns:
            bool: True if stall command was sent successfully
        """
        try:
            import json
            import time

            import pyautogui

            # Load coordinates
            with open(self.coord_path) as f:
                coords_data = json.load(f)

            if agent_id not in coords_data["agents"]:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            agent_coords = coords_data["agents"][agent_id]["chat_input_coordinates"]
            x, y = agent_coords[0], agent_coords[1]

            # Execute stall command
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.hotkey("ctrl", "shift", "backspace")
            time.sleep(0.5)

            logger.info(f"Stall command executed for {agent_id} at ({x}, {y})")
            return True

        except Exception as e:
            logger.error(f"Error stalling agent {agent_id}: {e}")
            return False

    def unstall_agent(self, agent_id: str, message: str = None) -> bool:
        """
        Unstall an agent by sending Ctrl+Enter with optional message.

        MESSAGE QUEUE BEHAVIOR:
        - Ctrl+Shift+Backspace (stall): Stops agent, any cued messages remain in queue
        - Ctrl+Enter (unstall): Sends next pending message in cue to agent
        - If message provided: Sends that message immediately to stalled agent
        - New messages sent to stalled agent go to top of queue (next to be processed)

        USAGE SCENARIOS:
        1. Unstall with message: "You were stuck, review why and report to captain so we can address this blocker later"
           Then press Ctrl+Enter to send immediately to stalled agent
        2. Unstall without message: Just send next queued message to agent

        WARNING: Ctrl+Enter may cause task abandonment if agent was stuck on previous work.

        Args:
            agent_id: The agent to unstall
            message: Optional message to send immediately to stalled agent

        Returns:
            bool: True if unstall command was sent successfully

        Warning:
            Use with caution - may cause task abandonment if agent was stuck on work.
        """
        try:
            import json
            import time

            import pyautogui

            # Load coordinates
            with open(self.coord_path) as f:
                coords_data = json.load(f)

            if agent_id not in coords_data["agents"]:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            agent_coords = coords_data["agents"][agent_id]["chat_input_coordinates"]
            x, y = agent_coords[0], agent_coords[1]

            # Execute unstall command
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)

            if message:
                # Send immediate message to stalled agent (goes to top of queue)
                pyautogui.write(message)
                time.sleep(0.2)

            # WARNING: Ctrl+Enter sends next pending message in cue to agent
            # If message was provided above, it sends that message immediately
            # If no message, sends the next queued message
            # This may cause task abandonment if agent was stuck on previous work
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.5)

            logger.info(f"Unstall command executed for {agent_id} at ({x}, {y})")
            return True

        except Exception as e:
            logger.error(f"Error unstalling agent {agent_id}: {e}")
            return False

    def hard_onboard_agent(self, agent_id: str) -> bool:
        """Comprehensive 7-step hard onboarding sequence for a single agent."""
        try:
            import json
            import time

            import pyautogui
            import pyperclip

            # Load coordinates
            with open(self.coord_path) as f:
                coords_data = json.load(f)

            if agent_id not in coords_data["agents"]:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            agent_data = coords_data["agents"][agent_id]
            chat_coords = agent_data["chat_input_coordinates"]
            onboard_coords = agent_data["onboarding_coordinates"]

            # Get agent's default role from capabilities
            default_role = self._get_agent_default_role(agent_id)

            # Create comprehensive onboarding message
            onboarding_message = self._create_onboarding_message(agent_id, default_role)

            logger.info(f"Starting 7-step onboarding sequence for {agent_id}")

            # Step 1: Click chat input coordinates to get attention
            logger.info(f"Step 1: Focusing chat input at {chat_coords}")
            pyautogui.moveTo(chat_coords[0], chat_coords[1], duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.3)

            # Step 2: Press Ctrl+Enter+Backspace to stop running agents
            logger.info("Step 2: Stopping running agents")
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.2)
            pyautogui.press("backspace")
            time.sleep(0.3)

            # Step 3: Press Ctrl+Enter to save all changes
            logger.info("Step 3: Saving all changes")
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.3)

            # Step 4: Press Ctrl+N to open new chat
            logger.info("Step 4: Opening new chat")
            pyautogui.hotkey("ctrl", "n")
            time.sleep(0.5)

            # Step 5: Navigate to onboarding coordinates
            logger.info(f"Step 5: Navigating to onboarding coordinates {onboard_coords}")
            pyautogui.moveTo(onboard_coords[0], onboard_coords[1], duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.3)

            # Step 6: Paste onboarding message
            logger.info("Step 6: Pasting onboarding message")
            pyperclip.copy(onboarding_message)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)

            # Step 7: Press Enter to send onboarding message
            logger.info("Step 7: Sending onboarding message")
            pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ 7-step onboarding sequence completed for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"Error in hard onboarding sequence for {agent_id}: {e}")
            return False

    def hard_onboard_all_agents(self) -> dict:
        """Hard onboard all active agents."""
        results = {}
        active_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        for agent_id in active_agents:
            logger.info(f"Starting hard onboarding for {agent_id}")
            results[agent_id] = self.hard_onboard_agent(agent_id)
            time.sleep(1)  # Small delay between agents

        return results

    def _get_agent_default_role(self, agent_id: str) -> str:
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

    def _create_onboarding_message(self, agent_id: str, default_role: str) -> str:
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


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Consolidated Messaging Service V2 - Modular Architecture"
    )

    parser.add_argument(
        "--coords", default="config/coordinates.json", help="Path to coordinates configuration file"
    )

    subparsers = parser.add_subparsers(dest="cmd", help="Available commands")

    # Send message command
    send_parser = subparsers.add_parser("send", help="Send message to specific agent")
    send_parser.add_argument("--agent", required=True, help="Target agent ID")
    send_parser.add_argument("--message", required=True, help="Message to send")
    send_parser.add_argument("--from-agent", required=True, help="Source agent ID (REQUIRED)")
    send_parser.add_argument("--priority", default="NORMAL", help="Message priority")

    # Broadcast message command
    broadcast_parser = subparsers.add_parser("broadcast", help="Send message to all agents")
    broadcast_parser.add_argument("--message", required=True, help="Message to broadcast")
    broadcast_parser.add_argument("--from-agent", required=True, help="Source agent ID (REQUIRED)")
    broadcast_parser.add_argument("--priority", default="NORMAL", help="Message priority")

    # Status command
    subparsers.add_parser("status", help="Get system status")

    # Protocol check command
    subparsers.add_parser("protocol-check", help="Check response protocol compliance")

    # Hard onboard command
    onboard_parser = subparsers.add_parser("hard-onboard", help="Hard onboard agents")
    onboard_group = onboard_parser.add_mutually_exclusive_group(required=True)
    onboard_group.add_argument("--agent", help="Specific agent to onboard")
    onboard_group.add_argument("--all-agents", action="store_true", help="Onboard all agents")

    # Stall command
    stall_parser = subparsers.add_parser("stall", help="Stall an agent")
    stall_parser.add_argument("--agent", required=True, help="Agent to stall")
    stall_parser.add_argument("--reason", help="Reason for stalling")

    # Unstall command
    unstall_parser = subparsers.add_parser("unstall", help="Unstall an agent")
    unstall_parser.add_argument("--agent", required=True, help="Agent to unstall")
    unstall_parser.add_argument("--message", help="Message to send with unstall")

    # Cue command
    cue_parser = subparsers.add_parser("cue", help="Send cued message to multiple agents")
    cue_parser.add_argument(
        "--agents", required=True, nargs="+", help="Target agent IDs (space-separated)"
    )
    cue_parser.add_argument("--message", required=True, help="Message to send")
    cue_parser.add_argument(
        "--cue", required=True, help="Queue/cue identifier for agents to respond to"
    )
    cue_parser.add_argument("--from-agent", default="Agent-5", help="Source agent ID")
    cue_parser.add_argument("--priority", default="HIGH", help="Message priority")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.cmd:
        parser.print_help()
        print("\n🐝 WE ARE SWARM - Messaging Service Help Complete")
        return 1

    try:
        # Initialize services
        messaging_service = ConsolidatedMessagingService(args.coords)

        # Handle commands
        if args.cmd == "send":
            success = messaging_service.send_message(args.agent, args.message, args.from_agent)
            print(f"WE ARE SWARM - Message {'sent' if success else 'failed'} to {args.agent}")
            return 0 if success else 1

        elif args.cmd == "broadcast":
            results = messaging_service.broadcast_message(args.message, args.from_agent)
            success_count = sum(1 for success in results.values() if success)
            print(f"WE ARE SWARM - Broadcast complete: {success_count}/{len(results)} agents")
            return 0 if success_count == len(results) else 1

        elif args.cmd == "status":
            # Get basic service status
            status = {
                "service_status": "Active",
                "agents_configured": len(messaging_service.agent_data),
                "active_agents": sum(
                    1
                    for agent_id in messaging_service.agent_data.keys()
                    if messaging_service._is_agent_active(agent_id)
                ),
                "coordination_requests": len(messaging_service.coordination_requests),
                "auto_devlog_enabled": messaging_service.auto_devlog_enabled,
                "response_protocol_enabled": messaging_service.response_protocol_enabled,
            }
            logging.info(f"Service Status: {status}")
            print("WE ARE SWARM - Status check complete")
            print(f"📊 Service Status: {status}")
            return 0

        elif args.cmd == "hard-onboard":
            # Comprehensive 7-step onboarding sequence
            if args.agent:
                success = messaging_service.hard_onboard_agent(args.agent)
                print(
                    f"WE ARE SWARM - Hard onboard {'successful' if success else 'failed'} for {args.agent}"
                )
                return 0 if success else 1
            elif args.all_agents:
                results = messaging_service.hard_onboard_all_agents()
                successful = sum(1 for success in results.values() if success)
                print(f"WE ARE SWARM - Hard onboard complete: {successful}/{len(results)} agents")
                return 0 if successful == len(results) else 1
            else:
                logging.error("Error: Must specify either --agent or --all-agents")
                print("WE ARE SWARM - Hard onboard error")
                return 1

        elif args.cmd == "stall":
            # Create consolidated service for stall functionality
            consolidated_service = ConsolidatedMessagingService(args.coords)
            success = consolidated_service.stall_agent(args.agent, args.reason)
            print(f"WE ARE SWARM - Agent {args.agent} {'stalled' if success else 'stall failed'}")
            return 0 if success else 1

        elif args.cmd == "unstall":
            # Create consolidated service for unstall functionality
            consolidated_service = ConsolidatedMessagingService(args.coords)
            success = consolidated_service.unstall_agent(args.agent, args.message)
            print(
                f"WE ARE SWARM - Agent {args.agent} {'unstalled' if success else 'unstall failed'}"
            )
            return 0 if success else 1

        elif args.cmd == "protocol-check":
            # Check response protocol compliance
            violations = messaging_service.check_response_protocol()
            print("🚨 PROTOCOL COMPLIANCE CHECK")
            print("=" * 50)

            if violations["overdue"]:
                print(f"❌ OVERDUE RESPONSES: {len(violations['overdue'])}")
                for req_id in violations["overdue"]:
                    print(f"   - {req_id}")

            if violations["unacknowledged"]:
                print(f"⚠️ UNACKNOWLEDGED: {len(violations['unacknowledged'])}")
                for req_id in violations["unacknowledged"]:
                    print(f"   - {req_id}")

            if violations["incomplete"]:
                print(f"🔄 INCOMPLETE: {len(violations['incomplete'])}")
                for req_id in violations["incomplete"]:
                    print(f"   - {req_id}")

            if not any(violations.values()):
                print("✅ ALL PROTOCOLS COMPLIANT")

            return 0

        elif args.cmd == "cue":
            # Handle cue command - send message to multiple agents with cue
            consolidated_service = ConsolidatedMessagingService(args.coords)

            # Format message with cue information
            cued_message = f"""🔔 CUE: {args.cue}

{args.message}

📋 RESPONSE INSTRUCTIONS:
• Queue: {args.cue}
• Respond via: Agent messaging system
• Priority: {args.priority}
• From: {args.from_agent}

This message sent via PyAutoGUI automation."""

            results = {}
            for agent_id in args.agents:
                if consolidated_service._is_agent_active(agent_id):
                    success = consolidated_service.send_message(
                        agent_id=agent_id,
                        message=cued_message,
                        from_agent=args.from_agent,
                        priority=args.priority,
                    )
                    results[agent_id] = success
                    print(f"  Agent {agent_id}: {'Sent' if success else 'Failed'}")
                else:
                    results[agent_id] = False
                    print(f"  Agent {agent_id}: Inactive")

            success_count = sum(1 for success in results.values() if success)
            print(
                f"WE ARE SWARM - Cue '{args.cue}' complete: {success_count}/{len(results)} agents"
            )
            return 0 if success_count == len(results) else 1

        else:
            parser.print_help()
            print("WE ARE SWARM - Unknown command")
            return 1

    except Exception as e:
        logging.error("Service error: %s", e)
        print(f"WE ARE SWARM - Service error: {e}")
        return 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
