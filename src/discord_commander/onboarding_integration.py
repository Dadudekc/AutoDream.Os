#!/usr/bin/env python3
"""
Discord Commander Onboarding Integration - V2 Compliant
======================================================

Integrates the unified onboarding service with Discord Commander
for seamless onboarding management through Discord commands.

Features:
- Discord command handling for onboarding
- Real-time onboarding status updates
- Agent state monitoring
- Contract management via Discord
- V2 compliance (≤400 lines)

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class DiscordOnboardingIntegration:
    """Discord Commander integration for unified onboarding service."""

    def __init__(self, discord_commander, onboarding_service):
        self.discord_commander = discord_commander
        self.onboarding_service = onboarding_service
        self.command_handlers = {
            "onboard": self._handle_onboard_command,
            "onboard_all": self._handle_onboard_all_command,
            "onboarding_status": self._handle_status_command,
            "agent_state": self._handle_agent_state_command,
            "contracts": self._handle_contracts_command,
            "reset_agent": self._handle_reset_agent_command,
        }

    async def handle_discord_command(self, command: str, args: dict[str, Any] = None) -> str:
        """Handle Discord commands for onboarding management."""
        try:
            if not args:
                args = {}

            command_parts = command.lower().split()
            base_command = command_parts[0] if command_parts else ""

            if base_command in self.command_handlers:
                return await self.command_handlers[base_command](args)
            else:
                return self._get_help_message()

        except Exception as e:
            logger.error(f"Discord onboarding command failed: {e}")
            return f"❌ Command failed: {e}"

    async def _handle_onboard_command(self, args: dict[str, Any]) -> str:
        """Handle individual agent onboarding command."""
        agent_id = args.get("agent_id")
        if not agent_id:
            return "❌ Please specify agent_id. Usage: onboard <agent_id>"

        if agent_id not in self.onboarding_service.agent_roles:
            return f"❌ Unknown agent: {agent_id}. Available agents: {list(self.onboarding_service.agent_roles.keys())}"

        try:
            success = await self.onboarding_service.perform_agent_onboarding(agent_id)
            if success:
                return f"✅ Agent {agent_id} onboarded successfully!"
            else:
                return f"❌ Failed to onboard agent {agent_id}"
        except Exception as e:
            return f"❌ Onboarding error for {agent_id}: {e}"

    async def _handle_onboard_all_command(self, args: dict[str, Any]) -> str:
        """Handle onboard all agents command."""
        try:
            results = await self.onboarding_service.onboard_all_agents()
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)

            if success_count == total_count:
                return f"🎉 All {total_count} agents onboarded successfully!"
            else:
                failed_agents = [agent for agent, success in results.items() if not success]
                return f"⚠️ Onboarding complete: {success_count}/{total_count} agents onboarded. Failed: {', '.join(failed_agents)}"
        except Exception as e:
            return f"❌ Bulk onboarding failed: {e}"

    async def _handle_status_command(self, args: dict[str, Any]) -> str:
        """Handle onboarding status command."""
        try:
            states = {}
            contracts = {}

            for agent_id in self.onboarding_service.agent_roles.keys():
                state = self.onboarding_service.get_agent_state(agent_id)
                contract = self.onboarding_service.get_agent_contract(agent_id)

                states[agent_id] = state.value if state else "unknown"
                contracts[agent_id] = contract.status if contract else "none"

            status_message = "📊 **Onboarding Status Report**\n\n"
            for agent_id, state in states.items():
                contract_status = contracts[agent_id]
                status_emoji = "✅" if state == "idle" else "🔄" if state == "onboarding" else "❌"
                status_message += (
                    f"{status_emoji} **{agent_id}**: {state} (Contract: {contract_status})\n"
                )

            return status_message
        except Exception as e:
            return f"❌ Failed to get status: {e}"

    async def _handle_agent_state_command(self, args: dict[str, Any]) -> str:
        """Handle agent state query command."""
        agent_id = args.get("agent_id")
        if not agent_id:
            return "❌ Please specify agent_id. Usage: agent_state <agent_id>"

        if agent_id not in self.onboarding_service.agent_roles:
            return f"❌ Unknown agent: {agent_id}"

        try:
            state = self.onboarding_service.get_agent_state(agent_id)
            contract = self.onboarding_service.get_agent_contract(agent_id)
            role = self.onboarding_service.agent_roles.get(agent_id, "Unknown")

            state_message = f"🤖 **Agent {agent_id} Status**\n\n"
            state_message += f"**Role**: {role}\n"
            state_message += f"**State**: {state.value if state else 'unknown'}\n"

            if contract:
                state_message += f"**Contract**: {contract.contract_type.value}\n"
                state_message += f"**Status**: {contract.status}\n"
                state_message += f"**Progress**: {contract.progress_percentage}%\n"
            else:
                state_message += "**Contract**: None\n"

            return state_message
        except Exception as e:
            return f"❌ Failed to get agent state: {e}"

    async def _handle_contracts_command(self, args: dict[str, Any]) -> str:
        """Handle contracts overview command."""
        try:
            contracts_message = "📋 **Active Contracts Overview**\n\n"

            active_contracts = 0
            for agent_id, contract in self.onboarding_service.contracts.items():
                if contract and contract.status in ["active", "pending"]:
                    active_contracts += 1
                    contracts_message += (
                        f"📄 **{agent_id}**: {contract.contract_type.value} ({contract.status})\n"
                    )
                    contracts_message += f"   └─ Progress: {contract.progress_percentage}% | Cycles: {contract.estimated_cycles}\n"

            if active_contracts == 0:
                contracts_message += "No active contracts found."
            else:
                contracts_message += f"\n**Total Active Contracts**: {active_contracts}"

            return contracts_message
        except Exception as e:
            return f"❌ Failed to get contracts: {e}"

    async def _handle_reset_agent_command(self, args: dict[str, Any]) -> str:
        """Handle agent reset command."""
        agent_id = args.get("agent_id")
        if not agent_id:
            return "❌ Please specify agent_id. Usage: reset_agent <agent_id>"

        if agent_id not in self.onboarding_service.agent_roles:
            return f"❌ Unknown agent: {agent_id}"

        try:
            # Reset agent state
            self.onboarding_service.agent_states[agent_id] = (
                self.onboarding_service.AgentState.UNINITIALIZED
            )

            # Remove contract
            if agent_id in self.onboarding_service.contracts:
                del self.onboarding_service.contracts[agent_id]

            return f"🔄 Agent {agent_id} has been reset to uninitialized state."
        except Exception as e:
            return f"❌ Failed to reset agent: {e}"

    def _get_help_message(self) -> str:
        """Get help message for onboarding commands."""
        help_message = """
🤖 **Onboarding Commands Help**

**Available Commands:**
• `onboard <agent_id>` - Onboard a specific agent
• `onboard_all` - Onboard all agents
• `onboarding_status` - Get status of all agents
• `agent_state <agent_id>` - Get detailed state of specific agent
• `contracts` - Show all active contracts
• `reset_agent <agent_id>` - Reset agent to uninitialized state

**Examples:**
• `onboard Agent-3` - Onboard Agent-3
• `agent_state Agent-1` - Get Agent-1's current state
• `onboarding_status` - Check all agents' onboarding status

**Available Agents:**
"""
        for agent_id, role in self.onboarding_service.agent_roles.items():
            help_message += f"• **{agent_id}**: {role}\n"

        return help_message

    async def send_onboarding_notification(self, agent_id: str, event_type: str, details: str = ""):
        """Send onboarding notification to Discord."""
        try:
            if not self.discord_commander:
                return

            notification = {
                "type": "onboarding_notification",
                "agent_id": agent_id,
                "event_type": event_type,
                "details": details,
                "timestamp": datetime.now().isoformat(),
            }

            # Send via Discord Commander's notification system
            if hasattr(self.discord_commander, "send_notification"):
                await self.discord_commander.send_notification(notification)

            logger.info(f"📢 Onboarding notification sent: {agent_id} - {event_type}")
        except Exception as e:
            logger.error(f"Failed to send onboarding notification: {e}")

    async def monitor_onboarding_events(self):
        """Monitor and report onboarding events."""
        try:
            # This could be expanded to monitor file changes, state changes, etc.
            logger.info("🔍 Onboarding event monitoring started")

            # Example: Check for state changes every 30 seconds
            while True:
                await asyncio.sleep(30)

                # Check for any agents that might need attention
                for agent_id, state in self.onboarding_service.agent_states.items():
                    if state == self.onboarding_service.AgentState.ERROR_RECOVERY:
                        await self.send_onboarding_notification(
                            agent_id, "error_recovery", "Agent is in error recovery state"
                        )

        except Exception as e:
            logger.error(f"Onboarding monitoring failed: {e}")


# Integration with existing Discord Commander
def integrate_onboarding_with_discord_commander(discord_commander, onboarding_service):
    """Integrate onboarding service with existing Discord Commander."""
    try:
        integration = DiscordOnboardingIntegration(discord_commander, onboarding_service)

        # Add onboarding command handler to Discord Commander
        if hasattr(discord_commander, "add_command_handler"):
            discord_commander.add_command_handler("onboarding", integration.handle_discord_command)

        # Start monitoring
        asyncio.create_task(integration.monitor_onboarding_events())

        logger.info("✅ Onboarding integration with Discord Commander completed")
        return integration

    except Exception as e:
        logger.error(f"❌ Failed to integrate onboarding with Discord Commander: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    from src.services.unified_onboarding_service import UnifiedOnboardingService

    # Initialize services
    onboarding_service = UnifiedOnboardingService()
    integration = DiscordOnboardingIntegration(None, onboarding_service)

    # Test command handling
    async def test_commands():
        print(await integration.handle_discord_command("onboarding_status"))
        print(await integration.handle_discord_command("onboard Agent-3"))

    asyncio.run(test_commands())

