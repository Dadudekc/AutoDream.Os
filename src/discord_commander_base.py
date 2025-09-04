"""
Discord Commander Base Module
V2 COMPLIANCE: Base functionality for Discord bot operations
Lines: ~80 (V2 Compliant)
"""



class DiscordCommanderBase(commands.Bot):
    """
    Discord Commander Base - Core bot functionality
    V2 COMPLIANCE: Base class with essential functionality only
    """

    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        """Initialize the Discord bot base"""
        # Setup intents
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True
            intents.guild_messages = True
            intents.guild_reactions = True
            intents.voice_states = True
            intents.presences = True

        # Initialize bot
        super().__init__(command_prefix=command_prefix, intents=intents)

        # Core attributes
        self.command_history: List[Dict] = []
        self.active_commands: Dict[str, asyncio.Task] = []
        self.logger = logging.getLogger(__name__)

        # Setup event handlers
        self._setup_base_events()

    def _setup_base_events(self):
        """Setup base event handlers"""
        @self.event
        async def on_ready():
            """Bot ready event"""
            self.get_logger(__name__).info(f"Discord Commander Base ready as {self.user}")

        @self.event
        async def on_command(ctx):
            """Command execution tracking"""
            self.command_history.append({
                'command': ctx.command.name,
                'user': str(ctx.author),
                'timestamp': ctx.message.created_at,
                'guild': str(ctx.guild) if ctx.guild else 'DM'
            })

            # Keep only last 100 commands
            if len(self.command_history) > 100:
                self.command_history.pop(0)

    def get_command_stats(self) -> Dict[str, Any]:
        """
        Get command execution statistics

        Returns:
            Dict containing command stats
        """
        total_commands = len(self.command_history)
        unique_users = len(set(cmd['user'] for cmd in self.command_history))

        return {
            'total_commands': total_commands,
            'unique_users': unique_users,
            'recent_commands': self.command_history[-10:] if self.command_history else []
        }

    def clear_command_history(self):
        """Clear command history"""
        self.command_history.clear()
        self.get_logger(__name__).info("Command history cleared")

    async def safe_send(self, ctx, content: str, **kwargs) -> bool:
        """
        Safely send a message with error handling

        Args:
            ctx: Command context
            content: Message content
            **kwargs: Additional embed/args

        Returns:
            bool: Success status
        """
        try:
            await ctx.send(content, **kwargs)
            return True
        except Exception as e:
            self.get_logger(__name__).error(f"Failed to send message: {str(e)}")
            return False
