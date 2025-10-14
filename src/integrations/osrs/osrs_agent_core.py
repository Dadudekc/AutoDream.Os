#!/usr/bin/env python3
"""
@file osrs_agent_core.py
@brief Core OSRS Agent - Autonomous Old School RuneScape coordination agent
@author Agent-4 Captain
@date 2025-09-12

V2 COMPLIANT: Refactored to ≤400 lines by extracting:
- Role activities → osrs_agent_activities.py
- Message handling → osrs_agent_messaging.py
"""

import json
import logging
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

import pyautogui

from .osrs_agent_activities import OSRSActivityExecutor
from .osrs_agent_messaging import OSRSMessageHandler


class AgentRole(Enum):
    """OSRS Agent specializations."""

    COMBAT_SPECIALIST = "combat_specialist"
    RESOURCE_MANAGER = "resource_manager"
    QUEST_COORDINATOR = "quest_coordinator"
    STRATEGIC_PLANNER = "strategic_planner"
    TRADING_SPECIALIST = "trading_specialist"
    SKILL_TRAINER = "skill_trainer"
    CLAN_COORDINATOR = "clan_coordinator"
    EMERGENCY_RESPONSE = "emergency_response"


class AgentStatus(Enum):
    """Agent operational status."""

    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    SHUTDOWN = "shutdown"


@dataclass
class OSRSAccount:
    """OSRS account configuration."""

    account_id: str
    username: str
    password: str
    display_name: str
    character_level: int
    skills: dict[str, int]
    location: str
    current_activity: str
    last_activity: datetime


@dataclass
class OSRSGameState:
    """Current OSRS game state."""

    player_health: int
    player_prayer: int
    player_energy: int
    current_location: str
    inventory_items: list[str]
    equipment_items: list[str]
    current_interface: str
    last_update: datetime


class OSRS_Agent_Core:
    """
    @brief Core OSRS Agent - Autonomous Old School RuneScape coordination agent.

    This class represents a single autonomous agent that can play OSRS
    continuously without manual intervention, coordinating with other agents
    in the swarm for maximum efficiency.
    """

    def __init__(self, agent_id: str, role: AgentRole, osrs_account: OSRSAccount):
        """Initialize OSRS agent."""
        self.agent_id = agent_id
        self.role = role
        self.osrs_account = osrs_account
        self.status = AgentStatus.INITIALIZING
        self.is_running = False
        self.current_activity = None
        self.game_state = None

        self.coordination_queue = []
        self.message_queue = []
        self.other_agents = {}

        self.logger = logging.getLogger(f"OSRS_Agent_{agent_id}")
        self.setup_logging()

        self.data_dir = Path(f"data/agent_logs/{agent_id}")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

        self.logger.info(f"OSRS Agent {agent_id} initialized with role {role.value}")

    def setup_logging(self):
        """Setup agent-specific logging."""
        log_file = self.data_dir / f"{self.agent_id}_agent.log"

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def start_autonomous_operation(self):
        """Start continuous autonomous OSRS operation."""
        self.logger.info(f"Starting autonomous operation for agent {self.agent_id}")
        self.is_running = True
        self.status = AgentStatus.ACTIVE

        try:
            while self.is_running:
                self.execute_osrs_cycle()
                time.sleep(1)

        except KeyboardInterrupt:
            self.logger.info(f"Agent {self.agent_id} received shutdown signal")
        except Exception as e:
            self.logger.error(f"Error in autonomous operation: {e}")
            self.status = AgentStatus.ERROR
        finally:
            self.shutdown()

    def execute_osrs_cycle(self):
        """Execute one OSRS gameplay cycle."""
        try:
            self.update_game_state()
            self.process_coordination_messages()
            self.execute_role_activity()
            self.update_status()
            OSRSMessageHandler.communicate_with_swarm(self)

        except Exception as e:
            self.logger.error(f"Error in OSRS cycle: {e}")
            self.status = AgentStatus.ERROR

    def update_game_state(self):
        """Update current OSRS game state."""
        try:
            self.game_state = OSRSGameState(
                player_health=100,
                player_prayer=100,
                player_energy=100,
                current_location="Lumbridge",
                inventory_items=["Bronze sword", "Shield"],
                equipment_items=["Bronze armor"],
                current_interface="game",
                last_update=datetime.now(),
            )

        except Exception as e:
            self.logger.error(f"Error updating game state: {e}")

    def process_coordination_messages(self):
        """Process messages from other agents."""
        try:
            while self.message_queue:
                message = self.message_queue.pop(0)
                OSRSMessageHandler.handle_coordination_message(self, message)

        except Exception as e:
            self.logger.error(f"Error processing coordination messages: {e}")

    def execute_role_activity(self):
        """Execute role-specific OSRS activity."""
        try:
            if self.role == AgentRole.COMBAT_SPECIALIST:
                OSRSActivityExecutor.execute_combat_activity(self)
            elif self.role == AgentRole.RESOURCE_MANAGER:
                OSRSActivityExecutor.execute_resource_activity(self)
            elif self.role == AgentRole.QUEST_COORDINATOR:
                OSRSActivityExecutor.execute_quest_activity(self)
            elif self.role == AgentRole.STRATEGIC_PLANNER:
                OSRSActivityExecutor.execute_strategic_activity(self)
            elif self.role == AgentRole.TRADING_SPECIALIST:
                OSRSActivityExecutor.execute_trading_activity(self)
            elif self.role == AgentRole.SKILL_TRAINER:
                OSRSActivityExecutor.execute_skill_training_activity(self)
            elif self.role == AgentRole.CLAN_COORDINATOR:
                OSRSActivityExecutor.execute_clan_activity(self)
            elif self.role == AgentRole.EMERGENCY_RESPONSE:
                OSRSActivityExecutor.execute_emergency_monitoring(self)

        except Exception as e:
            self.logger.error(f"Error executing role activity: {e}")

    def initiate_emergency_response(self, emergency_type: str, alerting_agent: str):
        """Initiate emergency response (placeholder for emergency response role)."""
        self.logger.warning(f"Emergency response initiated: {emergency_type} from {alerting_agent}")

    def update_status(self):
        """Update agent status and save to persistent storage."""
        try:
            status_data = {
                "agent_id": self.agent_id,
                "role": self.role.value,
                "status": self.status.value,
                "current_activity": self.current_activity,
                "osrs_account": self.osrs_account.__dict__,
                "game_state": self.game_state.__dict__ if self.game_state else None,
                "last_update": datetime.now().isoformat(),
            }

            status_file = self.data_dir / "agent_status.json"
            with open(status_file, "w") as f:
                json.dump(status_data, f, indent=2, default=str)

        except Exception as e:
            self.logger.error(f"Error updating status: {e}")

    def pause_agent(self):
        """Pause agent operation."""
        self.logger.info(f"Pausing agent {self.agent_id}")
        self.status = AgentStatus.PAUSED
        self.is_running = False

    def resume_agent(self):
        """Resume agent operation."""
        self.logger.info(f"Resuming agent {self.agent_id}")
        self.status = AgentStatus.ACTIVE
        self.is_running = True
        threading.Thread(target=self.start_autonomous_operation, daemon=True).start()

    def shutdown(self):
        """Shutdown agent gracefully."""
        self.logger.info(f"Shutting down agent {self.agent_id}")
        self.status = AgentStatus.SHUTDOWN
        self.is_running = False

        self.update_status()

        self.logger.info(f"Agent {self.agent_id} shutdown complete")


def create_osrs_agent(agent_id: str, role: AgentRole, osrs_account: OSRSAccount) -> OSRS_Agent_Core:
    """Factory function for creating OSRS agents."""
    return OSRS_Agent_Core(agent_id, role, osrs_account)


if __name__ == "__main__":
    account = OSRSAccount(
        account_id="agent1_account",
        username="test_user",
        password="test_pass",
        display_name="Agent1_Character",
        character_level=50,
        skills={"attack": 50, "strength": 50, "defence": 50},
        location="Lumbridge",
        current_activity="training",
        last_activity=datetime.now(),
    )

    agent = create_osrs_agent("Agent-1", AgentRole.COMBAT_SPECIALIST, account)

    try:
        agent.start_autonomous_operation()
    except KeyboardInterrupt:
        agent.shutdown()
