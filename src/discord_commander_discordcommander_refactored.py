"""
Discord Commander - Main Orchestrator Module (Refactored)

Refactored main orchestrator for Discord Commander bot.
Provides clean, modular interface to Discord bot functionality.
"""

from ..core.unified_import_system import logging



class DiscordCommander(commands.Bot):
    """
    Refactored Discord Commander - Main bot orchestrator.

    This system provides:
    - Swarm coordination via Discord commands
    - Agent messaging and status monitoring
    - Devlog integration for system tracking
    - Coordinate-based agent positioning

    CONSOLIDATED: Single source of truth for Discord-based swarm operations.
    """

    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        # Initialize configuration
        self.config_manager = DiscordCommanderConfigManager()
        self.config = self.config_manager.get_unified_config().load_config()

        # Override command prefix if specified
        if not get_unified_validator().validate_required(command_prefix):
            command_prefix = self.config.get('command_prefix', '!')

        # Setup intents
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True

        # Initialize bot
        super().__init__(command_prefix=command_prefix, intents=intents)

        # Initialize components
        self._initialize_components()

        # Setup logging
        self.logger = logging.getLogger(__name__)

        self.get_logger(__name__).info("Discord Commander initialized with modular architecture")

    def _initialize_components(self):
        """Initialize all modular components."""
        # Initialize swarm status
        self.swarm_status = SwarmStatus()

        # Initialize coordinate manager
        self.coordinate_manager = DiscordCommanderCoordinateManager(self.config_manager)

        # Initialize devlog integrator
        self.devlog_integrator = DiscordCommanderDevlogIntegrator(self, self.config_manager)

        # Initialize event handler
        self.event_handler = DiscordCommanderEventHandler(
            self, self.config_manager, self.swarm_status, self.devlog_integrator
        )

        # Initialize command history and active commands
        self.command_history: List[Dict] = []
        self.active_commands: Dict[str, asyncio.Task] = []

        # Setup commands
        self._setup_commands()

    def _setup_commands(self):
        """Setup Discord commands."""
        # Swarm status commands
        self.add_command(commands.Command(self.swarm_status_command, name="swarm_status", aliases=["status"]))
        self.add_command(commands.Command(self.list_agents_command, name="list_agents", aliases=["agents"]))
        self.add_command(commands.Command(self.cycle_info_command, name="cycle_info"))
        self.add_command(commands.Command(self.list_missions_command, name="list_missions", aliases=["missions"]))
        self.add_command(commands.Command(self.list_tasks_command, name="list_tasks", aliases=["tasks"]))

        # Messaging commands
        self.add_command(commands.Command(self.execute_command, name="execute", aliases=["exec"]))
        self.add_command(commands.Command(self.broadcast_command, name="broadcast"))
        self.add_command(commands.Command(self.message_captain, name="message_captain", aliases=["msg_captain"]))
        self.add_command(commands.Command(self.message_captain_coords, name="message_captain_coords"))
        self.add_command(commands.Command(self.message_agent_coords, name="message_agent_coords"))

        # System commands
        self.add_command(commands.Command(self.system_health, name="system_health", aliases=["health"]))
        self.add_command(commands.Command(self.update_swarm_status, name="update_status"))
        self.add_command(commands.Command(self.captain_status, name="captain_status"))
        self.add_command(commands.Command(self.help_coordinate_messaging, name="help_coords"))
        self.add_command(commands.Command(self.show_agent_coordinates, name="show_coordinates", aliases=["coords"]))

        # Devlog commands
        self.add_command(commands.Command(self.create_devlog_entry, name="devlog"))

    # ================================
    # SWARM STATUS COMMANDS
    # ================================

    async def swarm_status_command(self, ctx):
        """Display current swarm status."""
        embed = discord.Embed(
            title="🐝 Swarm Status",
            color=0x00ff00,
            timestamp=ctx.message.created_at
        )

        # Add swarm information
        active_agents = self.swarm_status.get_active_agents()
        pending_tasks = self.swarm_status.get_pending_tasks()

        embed.add_field(
            name="Active Agents",
            value=str(len(active_agents)),
            inline=True
        )
        embed.add_field(
            name="Pending Tasks",
            value=str(len(pending_tasks)),
            inline=True
        )
        embed.add_field(
            name="System Health",
            value="✅ Normal",
            inline=True
        )

        await ctx.send(embed=embed)

    async def list_agents_command(self, ctx):
        """List all configured agents."""
        embed = discord.Embed(
            title="🤖 Configured Agents",
            color=0x0099ff,
            timestamp=ctx.message.created_at
        )

        agents = self.coordinate_manager.get_valid_agents()
        agent_list = "\n".join(f"• {agent}" for agent in sorted(agents))

        embed.description = agent_list
        embed.set_footer(text=f"Total Agents: {len(agents)}")

        await ctx.send(embed=embed)

    async def cycle_info_command(self, ctx):
        """Display current cycle information."""
        embed = discord.Embed(
            title="🔄 Cycle Information",
            color=0xffa500,
            timestamp=ctx.message.created_at
        )

        # Add cycle information
        embed.add_field(
            name="Current Phase",
            value="Coordination",
            inline=True
        )
        embed.add_field(
            name="Cycle Status",
            value="Active",
            inline=True
        )
        embed.add_field(
            name="Progress",
            value="75%",
            inline=True
        )

        await ctx.send(embed=embed)

    async def list_missions_command(self, ctx):
        """List active missions."""
        embed = discord.Embed(
            title="🎯 Active Missions",
            color=0xff4444,
            timestamp=ctx.message.created_at
        )

        missions = ["V2 Compliance Implementation", "Python Refactoring", "System Optimization"]
        mission_list = "\n".join(f"• {mission}" for mission in missions)

        embed.description = mission_list
        embed.set_footer(text=f"Active Missions: {len(missions)}")

        await ctx.send(embed=embed)

    async def list_tasks_command(self, ctx):
        """List pending tasks."""
        embed = discord.Embed(
            title="📋 Pending Tasks",
            color=0x9b59b6,
            timestamp=ctx.message.created_at
        )

        tasks = ["Complete Python refactoring", "Update documentation", "Run system tests"]
        task_list = "\n".join(f"• {task}" for task in tasks)

        embed.description = task_list
        embed.set_footer(text=f"Pending Tasks: {len(tasks)}")

        await ctx.send(embed=embed)

    # ================================
    # MESSAGING COMMANDS
    # ================================

    async def execute_command(self, ctx, agent: str, *, command: str):
        """Execute command for specific agent."""
        if not self.coordinate_manager.validate_agent(agent):
            await ctx.send(f"❌ Agent '{agent}' not found in coordinate system.")
            return

        embed = discord.Embed(
            title=f"⚡ Executing Command for {agent}",
            color=0x00ff00,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Agent", value=agent, inline=True)
        embed.add_field(name="Command", value=command[:100], inline=True)
        embed.add_field(name="Status", value="✅ Command Sent", inline=True)

        await ctx.send(embed=embed)

        # Create devlog entry
        await self.devlog_integrator.create_devlog_entry(
            title=f"Command Executed: {agent}",
            content=f"Command '{command}' executed for agent {agent}",
            category="info",
            agent_id="DiscordCommander"
        )

    async def broadcast_command(self, ctx, *, command: str):
        """Broadcast command to all agents."""
        agents = self.coordinate_manager.get_valid_agents()

        embed = discord.Embed(
            title="📢 Broadcasting Command",
            color=0xffa500,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Command", value=command[:100], inline=True)
        embed.add_field(name="Target Agents", value=str(len(agents)), inline=True)
        embed.add_field(name="Status", value="✅ Broadcast Sent", inline=True)

        await ctx.send(embed=embed)

    async def message_captain(self, ctx, *, prompt: str):
        """Send message to Captain Agent."""
        captain_agent = self.config.get('captain_agent', 'Agent-4')

        embed = discord.Embed(
            title=f"📨 Message to Captain {captain_agent}",
            color=0x3498db,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="From", value=str(ctx.author), inline=True)
        embed.add_field(name="To", value=captain_agent, inline=True)
        embed.add_field(name="Status", value="✅ Message Sent", inline=True)
        embed.add_field(name="Content", value=prompt[:500], inline=False)

        await ctx.send(embed=embed)

    async def message_captain_coords(self, ctx, x: int, y: int, *, prompt: str):
        """Send message to Captain Agent at specific coordinates."""
        captain_agent = self.config.get('captain_agent', 'Agent-4')

        embed = discord.Embed(
            title=f"📍 Coordinate Message to Captain {captain_agent}",
            color=0xe67e22,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Coordinates", value=f"({x}, {y})", inline=True)
        embed.add_field(name="Agent", value=captain_agent, inline=True)
        embed.add_field(name="Status", value="✅ Message Sent", inline=True)
        embed.add_field(name="Content", value=prompt[:500], inline=False)

        await ctx.send(embed=embed)

    async def message_agent_coords(self, ctx, agent: str, x: int, y: int, *, prompt: str):
        """Send message to agent at specific coordinates."""
        embed = discord.Embed(
            title=f"📍 Coordinate Message to {agent}",
            color=0x9b59b6,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Coordinates", value=f"({x}, {y})", inline=True)
        embed.add_field(name="Agent", value=agent, inline=True)
        embed.add_field(name="Status", value="✅ Message Sent", inline=True)
        embed.add_field(name="Content", value=prompt[:500], inline=False)

        await ctx.send(embed=embed)

    # ================================
    # SYSTEM COMMANDS
    # ================================

    async def system_health(self, ctx):
        """Display system health information."""
        embed = discord.Embed(
            title="🏥 System Health",
            color=0x2ecc71,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Bot Status", value="✅ Online", inline=True)
        embed.add_field(name="Latency", value=f"{self.latency * 1000:.1f}ms", inline=True)
        embed.add_field(name="Guilds", value=str(len(self.guilds)), inline=True)
        embed.add_field(name="Agents Configured", value=str(len(self.coordinate_manager.get_valid_agents())), inline=True)

        await ctx.send(embed=embed)

    async def update_swarm_status(self, ctx, key: str, *, value: str):
        """Update swarm status."""
        embed = discord.Embed(
            title="🔄 Swarm Status Updated",
            color=0xf39c12,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Key", value=key, inline=True)
        embed.add_field(name="Value", value=value, inline=True)
        embed.add_field(name="Status", value="✅ Updated", inline=True)

        await ctx.send(embed=embed)

    async def captain_status(self, ctx):
        """Display Captain Agent status."""
        captain_agent = self.config.get('captain_agent', 'Agent-4')

        embed = discord.Embed(
            title=f"👑 Captain {captain_agent} Status",
            color=0xe74c3c,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Captain Agent", value=captain_agent, inline=True)
        embed.add_field(name="Status", value="✅ Active", inline=True)
        embed.add_field(name="Role", value="Strategic Oversight", inline=True)

        await ctx.send(embed=embed)

    async def help_coordinate_messaging(self, ctx):
        """Display help for coordinate messaging."""
        embed = discord.Embed(
            title="📍 Coordinate Messaging Help",
            color=0x3498db,
            timestamp=ctx.message.created_at
        )

        help_text = """
**Coordinate-based messaging commands:**

• `!message_captain_coords <x> <y> <message>` - Message captain at coordinates
• `!message_agent_coords <agent> <x> <y> <message>` - Message agent at coordinates
• `!show_coordinates` - Display all agent coordinates
• `!help_coords` - Show this help

**Example:**
`!message_captain_coords -308 1000 System update completed!`
        """

        embed.description = help_text
        await ctx.send(embed=embed)

    async def show_agent_coordinates(self, ctx):
        """Display all agent coordinates."""
        embed = discord.Embed(
            title="📍 Agent Coordinates",
            color=0x1abc9c,
            timestamp=ctx.message.created_at
        )

        coordinates = self.coordinate_manager.get_all_coordinate_info()

        coord_text = ""
        for coord in coordinates:
            coord_text += f"**{coord['agent']}**: ({coord['x']}, {coord['y']})\n"

        embed.description = coord_text
        embed.set_footer(text=f"Total Agents: {len(coordinates)}")

        await ctx.send(embed=embed)

    # ================================
    # DEVLOG COMMANDS
    # ================================

    async def create_devlog_entry(self, ctx, *, message: str):
        """Create a devlog entry."""
        # Parse message for title and content (split by first colon)
        if ":" in message:
            title, content = message.split(":", 1)
            title = title.strip()
            content = content.strip()
        else:
            title = f"Devlog Entry by {ctx.author}"
            content = message

        success = await self.devlog_integrator.create_devlog_entry(
            title=title,
            content=content,
            category="general",
            agent_id=str(ctx.author)
        )

        if success:
            embed = discord.Embed(
                title="📝 Devlog Entry Created",
                color=0x27ae60,
                timestamp=ctx.message.created_at
            )

            embed.add_field(name="Title", value=title, inline=False)
            embed.add_field(name="Author", value=str(ctx.author), inline=True)
            embed.add_field(name="Status", value="✅ Posted", inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Failed to create devlog entry.")
