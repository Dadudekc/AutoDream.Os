from ..core.unified_entry_point_system import main
"""
Discord Commander Unified System - Refactored Modular Version
Main entry point for Discord bot with modular architecture
V2 Compliance: Under 300-line limit achieved

@Author: Agent-3 - Infrastructure & DevOps Specialist
@Version: 2.0.0 - Modular Discord Commander
@License: MIT
"""


try:
    import discord
    from discord.ext import commands
    from discord.ui import View, Button, Select
except ImportError:
    get_logger(__name__).info("Discord.py not installed. Please install with: pip install discord.py")
    discord = None
    commands = None

class DiscordCommanderUnifiedSystem:
    """
    Unified Discord Commander System - Modular Refactored Version.
    Main orchestrator using modular components for clean architecture.
    V2 COMPLIANT: Under 300-line limit with proper modular architecture.
    """

    def __init__(self):
        # Initialize modular components
        self.config_manager = DiscordConfigManager()
        self.devlog_integrator = DiscordDevlogIntegrator(self.config_manager)

        # Initialize Discord bot components
        self.bot = None
        self.workflow_view = None

        # System state
        self.is_running = False
        self.command_stats: Dict[str, int] = {}

        # Initialize system
        self._initialize_system()

    def _initialize_system(self) -> None:
        """Initialize the unified Discord system"""
        if discord is None:
            raise ImportError("Discord.py is required but not installed")

        # Validate configuration
        validation = self.config_manager.validate_configuration()
        if not validation["valid"]:
            get_unified_validator().raise_validation_error(f"Configuration validation failed: {validation['errors']}")

        # Initialize Discord bot
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(
            command_prefix=self.config_manager.get_command_prefix(),
            intents=intents,
            help_command=None
        )

        # Initialize workflow view
        self.workflow_view = WorkflowView(self.config_manager, self.devlog_integrator)

        # Setup event handlers
        self._setup_event_handlers()

        # Setup commands
        self._setup_commands()

    def _setup_event_handlers(self) -> None:
        """Setup Discord event handlers"""

        @self.bot.event
        async def on_ready():
            """Bot ready event"""
            get_logger(__name__).info(f"🤖 Discord Commander System Online - {self.bot.user}")
            get_logger(__name__).info(f"📊 Connected to {len(self.bot.guilds)} guild(s)")

            # Post startup devlog
            self.devlog_integrator.post_devlog(
                "Discord System Online",
                f"Discord Commander System initialized with {len(self.bot.guilds)} guild connections.",
                "system",
                "Agent-3",
                "normal"
            )

        @self.bot.event
        async def on_command(ctx):
            """Command execution event"""
            cmd_name = ctx.command.name
            self.command_stats[cmd_name] = self.command_stats.get(cmd_name, 0) + 1

        @self.bot.event
        async def on_command_error(ctx, error):
            """Command error event"""
            embed = EmbedBuilder.create_error_embed(
                "Command Error",
                str(error)
            )
            await ctx.send(embed=embed)

    def _setup_commands(self) -> None:
        """Setup Discord commands"""

        @self.bot.command(name="status")
        async def status_command(ctx):
            """Display system status"""
            embed = EmbedBuilder.create_info_embed(
                "System Status",
                "Discord Commander System is operational."
            )
            embed.add_field(name="Uptime", value="Active", inline=True)
            embed.add_field(name="Commands Processed", value=str(sum(self.command_stats.values())), inline=True)
            await ctx.send(embed=embed)

        @self.bot.command(name="devlog")
        async def devlog_command(ctx, *, message: str):
            """Post a devlog entry"""
            result = self.devlog_integrator.post_devlog(
                "Manual Devlog Entry",
                message,
                "manual",
                str(ctx.author),
                "normal"
            )

            if result["success"]:
                embed = EmbedBuilder.create_success_embed(
                    "Devlog Posted",
                    f"Devlog entry created with ID: {result['devlog_id']}"
                )
            else:
                embed = EmbedBuilder.create_error_embed(
                    "Devlog Failed",
                    result["error"]
                )

            await ctx.send(embed=embed)

        @self.bot.command(name="workflow")
        async def workflow_command(ctx):
            """Display workflow interface"""
            embed = EmbedBuilder.create_info_embed(
                "Workflow Control",
                "Use the buttons below to control system workflows."
            )
            await ctx.send(embed=embed, view=self.workflow_view)

    async def start_system(self) -> None:
        """Start the Discord Commander System"""
        if self.is_running:
            get_logger(__name__).info("⚠️ System is already running")
            return

        token = self.config_manager.get_token()
        if not get_unified_validator().validate_required(token):
            get_unified_validator().raise_validation_error("Discord bot token not configured")

        self.is_running = True
        get_logger(__name__).info("🚀 Starting Discord Commander System...")

        try:
            await self.bot.start(token)
        except KeyboardInterrupt:
            get_logger(__name__).info("🛑 System shutdown requested")
        except Exception as e:
            get_logger(__name__).info(f"❌ System error: {e}")
        finally:
            await self.shutdown_system()

    async def shutdown_system(self) -> None:
        """Shutdown the Discord Commander System"""
        if not self.is_running:
            return

        get_logger(__name__).info("🔄 Shutting down Discord Commander System...")

        # Post shutdown devlog
        self.devlog_integrator.post_devlog(
            "System Shutdown",
            "Discord Commander System shutting down gracefully.",
            "system",
            "Agent-3",
            "normal"
        )

        if self.bot:
            await self.bot.close()

        self.is_running = False
        get_logger(__name__).info("✅ Discord Commander System shutdown complete")

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "is_running": self.is_running,
            "bot_connected": self.bot is not None and self.bot.is_ready(),
            "guilds_connected": len(self.bot.guilds) if self.bot else 0,
            "commands_processed": sum(self.command_stats.values()),
            "command_breakdown": self.command_stats.copy(),
            "config_validation": self.config_manager.validate_configuration(),
            "devlog_stats": self.devlog_integrator.get_devlog_stats()
        }

    def get_config_manager(self) -> DiscordConfigManager:
        """Get the configuration manager instance"""
        return self.config_manager

    def get_devlog_integrator(self) -> DiscordDevlogIntegrator:
        """Get the devlog integrator instance"""
        return self.devlog_integrator

    def reload_configuration(self) -> bool:
        """Reload system configuration"""
        try:
            # Re-initialize config manager
            self.config_manager = DiscordConfigManager()

            # Re-initialize devlog integrator
            self.devlog_integrator = DiscordDevlogIntegrator(self.config_manager)

            # Post reload devlog
            self.devlog_integrator.post_devlog(
                "Configuration Reloaded",
                "System configuration has been reloaded successfully.",
                "system",
                "Agent-3",
                "normal"
            )

            return True
        except Exception as e:
            get_logger(__name__).info(f"❌ Configuration reload failed: {e}")
            return False


if __name__ == "__main__":
    exit(main())

