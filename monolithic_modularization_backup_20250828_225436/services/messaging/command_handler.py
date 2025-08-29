import argparse
import logging

                    import json
                    import os
            from .interactive_coordinate_capture import (
            from agent_workspaces.meeting.contract_claiming_system import ContractClaimingSystem
            from contract_claiming_system import ContractClaimingSystem
            from datetime import datetime
            from datetime import datetime, timedelta
            import sys
from .config import DEFAULT_COORDINATE_MODE, AGENT_COUNT, CAPTAIN_ID
from .coordinate_manager import CoordinateManager
from .interfaces import MessagingMode, MessageType
from .output_formatter import OutputFormatter
from .unified_messaging_service import UnifiedMessagingService

#!/usr/bin/env python3
"""Command handler for messaging operations."""



logger = logging.getLogger(__name__)


class CommandHandler:
    """Process messaging-related commands."""

    def __init__(self, formatter: OutputFormatter | None = None):
        self.service = UnifiedMessagingService()
        self.formatter = formatter or OutputFormatter()
        logger.info("Messaging command handler initialized")

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
                return self._handle_contract_completion(
                    args.complete_contract, args.agent
                )
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
                return self._handle_message(args)
            elif args.onboard:
                return self._handle_onboarding(args)
            elif args.check_status:
                return self._handle_status_check()
            else:
                return False

        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return False

    def _handle_validation(self) -> bool:
        """Handle coordinate validation"""
        results = self.service.validate_coordinates()
        self.formatter.validation_results(results)
        return True

    def _handle_bulk_messaging(
        self, args: argparse.Namespace, mode: MessagingMode, message_type: MessageType
    ) -> bool:
        """Handle bulk messaging operations"""
        print(f"📡 Bulk messaging to all agents via {mode.value}...")

        messages = {f"Agent-{i}": args.message for i in range(1, AGENT_COUNT + 1)}

        # Check for onboarding flags
        new_chat = False
        if args.onboarding or args.new_chat:
            new_chat = True
            print("🚀 ONBOARDING messages detected - using new chat sequence!")
            if args.onboarding:
                message_type = MessageType.ONBOARDING_START

        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, message_type, new_chat
        )
        self.formatter.generic_results(
            "📊 Bulk Message Results:", results, args.high_priority
        )
        return True

    def _handle_campaign_messaging(self, args: argparse.Namespace) -> bool:
        """Handle campaign messaging operations"""
        print("🗳️ Campaign messaging...")
        results = self.service.send_campaign_message(args.message)
        self.formatter.generic_results("📊 Campaign Results:", results)
        return True

    def _handle_yolo_messaging(self, args: argparse.Namespace) -> bool:
        """Handle YOLO messaging operations"""
        print("🚀 YOLO MODE ACTIVATED...")
        results = self.service.activate_yolo_mode(args.message)
        self.formatter.generic_results("📊 YOLO Results:", results)
        return True

    def _handle_single_agent_messaging(
        self, args: argparse.Namespace, mode: MessagingMode, message_type: MessageType
    ) -> bool:
        """Handle single agent messaging operations"""
        print(f"🤖 Agent messaging via {mode.value}...")

        # Validate coordinates before sending message
        print("🔍 Validating coordinates before sending...")
        coordinate_mode = getattr(args, "coordinate_mode", DEFAULT_COORDINATE_MODE)
        validation_result = self.service.validate_agent_coordinates(
            args.agent, coordinate_mode
        )

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

        success = self.service.send_message(
            args.agent, args.message, message_type, mode, new_chat
        )

        if args.high_priority:
            status = (
                "✅ HIGH PRIORITY message sent successfully"
                if success
                else "❌ HIGH PRIORITY message failed"
            )
        else:
            status = "✅ Success" if success else "❌ Failed"

        print(f"Agent message: {status}")
        return success

    def _handle_interactive(self, mode: str):
        """Handle interactive coordinate capture"""
        try:
                InteractiveCoordinateCaptureService,
            )

            # Initialize coordinate manager
            coordinate_manager = CoordinateManager()

            # Initialize interactive capture service
            interactive_service = InteractiveCoordinateCaptureService(
                coordinate_manager
            )

            # Run full calibration
            success = interactive_service.run_full_calibration(mode)

            if success:
                print(
                    f"\n🎉 Interactive coordinate capture completed successfully for {mode} mode!"
                )
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
                return self._handle_bulk_messaging(
                    args, MessagingMode(args.mode), message_type
                )
            elif args.campaign:
                return self._handle_campaign_messaging(args)
            elif args.yolo:
                return self._handle_yolo_messaging(args)
            elif args.agent:
                return self._handle_single_agent_messaging(
                    args, MessagingMode(args.mode), message_type
                )
            else:
                print(
                    "❌ No message operation specified. Use --help for available options."
                )
                return False

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return False

    def _handle_onboarding(self, args: argparse.Namespace) -> bool:
        """Handle automatic agent onboarding with contract assignment"""
        try:
            print("🚀 AUTOMATIC AGENT ONBOARDING: Contract Assignment & System Overview")
            print("=" * 80)
            
            # Get available contracts for assignment
            contract_system = ContractClaimingSystem("agent_workspaces/meeting/task_list.json")
            available_contracts = contract_system.list_available_contracts()
            
            if not available_contracts:
                print("⚠️ No available contracts found - creating real problem-solving contracts...")
                # Create real contracts for SSOT, deduplication, and monolithic file modularization
                real_contracts = [
                    {
                        "contract_id": "SSOT-001",
                        "title": "SSOT Violation Analysis & Resolution",
                        "description": "Identify and resolve multiple sources of truth violations across the codebase",
                        "difficulty": "HIGH",
                        "estimated_time": "3-4 hours",
                        "extra_credit_points": 400,
                        "requirements": [
                            "Analyze codebase for SSOT violations",
                            "Identify duplicate data sources",
                            "Create consolidation plan",
                            "Implement SSOT resolution"
                        ],
                        "deliverables": [
                            "SSOT violation analysis report",
                            "Consolidation plan document",
                            "Implementation code changes"
                        ],
                        "status": "AVAILABLE",
                        "category": "SSOT_Resolution"
                    },
                    {
                        "contract_id": "DEDUP-001", 
                        "title": "Code Duplication Detection & Consolidation",
                        "description": "Find and eliminate duplicate code patterns, consolidate into reusable components",
                        "difficulty": "MEDIUM",
                        "estimated_time": "2-3 hours",
                        "extra_credit_points": 350,
                        "requirements": [
                            "Scan codebase for duplicate patterns",
                            "Identify consolidation opportunities",
                            "Create reusable components",
                            "Update affected code"
                        ],
                        "deliverables": [
                            "Duplication analysis report",
                            "Reusable component library",
                            "Code refactoring changes"
                        ],
                        "status": "AVAILABLE",
                        "category": "Deduplication"
                    },
                    {
                        "contract_id": "MODULAR-001",
                        "title": "Monolithic File Modularization",
                        "description": "Break down large files (>500 LOC) into smaller, maintainable modules",
                        "difficulty": "HIGH",
                        "estimated_time": "4-5 hours",
                        "extra_credit_points": 500,
                        "requirements": [
                            "Identify monolithic files",
                            "Design modular architecture",
                            "Break down into smaller files",
                            "Update imports and references"
                        ],
                        "deliverables": [
                            "Modularization plan",
                            "Refactored code files",
                            "Updated import statements"
                        ],
                        "status": "AVAILABLE",
                        "category": "Modularization"
                    },
                    {
                        "contract_id": "SSOT-002",
                        "title": "Data Source Consolidation",
                        "description": "Consolidate scattered data sources into single authoritative locations",
                        "difficulty": "MEDIUM",
                        "estimated_time": "2-3 hours",
                        "extra_credit_points": 450,
                        "requirements": [
                            "Map all data sources",
                            "Identify authoritative locations",
                            "Create migration plan",
                            "Execute consolidation"
                        ],
                        "deliverables": [
                            "Data source mapping",
                            "Consolidation plan",
                            "Migration implementation"
                        ],
                        "status": "AVAILABLE",
                        "category": "SSOT_Resolution"
                    },
                    {
                        "contract_id": "DEDUP-002",
                        "title": "Function Duplication Elimination",
                        "description": "Identify and eliminate duplicate function implementations across modules",
                        "difficulty": "MEDIUM",
                        "estimated_time": "2-3 hours",
                        "extra_credit_points": 300,
                        "requirements": [
                            "Find duplicate functions",
                            "Create unified implementations",
                            "Update all references",
                            "Remove duplicates"
                        ],
                        "deliverables": [
                            "Duplication analysis",
                            "Unified function library",
                            "Reference updates"
                        ],
                        "status": "AVAILABLE",
                        "category": "Deduplication"
                    },
                    {
                        "contract_id": "MODULAR-002",
                        "title": "Class Hierarchy Refactoring",
                        "description": "Refactor large classes into smaller, focused components with clear responsibilities",
                        "difficulty": "MEDIUM",
                        "estimated_time": "3-4 hours",
                        "extra_credit_points": 400,
                        "requirements": [
                            "Analyze class responsibilities",
                            "Design component hierarchy",
                            "Refactor large classes",
                            "Update dependencies"
                        ],
                        "deliverables": [
                            "Class analysis report",
                            "Refactored components",
                            "Updated class hierarchy"
                        ],
                        "status": "AVAILABLE",
                        "category": "Modularization"
                    }
                ]
                
                # Add these contracts to the actual task list
                try:
                    # Load existing task list
                    task_list_path = "agent_workspaces/meeting/task_list.json"
                    if os.path.exists(task_list_path):
                        with open(task_list_path, 'r', encoding='utf-8') as f:
                            task_list = json.load(f)
                        
                        # Add new category for these contracts
                        if "SSOT_AND_DEDUP_CONTRACTS" not in task_list.get("contracts", {}):
                            task_list["contracts"]["SSOT_AND_DEDUP_CONTRACTS"] = {
                                "category": "SSOT_Resolution",
                                "manager": "Agent-6",
                                "contracts": []
                            }
                        
                        # Add contracts to the task list
                        for contract in real_contracts:
                            # Ensure contract has the right structure
                            contract_copy = contract.copy()
                            if "status" not in contract_copy:
                                contract_copy["status"] = "AVAILABLE"
                            task_list["contracts"]["SSOT_AND_DEDUP_CONTRACTS"]["contracts"].append(contract_copy)
                        
                        # Update statistics
                        task_list["total_contracts"] = task_list.get("total_contracts", 0) + len(real_contracts)
                        task_list["available_contracts"] = task_list.get("available_contracts", 0) + len(real_contracts)
                        
                        # Save updated task list
                        with open(task_list_path, 'w', encoding='utf-8') as f:
                            json.dump(task_list, f, indent=2, ensure_ascii=False)
                        
                        print(f"✅ Added {len(real_contracts)} contracts to task list")
                    else:
                        print("⚠️ Task list not found, using in-memory contracts only")
                except Exception as e:
                    print(f"⚠️ Warning: Could not update task list: {e}")
                    print("   Using in-memory contracts only")
                
                available_contracts = real_contracts
                print(f"✅ Created {len(real_contracts)} real problem-solving contracts for onboarding")
            
            print(f"📋 Found {len(available_contracts)} available contracts for assignment")
            
            # Create simplified onboarding messages for each agent
            onboarding_messages = {}
            
            for i in range(1, 9):  # Agents 1-8
                if i == 4:  # Skip Agent-4 (Captain)
                    continue
                    
                agent_id = f"Agent-{i}"
                
                # Assign a contract if available
                if available_contracts:
                    contract = available_contracts.pop(0)
                    contract_name = contract.get("title", contract.get("name", "Unknown Contract"))
                    points = contract.get("extra_credit_points", contract.get("points", 0))
                    category = contract.get("category", "General")
                    
                    # Create simplified onboarding message
                    message = f"""🚨 AGENT ONBOARDING: CONTRACT ASSIGNMENT & SYSTEM OVERVIEW

📋 YOUR CONTRACT: {contract_name} - {points} points
🎯 DELIVERABLE: Complete the assigned contract with high quality - this is REAL project work
⏰ TIMELINE: Complete immediately

📚 ONBOARDING DIRECTORY REVIEW:
- Review: D:\\Agent_Cellphone_V2_Repository\\onboarding\\
- This contains your training materials and system protocols
- Read through the documentation to understand your role
- Familiarize yourself with the project structure and standards

🔄 HOW YOU WORK WITH OTHER AGENTS:
- You're part of a multiagentic feedback loop
- Other agents will review your work and provide feedback
- You'll review other agents' work and provide feedback
- This creates continuous improvement and quality assurance
- Always communicate clearly about your progress and blockers

📝 DEVLOG SYSTEM (COMMAND LINE):
- Use: python -m src.core.devlog_cli --add "Your progress message here"
- Read other agents' devlogs: python -m src.core.devlog_cli --list
- Search devlogs: python -m src.core.devlog_cli --search "keyword"
- This is how we maintain transparency and coordination
- Update devlog with any blockers, discoveries, or completed work
- Other agents read your devlog to understand what you're working on

🔧 CODING STANDARDS & EXPECTATIONS:
- Use existing architecture before developing new solutions
- Write clean, readable, well-documented code
- Follow proper error handling and validation patterns
- Test your changes thoroughly

🚨 CRITICAL PROBLEMS TO FIX WHEN YOU SEE THEM:
1. SSOT VIOLATIONS: Multiple sources of truth for the same data
2. DUPLICATION: Repeated code that should be consolidated
3. MONOLITHIC FILES: Files over 500 lines that need modularization

📬 COMMUNICATION:
- Check your inbox regularly: D:\\Agent_Cellphone_V2_Repository\\agent_workspaces\\{agent_id}\\
- Respond to messages from other agents and the Captain
- Keep your inbox updated with your progress

📊 STATUS TRACKING:
- Create/update: D:\\Agent_Cellphone_V2_Repository\\agent_workspaces\\{agent_id}\\status.json
- Include: current_contract, progress, blockers, estimated_completion, last_updated
- Example: {{"current_contract": "{contract_name}", "progress": "25%", "blockers": "None", "estimated_completion": "2 hours", "last_updated": "2025-08-28 22:30"}}
- Update status.json every time you make progress or encounter blockers

⚡ IMMEDIATE ACTION:
1. Review your contract details
2. Start working immediately
3. Submit deliverables when complete
4. Claim your next contract

🚀 OBJECTIVE: Help restore system momentum and reach INNOVATION PLANNING MODE

📋 CONTRACT CLAIMING SYSTEM (COMMAND LINE):
- List contracts: python agent_workspaces/meeting/contract_claiming_system.py --list
- Claim contract: python agent_workspaces/meeting/contract_claiming_system.py --claim [CONTRACT_ID] --agent [YOUR_AGENT_ID]
- Update progress: python agent_workspaces/meeting/contract_claiming_system.py --update-progress [CONTRACT_ID] --agent [YOUR_AGENT_ID] --progress "50% Complete"
- Complete contract: python agent_workspaces/meeting/contract_claiming_system.py --complete [CONTRACT_ID] --agent [YOUR_AGENT_ID] --deliverables "Report, Plan, Code"
- Check status: python agent_workspaces/meeting/contract_claiming_system.py --status [CONTRACT_ID]
- Show stats: python agent_workspaces/meeting/contract_claiming_system.py --stats

💡 TIP: Use --help to see all available commands and examples!"""
                    
                    onboarding_messages[agent_id] = message
                    print(f"✅ {agent_id}: Assigned {contract_name} ({points} pts)")
                else:
                    print(f"⚠️ {agent_id}: No contracts available for assignment")
            
            # Send onboarding messages to all agents with new chat sequence
            print(f"\n📡 Sending onboarding messages to {len(onboarding_messages)} agents...")
            print("🚀 Using new chat sequence (Ctrl+N) for onboarding messages...")
            
            results = self.service.send_bulk_messages(onboarding_messages, "8-agent", new_chat=True)
            
            # Display results
            if isinstance(results, dict):
                success_count = sum(1 for success in results.values() if success)
                print(f"\n📊 Onboarding Results: {success_count}/{len(onboarding_messages)} successful")
                
                for agent_id, success in results.items():
                    status = "✅ Success" if success else "❌ Failed"
                    print(f"   {agent_id}: {status}")
            else:
                print(f"\n📊 Onboarding Results: {results}")
                success_count = len(onboarding_messages)  # Assume success if results format is unexpected
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Onboarding failed: {e}")
            print(f"❌ Onboarding failed: {e}")
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
                input_coords = agent_info.get("input_box", {}).get(
                    "coordinates", (None, None)
                )
                starter_coords = agent_info.get("starter_location", {}).get(
                    "coordinates", (None, None)
                )
                valid = agent_info.get("overall_valid", False)

                status = "✅" if valid else "❌"
                print(f"{status} {agent_id}:")
                print(f"    Input Box: ({input_coords[0]}, {input_coords[1]})")
                print(
                    f"    Starter Location: ({starter_coords[0]}, {starter_coords[1]})"
                )
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

            print(
                f"📁 Primary File: {consolidation_results.get('primary_file', 'Unknown')}"
            )
            print(
                f"📥 Sources Found: {len(consolidation_results.get('sources_found', []))}"
            )

            for source in consolidation_results.get("sources_found", []):
                print(f"    - {source}")

            print(
                f"✅ Sources Merged: {len(consolidation_results.get('sources_merged', []))}"
            )

            conflicts = consolidation_results.get("conflicts", [])
            if conflicts:
                print(f"⚠️  Conflicts Found: {len(conflicts)}")
                for conflict in conflicts:
                    print(f"    - {conflict['agent']} in {conflict['mode']} mode")
            else:
                print("✅ No conflicts found")

            final_coords = consolidation_results.get("final_coordinates", {})
            total_agents = sum(len(agents) for agents in final_coords.values())
            print(
                f"📊 Final Result: {len(final_coords)} modes, {total_agents} agent configurations"
            )

            return True
        except Exception as e:
            logger.error(f"Coordinate consolidation failed: {e}")
            return False

    def _handle_coordinate_calibration(self, calibrate_args: list) -> bool:
        """Handle coordinate calibration"""
        try:
            if len(calibrate_args) != 5:
                print(
                    "❌ Calibration requires exactly 5 arguments: Agent ID, Input X, Input Y, Starter X, Starter Y"
                )
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
                agent_id, (input_x, input_y), (starter_x, starter_y)
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

            sys.path.append(os.path.join(os.getcwd(), "agent_workspaces", "meeting"))

            # Use the correct path for task_list.json
            task_list_path = os.path.join(
                os.getcwd(), "agent_workspaces", "meeting", "task_list.json"
            )
            system = ContractClaimingSystem(task_list_path)
            result = system.claim_contract(contract_id, agent_id)

            if result["success"]:
                print(f"✅ {result['message']}")
                print(f"📊 Contract: {result['contract']['title']}")
                print(f"⏱️  Estimated Time: {result['contract']['estimated_time']}")
                print(
                    f"🏆 Extra Credit: {result['contract']['extra_credit_points']} points"
                )
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
                print(
                    "❌ Agent ID required for contract completion. Use --agent Agent-X"
                )
                return False

            print(f"🎯 Completing contract {contract_id} for {agent_id}...")

            # Import contract system

            sys.path.append(os.path.join(os.getcwd(), "agent_workspaces", "meeting"))

            # Use the correct path for task_list.json
            task_list_path = os.path.join(
                os.getcwd(), "agent_workspaces", "meeting", "task_list.json"
            )
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

            sys.path.append(os.path.join(os.getcwd(), "agent_workspaces", "meeting"))

            # Use the correct path for task_list.json
            task_list_path = os.path.join(
                os.getcwd(), "agent_workspaces", "meeting", "task_list.json"
            )
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
                CAPTAIN_ID: "strategic_oversight",
                "Agent-5": "refactoring_tool_preparation",
                "Agent-6": "performance_optimization",
                "Agent-7": "quality_completion_optimization",
                "Agent-8": "integration_enhancement_optimization",
            }

            agent_role = agent_roles.get(agent_id, "general")

            # Prioritize contracts matching agent's role
            priority_contracts = [
                c
                for c in available
                if c.get("category", "").lower() == agent_role.lower()
            ]
            other_contracts = [
                c
                for c in available
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
            print(f"\n💡 To claim this task, run:")
            print(
                f"   python -m src.services.messaging --agent {agent_id} --claim-contract {next_contract['contract_id']}"
            )

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

            sys.path.append(os.path.join(os.getcwd(), "agent_workspaces", "meeting"))

            # Use the correct path for task_list.json
            task_list_path = os.path.join(
                os.getcwd(), "agent_workspaces", "meeting", "task_list.json"
            )
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
                print(
                    "❌ Message content required for Captain communication. Use --message 'Your message'"
                )
                return False

            # Determine which agent is sending the message
            agent_id = args.agent if args.agent else "UNKNOWN_AGENT"

            # Create enhanced message with agent identification and contract generation prompt
            enhanced_message = f"🎯 CAPTAIN MESSAGE FROM {agent_id}: {args.message}\n\n📋 CAPTAIN ACTION REQUIRED:\n1) Review this agent's message and status\n2) Create additional contracts if needed\n3) Message all agents that new contracts are available\n4) Ensure continuous work cycle maintenance"

            print(f"🎯 Sending Captain message from {agent_id}...")
            print(f"📝 Enhanced message: {enhanced_message}")

            # Send message to Captain
            success = self.service.send_message(
                CAPTAIN_ID,
                enhanced_message,
                MessageType.TEXT,
                MessagingMode.PYAUTOGUI,
                False,
            )

            if success:
                print(f"✅ Captain message sent successfully from {agent_id}")
                print(
                    f"📋 Captain will receive enhanced prompt for contract generation and agent messaging"
                )
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
                    print(
                        "🎯 Perpetual motion system restored - all agents should resume workflow"
                    )
                    return True
                else:
                    print(
                        "⚠️ Resume system partially activated - some messages may have failed"
                    )
                    return False
            else:
                print(
                    "⏰ Resume message sent recently - waiting for next cycle (10 message minimum interval)"
                )
                print(
                    "💡 Use --resume-captain or --resume-agents for immediate individual messages"
                )
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

            # Send message to Captain
            success = self.service.send_message(
                CAPTAIN_ID,
                captain_message,
                MessageType.TEXT,
                MessagingMode.PYAUTOGUI,
                False,
            )

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
            messages = {f"Agent-{i}": agent_message for i in range(1, AGENT_COUNT + 1)}
            results = self.service.send_bulk_messages(
                messages, DEFAULT_COORDINATE_MODE, MessageType.TEXT, False
            )

            print("📊 Agent Resume Message Results:")
            success_count = 0
            for agent_id, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"  {agent_id}: {status}")
                if success:
                    success_count += 1

            if success_count >= 6:  # At least 6 out of 8 agents
                print(
                    f"✅ Agent resume messages sent successfully to {success_count}/8 agents"
                )
                return True
            else:
                print(
                    f"⚠️ Agent resume messages partially successful: {success_count}/8 agents"
                )
                return False

        except Exception as e:
            logger.error(f"Agent resume message failed: {e}")
            return False

    def _should_send_resume_message(self) -> bool:
        """Check if enough time has passed since last resume message"""
        try:

            counter_file = "resume_message_counter.json"

            if not os.path.exists(counter_file):
                return True  # First time, allow message

            with open(counter_file, "r") as f:
                data = json.load(f)

            last_message_time = datetime.fromisoformat(
                data.get("last_message_time", "2000-01-01T00:00:00")
            )
            message_count = data.get("message_count", 0)

            # Allow message if 10+ messages have been sent since last resume
            # or if more than 1 hour has passed
            time_since_last = datetime.now() - last_message_time
            messages_since_last = message_count - data.get(
                "last_resume_message_count", 0
            )

            if messages_since_last >= 10 or time_since_last > timedelta(hours=1):
                return True

            return False

        except Exception as e:
            logger.error(f"Error checking resume message frequency: {e}")
            return True  # Default to allowing message if check fails

    def _update_resume_message_counter(self):
        """Update the resume message counter after sending"""
        try:

            counter_file = "resume_message_counter.json"

            # Load existing data or create new
            if os.path.exists(counter_file):
                with open(counter_file, "r") as f:
                    data = json.load(f)
            else:
                data = {"message_count": 0, "last_message_time": "2000-01-01T00:00:00"}

            # Update counters
            data["last_resume_message_time"] = datetime.now().isoformat()
            data["last_resume_message_count"] = data.get("message_count", 0)

            # Save updated data
            with open(counter_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logger.error(f"Error updating resume message counter: {e}")

    def _handle_status_check(self) -> bool:
        """Handle checking all agent statuses from their status.json files"""
        try:
            print("📊 AGENT STATUS CHECK: Checking all agent statuses...")
            print("=" * 80)
            
            
            status_results = {}
            total_agents = 0
            active_agents = 0
            
            for i in range(1, 9):  # Agents 1-8
                if i == 4:  # Skip Agent-4 (Captain)
                    continue
                    
                agent_id = f"Agent-{i}"
                total_agents += 1
                
                status_file_path = f"agent_workspaces/{agent_id}/status.json"
                
                if os.path.exists(status_file_path):
                    try:
                        with open(status_file_path, "r") as f:
                            status_data = json.load(f)
                        
                        status_results[agent_id] = status_data
                        active_agents += 1
                        
                        # Display agent status
                        current_contract = status_data.get("current_contract", "Unknown")
                        progress = status_data.get("progress", "Unknown")
                        blockers = status_data.get("blockers", "None")
                        estimated_completion = status_data.get("estimated_completion", "Unknown")
                        last_updated = status_data.get("last_updated", "Unknown")
                        
                        print(f"✅ {agent_id}:")
                        print(f"   📋 Contract: {current_contract}")
                        print(f"   📊 Progress: {progress}")
                        print(f"   🚧 Blockers: {blockers}")
                        print(f"   ⏰ ETA: {estimated_completion}")
                        print(f"   🕒 Last Updated: {last_updated}")
                        print()
                        
                    except Exception as e:
                        print(f"❌ {agent_id}: Error reading status.json - {e}")
                        status_results[agent_id] = {"error": str(e)}
                else:
                    print(f"⚠️ {agent_id}: No status.json found - agent may be inactive")
                    status_results[agent_id] = {"status": "inactive"}
                    print()
            
            # Display summary
            print("=" * 80)
            print(f"📊 STATUS SUMMARY:")
            print(f"   Total Agents: {total_agents}")
            print(f"   Active Agents: {active_agents}")
            print(f"   Inactive Agents: {total_agents - active_agents}")
            
            if active_agents > 0:
                print(f"\n🎯 ACTIVE AGENTS: {', '.join([k for k, v in status_results.items() if 'error' not in v and v.get('status') != 'inactive'])}")
            
            return True
            
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            print(f"❌ Status check failed: {e}")
            return False
