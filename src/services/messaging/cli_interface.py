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
        
        # Coordinate validation
        parser.add_argument("--validate", action="store_true", help="Validate coordinates")
        
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
        return True
    
    def _handle_bulk_messaging(self, args: argparse.Namespace, mode: MessagingMode) -> bool:
        """Handle bulk messaging operations"""
        print(f"📡 Bulk messaging via {mode.value}...")
        
        # Check for high priority flag
        if args.high_priority:
            print("🚨 HIGH PRIORITY bulk messaging detected - using Ctrl+Enter 2x sequence!")
            message_type = MessageType.HIGH_PRIORITY
        else:
            message_type = MessageType.TEXT
        
        messages = {f"Agent-{i}": args.message for i in range(1, 9)}
        results = self.service.send_bulk_messages(messages, "8-agent", message_type)
        
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
        
        # Check for high priority flag
        if args.high_priority:
            print("🚨 HIGH PRIORITY message detected - using Ctrl+Enter 2x sequence!")
            # Override message type to high priority
            message_type = MessageType.HIGH_PRIORITY
        
        success = self.service.send_message(args.agent, args.message, message_type, mode)
        
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
                return self._handle_bulk_messaging(args, MessagingMode(args.mode))
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
