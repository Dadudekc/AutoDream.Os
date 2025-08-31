#!/usr/bin/env python3
"""
Onboarding Handler - Onboarding Message Logic

This module provides onboarding message functionality.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""

import argparse
import logging
from ..config import DEFAULT_COORDINATE_MODE, AGENT_COUNT
from ..interfaces import MessageType
from ..contract_system_manager import ContractSystemManager
from ..error_handler import ErrorHandler
from ..prompt_loader import PromptLoader


class OnboardingHandler:
    """Handles onboarding message operations."""
    
    def __init__(self, service, formatter):
        """Initialize the onboarding handler."""
        self.service = service
        self.formatter = formatter
        self.contract_manager = ContractSystemManager()
        self.prompt_loader = PromptLoader()
        self.logger = logging.getLogger(f"{__name__}.OnboardingHandler")
        self.logger.info("✅ Onboarding Handler initialized")
    
    def handle_onboarding(self, args: argparse.Namespace) -> bool:
        """Handle onboarding messages."""
        return ErrorHandler.safe_execute(
            "Onboarding", self.logger, self._onboarding_internal, args
        )
    
    def _onboarding_internal(self, args: argparse.Namespace) -> bool:
        """Generate comprehensive onboarding messages with agent identity and responsibilities."""
        contracts = self.contract_manager.list_available_contracts()
        messages: dict[str, str] = {}
        
        for i in range(1, AGENT_COUNT + 1):
            agent_id = f"Agent-{i}"
            
            # Determine agent role and responsibilities
            if agent_id == "Agent-4":  # Captain
                base = self._generate_captain_onboarding(agent_id, args.message)
            else:  # Regular agents
                base = self._generate_agent_onboarding(agent_id, i, contracts, args.message)
            
            messages[agent_id] = base
        
        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, MessageType.ONBOARDING_START, True
        )
        self.formatter.generic_results("📊 Onboarding Results:", results)
        return True
    
    def _generate_captain_onboarding(self, agent_id: str, custom_message: str = None) -> str:
        """Generate comprehensive onboarding message for Captain (Agent-4)."""
        return self.prompt_loader.load_captain_onboarding(agent_id, custom_message)
    
    def _generate_agent_onboarding(self, agent_id: str, agent_number: int, contracts: list, custom_message: str = None) -> str:
        """Generate comprehensive onboarding message for regular agents."""
        
        # Get assigned contract if available
        contract_info = ""
        if agent_number - 1 < len(contracts):
            c = contracts[agent_number - 1]
            contract_info = f"{c['contract_id']}: {c['title']}"
        
        return self.prompt_loader.load_agent_onboarding(agent_id, agent_number, contract_info, custom_message)
