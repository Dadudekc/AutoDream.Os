"""
Discord Agent Control Commands
===============================

Slash commands for easy agent control through Discord.
Implements user-friendly interface for agent interaction.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging

try:
    import discord
    from discord import app_commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)


class AgentControlCommands:
    """Agent control slash commands for Discord"""

    def __init__(self, bot, messaging_service=None):
        """Initialize agent control commands"""
        self.bot = bot
        self.messaging_service = messaging_service
        self.logger = logger

    def register_commands(self, tree: app_commands.CommandTree):
        """Register all agent control commands"""
        if not DISCORD_AVAILABLE:
            return

        @tree.command(name="send_message", description="Send message to an agent")
        @app_commands.describe(
            agent_id="Target agent (Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)",
            message="Message content to send",
        )
        async def send_message_command(
            interaction: discord.Interaction, agent_id: str, message: str
        ):
            """Send custom message to agent"""
            await self._handle_send_message(interaction, agent_id, message)

        @tree.command(name="run_scan", description="Run project scanner")
        @app_commands.describe(scan_type="Type of scan (full, compliance, dependencies, health)")
        async def run_scan_command(interaction: discord.Interaction, scan_type: str = "full"):
            """Run project scanner"""
            await self._handle_run_scan(interaction, scan_type)

        @tree.command(name="agent_status", description="Get agent status")
        @app_commands.describe(agent_id="Agent to check (leave empty for all agents)")
        async def agent_status_command(
            interaction: discord.Interaction, agent_id: str | None = None
        ):
            """Get agent status information"""
            await self._handle_agent_status(interaction, agent_id)

        @tree.command(name="custom_task", description="Assign custom task to agent")
        @app_commands.describe(
            agent_id="Target agent", task_title="Task title", task_description="Task description"
        )
        async def custom_task_command(
            interaction: discord.Interaction, agent_id: str, task_title: str, task_description: str
        ):
            """Assign custom task to agent"""
            await self._handle_custom_task(interaction, agent_id, task_title, task_description)

        @tree.command(name="fix_violations", description="Fix V2 compliance violations")
        async def fix_violations_command(interaction: discord.Interaction):
            """Fix V2 compliance violations"""
            await self._handle_fix_violations(interaction)

        self.logger.info("Agent control commands registered")

    def register_regular_commands(self, bot):
        """Register regular commands (help, ping) with Discord bot."""
        if not DISCORD_AVAILABLE or not bot:
            return

        # Add help command
        @bot.command(name="help")
        async def help_command(ctx):
            """Show help information."""
            help_text = """🤖 Discord Commander - Agent Control Hub

**Available Commands:**
- `!help` - Show this help message
- `!ping` - Test bot responsiveness
- `/send_message <agent_id> <message>` - Send message to agent
- `/agent_status [agent_id]` - Get agent status
- `/run_scan [scan_type]` - Run project scanner
- `/custom_task <agent_id> <title> <description>` - Assign custom task
- `/fix_violations` - Fix V2 compliance violations

**Examples:**
- `/send_message Agent-5 Check project status`
- `/agent_status Agent-4`
- `/run_scan compliance`
"""
            await ctx.send(help_text)

        # Add ping command
        @bot.command(name="ping")
        async def ping_command(ctx):
            """Test bot responsiveness."""
            await ctx.send("🏓 Pong! Bot is responsive.")

        self.logger.info("Regular commands (help, ping) registered")

    async def _handle_send_message(
        self, interaction: discord.Interaction, agent_id: str, message: str
    ):
        """Handle /send_message command"""
        try:
            await interaction.response.defer()

            # Validate agent ID
            valid_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            if agent_id not in valid_agents:
                await interaction.followup.send(
                    f"❌ Invalid agent ID. Use: {', '.join(valid_agents)}", ephemeral=True
                )
                return

            # Send message via messaging service
            if self.messaging_service:
                # Use consolidated messaging service
                import subprocess

                result = subprocess.run(
                    [
                        "python",
                        "-m",
                        "src.services.consolidated_messaging_service",
                        "send",
                        "--agent",
                        agent_id,
                        "--message",
                        message,
                        "--from-agent",
                        "Discord-User",
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message delivered to **{agent_id}**",
                        color=discord.Color.green(),
                    )
                    embed.add_field(name="Content", value=message[:1000], inline=False)
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send(
                        f"❌ Failed to send message: {result.stderr}", ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    "⚠️ Messaging service not available", ephemeral=True
                )

        except Exception as e:
            self.logger.error(f"Error in send_message: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

    async def _handle_run_scan(self, interaction: discord.Interaction, scan_type: str):
        """Handle /run_scan command"""
        try:
            await interaction.response.defer()

            # Run project scanner
            import subprocess

            scan_commands = {
                "full": ["python", "tools/simple_project_scanner.py"],
                "compliance": [
                    "python",
                    "tools/simple_project_scanner.py",
                    "--focus",
                    "compliance",
                ],
                "dependencies": [
                    "python",
                    "tools/simple_project_scanner.py",
                    "--focus",
                    "dependencies",
                ],
                "health": ["python", "tools/simple_project_scanner.py", "--focus", "health"],
            }

            command = scan_commands.get(scan_type, scan_commands["full"])

            result = subprocess.run(command, capture_output=True, text=True, timeout=30)

            embed = discord.Embed(
                title=f"📊 Project Scan: {scan_type.title()}",
                description="Scan completed successfully"
                if result.returncode == 0
                else "Scan had issues",
                color=discord.Color.blue() if result.returncode == 0 else discord.Color.orange(),
            )

            # Add summary (first 1000 chars of output)
            output_summary = result.stdout[:1000] if result.stdout else "No output"
            embed.add_field(name="Results", value=f"```{output_summary}```", inline=False)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in run_scan: {e}")
            await interaction.followup.send(f"❌ Error running scan: {str(e)}", ephemeral=True)

    async def _handle_agent_status(self, interaction: discord.Interaction, agent_id: str | None):
        """Handle /agent_status command"""
        try:
            await interaction.response.defer()

            # Get agent status using captain CLI
            import subprocess

            result = subprocess.run(
                ["python", "tools/captain_cli.py", "status"], capture_output=True, text=True
            )

            if result.returncode == 0:
                embed = discord.Embed(
                    title="🤖 Agent Status",
                    description="Current agent status overview",
                    color=discord.Color.green(),
                )

                # Parse output and format
                output_lines = result.stdout.split("\n")[:20]
                status_text = "\n".join(output_lines)

                embed.add_field(name="Status", value=f"```{status_text}```", inline=False)

                if agent_id:
                    embed.add_field(name="Filter", value=f"Showing: {agent_id}", inline=False)

                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Failed to get status: {result.stderr}", ephemeral=True
                )

        except Exception as e:
            self.logger.error(f"Error in agent_status: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

    async def _handle_custom_task(
        self,
        interaction: discord.Interaction,
        agent_id: str,
        task_title: str,
        task_description: str,
    ):
        """Handle /custom_task command"""
        try:
            await interaction.response.defer()

            # Validate agent ID
            valid_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            if agent_id not in valid_agents:
                await interaction.followup.send(
                    f"❌ Invalid agent ID. Use: {', '.join(valid_agents)}", ephemeral=True
                )
                return

            # Assign task using simple workflow automation
            import subprocess

            result = subprocess.run(
                [
                    "python",
                    "tools/simple_workflow_automation.py",
                    "assign",
                    "--task-id",
                    f'DISCORD_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                    "--title",
                    task_title,
                    "--description",
                    task_description,
                    "--to",
                    agent_id,
                    "--from",
                    "Discord-User",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                embed = discord.Embed(
                    title="✅ Task Assigned",
                    description=f"Custom task assigned to **{agent_id}**",
                    color=discord.Color.green(),
                )
                embed.add_field(name="Title", value=task_title, inline=False)
                embed.add_field(name="Description", value=task_description[:500], inline=False)
                embed.add_field(name="Agent", value=agent_id, inline=True)

                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Failed to assign task: {result.stderr}", ephemeral=True
                )

        except Exception as e:
            self.logger.error(f"Error in custom_task: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

    async def _handle_fix_violations(self, interaction: discord.Interaction):
        """Handle /fix_violations command"""
        try:
            await interaction.response.defer()

            # Run quality gates to fix violations
            import subprocess

            result = subprocess.run(
                ["python", "quality_gates.py"], capture_output=True, text=True, timeout=60
            )

            if result.returncode == 0:
                embed = discord.Embed(
                    title="✅ Violations Fixed",
                    description="V2 compliance violations have been addressed",
                    color=discord.Color.green(),
                )

                # Parse output for summary
                output_lines = result.stdout.split("\n")[:10]
                summary_text = "\n".join(output_lines)

                embed.add_field(name="Fix Summary", value=f"```{summary_text}```", inline=False)

                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="⚠️ Fix Issues",
                    description="Some violations could not be automatically fixed",
                    color=discord.Color.orange(),
                )

                error_summary = result.stderr[:500] if result.stderr else "Unknown error"
                embed.add_field(name="Issues", value=f"```{error_summary}```", inline=False)

                await interaction.followup.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in fix_violations: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


# Import datetime for task IDs
from datetime import datetime

__all__ = ["AgentControlCommands"]
