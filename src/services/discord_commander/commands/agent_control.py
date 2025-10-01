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
from typing import Optional

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
            message="Message content to send"
        )
        async def send_message_command(
            interaction: discord.Interaction,
            agent_id: str,
            message: str
        ):
            """Send custom message to agent"""
            await self._handle_send_message(interaction, agent_id, message)
        
        @tree.command(name="run_scan", description="Run project scanner")
        @app_commands.describe(
            scan_type="Type of scan (full, compliance, dependencies, health)"
        )
        async def run_scan_command(
            interaction: discord.Interaction,
            scan_type: str = "full"
        ):
            """Run project scanner"""
            await self._handle_run_scan(interaction, scan_type)
        
        @tree.command(name="agent_status", description="Get agent status")
        @app_commands.describe(
            agent_id="Agent to check (leave empty for all agents)"
        )
        async def agent_status_command(
            interaction: discord.Interaction,
            agent_id: Optional[str] = None
        ):
            """Get agent status information"""
            await self._handle_agent_status(interaction, agent_id)
        
        @tree.command(name="custom_task", description="Assign custom task to agent")
        @app_commands.describe(
            agent_id="Target agent",
            task_title="Task title",
            task_description="Task description"
        )
        async def custom_task_command(
            interaction: discord.Interaction,
            agent_id: str,
            task_title: str,
            task_description: str
        ):
            """Assign custom task to agent"""
            await self._handle_custom_task(interaction, agent_id, task_title, task_description)
        
        self.logger.info("Agent control commands registered")
    
    async def _handle_send_message(
        self,
        interaction: discord.Interaction,
        agent_id: str,
        message: str
    ):
        """Handle /send_message command"""
        try:
            await interaction.response.defer()
            
            # Validate agent ID
            valid_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            if agent_id not in valid_agents:
                await interaction.followup.send(
                    f"❌ Invalid agent ID. Use: {', '.join(valid_agents)}",
                    ephemeral=True
                )
                return
            
            # Send message via messaging service
            if self.messaging_service:
                # Use consolidated messaging service
                import subprocess
                result = subprocess.run([
                    'python', '-m', 'src.services.consolidated_messaging_service',
                    'send', '--agent', agent_id,
                    '--message', message,
                    '--from-agent', 'Discord-User'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message delivered to **{agent_id}**",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Content", value=message[:1000], inline=False)
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send(
                        f"❌ Failed to send message: {result.stderr}",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    "⚠️ Messaging service not available",
                    ephemeral=True
                )
        
        except Exception as e:
            self.logger.error(f"Error in send_message: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
    
    async def _handle_run_scan(
        self,
        interaction: discord.Interaction,
        scan_type: str
    ):
        """Handle /run_scan command"""
        try:
            await interaction.response.defer()
            
            # Run project scanner
            import subprocess
            
            scan_commands = {
                'full': ['python', 'tools/simple_project_scanner.py'],
                'compliance': ['python', 'tools/simple_project_scanner.py', '--focus', 'compliance'],
                'dependencies': ['python', 'tools/simple_project_scanner.py', '--focus', 'dependencies'],
                'health': ['python', 'tools/simple_project_scanner.py', '--focus', 'health']
            }
            
            command = scan_commands.get(scan_type, scan_commands['full'])
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            embed = discord.Embed(
                title=f"📊 Project Scan: {scan_type.title()}",
                description="Scan completed successfully" if result.returncode == 0 else "Scan had issues",
                color=discord.Color.blue() if result.returncode == 0 else discord.Color.orange()
            )
            
            # Add summary (first 1000 chars of output)
            output_summary = result.stdout[:1000] if result.stdout else "No output"
            embed.add_field(name="Results", value=f"```{output_summary}```", inline=False)
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            self.logger.error(f"Error in run_scan: {e}")
            await interaction.followup.send(f"❌ Error running scan: {str(e)}", ephemeral=True)
    
    async def _handle_agent_status(
        self,
        interaction: discord.Interaction,
        agent_id: Optional[str]
    ):
        """Handle /agent_status command"""
        try:
            await interaction.response.defer()
            
            # Get agent status using captain CLI
            import subprocess
            
            result = subprocess.run(
                ['python', 'tools/captain_cli.py', 'status'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                embed = discord.Embed(
                    title="🤖 Agent Status",
                    description="Current agent status overview",
                    color=discord.Color.green()
                )
                
                # Parse output and format
                output_lines = result.stdout.split('\n')[:20]
                status_text = '\n'.join(output_lines)
                
                embed.add_field(name="Status", value=f"```{status_text}```", inline=False)
                
                if agent_id:
                    embed.add_field(name="Filter", value=f"Showing: {agent_id}", inline=False)
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Failed to get status: {result.stderr}",
                    ephemeral=True
                )
        
        except Exception as e:
            self.logger.error(f"Error in agent_status: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
    
    async def _handle_custom_task(
        self,
        interaction: discord.Interaction,
        agent_id: str,
        task_title: str,
        task_description: str
    ):
        """Handle /custom_task command"""
        try:
            await interaction.response.defer()
            
            # Validate agent ID
            valid_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            if agent_id not in valid_agents:
                await interaction.followup.send(
                    f"❌ Invalid agent ID. Use: {', '.join(valid_agents)}",
                    ephemeral=True
                )
                return
            
            # Assign task using simple workflow automation
            import subprocess
            
            result = subprocess.run([
                'python', 'tools/simple_workflow_automation.py',
                'assign',
                '--task-id', f'DISCORD_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                '--title', task_title,
                '--description', task_description,
                '--to', agent_id,
                '--from', 'Discord-User'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                embed = discord.Embed(
                    title="✅ Task Assigned",
                    description=f"Custom task assigned to **{agent_id}**",
                    color=discord.Color.green()
                )
                embed.add_field(name="Title", value=task_title, inline=False)
                embed.add_field(name="Description", value=task_description[:500], inline=False)
                embed.add_field(name="Agent", value=agent_id, inline=True)
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Failed to assign task: {result.stderr}",
                    ephemeral=True
                )
        
        except Exception as e:
            self.logger.error(f"Error in custom_task: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


# Import datetime for task IDs
from datetime import datetime


__all__ = ['AgentControlCommands']

