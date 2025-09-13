"""
Discord agent shortcut commands integration.

Provides !a1-!a4 and !broadcast commands that route messages
through the UnifiedMessaging system to PyAutoGUI delivery.
"""

from __future__ import annotations
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Agent name mappings for Discord shortcuts
AGENT_ALIASES: Dict[str, str] = {
    "a1": "Agent-1",
    "a2": "Agent-2",
    "a3": "Agent-3",
    "a4": "Agent-4"
}

# Default summary prompt for status requests
SUMMARY_PROMPT = (
    "📡 Status request:\n"
    "- Send a concise summary of actions since last report\n"
    "- Include blockers + next step\n"
    "- Format: Task / Actions / Status"
)


class AgentShortcutHandler:
    """Handler for Discord agent shortcut commands."""

    def __init__(self, messaging_service=None):
        """
        Initialize the agent shortcut handler.

        Args:
            messaging_service: The messaging service to use for delivery
        """
        self.messaging_service = messaging_service
        self._setup_messaging_service()

    def _setup_messaging_service(self):
        """Setup the messaging service if not provided."""
        if self.messaging_service is None:
            try:
                # Import the consolidated messaging service
                from src.services.messaging.consolidated_messaging_service import ConsolidatedMessagingService
                self.messaging_service = ConsolidatedMessagingService(dry_run=False)
                logger.info("Initialized ConsolidatedMessagingService for agent shortcuts")
            except ImportError as e:
                logger.error(f"Failed to import ConsolidatedMessagingService: {e}")
                self.messaging_service = None

    def _send_to_agent(self, agent_name: str, text: str) -> bool:
        """
        Send a message to a specific agent via the messaging service.

        Args:
            agent_name: Name of the target agent
            text: Message content to send

        Returns:
            True if message was sent successfully, False otherwise
        """
        if not self.messaging_service:
            logger.error("No messaging service available")
            return False

        try:
            # Create a unified message
            from src.services.messaging.models.messaging_models import UnifiedMessage
            from src.services.messaging.models.messaging_enums import (
                UnifiedMessageType,
                UnifiedMessagePriority
            )

            message = UnifiedMessage(
                content=text,
                recipient=agent_name,
                sender="Discord",
                message_type=UnifiedMessageType.DIRECT,
                priority=UnifiedMessagePriority.REGULAR
            )

            # Send the message
            result = self.messaging_service.send_message(message)

            if result:
                logger.info(f"Successfully sent message to {agent_name}")
            else:
                logger.warning(f"Failed to send message to {agent_name}")

            return result

        except Exception as e:
            logger.error(f"Error sending message to {agent_name}: {e}")
            return False

    def handle_agent_command(self, alias: str, content: Optional[str] = None) -> str:
        """
        Handle a Discord agent command (!a1, !a2, etc.).

        Args:
            alias: The agent alias (a1, a2, a3, a4)
            content: Optional custom message content

        Returns:
            Response message for Discord
        """
        agent = AGENT_ALIASES.get(alias.lower())
        if not agent:
            return f"❌ Unknown agent: {alias}. Available: {', '.join(AGENT_ALIASES.keys())}"

        # Use custom content or default summary prompt
        msg = content.strip() if content else SUMMARY_PROMPT

        # Send the message
        success = self._send_to_agent(agent, msg)

        if success:
            return f"✅ Sent to {agent}"
        else:
            return f"❌ Failed to send to {agent}"

    def handle_broadcast(self, content: Optional[str] = None) -> str:
        """
        Handle a Discord broadcast command (!broadcast).

        Args:
            content: Optional custom message content

        Returns:
            Response message for Discord with results for each agent
        """
        # Use custom content or default summary prompt
        msg = content.strip() if content else SUMMARY_PROMPT

        results = []
        for alias, agent_name in AGENT_ALIASES.items():
            success = self._send_to_agent(agent_name, msg)
            status_icon = "✅" if success else "❌"
            results.append(f"{status_icon} {agent_name}")

        return " | ".join(results)

    def get_available_agents(self) -> str:
        """
        Get a list of available agents for Discord help.

        Returns:
            Formatted string of available agents
        """
        agent_list = []
        for alias, agent_name in AGENT_ALIASES.items():
            agent_list.append(f"`!{alias}` → {agent_name}")

        return "Available agents:\n" + "\n".join(agent_list)


# Global handler instance
_shortcut_handler: Optional[AgentShortcutHandler] = None


def get_shortcut_handler() -> AgentShortcutHandler:
    """
    Get the global agent shortcut handler instance.

    Returns:
        AgentShortcutHandler instance
    """
    global _shortcut_handler
    if _shortcut_handler is None:
        _shortcut_handler = AgentShortcutHandler()
    return _shortcut_handler


def handle_agent_command(alias: str, content: Optional[str] = None) -> str:
    """
    Convenience function to handle agent commands.

    Args:
        alias: The agent alias (a1, a2, a3, a4)
        content: Optional custom message content

    Returns:
        Response message for Discord
    """
    handler = get_shortcut_handler()
    return handler.handle_agent_command(alias, content)


def handle_broadcast(content: Optional[str] = None) -> str:
    """
    Convenience function to handle broadcast commands.

    Args:
        content: Optional custom message content

    Returns:
        Response message for Discord
    """
    handler = get_shortcut_handler()
    return handler.handle_broadcast(content)


# Discord command integration examples
def register_discord_commands(bot):
    """
    Register Discord commands with a bot instance.

    This is an example of how to integrate with your Discord bot.
    Adapt this to your specific bot framework.

    Args:
        bot: Discord bot instance
    """
    handler = get_shortcut_handler()

    @bot.command(name='a1')
    async def agent_1_command(ctx, *, content: Optional[str] = None):
        """Send message to Agent-1."""
        response = handler.handle_agent_command('a1', content)
        await ctx.send(response)

    @bot.command(name='a2')
    async def agent_2_command(ctx, *, content: Optional[str] = None):
        """Send message to Agent-2."""
        response = handler.handle_agent_command('a2', content)
        await ctx.send(response)

    @bot.command(name='a3')
    async def agent_3_command(ctx, *, content: Optional[str] = None):
        """Send message to Agent-3."""
        response = handler.handle_agent_command('a3', content)
        await ctx.send(response)

    @bot.command(name='a4')
    async def agent_4_command(ctx, *, content: Optional[str] = None):
        """Send message to Agent-4."""
        response = handler.handle_agent_command('a4', content)
        await ctx.send(response)

    @bot.command(name='broadcast')
    async def broadcast_command(ctx, *, content: Optional[str] = None):
        """Broadcast message to all agents."""
        response = handler.handle_broadcast(content)
        await ctx.send(response)

    @bot.command(name='agents')
    async def agents_help_command(ctx):
        """Show available agent commands."""
        response = handler.get_available_agents()
        await ctx.send(response)

    logger.info("Registered Discord agent shortcut commands")
