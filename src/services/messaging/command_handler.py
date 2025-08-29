#!/usr/bin/env python3
"""Refactored command handler with eliminated function duplication."""

import argparse
import logging
from .interfaces import MessagingMode
from .unified_messaging_service import UnifiedMessagingService
from .output_formatter import OutputFormatter
from .config import CAPTAIN_ID, DEFAULT_COORDINATE_MODE
from .contract_system_manager import ContractSystemManager
from .error_handler import ErrorHandler
from .handlers.messaging_handlers import MessagingHandlers

logger = logging.getLogger(__name__)


class CommandHandler:
    """Process messaging-related commands with eliminated duplication."""

    def __init__(self, formatter: OutputFormatter | None = None):
        self.service = UnifiedMessagingService()
        self.formatter = formatter or OutputFormatter()
        self.contract_manager = ContractSystemManager()
        self.messaging_handlers = MessagingHandlers(self.service, self.formatter)
        logger.info("Refactored messaging command handler initialized")

    def execute_command(self, args: argparse.Namespace) -> bool:
        """Execute the parsed command using centralized error handling."""
        return ErrorHandler.safe_execute(
            "Command execution", logger, self._execute_command_internal, args
        )
    
    def _execute_command_internal(self, args: argparse.Namespace) -> bool:
        """Internal command execution logic."""
        try:
            mode = MessagingMode(args.mode)
            self.service.set_mode(mode)
            if args.validate:
                return self._handle_validation()
            if args.coordinates:
                self._handle_coordinate_mapping(args.map_mode)
            elif args.consolidate:
                self._handle_coordinate_consolidation()
            elif args.calibrate:
                self._handle_coordinate_calibration(args.calibrate)
            elif args.interactive:
                self._handle_interactive(args.interactive_mode)
            elif args.claim_contract:
                return self._handle_contract_claiming(args.claim_contract, args.agent)
            elif args.complete_contract:
                return self._handle_contract_completion(args.complete_contract, args.agent)
            elif args.get_next_task:
                return self._handle_get_next_task(args.agent)
            elif args.contract_status:
                return self._handle_contract_status()
            elif args.captain:
                return self.messaging_handlers.captain_message(args)
            elif args.resume:
                return self.messaging_handlers.resume_system(args)
            elif args.resume_captain:
                return self.messaging_handlers.resume_captain(args)
            elif args.resume_agents:
                return self.messaging_handlers.resume_agents(args)
            elif args.message:
                return self.messaging_handlers.message(args, mode)
            elif args.onboard:
                return self.messaging_handlers.onboarding(args)
            elif args.check_status:
                return self.messaging_handlers.status_check()
            return False
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return False

    def _handle_validation(self) -> bool:
        """Handle coordinate validation using centralized error handling."""
        return ErrorHandler.safe_execute(
            "Coordinate validation", logger, self._handle_validation_internal
        )
    
    def _handle_validation_internal(self) -> bool:
        """Internal validation logic."""
        results = self.service.validate_coordinates()
        self.formatter.validation_results(results)
        return True

    def _handle_contract_claiming(self, contract_id: str, agent_id: str) -> bool:
        """Handle contract claiming using centralized contract manager."""
        # Validate required arguments
        if not ErrorHandler.validate_required_args(agent_id, "contract claiming", logger):
            return False
            
        return ErrorHandler.safe_execute(
            "Contract claiming", logger, self._handle_contract_claiming_internal, contract_id, agent_id
        )
    
    def _handle_contract_claiming_internal(self, contract_id: str, agent_id: str) -> bool:
        print(f"📋 Claiming contract {contract_id} for {agent_id}...")

        # Use centralized contract manager
        result = self.contract_manager.claim_contract(contract_id, agent_id)

        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"📊 Contract: {result['contract']['title']}")
            print(f"⏱️  Estimated Time: {result['contract']['estimated_time']}")
            print(f"🏆 Extra Credit: {result['contract']['extra_credit_points']} points")
            return True
        else:
            print(f"❌ {result['message']}")
            return False

    def _handle_contract_completion(self, contract_id: str, agent_id: str) -> bool:
        """Handle contract completion using centralized contract manager."""
        # Validate required arguments
        if not ErrorHandler.validate_required_args(agent_id, "contract completion", logger):
            return False
            
        return ErrorHandler.safe_execute(
            "Contract completion", logger, self._handle_contract_completion_internal, contract_id, agent_id
        )
    
    def _handle_contract_completion_internal(self, contract_id: str, agent_id: str) -> bool:
        print(f"🎯 Completing contract {contract_id} for {agent_id}...")

        # Get contract details using centralized manager
        contract_details = self.contract_manager.get_contract_details(contract_id)
        if not contract_details:
            print(f"❌ Contract {contract_id} not found")
            return False

        deliverables = contract_details.get("deliverables", [])
        
        # Use centralized contract manager
        result = self.contract_manager.complete_contract(contract_id, agent_id, deliverables)

        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"🏆 Extra credit earned: {result['extra_credit_earned']} points!")
            print(f"📦 Deliverables: {', '.join(deliverables)}")
            return True
        else:
            print(f"❌ {result['message']}")
            return False

    def _handle_get_next_task(self, agent_id: str) -> bool:
        """Handle getting next available task using centralized contract manager."""
        # Validate required arguments
        if not ErrorHandler.validate_required_args(agent_id, "getting next task", logger):
            return False
            
        return ErrorHandler.safe_execute(
            "Get next task", logger, self._handle_get_next_task_internal, agent_id
        )
    
    def _handle_get_next_task_internal(self, agent_id: str) -> bool:
        print(f"🔍 Finding next available task for {agent_id}...")

        # Use centralized contract manager
        available = self.contract_manager.list_available_contracts()

        if not available:
            print("❌ No available contracts found")
            return False

        # Find best match for agent based on their role
        agent_roles = {
            "Agent-1": "coordination_enhancement",
            "Agent-2": "phase_transition_optimization",
            "Agent-3": "testing_framework_enhancement",
            CAPTAIN_ID: "strategic_oversight",
            "Agent-5": "refactoring_tool_preparation",
            "Agent-6": "performance_optimization",
            "Agent-7": "quality_completion_optimization",
            "Agent-8": "integration_enhancement_optimization",
        }

        agent_role = agent_roles.get(agent_id, "general")

        # Prioritize contracts matching agent's role
        priority_contracts = [
            c for c in available
            if c.get("category", "").lower() == agent_role.lower()
        ]
        other_contracts = [
            c for c in available
            if c.get("category", "").lower() != agent_role.lower()
        ]

        if priority_contracts:
            next_contract = priority_contracts[0]
            print(f"🎯 Priority task found for {agent_id}:")
        else:
            next_contract = other_contracts[0]
            print(f"📋 General task found for {agent_id}:")

        print(f"📋 Contract ID: {next_contract['contract_id']}")
        print(f"📝 Title: {next_contract['title']}")
        print(f"⚡ Difficulty: {next_contract['difficulty']}")
        print(f"⏱️  Estimated Time: {next_contract['estimated_time']}")
        print(f"🏆 Extra Credit: {next_contract['extra_credit_points']} points")
        print("\n💡 To claim this task, run:")
        print(f"   python -m src.services.messaging --agent {agent_id} --claim-contract {next_contract['contract_id']}")

        return True

    def _handle_contract_status(self) -> bool:
        """Handle contract status display using centralized contract manager."""
        return ErrorHandler.safe_execute(
            "Contract status", logger, self._handle_contract_status_internal
        )
    
    def _handle_contract_status_internal(self) -> bool:
        print("📊 CONTRACT CLAIMING SYSTEM STATUS")
        print("=" * 60)

        # Use centralized contract manager
        stats = self.contract_manager.get_contract_statistics()

        print(f"📋 Total Contracts: {stats['total_contracts']}")
        print(f"✅ Available: {stats['available_contracts']}")
        print(f"📊 Claimed: {stats.get('claimed_contracts', 0)}")
        print(f"🎯 Completed: {stats.get('completed_contracts', 0)}")

        return True

    def _handle_coordinate_mapping(self, mode: str) -> bool:
        """Handle coordinate mapping using centralized error handling."""
        return ErrorHandler.safe_execute(
            "Coordinate mapping", logger, self._handle_coordinate_mapping_internal, mode
        )
    
    def _handle_coordinate_mapping_internal(self, mode: str) -> bool:
        mapping = self.service.coordinate_manager.map_coordinates(mode)
        for agent_id, data in mapping["agents"].items():
            input_coords = data["input_box"]["coordinates"]
            starter_coords = data["starter_location"]["coordinates"]
            valid = "✅" if data["overall_valid"] else "❌"
            print(
                f"{agent_id}: starter {starter_coords} input {input_coords} {valid}"
            )
        self.formatter.mapping_results(mapping["summary"])
        return True

    def _handle_coordinate_consolidation(self) -> bool:
        """Handle coordinate consolidation using centralized error handling."""
        return ErrorHandler.safe_execute(
            "Coordinate consolidation", logger, self._handle_coordinate_consolidation_internal
        )
    
    def _handle_coordinate_consolidation_internal(self) -> bool:
        result = self.service.coordinate_manager.consolidate_coordinate_files()
        self.formatter.consolidation_results(result)
        return True

    def _handle_coordinate_calibration(self, calibrate_args: list) -> bool:
        """Handle coordinate calibration using centralized error handling."""
        return ErrorHandler.safe_execute(
            "Coordinate calibration", logger, self._handle_coordinate_calibration_internal, calibrate_args
        )
    
    def _handle_coordinate_calibration_internal(self, calibrate_args: list) -> bool:
        agent_id, input_x, input_y, starter_x, starter_y = calibrate_args
        input_coords = (int(input_x), int(input_y))
        starter_coords = (int(starter_x), int(starter_y))
        success = self.service.coordinate_manager.calibrate_coordinates(
            agent_id, input_coords, starter_coords, DEFAULT_COORDINATE_MODE
        )
        status = "✅" if success else "❌"
        print(
            f"{status} Calibrated {agent_id}: input {input_coords} starter {starter_coords}"
        )
        return success

    def _handle_interactive(self, mode: str) -> bool:
        """Handle interactive mode using centralized error handling."""
        return ErrorHandler.safe_execute(
            "Interactive mode", logger, self._handle_interactive_internal, mode
        )
    
    def _handle_interactive_internal(self, mode: str) -> bool:
        try:
            from .interactive_coordinate_capture import (
                InteractiveCoordinateCaptureService,
            )

            interactive_service = InteractiveCoordinateCaptureService(
                self.service.coordinate_manager
            )
            return interactive_service.run_full_calibration(mode)
        except ImportError as e:
            print(f"❌ {e}")
            return False
