"""
Discord Commander Event Handler Module

Provides Discord event handling functionality for the commander system.
"""



class DiscordCommanderEventHandler:
    """
    Event handler for Discord Commander.

    Manages Discord events like on_ready, on_message, and provides
    initialization and startup functionality.
    """

    def __init__(self, bot: commands.Bot, config_manager, swarm_status, devlog_integrator):
        self.bot = bot
        self.config_manager = config_manager
        self.swarm_status = swarm_status
        self.devlog_integrator = devlog_integrator
        self.logger = logging.getLogger(__name__)

        # Setup event handlers
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Setup Discord event handlers."""
        @self.bot.event
        async def on_ready():
            await self._handle_on_ready()

        @self.bot.event
        async def on_message(message):
            await self._handle_on_message(message)

    async def _handle_on_ready(self):
        """Handle bot ready event."""
        self.get_logger(__name__).info(f'Bot logged in as {self.bot.user}')

        # Initialize channels and send startup message
        await self._initialize_channels()
        await self._send_startup_message()

        # Create devlog entry for bot startup
        await self.devlog_integrator.create_devlog_entry(
            title="Discord Commander Startup",
            content=f"Discord Commander bot started successfully as {self.bot.user}",
            category="success",
            agent_id="DiscordCommander"
        )

    async def _initialize_channels(self):
        """Initialize required Discord channels."""
        config = self.config_manager.get_unified_config().load_config()

        if config.get('auto_startup_message', True):
            # Ensure we have access to the devlog channel
            if config.get('devlog_channel_id'):
                try:
                    channel = self.bot.get_channel(int(config['devlog_channel_id']))
                    if channel:
                        self.get_logger(__name__).info(f"Devlog channel initialized: {channel.name}")
                    else:
                        self.get_logger(__name__).warning("Devlog channel not found")
                except Exception as e:
                    self.get_logger(__name__).error(f"Error initializing devlog channel: {e}")

    async def _send_startup_message(self):
        """Send startup message to devlog channel."""
        config = self.config_manager.get_unified_config().load_config()

        if config.get('auto_startup_message', True):
            startup_content = f"""
🚀 **Discord Commander Online**

**Status:** Operational
**Bot User:** {self.bot.user}
**Guild:** {self.bot.guilds[0].name if self.bot.guilds else 'No guild'}
**Command Prefix:** {config.get('command_prefix', '!')}
**Captain Agent:** {config.get('captain_agent', 'Agent-4')}

**Swarm Status:**
- Active Agents: {len(self.swarm_status.get_active_agents())}
- Pending Tasks: {len(self.swarm_status.get_pending_tasks())}
- System Health: ✅ Normal

Ready for swarm coordination commands.
            """

            await self.devlog_integrator.create_devlog_entry(
                title="System Startup",
                content=startup_content,
                category="success",
                agent_id="DiscordCommander"
            )

    async def _handle_on_message(self, message):
        """Handle incoming messages."""
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Log the message for monitoring
        await self._log_message(message)

        # Process commands
        await self.bot.process_commands(message)

    async def _log_message(self, message):
        """Log incoming messages for monitoring."""
        log_entry = {
            'timestamp': message.created_at.isoformat(),
            'author': str(message.author),
            'channel': str(message.channel),
            'content': message.content[:500],  # Truncate long messages
            'has_attachments': len(message.attachments) > 0,
            'is_command': message.content.startswith(self.bot.command_prefix)
        }

        # Store in swarm status for monitoring
        self.swarm_status.log_message(log_entry)

        # Log to devlog if it's a command
        if log_entry['is_command']:
            await self.devlog_integrator.create_devlog_entry(
                title="Command Received",
                content=f"Command from {message.author}: {message.content[:200]}...",
                category="info",
                agent_id="DiscordCommander"
            )

    async def get_bot_status(self) -> Dict[str, Any]:
        """Get current bot status information."""
        config = self.config_manager.get_unified_config().load_config()

        return {
            'bot_user': str(self.bot.user) if self.bot.user else None,
            'guild_name': self.bot.guilds[0].name if self.bot.guilds else None,
            'guild_count': len(self.bot.guilds),
            'command_prefix': config.get('command_prefix', '!'),
            'captain_agent': config.get('captain_agent', 'Agent-4'),
            'latency': self.bot.latency * 1000 if self.bot.latency else None,
            'is_ready': self.bot.is_ready(),
            'uptime': get_unified_validator().safe_getattr(self.bot, '_uptime', None)
        }

