#!/usr/bin/env python3
"""
CLI Interface - Agent Cellphone V2
=================================

Handles command-line interface for messaging operations.
Single responsibility: CLI operations only.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any

from .interfaces import MessagingMode, MessageType
from .unified_messaging_service import UnifiedMessagingService
from .coordinate_manager import CoordinateManager

logger = logging.getLogger(__name__)


class MessagingCLI:
    """
    Messaging CLI - Single responsibility: Command-line interface operations
    
    This class only handles:
    - Argument parsing
    - Command execution
    - Output formatting
    """
    
    def __init__(self):
        """Initialize the CLI interface"""
        self.parser = self._create_parser()
        self.service = UnifiedMessagingService()
        logger.info("Messaging CLI initialized")
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with all available options"""
        parser = argparse.ArgumentParser(description="Unified Messaging Service CLI")
        
        # Mode selection
        parser.add_argument("--mode", type=str, choices=[m.value for m in MessagingMode], 
                           default="pyautogui", help="Messaging mode")
        
        # Coordinate mode selection
        parser.add_argument("--coordinate-mode", type=str, default="8-agent", 
                           help="Coordinate mode to use (default: 8-agent)")
        
        # Message content
        parser.add_argument("--message", type=str, help="Message content to send")
        
        # Recipient options
        parser.add_argument("--agent", type=str, help="Send to specific agent")
        parser.add_argument("--bulk", action="store_true", help="Send to all agents in 8-agent mode")
        parser.add_argument("--campaign", action="store_true", help="Campaign mode (election broadcast)")
        parser.add_argument("--yolo", action="store_true", help="YOLO mode (automatic activation)")
        
        # Message type
        parser.add_argument("--type", type=str, choices=[t.value for t in MessageType], 
                           default="text", help="Message type")
        
        # High priority flag
        parser.add_argument("--high-priority", action="store_true", 
                           help="Send as HIGH PRIORITY message (Ctrl+Enter 2x)")
        
        # Onboarding flags
        parser.add_argument("--onboarding", action="store_true", 
                           help="Send as onboarding message (new chat sequence)")
        parser.add_argument("--new-chat", action="store_true", 
                           help="Send as new chat message (onboarding sequence)")
        
        # Coordinate validation
        parser.add_argument("--validate", action="store_true", help="Validate coordinates")
        
        # Contract automation flags
        parser.add_argument("--claim-contract", type=str, help="Claim a contract by ID")
        parser.add_argument("--complete-contract", type=str, help="Complete a contract by ID")
        parser.add_argument("--get-next-task", action="store_true", help="Get next available task from queue")
        parser.add_argument("--contract-status", action="store_true", help="Show contract claiming status")
        
        # Captain communication flags
        parser.add_argument("--captain", action="store_true", help="Send message directly to Captain (Agent-4) with automatic agent identification and contract generation prompt")
        
        # Resume system flags
        parser.add_argument("--resume", action="store_true", help="Resume perpetual motion system with automatic workflow restoration messages")
        parser.add_argument("--resume-captain", action="store_true", help="Send Captain resume message for strategic oversight")
        parser.add_argument("--resume-agents", action="store_true", help="Send Agent resume message for perpetual motion workflow")
        
        # Add coordinate management flags
        parser.add_argument('--coordinates', action='store_true', 
                          help='Show coordinate mapping for all agents')
        parser.add_argument('--map-mode', type=str, default='8-agent',
                          help='Coordinate mode to map (default: 8-agent)')
        parser.add_argument('--consolidate', action='store_true',
                          help='Consolidate coordinate files from multiple sources')
        parser.add_argument('--calibrate', nargs=5, metavar=('AGENT', 'INPUT_X', 'INPUT_Y', 'STARTER_X', 'STARTER_Y'),
                          help='Calibrate coordinates for a specific agent (AGENT INPUT_X INPUT_Y STARTER_X STARTER_Y)')
        parser.add_argument('--interactive', action='store_true',
                          help='Run interactive coordinate capture for all agents')
        parser.add_argument('--interactive-mode', type=str, default='8-agent',
                          help='Mode for interactive coordinate capture (default: 8-agent)')
        
        return parser
    
    def execute_command(self, args: argparse.Namespace) -> bool:
        """Execute the parsed command"""
        try:
            # Set mode
            mode = MessagingMode(args.mode)
            self.service.set_mode(mode)
            
            if args.validate:
                return self._handle_validation()
            
            # Handle coordinate management
            if args.coordinates:
                self._handle_coordinate_mapping(args.map_mode)
            elif args.consolidate:
                self._handle_coordinate_consolidation()
            elif args.calibrate:
                self._handle_coordinate_calibration(args.calibrate)
            elif args.interactive:
                self._handle_interactive(args.interactive_mode)
            # Handle contract automation
            elif args.claim_contract:
                return self._handle_contract_claiming(args.claim_contract, args.agent)
            elif args.complete_contract:
                return self._handle_contract_completion(args.complete_contract, args.agent)
            elif args.get_next_task:
                return self._handle_get_next_task(args.agent)
            elif args.contract_status:
                return self._handle_contract_status()
            # Handle Captain communication
            elif args.captain:
                return self._handle_captain_message(args)
            # Handle resume system
            elif args.resume:
                return self._handle_resume_system(args)
            elif args.resume_captain:
                return self._handle_resume_captain(args)
            elif args.resume_agents:
                return self._handle_resume_agents(args)
            elif args.message:
                self._handle_message(args)
            else:
                self.parser.print_help()
                
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return False
    
    def _handle_validation(self) -> bool:
        """Handle coordinate validation"""
        results = self.service.validate_coordinates()
        print("📊 Coordinate Validation Results:")
        for key, value in results.items():
            print(f"  {key}: {value}")
        return True
    
    def _show_help(self) -> bool:
        """Show help information"""
        print("🤖 Unified Messaging Service - Use --help for available commands")
        print("\n🚀 AVAILABLE MODES:")
        for mode in MessagingMode:
            print(f"  --mode {mode.value:<15} # {mode.name.replace('_', ' ').title()}")
        print("\n📡 SPECIAL FLAGS:")
        print("  --bulk              # Send to ALL agents")
        print("  --campaign          # Campaign broadcast mode")
        print("  --yolo              # YOLO automatic mode")
        print("  --captain           # Send message directly to Captain (Agent-4)")
        print("  --resume            # Resume perpetual motion system (Captain + Agents)")
        print("  --resume-captain    # Send Captain resume message for oversight")
        print("  --resume-agents     # Send Agent resume message for workflow")
        return True
    
    def _handle_bulk_messaging(self, args: argparse.Namespace, mode: MessagingMode, 
                              message_type: MessageType) -> bool:
        """Handle bulk messaging operations"""
        print(f"📡 Bulk messaging to all agents via {mode.value}...")
        
        messages = {f"Agent-{i}": args.message for i in range(1, 9)}
        
        # Check for onboarding flags
        new_chat = False
        if args.onboarding or args.new_chat:
            new_chat = True
            print("🚀 ONBOARDING messages detected - using new chat sequence!")
            if args.onboarding:
                message_type = MessageType.ONBOARDING_START
        
        results = self.service.send_bulk_messages(messages, "8-agent", message_type, new_chat)
        
        print("📊 Bulk Message Results:")
        for agent_id, success in results.items():
            if args.high_priority:
                status = "🚨 HIGH PRIORITY Success" if success else "❌ HIGH PRIORITY Failed"
            else:
                status = "✅ Success" if success else "❌ Failed"
            print(f"  {agent_id}: {status}")
        
        return True
    
    def _handle_campaign_messaging(self, args: argparse.Namespace) -> bool:
        """Handle campaign messaging operations"""
        print(f"🗳️ Campaign messaging...")
        results = self.service.send_campaign_message(args.message)
        
        print("📊 Campaign Results:")
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {agent_id}: {status}")
        
        return True
    
    def _handle_yolo_messaging(self, args: argparse.Namespace) -> bool:
        """Handle YOLO messaging operations"""
        print(f"🚀 YOLO MODE ACTIVATED...")
        results = self.service.activate_yolo_mode(args.message)
        
        print("📊 YOLO Results:")
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {agent_id}: {status}")
        
        return True
    
    def _handle_single_agent_messaging(self, args: argparse.Namespace, mode: MessagingMode, 
                                     message_type: MessageType) -> bool:
        """Handle single agent messaging operations"""
        print(f"🤖 Agent messaging via {mode.value}...")
        
        # Validate coordinates before sending message
        print("🔍 Validating coordinates before sending...")
        coordinate_mode = getattr(args, 'coordinate_mode', '8-agent')
        validation_result = self.service.validate_agent_coordinates(args.agent, coordinate_mode)
        
        if not validation_result.get("valid", False):
            print(f"❌ Coordinate validation failed for {args.agent}:")
            print(f"   Error: {validation_result.get('error', 'Unknown error')}")
            print("   Please check coordinates and try again.")
            return False
        
        print(f"✅ Coordinates validated for {args.agent}")
        
        # Check for high priority flag
        if args.high_priority:
            print("🚨 HIGH PRIORITY message detected - using Ctrl+Enter 2x sequence!")
            # Override message type to high priority
            message_type = MessageType.HIGH_PRIORITY
        
        # Check for onboarding flags
        new_chat = False
        if args.onboarding or args.new_chat:
            new_chat = True
            print("🚀 ONBOARDING message detected - using new chat sequence!")
            if args.onboarding:
                message_type = MessageType.ONBOARDING_START
        
        success = self.service.send_message(args.agent, args.message, message_type, mode, new_chat)
        
        if args.high_priority:
            status = "✅ HIGH PRIORITY message sent successfully" if success else "❌ HIGH PRIORITY message failed"
        else:
            status = "✅ Success" if success else "❌ Failed"
            
        print(f"Agent message: {status}")
        return success
    
    def run(self, argv=None) -> bool:
        """Run the CLI with given arguments"""
        try:
            args = self.parser.parse_args(argv)
            return self.execute_command(args)
        except Exception as e:
            logger.error(f"Error running CLI: {e}")
            return False
    
    def _handle_interactive(self, mode: str):
        """Handle interactive coordinate capture"""
        try:
            from .interactive_coordinate_capture import InteractiveCoordinateCaptureService
            
            # Initialize coordinate manager
            coordinate_manager = CoordinateManager()
            
            # Initialize interactive capture service
            interactive_service = InteractiveCoordinateCaptureService(coordinate_manager)
            
            # Run full calibration
            success = interactive_service.run_full_calibration(mode)
            
            if success:
                print(f"\n🎉 Interactive coordinate capture completed successfully for {mode} mode!")
            else:
                print(f"\n❌ Interactive coordinate capture failed for {mode} mode")
                
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("💡 Make sure PyAutoGUI is installed: pip install pyautogui")
        except Exception as e:
            print(f"❌ Error during interactive coordinate capture: {e}")
    
    def _handle_message(self, args: argparse.Namespace):
        """Handle message sending operations"""
        try:
            # Determine message type
            message_type = MessageType(args.type)
            
            if args.bulk:
                return self._handle_bulk_messaging(args, MessagingMode(args.mode), message_type)
            elif args.campaign:
                return self._handle_campaign_messaging(args)
            elif args.yolo:
                return self._handle_yolo_messaging(args)
            elif args.agent:
                return self._handle_single_agent_messaging(args, MessagingMode(args.mode), message_type)
            else:
                print("❌ No message operation specified. Use --help for available options.")
                return False
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return False
    
    def _handle_coordinate_mapping(self, mode: str) -> bool:
        """Handle coordinate mapping display"""
        try:
            print(f"🗺️  Coordinate Mapping for {mode} mode")
            print("=" * 60)
            
            mapping_results = self.service.map_coordinates(mode)
            
            # Display summary
            summary = mapping_results.get("summary", {})
            print(f"📊 Summary:")
            print(f"  Total Agents: {summary.get('total_agents', 0)}")
            print(f"  Valid Agents: {summary.get('valid_agents', 0)}")
            print(f"  Invalid Agents: {summary.get('invalid_agents', 0)}")
            print()
            
            # Display detailed mapping
            agents = mapping_results.get("agents", {})
            for agent_id, agent_info in agents.items():
                input_coords = agent_info.get("input_box", {}).get("coordinates", (None, None))
                starter_coords = agent_info.get("starter_location", {}).get("coordinates", (None, None))
                valid = agent_info.get("overall_valid", False)
                
                status = "✅" if valid else "❌"
                print(f"{status} {agent_id}:")
                print(f"    Input Box: ({input_coords[0]}, {input_coords[1]})")
                print(f"    Starter Location: ({starter_coords[0]}, {starter_coords[1]})")
                print()
            
            return True
        except Exception as e:
            logger.error(f"Coordinate mapping failed: {e}")
            return False
    
    def _handle_coordinate_consolidation(self) -> bool:
        """Handle coordinate file consolidation"""
        try:
            print("🔄 Consolidating Coordinate Files...")
            print("=" * 60)
            
            consolidation_results = self.service.consolidate_coordinate_files()
            
            print(f"📁 Primary File: {consolidation_results.get('primary_file', 'Unknown')}")
            print(f"📥 Sources Found: {len(consolidation_results.get('sources_found', []))}")
            
            for source in consolidation_results.get("sources_found", []):
                print(f"    - {source}")
            
            print(f"✅ Sources Merged: {len(consolidation_results.get('sources_merged', []))}")
            
            conflicts = consolidation_results.get("conflicts", [])
            if conflicts:
                print(f"⚠️  Conflicts Found: {len(conflicts)}")
                for conflict in conflicts:
                    print(f"    - {conflict['agent']} in {conflict['mode']} mode")
            else:
                print("✅ No conflicts found")
            
            final_coords = consolidation_results.get("final_coordinates", {})
            total_agents = sum(len(agents) for agents in final_coords.values())
            print(f"📊 Final Result: {len(final_coords)} modes, {total_agents} agent configurations")
            
            return True
        except Exception as e:
            logger.error(f"Coordinate consolidation failed: {e}")
            return False
    
    def _handle_coordinate_calibration(self, calibrate_args: list) -> bool:
        """Handle coordinate calibration"""
        try:
            if len(calibrate_args) != 5:
                print("❌ Calibration requires exactly 5 arguments: Agent ID, Input X, Input Y, Starter X, Starter Y")
                return False
            
            agent_id = calibrate_args[0]
            try:
                input_x = int(calibrate_args[1])
                input_y = int(calibrate_args[2])
                starter_x = int(calibrate_args[3])
                starter_y = int(calibrate_args[4])
            except ValueError:
                print("❌ Coordinate values must be integers")
                return False
            
            print(f"🔧 Calibrating coordinates for {agent_id}...")
            print(f"   Input Box: ({input_x}, {input_y})")
            print(f"   Starter Location: ({starter_x}, {starter_y})")
            
            success = self.service.calibrate_coordinates(
                agent_id, 
                (input_x, input_y), 
                (starter_x, starter_y)
            )
            
            if success:
                print(f"✅ Coordinates successfully calibrated for {agent_id}")
            else:
                print(f"❌ Failed to calibrate coordinates for {agent_id}")
            
            return success
        except Exception as e:
            logger.error(f"Coordinate calibration failed: {e}")
            return False
    
    def _handle_contract_claiming(self, contract_id: str, agent_id: str) -> bool:
        """Handle contract claiming"""
        try:
            if not agent_id:
                print("❌ Agent ID required for contract claiming. Use --agent Agent-X")
                return False
            
            print(f"📋 Claiming contract {contract_id} for {agent_id}...")
            
            # Import contract system
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd(), 'agent_workspaces', 'meeting'))
            from contract_claiming_system import ContractClaimingSystem
            
            # Use the correct path for task_list.json
            task_list_path = os.path.join(os.getcwd(), 'agent_workspaces', 'meeting', 'task_list.json')
            system = ContractClaimingSystem(task_list_path)
            result = system.claim_contract(contract_id, agent_id)
            
            if result["success"]:
                print(f"✅ {result['message']}")
                print(f"📊 Contract: {result['contract']['title']}")
                print(f"⏱️  Estimated Time: {result['contract']['estimated_time']}")
                print(f"🏆 Extra Credit: {result['contract']['extra_credit_points']} points")
                return True
            else:
                print(f"❌ {result['message']}")
                return False
                
        except Exception as e:
            logger.error(f"Contract claiming failed: {e}")
            return False
    
    def _handle_contract_completion(self, contract_id: str, agent_id: str) -> bool:
        """Handle contract completion"""
        try:
            if not agent_id:
                print("❌ Agent ID required for contract completion. Use --agent Agent-X")
                return False
            
            print(f"🎯 Completing contract {contract_id} for {agent_id}...")
            
            # Import contract system
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd(), 'agent_workspaces', 'meeting'))
            from contract_claiming_system import ContractClaimingSystem
            
            # Use the correct path for task_list.json
            task_list_path = os.path.join(os.getcwd(), 'agent_workspaces', 'meeting', 'task_list.json')
            system = ContractClaimingSystem(task_list_path)
            
            # Get contract details for deliverables
            contracts = system.load_contracts()
            deliverables = []
            
            for category_name, category_data in contracts.get("contracts", {}).items():
                for contract in category_data.get("contracts", []):
                    if contract.get("contract_id") == contract_id:
                        deliverables = contract.get("deliverables", [])
                        break
                if deliverables:
                    break
            
            result = system.complete_contract(contract_id, agent_id, deliverables)
            
            if result["success"]:
                print(f"✅ {result['message']}")
                print(f"🏆 Extra credit earned: {result['extra_credit_earned']} points!")
                print(f"📦 Deliverables: {', '.join(deliverables)}")
                return True
            else:
                print(f"❌ {result['message']}")
                return False
                
        except Exception as e:
            logger.error(f"Contract completion failed: {e}")
            return False
    
    def _handle_get_next_task(self, agent_id: str) -> bool:
        """Handle getting next available task"""
        try:
            if not agent_id:
                print("❌ Agent ID required for getting next task. Use --agent Agent-X")
                return False
            
            print(f"🔍 Finding next available task for {agent_id}...")
            
            # Import contract system
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd(), 'agent_workspaces', 'meeting'))
            from contract_claiming_system import ContractClaimingSystem
            
            # Use the correct path for task_list.json
            task_list_path = os.path.join(os.getcwd(), 'agent_workspaces', 'meeting', 'task_list.json')
            system = ContractClaimingSystem(task_list_path)
            available = system.list_available_contracts()
            
            if not available:
                print("❌ No available contracts found")
                return False
            
            # Find best match for agent based on their role
            agent_roles = {
                "Agent-1": "coordination_enhancement",
                "Agent-2": "phase_transition_optimization", 
                "Agent-3": "testing_framework_enhancement",
                "Agent-4": "strategic_oversight",
                "Agent-5": "refactoring_tool_preparation",
                "Agent-6": "performance_optimization",
                "Agent-7": "quality_completion_optimization",
                "Agent-8": "integration_enhancement_optimization"
            }
            
            agent_role = agent_roles.get(agent_id, "general")
            
            # Prioritize contracts matching agent's role
            priority_contracts = [c for c in available if c.get("category", "").lower() == agent_role.lower()]
            other_contracts = [c for c in available if c.get("category", "").lower() != agent_role.lower()]
            
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
            print(f"\n💡 To claim this task, run:")
            print(f"   python -m src.services.messaging --agent {agent_id} --claim-contract {next_contract['contract_id']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Get next task failed: {e}")
            return False
    
    def _handle_contract_status(self) -> bool:
        """Handle contract status display"""
        try:
            print("📊 CONTRACT CLAIMING SYSTEM STATUS")
            print("=" * 60)
            
            # Import contract system
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd(), 'agent_workspaces', 'meeting'))
            from contract_claiming_system import ContractClaimingSystem
            
            # Use the correct path for task_list.json
            task_list_path = os.path.join(os.getcwd(), 'agent_workspaces', 'meeting', 'task_list.json')
            system = ContractClaimingSystem(task_list_path)
            stats = system.get_contract_statistics()
            
            print(f"📋 Total Contracts: {stats['total_contracts']}")
            print(f"✅ Available: {stats['available_contracts']}")
            print(f"🔄 Claimed: {stats['claimed_contracts']}")
            print(f"🏆 Completed: {stats['completed_contracts']}")
            print(f"💎 Total Extra Credit: {stats['total_extra_credit']} points")
            
            return True
            
        except Exception as e:
            logger.error(f"Contract status failed: {e}")
            return False
    
    def _handle_captain_message(self, args: argparse.Namespace) -> bool:
        """Handle Captain communication with automatic agent identification and contract generation prompt"""
        try:
            if not args.message:
                print("❌ Message content required for Captain communication. Use --message 'Your message'")
                return False
            
            # Determine which agent is sending the message
            agent_id = args.agent if args.agent else "UNKNOWN_AGENT"
            
            # Create enhanced message with agent identification and contract generation prompt
            enhanced_message = f"🎯 CAPTAIN MESSAGE FROM {agent_id}: {args.message}\n\n📋 CAPTAIN ACTION REQUIRED:\n1) Review this agent's message and status\n2) Create additional contracts if needed\n3) Message all agents that new contracts are available\n4) Ensure continuous work cycle maintenance"
            
            print(f"🎯 Sending Captain message from {agent_id}...")
            print(f"📝 Enhanced message: {enhanced_message}")
            
            # Send message to Captain (Agent-4)
            success = self.service.send_message("Agent-4", enhanced_message, MessageType.TEXT, MessagingMode.PYAUTOGUI, False)
            
            if success:
                print(f"✅ Captain message sent successfully from {agent_id}")
                print(f"📋 Captain will receive enhanced prompt for contract generation and agent messaging")
                return True
            else:
                print(f"❌ Failed to send Captain message from {agent_id}")
                return False
                
        except Exception as e:
            logger.error(f"Captain message handling failed: {e}")
            return False

    def _handle_resume_system(self, args: argparse.Namespace) -> bool:
        """Handle complete resume system activation for perpetual motion"""
        try:
            print("🚨 RESUME SYSTEM ACTIVATED: Perpetual Motion System Restoration!")
            
            # Check message frequency to prevent spam
            if self._should_send_resume_message():
                # Send Captain resume message
                captain_success = self._handle_resume_captain(args)
                
                # Send Agent resume message
                agent_success = self._handle_resume_agents(args)
                
                # Always update message counter if we attempted to send
                self._update_resume_message_counter()
                
                if captain_success and agent_success:
                    print("✅ Resume system activation complete!")
                    print("🎯 Perpetual motion system restored - all agents should resume workflow")
                    return True
                else:
                    print("⚠️ Resume system partially activated - some messages may have failed")
                    return False
            else:
                print("⏰ Resume message sent recently - waiting for next cycle (10 message minimum interval)")
                print("💡 Use --resume-captain or --resume-agents for immediate individual messages")
                return True
                
        except Exception as e:
            logger.error(f"Resume system activation failed: {e}")
            return False

    def _handle_resume_captain(self, args: argparse.Namespace) -> bool:
        """Handle Captain resume message for strategic oversight"""
        try:
            print("🎯 Sending Captain resume message for strategic oversight...")
            
            captain_message = """🚨 CAPTAIN RESUME DIRECTIVE: PERPETUAL MOTION SYSTEM RESTORATION REQUIRED!

📊 CURRENT SYSTEM STATUS:
- Emergency workflow restoration active
- 40+ contracts available for momentum sustainment
- Agents may have gone dark - immediate intervention required

🎯 CAPTAIN RESPONSIBILITIES:
1. Review current contract availability and agent engagement
2. Generate additional contracts if needed to maintain 40+ available
3. Send bulk resume message to all agents
4. Monitor agent response and workflow restoration
5. Ensure perpetual motion system continues

⚡ IMMEDIATE ACTION REQUIRED:
- Assess system health and contract status
- Activate agent mobilization protocols
- Restore continuous workflow cycle
- Maintain sprint acceleration momentum

🔧 CODING STANDARDS ENFORCEMENT:
- Follow existing architecture before developing new solutions
- Maintain code quality and consistency across all agents
- Ensure proper error handling and validation
- Document all major changes and decisions

🚀 OBJECTIVE: Restore perpetual motion system and reach INNOVATION PLANNING MODE!"""
            
            # Send message to Captain (Agent-4)
            success = self.service.send_message("Agent-4", captain_message, MessageType.TEXT, MessagingMode.PYAUTOGUI, False)
            
            if success:
                print("✅ Captain resume message sent successfully")
                return True
            else:
                print("❌ Failed to send Captain resume message")
                return False
                
        except Exception as e:
            logger.error(f"Captain resume message failed: {e}")
            return False

    def _handle_resume_agents(self, args: argparse.Namespace) -> bool:
        """Handle Agent resume message for perpetual motion workflow"""
        try:
            print("📡 Sending Agent resume message for perpetual motion workflow...")
            
            agent_message = """🚨 AGENT RESUME DIRECTIVE: PERPETUAL MOTION WORKFLOW RESTORATION!

📊 WORKFLOW EXPECTATIONS:
1. IMMEDIATE ACTION: Use --get-next-task flag to claim contracts
2. CONTINUOUS WORK: Never stop working - always have a task in progress
3. TASK COMPLETION: Mark tasks complete and immediately claim next
4. MOMENTUM MAINTENANCE: Maintain continuous workflow cycle

🎯 PERPETUAL MOTION PROTOCOL:
- TASK → EXECUTE → COMPLETE → IMMEDIATELY_CLAIM_NEXT → REPEAT_FOREVER
- Use --get-next-task flag immediately when tasks complete
- Never allow idle time - always be working on contracts
- Maintain sprint acceleration momentum

🔧 CODING STANDARDS COMPLIANCE:
- PRIORITY: Use existing architecture before developing new solutions
- Code Quality: Maintain consistency, readability, and proper documentation
- Error Handling: Implement robust validation and error management
- Testing: Ensure all changes are properly tested and validated
- Documentation: Update relevant documentation for all modifications

⚡ AVAILABLE CONTRACTS:
- 40+ contracts available across 14 categories
- Emergency workflow restoration contracts worth 5,275+ points
- High-value contracts: 400-500 points each
- Immediate claiming required

🚀 OBJECTIVE: Complete emergency contracts to restore system momentum and reach INNOVATION PLANNING MODE!

📋 COMMAND: --get-next-task"""
            
            # Send bulk message to all agents
            messages = {f"Agent-{i}": agent_message for i in range(1, 9)}
            results = self.service.send_bulk_messages(messages, "8-agent", MessageType.TEXT, False)
            
            print("📊 Agent Resume Message Results:")
            success_count = 0
            for agent_id, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"  {agent_id}: {status}")
                if success:
                    success_count += 1
            
            if success_count >= 6:  # At least 6 out of 8 agents
                print(f"✅ Agent resume messages sent successfully to {success_count}/8 agents")
                return True
            else:
                print(f"⚠️ Agent resume messages partially successful: {success_count}/8 agents")
                return False
                
        except Exception as e:
            logger.error(f"Agent resume message failed: {e}")
            return False

    def _should_send_resume_message(self) -> bool:
        """Check if enough time has passed since last resume message"""
        try:
            import os
            import json
            from datetime import datetime, timedelta
            
            counter_file = "resume_message_counter.json"
            
            if not os.path.exists(counter_file):
                return True  # First time, allow message
            
            with open(counter_file, 'r') as f:
                data = json.load(f)
            
            last_message_time = datetime.fromisoformat(data.get("last_message_time", "2000-01-01T00:00:00"))
            message_count = data.get("message_count", 0)
            
            # Allow message if 10+ messages have been sent since last resume
            # or if more than 1 hour has passed
            time_since_last = datetime.now() - last_message_time
            messages_since_last = message_count - data.get("last_resume_message_count", 0)
            
            if messages_since_last >= 10 or time_since_last > timedelta(hours=1):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking resume message frequency: {e}")
            return True  # Default to allowing message if check fails

    def _update_resume_message_counter(self):
        """Update the resume message counter after sending"""
        try:
            import os
            import json
            from datetime import datetime
            
            counter_file = "resume_message_counter.json"
            
            # Load existing data or create new
            if os.path.exists(counter_file):
                with open(counter_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"message_count": 0, "last_message_time": "2000-01-01T00:00:00"}
            
            # Update counters
            data["last_resume_message_time"] = datetime.now().isoformat()
            data["last_resume_message_count"] = data.get("message_count", 0)
            
            # Save updated data
            with open(counter_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error updating resume message counter: {e}")
