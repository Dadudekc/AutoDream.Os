#!/usr/bin/env python3
"""
Onboarding Coordinator - Agent Initialization and Workspace Setup
================================================================

Onboarding coordinator for agent initialization and workspace setup.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
import time
from pathlib import Path

from .contract_system import AgentContract, ContractType
from .fsm_system import AgentFSM, AgentState

logger = logging.getLogger(__name__)

# PyAutoGUI imports
try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
    pyautogui.PAUSE = 0.05
    pyautogui.FAILSAFE = True
except ImportError as e:
    PYAUTOGUI_AVAILABLE = False
    logger.error(f"❌ PyAutoGUI not available: {e}")


class OnboardingCoordinator:
    """Onboarding coordinator for agent initialization and workspace setup."""

    def __init__(self, coordinates_file: str = "cursor_agent_coords.json"):
        """Initialize the onboarding coordinator."""
        self.coordinates_file = Path(coordinates_file)
        self.agent_coordinates = self.load_coordinates()
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Strategic Oversight & Emergency Intervention Manager",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist",
        }
        self.onboarding_status: dict[str, bool] = {}
        self.active_contracts: dict[str, AgentContract] = {}
        self.contract_history: list[AgentContract] = []
        self.agent_fsms: dict[str, AgentFSM] = {}

        # Initialize FSM for all agents
        for agent_id in self.agent_roles.keys():
            self.agent_fsms[agent_id] = AgentFSM(agent_id)

    def load_coordinates(self) -> dict:
        """Load agent coordinates from file."""
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file) as f:
                    return json.load(f)
            else:
                logger.warning(f"⚠️ Coordinates file not found: {self.coordinates_file}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error loading coordinates: {e}")
            return {}

    def get_chat_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get chat input coordinates for a specific agent."""
        if agent_id not in self.agent_coordinates:
            logger.error(f"❌ No coordinates found for {agent_id}")
            return None

        coords = self.agent_coordinates[agent_id].get("chat_input_coordinates")
        if not coords or len(coords) != 2:
            logger.error(f"❌ Invalid coordinates for {agent_id}: {coords}")
            return None

        return tuple(coords)

    def get_onboarding_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get onboarding input coordinates for a specific agent."""
        # DEDUPLICATION: Consolidated function - using unified implementation
        from src.core.unified_onboarding_coordinates import get_onboarding_coordinates

        return get_onboarding_coordinates(agent_id)

    def create_onboarding_contract(self, agent_id: str) -> AgentContract:
        """Create an onboarding contract for an agent."""
        # DEDUPLICATION: Consolidated function - using shared implementation
        from src.services.onboarding.onboarding_service import OnboardingService

        service = OnboardingService()
        contract = service.create_onboarding_contract(agent_id)
        self.active_contracts[agent_id] = contract
        return contract

    def create_contract(
        self,
        agent_id: str,
        contract_type: ContractType,
        description: str,
        estimated_cycles: int,
        dependencies: list[str] = None,
    ):
        """Create a new contract for an agent."""
        contract = AgentContract(
            agent_id, contract_type, description, estimated_cycles, dependencies
        )
        self.active_contracts[agent_id] = contract
        self.contract_history.append(contract)
        logger.info(f"📋 Contract created for {agent_id}: {contract_type.value} - {description}")
        return contract

    def perform_agent_onboarding(self, agent_id: str, role: str) -> bool:
        """Perform onboarding sequence for a specific agent."""
        if not PYAUTOGUI_AVAILABLE:
            logger.error("❌ PyAutoGUI not available for onboarding")
            return False

        # Get coordinates
        chat_coords = self.get_chat_coordinates(agent_id)
        onboarding_coords = self.get_onboarding_coordinates(agent_id)

        if not chat_coords or not onboarding_coords:
            logger.error(f"❌ Missing coordinates for {agent_id}")
            return False

        try:
            # Create onboarding contract
            self.create_onboarding_contract(agent_id)
            fsm = self.agent_fsms[agent_id]
            fsm.transition_to(AgentState.ONBOARDING)

            logger.info(f"🎯 Starting onboarding for {agent_id} ({role})")

            # Execute onboarding sequence
            success = self._execute_onboarding_sequence(agent_id, chat_coords, onboarding_coords)

            if success:
                self.onboarding_status[agent_id] = True
                fsm.transition_to(AgentState.IDLE)
                logger.info(f"✅ Onboarding completed for {agent_id}")
            else:
                fsm.transition_to(AgentState.ERROR_RECOVERY)
                logger.error(f"❌ Onboarding failed for {agent_id}")

            return success

        except Exception as e:
            logger.error(f"❌ Onboarding failed for {agent_id}: {e}")
            fsm = self.agent_fsms[agent_id]
            fsm.transition_to(AgentState.ERROR_RECOVERY)
            return False

    def _execute_onboarding_sequence(
        self, agent_id: str, chat_coords: tuple[int, int], onboarding_coords: tuple[int, int]
    ) -> bool:
        """Execute the onboarding sequence steps."""
        try:
            # Step 1: Click chat input coordinates
            pyautogui.moveTo(chat_coords[0], chat_coords[1], duration=0.4)
            pyautogui.click()
            time.sleep(0.1)

            # Step 2: Press Ctrl+N (new chat)
            pyautogui.hotkey("ctrl", "n")
            time.sleep(0.2)

            # Step 3: Click onboarding input coordinates
            pyautogui.moveTo(onboarding_coords[0], onboarding_coords[1], duration=0.4)
            pyautogui.click()
            time.sleep(0.1)

            # Step 4: Create and send onboarding message
            onboarding_message = self.create_onboarding_message(
                agent_id, self.agent_roles.get(agent_id, "Swarm Agent")
            )
            pyperclip.copy(onboarding_message)
            time.sleep(0.05)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.1)

            # Step 5: Press Enter to send
            pyautogui.press("enter")
            time.sleep(0.2)

            return True

        except Exception as e:
            logger.error(f"❌ Onboarding sequence failed: {e}")
            return False

    def create_onboarding_message(self, agent_id: str, role: str) -> str:
        """Create onboarding message for agent."""
        return f"""🚀 AGENT ONBOARDING - {agent_id.upper()}
Role: {role}

Priority: HIGH
Tags: ONBOARDING, INITIALIZATION

🎯 ONBOARDING DIRECTIVE FOR {agent_id.upper()}:

Welcome to the enhanced swarm coordination system! You are being onboarded as {role}.

📋 ONBOARDING REQUIREMENTS:
1. ✅ Confirm your agent identity and role
2. ✅ Initialize your workspace and status tracking
3. ✅ Complete SSOT compliance training
4. ✅ Establish communication with Captain Agent-4
5. ✅ Claim your first contract assignment

🛠️ IMMEDIATE ONBOARDING ACTIONS:
• Check workspace: agent_workspaces/{agent_id}/
• Update status: agent_workspaces/{agent_id}/status.json
• Message Captain: python src/services/consolidated_messaging_service.py --agent Agent-4 --message "Onboarding: {agent_id} ready for assignment"
• Get first task: python src/services/consolidated_messaging_service.py --agent {agent_id} --get-next-task

🐝 WE ARE SWARM - Enhanced onboarding with contracts and FSM active!

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory

You are {agent_id}
Timestamp: {time.strftime("%Y-%m-%d %H:%M:%S")}"""

    def get_onboarding_status(self, agent_id: str) -> bool:
        """Get onboarding status for an agent."""
        return self.onboarding_status.get(agent_id, False)

    def get_agent_fsm(self, agent_id: str) -> AgentFSM | None:
        """Get FSM for an agent."""
        return self.agent_fsms.get(agent_id)

    def get_active_contract(self, agent_id: str) -> AgentContract | None:
        """Get active contract for an agent."""
        return self.active_contracts.get(agent_id)

