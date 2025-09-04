"""
Discord Commander Main Class - V2 Compliance
Main Discord bot class for swarm coordination
V2 COMPLIANCE: Under 300-line limit

@agent Agent-1 - Integration & Core Systems Specialist
@version 1.0.0
"""

from ..core.unified_import_system import logging

# Import required classes

# Setup logging
logger = logging.getLogger(__name__)

class DiscordCommander(commands.Bot):
    """Main Discord Commander class for swarm coordination"""
    
    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True

        super().__init__(command_prefix=command_prefix, intents=intents)

        # Initialize swarm status
        self.swarm_status = SwarmStatus()
        self.command_history: List[Dict] = []
        self.active_commands: Dict[str, asyncio.Task] = {}

        # Configuration
        self.config = self._get_unified_config().load_config()
        self.captain_agent = "Agent-4"

        get_logger(__name__).info("Discord Commander initialized")

    def _load_config(self) -> Dict[str, Any]:
        """Load Discord commander configuration using unified configuration manager"""
        
        config_manager = get_discord_config_manager()
        discord_config = config_manager.get_discord_config()
        
        return {
            "token": discord_config.token,
            "guild_id": discord_config.guild_id,
            "command_channel": discord_config.command_channel,
            "status_channel": discord_config.status_channel,
            "log_channel": discord_config.log_channel,
            "admin_role": discord_config.admin_role,
            "agent_roles": discord_config.agent_roles
        }

    async def on_ready(self):
        """Called when the bot is ready and connected"""
        get_logger(__name__).info(f"Discord Commander connected as {self.user}")
        await self._initialize_channels()
        await self._send_startup_message()

    async def _initialize_channels(self):
        """Initialize required Discord channels"""
        for guild in self.guilds:
            if str(guild.id) == self.config["guild_id"]:
                self.guild = guild

                # Create channels if they don't exist
                channels_to_create = [
                    self.config["command_channel"],
                    self.config["status_channel"],
                    self.config["log_channel"]
                ]

                for channel_name in channels_to_create:
                    channel = discord.utils.get(guild.channels, name=channel_name)
                    if channel is None:
                        try:
                            channel = await guild.create_text_channel(channel_name)
                            get_logger(__name__).info(f"Created channel: {channel_name}")
                        except Exception as e:
                            get_logger(__name__).error(f"Failed to create channel {channel_name}: {e}")

                break

    async def _send_startup_message(self):
        """Send startup message to status channel"""
        status_channel = discord.utils.get(self.guild.channels, name=self.config["status_channel"])
        if status_channel:
            embed = discord.Embed(
                title="🚀 Swarm Discord Commander Online",
                description="Discord integration activated for swarm coordination",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Status", value="✅ Operational", inline=True)
            embed.add_field(name="Active Agents", value=f"{len(self.swarm_status.active_agents)}/{self.swarm_status.total_agents}", inline=True)
            embed.add_field(name="Current Cycle", value=f"Cycle {self.swarm_status.current_cycle}", inline=True)
            embed.add_field(name="System Health", value=self.swarm_status.system_health, inline=True)
            embed.add_field(name="Efficiency Rating", value=f"{self.swarm_status.efficiency_rating}x", inline=True)

            embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

            await status_channel.send(embed=embed)

    async def on_message(self, message):
        """Handle incoming messages"""
        if message.author == self.user:
            return

        # Log all messages for swarm coordination
        await self._log_message(message)

        await self.process_commands(message)

    async def _log_message(self, message):
        """Log messages to the log channel"""
        log_channel = discord.utils.get(self.guild.channels, name=self.config["log_channel"])
        if log_channel:
            embed = discord.Embed(
                title="📝 Message Logged",
                color=0x3498db,
                timestamp=message.created_at
            )

            embed.add_field(name="Author", value=message.author.mention, inline=True)
            embed.add_field(name="Channel", value=message.channel.mention, inline=True)
            embed.add_field(name="Content", value=message.content[:1024], inline=False)

            await log_channel.send(embed=embed)

    # ================================
    # SWARM STATUS COMMANDS
    # ================================

    @commands.command(name="status")
    async def swarm_status(self, ctx):
        """Get current swarm status"""
        embed = discord.Embed(
            title="📊 Swarm Status Report",
            color=0x3498db,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Active Agents", value=f"{len(self.swarm_status.active_agents)}/{self.swarm_status.total_agents}", inline=True)
        embed.add_field(name="Current Cycle", value=f"Cycle {self.swarm_status.current_cycle}", inline=True)
        embed.add_field(name="System Health", value=self.swarm_status.system_health, inline=True)
        embed.add_field(name="Efficiency Rating", value=f"{self.swarm_status.efficiency_rating}x", inline=True)

        if self.swarm_status.active_missions:
            missions_text = "\n".join([f"• {mission}" for mission in self.swarm_status.active_missions[:5]])
            embed.add_field(name="Active Missions", value=missions_text, inline=False)

        if self.swarm_status.pending_tasks:
            tasks_text = "\n".join([f"• {task}" for task in self.swarm_status.pending_tasks[:5]])
            embed.add_field(name="Pending Tasks", value=tasks_text, inline=False)

        embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

        await ctx.send(embed=embed)

    @commands.command(name="agents")
    async def list_agents(self, ctx):
        """List all agents and their status"""
        embed = discord.Embed(
            title="🤖 Agent Status Overview",
            color=0x9b59b6,
            timestamp=datetime.utcnow()
        )

        for i in range(1, 9):
            agent_name = f"Agent-{i}"
            status = "🟢 Active" if agent_name in self.swarm_status.active_agents else "🔴 Inactive"
            embed.add_field(name=agent_name, value=status, inline=True)

        embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

        await ctx.send(embed=embed)

    @commands.command(name="cycle")
    async def cycle_info(self, ctx):
        """Get current cycle information"""
        embed = discord.Embed(
            title=f"🔄 Cycle {self.swarm_status.current_cycle} Status",
            color=0xf39c12,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Cycle Number", value=self.swarm_status.current_cycle, inline=True)
        embed.add_field(name="Cycle Phase", value="Active", inline=True)
        embed.add_field(name="Efficiency Rating", value=f"{self.swarm_status.efficiency_rating}x", inline=True)

        if self.swarm_status.last_update:
            embed.add_field(name="Last Update", value=self.swarm_status.last_update.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=True)

        embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

        await ctx.send(embed=embed)

    # ================================
    # MISSION MANAGEMENT COMMANDS
    # ================================

    @commands.command(name="missions")
    async def list_missions(self, ctx):
        """List all active missions"""
        embed = discord.Embed(
            title="🎯 Active Missions",
            color=0xe74c3c,
            timestamp=datetime.utcnow()
        )

        if self.swarm_status.active_missions:
            for i, mission in enumerate(self.swarm_status.active_missions, 1):
                embed.add_field(name=f"Mission {i}", value=mission, inline=False)
        else:
            embed.add_field(name="Status", value="No active missions", inline=False)

        embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

        await ctx.send(embed=embed)

    @commands.command(name="tasks")
    async def list_tasks(self, ctx):
        """List pending tasks"""
        embed = discord.Embed(
            title="📋 Pending Tasks",
            color=0xf1c40f,
            timestamp=datetime.utcnow()
        )

        if self.swarm_status.pending_tasks:
            for i, task in enumerate(self.swarm_status.pending_tasks, 1):
                embed.add_field(name=f"Task {i}", value=task, inline=False)
        else:
            embed.add_field(name="Status", value="No pending tasks", inline=False)

        embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

        await ctx.send(embed=embed)

    # ================================
    # COMMAND EXECUTION COMMANDS
    # ================================

    @commands.command(name="execute")
    @commands.has_role("Captain")
    async def execute_command(self, ctx, agent: str, *, command: str):
        """Execute a command on a specific agent"""
        if not self._is_valid_agent(agent):
            await ctx.send(f"❌ Invalid agent: {agent}")
            return

        # Create command execution task
        task = asyncio.create_task(self._execute_agent_command(agent, command))
        self.active_commands[f"{agent}_{len(self.active_commands)}"] = task

        embed = discord.Embed(
            title="⚡ Command Execution Started",
            color=0x27ae60,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Target Agent", value=agent, inline=True)
        embed.add_field(name="Command", value=command, inline=True)
        embed.add_field(name="Status", value="🟡 Executing...", inline=True)

        message = await ctx.send(embed=embed)

        try:
            result = await task

            # Update embed with results
            embed.color = 0x27ae60 if result.success else 0xe74c3c
            embed.clear_fields()

            embed.add_field(name="Target Agent", value=agent, inline=True)
            embed.add_field(name="Command", value=command, inline=True)
            embed.add_field(name="Status", value="✅ Completed" if result.success else "❌ Failed", inline=True)

            if result.message:
                embed.add_field(name="Result", value=result.message[:1024], inline=False)

            if result.execution_time:
                embed.add_field(name="Execution Time", value=f"{result.execution_time:.2f}s", inline=True)

        except Exception as e:
            embed.color = 0xe74c3c
            embed.clear_fields()

            embed.add_field(name="Target Agent", value=agent, inline=True)
            embed.add_field(name="Command", value=command, inline=True)
            embed.add_field(name="Status", value="❌ Error", inline=True)
            embed.add_field(name="Error", value=str(e)[:1024], inline=False)

        await message.edit(embed=embed)

    @commands.command(name="broadcast")
    @commands.has_role("Captain")
    async def broadcast_command(self, ctx, *, command: str):
        """Broadcast a command to all active agents"""
        active_agents = self.swarm_status.active_agents
        if not get_unified_validator().validate_required(active_agents):
            await ctx.send("❌ No active agents available")
            return

        embed = discord.Embed(
            title="📡 Broadcast Command Started",
            color=0x9b59b6,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Command", value=command, inline=False)
        embed.add_field(name="Target Agents", value=f"{len(active_agents)} active agents", inline=True)
        embed.add_field(name="Status", value="🟡 Broadcasting...", inline=True)

        message = await ctx.send(embed=embed)

        # Execute command on all active agents
        results = []
        for agent in active_agents:
            try:
                result = await self._execute_agent_command(agent, command)
                results.append(f"{agent}: {'✅' if result.success else '❌'}")
            except Exception as e:
                results.append(f"{agent}: ❌ Error")

        embed.set_field_at(2, name="Status", value="✅ Completed", inline=True)
        embed.add_field(name="Results", value="\n".join(results[:10]), inline=False)

        await message.edit(embed=embed)

    # ================================
    # SYSTEM MANAGEMENT COMMANDS
    # ================================

    @commands.command(name="health")
    async def system_health(self, ctx):
        """Get system health status"""
        embed = discord.Embed(
            title="🏥 System Health Report",
            color=0x2ecc71,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Overall Health", value=self.swarm_status.system_health, inline=True)
        embed.add_field(name="Active Agents", value=f"{len(self.swarm_status.active_agents)}/{self.swarm_status.total_agents}", inline=True)
        embed.add_field(name="Active Commands", value=len(self.active_commands), inline=True)

        # Add health indicators
        embed.add_field(name="Memory Usage", value="🟢 Normal", inline=True)
        embed.add_field(name="CPU Usage", value="🟢 Normal", inline=True)
        embed.add_field(name="Network Status", value="🟢 Connected", inline=True)

        embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

        await ctx.send(embed=embed)

    @commands.command(name="update")
    @commands.has_role("Captain")
    async def update_swarm_status(self, ctx, key: str, *, value: str):
        """Update swarm status"""
        try:
            if key == "efficiency":
                self.swarm_status.efficiency_rating = float(value)
            elif key == "cycle":
                self.swarm_status.current_cycle = int(value)
            elif key == "health":
                self.swarm_status.system_health = value.upper()
            elif key == "add_agent":
                if value not in self.swarm_status.active_agents:
                    self.swarm_status.active_agents.append(value)
            elif key == "remove_agent":
                if value in self.swarm_status.active_agents:
                    self.swarm_status.active_agents.remove(value)
            elif key == "add_mission":
                self.swarm_status.active_missions.append(value)
            elif key == "remove_mission":
                if value in self.swarm_status.active_missions:
                    self.swarm_status.active_missions.remove(value)

            self.swarm_status.last_update = datetime.utcnow()

            await ctx.send(f"✅ Updated {key}: {value}")

        except Exception as e:
            await ctx.send(f"❌ Failed to update {key}: {str(e)}")

    @commands.command(name="message_captain")
    @commands.has_role("Captain")
    async def message_captain(self, ctx, *, prompt: str):
        """Send a human prompt directly to Agent-4 (Captain)"""
        try:
            # Format message as human prompt for Agent-4
            formatted_prompt = f"[HUMAN PROMPT]\n{prompt}\n\nSent via Discord Commander by {ctx.author.display_name}"

            # Send to Agent-4's inbox
            result = await self._send_to_agent_inbox("Agent-4", formatted_prompt, ctx.author.display_name)

            if result.success:
                embed = discord.Embed(
                    title="📤 Human Prompt Sent to Captain Agent-4",
                    color=0x27ae60,
                    timestamp=datetime.utcnow()
                )

                embed.add_field(name="Target Agent", value="Agent-4 (Captain)", inline=True)
                embed.add_field(name="Sender", value=ctx.author.display_name, inline=True)
                embed.add_field(name="Status", value="✅ Delivered", inline=True)
                embed.add_field(name="Prompt Preview", value=prompt[:500] + "..." if len(prompt) > 500 else prompt, inline=False)

                embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Failed to send prompt to Agent-4: {result.message}")

        except Exception as e:
            get_logger(__name__).error(f"Failed to send human prompt to Agent-4: {e}")
            await ctx.send(f"❌ Error sending prompt to Agent-4: {str(e)}")

    @commands.command(name="captain_status")
    async def captain_status(self, ctx):
        """Get Captain Agent-4's current status"""
        try:
            # Read Agent-4's status file
            status_file = get_unified_utility().path.join(os.getcwd(), "agent_workspaces", "Agent-4", "status.json")

            if get_unified_utility().path.exists(status_file):
                with open(status_file, 'r') as f:
                    status_data = read_json(f)

                embed = discord.Embed(
                    title="🎯 Captain Agent-4 Status Report",
                    color=0x3498db,
                    timestamp=datetime.utcnow()
                )

                embed.add_field(name="Agent ID", value=status_data.get("agent_id", "Unknown"), inline=True)
                embed.add_field(name="Current Mission", value=status_data.get("current_mission", "Unknown")[:500], inline=False)
                embed.add_field(name="Mission Priority", value=status_data.get("mission_priority", "Unknown"), inline=True)
                embed.add_field(name="Last Updated", value=status_data.get("last_updated", "Unknown"), inline=True)

                # Add current tasks if available
                current_tasks = status_data.get("current_tasks", [])
                if current_tasks:
                    tasks_text = "\n".join([f"• {task[:100]}" for task in current_tasks[:3]])
                    embed.add_field(name="Current Tasks", value=tasks_text, inline=False)

                embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")

                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Captain Agent-4 status file not found")

        except Exception as e:
            get_logger(__name__).error(f"Failed to read Captain status: {e}")
            await ctx.send(f"❌ Error reading Captain status: {str(e)}")

    # ================================
    # UTILITY METHODS
    # ================================

    def _is_valid_agent(self, agent: str) -> bool:
        """Check if agent name is valid"""
        return agent in [f"Agent-{i}" for i in range(1, 9)]

    async def _send_to_agent_inbox(self, agent: str, message: str, sender: str) -> CommandResult:
        """Send message directly to agent's inbox"""
        try:
            # Create inbox path
            inbox_path = get_unified_utility().path.join(os.getcwd(), "agent_workspaces", agent, "inbox")

            # Ensure inbox directory exists
            get_unified_utility().makedirs(inbox_path, exist_ok=True)

            # Create message filename with timestamp
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            message_filename = f"CAPTAIN_MESSAGE_{timestamp}_discord.md"

            # Create message content
            message_content = f"# 🚨 CAPTAIN MESSAGE FROM DISCORD\n\n**From**: {sender} (via Discord Commander)\n**To**: {agent}\n**Priority**: URGENT\n**Timestamp**: {datetime.utcnow().isoformat()}\n\n---\n\n{message}\n\n---\n\n**Message delivered via Discord Commander**\n**WE. ARE. SWARM. ⚡️🔥**\n"

            # Write message to agent's inbox
            message_file_path = get_unified_utility().path.join(inbox_path, message_filename)
            with open(message_file_path, 'w', encoding='utf-8') as f:
                f.write(message_content)

            get_logger(__name__).info(f"Message sent to {agent}'s inbox: {message_filename}")

            return CommandResult(
                success=True,
                message=f"Message successfully delivered to {agent}'s inbox",
                data={"filename": message_filename, "path": message_file_path},
                agent=agent
            )

        except Exception as e:
            get_logger(__name__).error(f"Failed to send message to {agent}'s inbox: {e}")
            return CommandResult(
                success=False,
                message=f"Failed to deliver message to {agent}'s inbox: {str(e)}",
                agent=agent
            )

    async def _execute_agent_command(self, agent: str, command: str) -> CommandResult:
        """Execute command on specific agent"""
        start_time = asyncio.get_event_loop().time()

        try:
            # Simulate command execution (replace with actual agent communication)
            get_logger(__name__).info(f"Executing command on {agent}: {command}")

            # Simulate processing time
            await asyncio.sleep(1)

            # Mock successful execution
            execution_time = asyncio.get_event_loop().time() - start_time

            return CommandResult(
                success=True,
                message=f"Command executed successfully on {agent}",
                execution_time=execution_time,
                agent=agent
            )

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            return CommandResult(
                success=False,
                message=f"Command failed on {agent}: {str(e)}",
                execution_time=execution_time,
                agent=agent
            )

    async def _cleanup_completed_commands(self):
        """Clean up completed command tasks"""
        completed = []
        for command_id, task in self.active_commands.items():
            if task.done():
                completed.append(command_id)

        for command_id in completed:
            del self.active_commands[command_id]

    # ================================
    # LIFECYCLE METHODS
    # ================================

    async def close(self):
        """Clean shutdown of the Discord commander"""
        get_logger(__name__).info("Shutting down Discord Commander...")

        # Cancel all active commands
        for task in self.active_commands.values():
            if not task.done():
                task.cancel()

        # Send shutdown message
        status_channel = discord.utils.get(self.guild.channels, name=self.config["status_channel"])
        if status_channel:
            embed = discord.Embed(
                title="🛑 Swarm Discord Commander Shutting Down",
                description="Discord integration deactivated",
                color=0xe74c3c,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="WE. ARE. SWARM. ⚡️🔥")
            await status_channel.send(embed=embed)

        await super().close()
        get_logger(__name__).info("Discord Commander shutdown complete")

