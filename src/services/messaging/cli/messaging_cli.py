#!/usr/bin/env python3
"""
Unified Messaging CLI - V2 Compliant Command Interface
=====================================================

V2 compliant command-line interface for unified messaging system.
Consolidates all CLI functionality into a single, maintainable module.

V2 Compliance: <300 lines, single responsibility for CLI operations
Enterprise Ready: Comprehensive command support, error handling, help

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from src.services.messaging.unified_service import (
        UnifiedMessagingService,
        get_unified_messaging_service,
        send_message_to_agent,
        broadcast_to_swarm,
        get_messaging_status,
    )
    MESSAGING_AVAILABLE = True
except ImportError as e:
    logging.error(f"❌ Messaging service not available: {e}")
    MESSAGING_AVAILABLE = False

logger = logging.getLogger(__name__)

# Constants
SWARM_AGENTS = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
]

CLI_HELP_EPILOG = """
🐝 UNIFIED MESSAGING CLI - SWARM COMMAND CENTER
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging.cli.messaging_cli --message "Start survey" --agent Agent-1

# Broadcast to all agents
python -m src.services.messaging.cli.messaging_cli --message "SWARM ALERT!" --broadcast

# Send with priority and tags
python -m src.services.messaging.cli.messaging_cli --message "URGENT: Fix issue" --agent Agent-2 --priority urgent

# Show system status
python -m src.services.messaging.cli.messaging_cli --status

# List available agents
python -m src.services.messaging.cli.messaging_cli --list-agents

🐝 WE. ARE. SWARM - UNIFIED MESSAGING SYSTEM!
"""

class UnifiedMessagingCLI:
    """V2 compliant unified messaging CLI."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.parser = self._create_parser()
        self.messaging_service = get_unified_messaging_service() if MESSAGING_AVAILABLE else None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="🐝 Unified Messaging CLI - Command the swarm through unified messaging",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=CLI_HELP_EPILOG,
        )
        
        # Core messaging arguments
        parser.add_argument("--message", "-m", type=str, help="Message content to send")
        parser.add_argument("--agent", "-a", type=str, help="Target agent ID (e.g., Agent-1, Agent-2)")
        parser.add_argument("--broadcast", "-b", action="store_true", help="Broadcast message to all agents")
        
        # Message options
        parser.add_argument("--priority", "-p", choices=["normal", "urgent"], default="normal",
                          help="Message priority (default: normal)")
        parser.add_argument("--tag", "-t", choices=["general", "coordination", "system", "onboarding"],
                          default="general", help="Message tag for categorization")
        
        # System commands
        parser.add_argument("--status", action="store_true", help="Show messaging system status")
        parser.add_argument("--list-agents", "-l", action="store_true", help="List available agents")
        parser.add_argument("--metrics", action="store_true", help="Show messaging metrics")
        parser.add_argument("--health-check", action="store_true", help="Perform health check")
        
        # Operational options
        parser.add_argument("--dry-run", action="store_true", help="Dry run mode (no actual sending)")
        parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
        
        return parser
    
    def execute(self, args: Optional[List[str]] = None) -> int:
        """Execute the CLI with given arguments."""
        if not MESSAGING_AVAILABLE:
            logger.error("❌ Messaging system not available")
            return 1
        
        try:
            parsed_args = self.parser.parse_args(args)
            
            # Configure logging
            if parsed_args.verbose:
                logging.basicConfig(level=logging.DEBUG)
            else:
                logging.basicConfig(level=logging.INFO)
            
            # Set dry run mode
            if parsed_args.dry_run:
                self.messaging_service.dry_run = True
                logger.info("🔍 DRY RUN MODE ENABLED")
            
            # Execute commands
            if parsed_args.status:
                return self._handle_status()
            elif parsed_args.list_agents:
                return self._handle_list_agents()
            elif parsed_args.metrics:
                return self._handle_metrics()
            elif parsed_args.health_check:
                return self._handle_health_check()
            elif parsed_args.broadcast:
                return self._handle_broadcast(parsed_args)
            elif parsed_args.agent and parsed_args.message:
                return self._handle_send_message(parsed_args)
            else:
                self.parser.print_help()
                return 0
                
        except Exception as e:
            logger.error(f"❌ CLI execution error: {e}")
            return 1
    
    def _handle_status(self) -> int:
        """Handle status command."""
        try:
            status = get_messaging_status()
            print("📊 MESSAGING SYSTEM STATUS")
            print("=" * 40)
            print(f"Service Available: {'✅' if status['service_available'] else '❌'}")
            print(f"Dry Run Mode: {'✅' if status['dry_run_mode'] else '❌'}")
            print(f"Available Agents: {status['available_agents']}")
            print(f"Last Activity: {status['last_activity'] or 'None'}")
            print(f"Total Messages: {status['metrics']['total_messages_sent']}")
            print(f"Successful: {status['metrics']['successful_deliveries']}")
            print(f"Failed: {status['metrics']['failed_deliveries']}")
            return 0
        except Exception as e:
            logger.error(f"❌ Status check failed: {e}")
            return 1
    
    def _handle_list_agents(self) -> int:
        """Handle list agents command."""
        try:
            agents = self.messaging_service.list_available_agents()
            print("🤖 AVAILABLE AGENTS")
            print("=" * 30)
            for agent in agents:
                print(f"  • {agent}")
            print(f"\nTotal: {len(agents)} agents")
            return 0
        except Exception as e:
            logger.error(f"❌ List agents failed: {e}")
            return 1
    
    def _handle_metrics(self) -> int:
        """Handle metrics command."""
        try:
            metrics = self.messaging_service.get_metrics()
            print("📈 MESSAGING METRICS")
            print("=" * 30)
            print(f"Total Messages Sent: {metrics['total_messages_sent']}")
            print(f"Successful Deliveries: {metrics['successful_deliveries']}")
            print(f"Failed Deliveries: {metrics['failed_deliveries']}")
            print(f"Last Activity: {metrics['last_activity'] or 'None'}")
            
            # Calculate success rate
            total = metrics['total_messages_sent']
            if total > 0:
                success_rate = (metrics['successful_deliveries'] / total) * 100
                print(f"Success Rate: {success_rate:.1f}%")
            return 0
        except Exception as e:
            logger.error(f"❌ Metrics retrieval failed: {e}")
            return 1
    
    def _handle_health_check(self) -> int:
        """Handle health check command."""
        try:
            health = self.messaging_service.health_check()
            print("🏥 HEALTH CHECK")
            print("=" * 20)
            print(f"Status: {'✅ HEALTHY' if health['status'] == 'healthy' else '❌ UNHEALTHY'}")
            print(f"Service Available: {'✅' if health['service_available'] else '❌'}")
            print(f"Core Available: {'✅' if health['core_available'] else '❌'}")
            print(f"Timestamp: {health['timestamp']}")
            
            if health['status'] != 'healthy':
                print(f"Error: {health.get('error', 'Unknown error')}")
                return 1
            return 0
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return 1
    
    def _handle_broadcast(self, args) -> int:
        """Handle broadcast command."""
        if not args.message:
            logger.error("❌ Message required for broadcast")
            return 1
        
        try:
            results = broadcast_to_swarm(
                message=args.message,
                priority=args.priority.upper(),
                tag=args.tag.upper()
            )
            
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            print(f"📢 BROADCAST RESULTS")
            print("=" * 25)
            print(f"Message: {args.message}")
            print(f"Priority: {args.priority}")
            print(f"Tag: {args.tag}")
            print(f"Results: {successful}/{total} successful")
            
            if successful > 0:
                logger.info(f"✅ Broadcast sent to {successful}/{total} agents")
                return 0
            else:
                logger.error(f"❌ Broadcast failed to all agents")
                return 1
                
        except Exception as e:
            logger.error(f"❌ Broadcast failed: {e}")
            return 1
    
    def _handle_send_message(self, args) -> int:
        """Handle send message command."""
        try:
            success = send_message_to_agent(
                agent_id=args.agent,
                message=args.message,
                priority=args.priority.upper(),
                tag=args.tag.upper()
            )
            
            print(f"📨 MESSAGE SENT")
            print("=" * 20)
            print(f"To: {args.agent}")
            print(f"Message: {args.message}")
            print(f"Priority: {args.priority}")
            print(f"Tag: {args.tag}")
            print(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
            
            if success:
                logger.info(f"✅ Message sent to {args.agent}")
                return 0
            else:
                logger.error(f"❌ Failed to send message to {args.agent}")
                return 1
                
        except Exception as e:
            logger.error(f"❌ Send message failed: {e}")
            return 1

def main() -> int:
    """Main entry point."""
    cli = UnifiedMessagingCLI()
    return cli.execute()

if __name__ == "__main__":
    exit_code = main()
    print()  # Add line break
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
    sys.exit(exit_code)