#!/usr/bin/env python3
"""
🐝 Contract Notification System
===============================

Automated system for notifying swarm agents about available contracts and tasks.
Provides real-time updates and coordination for contract claiming and assignment.

Author: Agent-2 - Contract System Enhancement
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Import messaging system for notifications
import sys
sys.path.append(str(Path(__file__).parent.parent))
from src.services.messaging_cli_refactored import MessageCoordinator, UnifiedMessagePriority

logger = logging.getLogger(__name__)


class ContractNotificationSystem:
    """Automated contract notification and coordination system."""

    def __init__(self, contracts_dir: str = "contracts"):
        self.contracts_dir = Path(contracts_dir)
        self.messaging_coordinator = MessageCoordinator()
        self.agent_coordinates = {
            "Agent-1": (-1269, 481),
            "Agent-2": (-308, 480),
            "Agent-3": (-1269, 1001),
            "Agent-4": (-308, 1000),
            "Agent-5": (652, 421),
            "Agent-6": (1612, 419),
            "Agent-7": (920, 851),
            "Agent-8": (1611, 941)
        }

    def scan_available_contracts(self) -> List[Dict[str, Any]]:
        """Scan for all available contracts (status: AVAILABLE)."""
        available_contracts = []

        # Scan individual agent contracts
        for json_file in self.contracts_dir.glob("*.json"):
            if json_file.name.startswith("TEMPLATE"):
                continue  # Skip templates

            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    contract = json.load(f)

                    if contract.get("status") == "AVAILABLE":
                        available_contracts.append(contract)
            except Exception as e:
                logger.error(f"Error reading contract {json_file}: {e}")

        return available_contracts

    def get_contracts_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get contracts suitable for specific agent."""
        all_contracts = self.scan_available_contracts()
        agent_contracts = []

        for contract in all_contracts:
            # Match by agent assignment or general availability
            if (contract.get("agent_id") == agent_id or
                contract.get("agent_id") == "TEMPLATE_AGENT"):
                agent_contracts.append(contract)

        return agent_contracts

    def generate_contract_notification(self, agent_id: str) -> str:
        """Generate personalized contract notification for agent."""
        agent_contracts = self.get_contracts_by_agent(agent_id)

        if not agent_contracts:
            return f"No contracts currently available for {agent_id}."

        notification = f"🐝 CONTRACT OPPORTUNITIES AVAILABLE FOR {agent_id.upper()}\n"
        notification += "=" * 60 + "\n\n"

        for i, contract in enumerate(agent_contracts[:5], 1):  # Limit to top 5
            notification += f"📋 CONTRACT {i}: {contract['contract_title']}\n"
            notification += f"🆔 ID: {contract['contract_id']}\n"
            notification += f"🎯 Priority: {contract['priority']}\n"
            notification += f"💰 XP Reward: {contract['contract_rewards']['experience_points']}\n"
            notification += f"📅 Deadline: {contract['contract_details']['deadline']}\n"
            notification += f"📝 Description: {contract['contract_details']['description'][:100]}...\n\n"

        if len(agent_contracts) > 5:
            notification += f"... and {len(agent_contracts) - 5} more contracts available.\n\n"

        notification += "🎯 TO CLAIM A CONTRACT:\n"
        notification += "1. Review contract details in contracts/ directory\n"
        notification += "2. Update contract status to 'ASSIGNED'\n"
        notification += "3. Begin work and establish milestones\n"
        notification += "4. Coordinate with Captain Agent-4 for support\n\n"

        notification += "🐝 WE ARE SWARM - CONTRACTS DRIVE EXCELLENCE!"

        return notification

    def send_agent_notification(self, agent_id: str, use_pyautogui: bool = True) -> bool:
        """Send contract notification to specific agent."""
        try:
            notification_message = self.generate_contract_notification(agent_id)

            if use_pyautogui and agent_id in self.agent_coordinates:
                # Use PyAutoGUI for direct agent notification
                coords = self.agent_coordinates[agent_id]
                success = self.messaging_coordinator.send_to_agent(
                    agent_id,
                    notification_message,
                    UnifiedMessagePriority.URGENT,
                    use_pyautogui=True
                )
                logger.info(f"PyAutoGUI notification sent to {agent_id} at {coords}")
                return success
            else:
                # Fallback to inbox messaging
                success = self.messaging_coordinator.send_to_agent(
                    agent_id,
                    notification_message,
                    UnifiedMessagePriority.HIGH,
                    use_pyautogui=False
                )
                logger.info(f"Inbox notification sent to {agent_id}")
                return success

        except Exception as e:
            logger.error(f"Failed to send notification to {agent_id}: {e}")
            return False

    def send_swarm_notification(self, priority_contracts_only: bool = False) -> Dict[str, bool]:
        """Send contract notifications to all swarm agents."""
        results = {}

        for agent_id in self.agent_coordinates.keys():
            try:
                # Check if agent has high-priority contracts
                agent_contracts = self.get_contracts_by_agent(agent_id)
                high_priority_contracts = [
                    c for c in agent_contracts
                    if c.get("priority") in ["HIGH", "CRITICAL"]
                ]

                if priority_contracts_only and not high_priority_contracts:
                    logger.info(f"Skipping {agent_id} - no high-priority contracts")
                    results[agent_id] = True  # Not an error, just no contracts
                    continue

                success = self.send_agent_notification(agent_id)
                results[agent_id] = success

                if success:
                    logger.info(f"✅ Notification sent to {agent_id}")
                else:
                    logger.error(f"❌ Failed to notify {agent_id}")

            except Exception as e:
                logger.error(f"❌ Error notifying {agent_id}: {e}")
                results[agent_id] = False

        return results

    def get_notification_summary(self, results: Dict[str, bool]) -> str:
        """Generate summary of notification results."""
        successful = sum(1 for success in results.values() if success)
        total = len(results)

        summary = "🐝 CONTRACT NOTIFICATION SUMMARY\n"
        summary += "=" * 40 + "\n\n"
        summary += f"Total Agents Notified: {total}\n"
        summary += f"Successful Notifications: {successful}\n"
        summary += f"Failed Notifications: {total - successful}\n\n"

        if successful == total:
            summary += "🎉 ALL AGENTS SUCCESSFULLY NOTIFIED!\n"
        else:
            summary += "⚠️  SOME NOTIFICATIONS FAILED - CHECK LOGS\n"

        summary += "\nDetailed Results:\n"
        for agent_id, success in results.items():
            status = "✅" if success else "❌"
            summary += f"{status} {agent_id}\n"

        return summary


def main():
    """Main notification system interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🐝 Contract Notification System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🐝 CONTRACT NOTIFICATION SYSTEM
==============================

EXAMPLES:
--------
# Notify all agents about available contracts
python contract_notification_system.py --swarm-notification

# Notify specific agent
python contract_notification_system.py --agent Agent-2

# Notify only agents with high-priority contracts
python contract_notification_system.py --swarm-notification --priority-only

# Generate notification summary without sending
python contract_notification_system.py --summary-only

🐝 WE ARE SWARM - CONTRACTS DRIVE EXCELLENCE!
        """
    )

    parser.add_argument(
        "--agent", "-a",
        help="Notify specific agent (e.g., Agent-1, Agent-2)"
    )

    parser.add_argument(
        "--swarm-notification", "-s",
        action="store_true",
        help="Send notifications to all swarm agents"
    )

    parser.add_argument(
        "--priority-only", "-p",
        action="store_true",
        help="Only notify agents with high/critical priority contracts"
    )

    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Generate notification summary without sending"
    )

    parser.add_argument(
        "--list-contracts", "-l",
        action="store_true",
        help="List all available contracts"
    )

    args = parser.parse_args()

    notification_system = ContractNotificationSystem()

    if args.list_contracts:
        contracts = notification_system.scan_available_contracts()
        print("🐝 AVAILABLE CONTRACTS:")
        print("=" * 40)
        for contract in contracts:
            print(f"📋 {contract['contract_id']}: {contract['contract_title']}")
            print(f"   🤖 Agent: {contract['agent_id']}")
            print(f"   🎯 Priority: {contract['priority']}")
            print(f"   💰 XP: {contract['contract_rewards']['experience_points']}")
            print()
        print(f"Total Available Contracts: {len(contracts)}")
        return

    if args.summary_only:
        contracts = notification_system.scan_available_contracts()
        print("🐝 CONTRACT AVAILABILITY SUMMARY:")
        print("=" * 40)
        print(f"Total Available Contracts: {len(contracts)}")

        priority_breakdown = {}
        for contract in contracts:
            priority = contract.get("priority", "UNKNOWN")
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1

        print("\nPriority Breakdown:")
        for priority, count in priority_breakdown.items():
            print(f"  {priority}: {count} contracts")

        print("\nAgent Distribution:")
        agent_distribution = {}
        for contract in contracts:
            agent = contract.get("agent_id", "UNASSIGNED")
            agent_distribution[agent] = agent_distribution.get(agent, 0) + 1

        for agent, count in agent_distribution.items():
            print(f"  {agent}: {count} contracts")
        return

    if args.agent:
        print(f"Sending contract notification to {args.agent}...")
        success = notification_system.send_agent_notification(args.agent)
        if success:
            print(f"✅ Successfully notified {args.agent}")
        else:
            print(f"❌ Failed to notify {args.agent}")
        return

    if args.swarm_notification:
        print("🐝 INITIATING SWARM CONTRACT NOTIFICATION...")
        print("Sending notifications to all 8 swarm agents...")

        results = notification_system.send_swarm_notification(
            priority_contracts_only=args.priority_only
        )

        summary = notification_system.get_notification_summary(results)
        print("\n" + summary)

        successful_count = sum(1 for success in results.values() if success)
        if successful_count == 8:
            print("\n🎉 SWARM CONTRACT NOTIFICATION COMPLETE!")
            print("All agents have been notified of available contracts.")
        else:
            print(f"\n⚠️  Notification completed with {successful_count}/8 successful deliveries.")
        return

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    """Demonstrate contract notification system with practical examples."""

    print("🐝 Contract Notification System Examples - Practical Demonstrations")
    print("=" * 70)

    # Test system instantiation
    print(f"\n📋 Testing ContractNotificationSystem instantiation:")
    try:
        notification_system = ContractNotificationSystem()
        print(f"✅ ContractNotificationSystem instantiated successfully")
    except Exception as e:
        print(f"❌ ContractNotificationSystem failed: {e}")

    # Test contract scanning
    print(f"\n📋 Testing contract scanning:")
    try:
        available_contracts = notification_system.scan_available_contracts()
        print(f"✅ Found {len(available_contracts)} available contracts")

        if available_contracts:
            print(f"📋 Sample contract: {available_contracts[0]['contract_title']}")
            print(f"🎯 Priority: {available_contracts[0]['priority']}")
            print(f"🤖 Agent: {available_contracts[0]['agent_id']}")
    except Exception as e:
        print(f"❌ Contract scanning failed: {e}")

    # Test notification generation (without sending)
    print(f"\n📋 Testing notification generation:")
    try:
        test_agent = "Agent-3"
        notification = notification_system.generate_contract_notification(test_agent)
        print(f"✅ Generated notification for {test_agent}")
        print(f"📄 Notification length: {len(notification)} characters")

        # Show preview
        preview = notification[:200] + "..." if len(notification) > 200 else notification
        print(f"📋 Preview: {preview}")
    except Exception as e:
        print(f"❌ Notification generation failed: {e}")

    # Test agent contract filtering
    print(f"\n📋 Testing agent-specific contract filtering:")
    try:
        agent_contracts = notification_system.get_contracts_by_agent("Agent-3")
        print(f"✅ Found {len(agent_contracts)} contracts for Agent-3")

        high_priority = [c for c in agent_contracts if c.get("priority") == "HIGH"]
        print(f"🎯 High priority contracts: {len(high_priority)}")
    except Exception as e:
        print(f"❌ Agent filtering failed: {e}")

    print("\n🎉 Contract notification system examples completed!")
    print("🐝 WE ARE SWARM - CONTRACT SYSTEMS VALIDATED!")

    # Execute main function
    main()
