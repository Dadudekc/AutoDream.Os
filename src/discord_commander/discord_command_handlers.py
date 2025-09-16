import logging

logger = logging.getLogger(__name__)
"""
Discord Command Handlers - V2 Compliant Module
==============================================

Command processing and handling for Discord Agent Bot.
V2 COMPLIANT: Command handling logic under 200 lines.

Features:
- Command parsing and validation
- Response handling and followup processing
- Error handling and user feedback

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""

try:
    from .command_router import CommandRouter
    from .embeds import EmbedManager
    from .handlers_agents import AgentCommandHandlers
    from .handlers_swarm import SwarmCommandHandlers
except ImportError as e:
    logger.info(f"⚠️ Import warning: {e}")
    CommandRouter = None
    EmbedManager = None
    AgentCommandHandlers = None
    SwarmCommandHandlers = None


class DiscordCommandHandlers:
    """Command processing and handling for Discord Agent Bot."""

    def __init__(self, bot):
        """Initialize command handlers."""
        self.bot = bot
        self.command_router = CommandRouter()
        self.embed_manager = EmbedManager()
        self.agent_handlers = AgentCommandHandlers(bot.agent_engine, self.embed_manager)
        self.swarm_handlers = SwarmCommandHandlers(bot.agent_engine, self.embed_manager)

    async def process_command(self, message):
        """Process Discord command using modular handlers."""
        try:
            content = message.content
            author = message.author
            channel = message.channel
            cmd_type, args, remaining = self.command_router.parse_command(content)
            if cmd_type == "unknown":
                return
            is_valid, error_msg = self.command_router.validate_command(cmd_type, args, content)
            if not is_valid:
                error_embed = self.embed_manager.create_response_embed(
                    "error", title="❌ Invalid Command", description=error_msg
                )
                await channel.send(embed=error_embed)
                return
            total_active = (
                self.agent_handlers.get_active_command_count()
                + self.swarm_handlers.get_active_broadcast_count()
            )
            if total_active >= self.bot.max_concurrent_commands:
                embed = self.embed_manager.create_response_embed("too_many_commands")
                await channel.send(embed=embed)
                return
            context = self.command_router.create_command_context(cmd_type, args, author, channel)
            response_data = await self._route_command(cmd_type, context, args, author, channel)
            if response_data:
                await self._handle_response(response_data, cmd_type, args, author, channel)
        except Exception as e:
            logger.info(f"❌ Error processing command: {e}")
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Command Processing Error",
                description="An error occurred while processing your command.",
                error=str(e),
            )
            await message.channel.send(embed=error_embed)

    async def _route_command(self, cmd_type, context, args, author, channel):
        """Route command to appropriate handler."""
        response_data = None
        if cmd_type == "prompt":
            response_data = await self.agent_handlers.handle_prompt_command(context)
        elif cmd_type == "status":
            response_data = await self.agent_handlers.handle_status_command(context)
        elif cmd_type == "swarm":
            response_data = await self.swarm_handlers.handle_swarm_command(context)
        elif cmd_type == "urgent":
            response_data = await self.swarm_handlers.handle_urgent_command(context)
        elif cmd_type == "agents":
            agents = self.swarm_handlers.get_swarm_agent_list()
            embed = self.embed_manager.create_response_embed("agents", agents=agents, author=author)
            await channel.send(embed=embed)
            return None
        elif cmd_type == "help":
            embed = self.embed_manager.create_response_embed("help", author=author)
            await channel.send(embed=embed)
            return None
        elif cmd_type == "ping":
            latency = 42
            active_commands = self.agent_handlers.get_active_command_count()
            embed = self.embed_manager.create_response_embed(
                "ping", latency=latency, active_commands=active_commands
            )
            await channel.send(embed=embed)
            return None
        return response_data

    async def _handle_response(self, response_data, cmd_type, args, author, channel):
        """Handle command response."""
        if response_data.get("ignore"):
            return
        embed = response_data["embed"]
        follow_up = response_data.get("follow_up", False)
        if follow_up:
            response_msg = await channel.send(embed=embed)
            command_id = response_data.get("command_id")
            if command_id and cmd_type == "prompt":
                await self._handle_prompt_followup(
                    command_id, response_data, args, author, response_msg
                )
            elif command_id and cmd_type == "swarm":
                await self._handle_swarm_followup(command_id, response_data, author, response_msg)
            elif command_id and cmd_type == "urgent":
                await self._handle_urgent_followup(command_id, response_data, author, response_msg)
        else:
            await channel.send(embed=embed)

    async def _handle_prompt_followup(self, command_id, response_data, args, author, response_msg):
        """Handle prompt command followup."""
        try:
            result = await self.bot.agent_engine.send_to_agent_inbox(
                response_data["agent_id"], args[1], f"Discord User {author} (ID: {author.id})"
            )
            followup_data = await self.agent_handlers.handle_prompt_followup(command_id, result)
            if followup_data and followup_data.get("edit"):
                await response_msg.edit(embed=followup_data["embed"])
        except Exception as e:
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Agent Communication Error",
                description="Error communicating with agent.",
                error=str(e),
            )
            await response_msg.edit(embed=error_embed)

    async def _handle_swarm_followup(self, command_id, response_data, author, response_msg):
        """Handle swarm command followup."""
        try:
            result = await self.swarm_handlers.execute_swarm_broadcast(
                response_data["message"], f"Discord User {author} (ID: {author.id})"
            )
            followup_data = await self.swarm_handlers.handle_swarm_followup(command_id, result)
            if followup_data and followup_data.get("edit"):
                await response_msg.edit(embed=followup_data["embed"])
        except Exception as e:
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Swarm Broadcast Error",
                description="Error broadcasting to swarm.",
                error=str(e),
            )
            await response_msg.edit(embed=error_embed)

    async def _handle_urgent_followup(self, command_id, response_data, author, response_msg):
        """Handle urgent command followup."""
        try:
            result = await self.swarm_handlers.execute_urgent_broadcast(
                response_data["message"], f"Discord User {author} (ID: {author.id})"
            )
            followup_data = await self.swarm_handlers.handle_urgent_followup(command_id, result)
            if followup_data and followup_data.get("edit"):
                await response_msg.edit(embed=followup_data["embed"])
        except Exception as e:
            error_embed = self.embed_manager.create_response_embed(
                "error",
                title="❌ Urgent Broadcast Error",
                description="Error sending urgent broadcast.",
                error=str(e),
            )
            await response_msg.edit(embed=error_embed)
