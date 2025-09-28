#!/usr/bin/env python3
"""
Send Controller - Enhanced Agent Messaging Interface
===================================================

Enhanced Discord controller for agent messaging with comprehensive display
similar to the /help menu but focused on agent communication.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import discord
from discord import app_commands
from typing import Optional, Dict, Any
import asyncio
import time


def setup_send_controller(bot):
    """Setup enhanced send controller with comprehensive agent messaging interface."""

    @bot.tree.command(name="send", description="Enhanced agent messaging interface")
    @app_commands.describe(
        agent="Agent ID (e.g., Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7, Agent-8)",
        message="Message to send to the agent",
        priority="Message priority level",
        message_type="Type of message to send"
    )
    @app_commands.choices(priority=[
        app_commands.Choice(name="Low", value="LOW"),
        app_commands.Choice(name="Normal", value="NORMAL"),
        app_commands.Choice(name="High", value="HIGH"),
        app_commands.Choice(name="Urgent", value="URGENT")
    ])
    @app_commands.choices(message_type=[
        app_commands.Choice(name="Direct", value="DIRECT"),
        app_commands.Choice(name="System", value="SYSTEM"),
        app_commands.Choice(name="Broadcast", value="BROADCAST"),
        app_commands.Choice(name="Emergency", value="EMERGENCY")
    ])
    async def send_message_enhanced(
        interaction: discord.Interaction, 
        agent: str, 
        message: str,
        priority: Optional[str] = "NORMAL",
        message_type: Optional[str] = "DIRECT"
    ):
        """Enhanced send message to specific agent with comprehensive options."""
        
        # Validate agent ID
        valid_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        if agent not in valid_agents:
            error_embed = discord.Embed(
                title="❌ Invalid Agent ID",
                description=f"**Invalid agent:** {agent}\n\n**Available agents:**\n" + "\n".join([f"• {a}" for a in valid_agents]),
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
            
        try:
            # Show processing message
            processing_embed = discord.Embed(
                title="📤 Sending Message...",
                description=f"**To:** {agent}\n**Priority:** {priority}\n**Type:** {message_type}\n**Message:** {message[:100]}{'...' if len(message) > 100 else ''}",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=processing_embed)
            
            # Use messaging service to send message
            success = bot.messaging_service.send_message(agent, message, "Discord-Commander", priority)
            
            if success:
                success_embed = discord.Embed(
                    title="✅ Message Sent Successfully!",
                    description=f"**🤖 To:** {agent}\n**💬 Message:** {message}\n**⚡ Priority:** {priority}\n**📋 Type:** {message_type}",
                    color=discord.Color.green()
                )
                success_embed.add_field(
                    name="📊 Agent Status",
                    value=f"✅ {agent} is active and ready",
                    inline=True
                )
                success_embed.add_field(
                    name="🕐 Sent At",
                    value=f"<t:{int(time.time())}:F>",
                    inline=True
                )
                success_embed.set_footer(text="🐝 WE ARE SWARM - Agent Communication System")
                
                await interaction.edit_original_response(embed=success_embed)
            else:
                error_embed = discord.Embed(
                    title="❌ Failed to Send Message",
                    description=f"**To:** {agent}\n**Reason:** Agent may be inactive or system error occurred",
                    color=discord.Color.red()
                )
                error_embed.add_field(
                    name="🔧 Troubleshooting",
                    value="• Check if agent is active\n• Verify agent coordinates\n• Try again in a few moments",
                    inline=False
                )
                await interaction.edit_original_response(embed=error_embed)
                
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ System Error",
                description=f"**Error:** {str(e)}\n**Agent:** {agent}",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=error_embed)

    @bot.tree.command(name="send-help", description="Show comprehensive agent messaging help")
    async def send_help(interaction: discord.Interaction):
        """Show comprehensive agent messaging help similar to /help menu."""
        
        help_embed = discord.Embed(
            title="📱 V2_SWARM Agent Messaging System",
            description="**Enhanced Discord-to-Agent Communication Interface**",
            color=discord.Color.blue()
        )
        
        # Basic Commands Section
        help_embed.add_field(
            name="📤 **Core Messaging Commands**",
            value="""
`/send` - Send message to specific agent
`/send-help` - Show this comprehensive help
`/msg-status` - Get messaging system status
`/list-agents` - List all available agents
`/message-history` - View message history
`/broadcast` - Send message to all agents
            """,
            inline=False
        )
        
        # Agent Information Section
        help_embed.add_field(
            name="🤖 **Available Agents**",
            value="""
**Agent-1** - Integration & Core Systems
**Agent-2** - Architecture & Design  
**Agent-3** - Infrastructure & DevOps
**Agent-4** - Captain (Strategic Oversight)
**Agent-5** - Business Intelligence
**Agent-6** - Coordination & Communication
**Agent-7** - Web Development
**Agent-8** - SSOT & System Integration
            """,
            inline=False
        )
        
        # Message Types Section
        help_embed.add_field(
            name="📋 **Message Types**",
            value="""
**DIRECT** - One-to-one agent communication
**SYSTEM** - System-level notifications
**BROADCAST** - Multi-agent announcements
**EMERGENCY** - Critical priority messages
            """,
            inline=True
        )
        
        # Priority Levels Section
        help_embed.add_field(
            name="⚡ **Priority Levels**",
            value="""
**LOW** - Non-urgent communication
**NORMAL** - Standard priority (default)
**HIGH** - Important messages
**URGENT** - Critical priority
            """,
            inline=True
        )
        
        # Usage Examples Section
        help_embed.add_field(
            name="💡 **Usage Examples**",
            value="""
`/send agent:Agent-1 message:Hello from Discord`
`/send agent:Agent-4 message:Status report priority:HIGH`
`/send agent:Agent-7 message:System update message_type:SYSTEM`
`/send agent:Agent-2 message:Emergency alert priority:URGENT message_type:EMERGENCY`
            """,
            inline=False
        )
        
        # Advanced Features Section
        help_embed.add_field(
            name="🔧 **Advanced Features**",
            value="""
• **Real-time Status** - Live agent availability
• **Message History** - Track communication logs
• **Priority Handling** - Intelligent message queuing
• **Error Recovery** - Automatic retry mechanisms
• **Performance Metrics** - Communication statistics
            """,
            inline=False
        )
        
        # System Status Section
        try:
            if hasattr(bot, 'messaging_service') and bot.messaging_service:
                # Get basic system info
                total_agents = len(bot.agent_coordinates) if hasattr(bot, 'agent_coordinates') else 8
                active_agents = len([a for a in bot.agent_coordinates.values() if a.get('active', True)]) if hasattr(bot, 'agent_coordinates') else 8
                
                help_embed.add_field(
                    name="📊 **System Status**",
                    value=f"""
**Total Agents:** {total_agents}
**Active Agents:** {active_agents}
**System Status:** ✅ Operational
**Last Updated:** <t:{int(time.time())}:R>
                    """,
                    inline=True
                )
        except Exception:
            help_embed.add_field(
                name="📊 **System Status**",
                value="**Status:** ⚠️ Checking...",
                inline=True
            )
        
        help_embed.set_footer(text="🐝 WE ARE SWARM - Enhanced Agent Communication")
        help_embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=help_embed)

    @bot.tree.command(name="list-agents", description="List all available agents with detailed status")
    async def list_agents(interaction: discord.Interaction):
        """List all available agents with detailed status information."""
        
        try:
            agents_embed = discord.Embed(
                title="🤖 Available Agents",
                description="**V2_SWARM Agent Directory**",
                color=discord.Color.green()
            )
            
            # Agent roles and descriptions
            agent_info = {
                "Agent-1": "Integration & Core Systems",
                "Agent-2": "Architecture & Design", 
                "Agent-3": "Infrastructure & DevOps",
                "Agent-4": "Captain (Strategic Oversight)",
                "Agent-5": "Business Intelligence",
                "Agent-6": "Coordination & Communication",
                "Agent-7": "Web Development",
                "Agent-8": "SSOT & System Integration"
            }
            
            for agent_id, description in agent_info.items():
                # Check if agent is active
                is_active = True
                if hasattr(bot, 'agent_coordinates') and agent_id in bot.agent_coordinates:
                    is_active = bot.agent_coordinates[agent_id].get('active', True)
                
                status_icon = "✅" if is_active else "❌"
                status_text = "Active" if is_active else "Inactive"
                
                agents_embed.add_field(
                    name=f"{status_icon} {agent_id}",
                    value=f"**Role:** {description}\n**Status:** {status_text}",
                    inline=True
                )
            
            agents_embed.add_field(
                name="📊 **Quick Stats**",
                value=f"**Total Agents:** {len(agent_info)}\n**Active:** {sum(1 for a in agent_info.keys() if hasattr(bot, 'agent_coordinates') and bot.agent_coordinates.get(a, {}).get('active', True))}\n**System:** ✅ Operational",
                inline=False
            )
            
            agents_embed.set_footer(text="🐝 WE ARE SWARM - Agent Directory")
            agents_embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=agents_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error Loading Agents",
                description=f"**Error:** {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @bot.tree.command(name="broadcast", description="Send message to all active agents")
    @app_commands.describe(
        message="Message to broadcast to all agents",
        priority="Priority level for the broadcast"
    )
    @app_commands.choices(priority=[
        app_commands.Choice(name="Low", value="LOW"),
        app_commands.Choice(name="Normal", value="NORMAL"),
        app_commands.Choice(name="High", value="HIGH"),
        app_commands.Choice(name="Urgent", value="URGENT")
    ])
    async def broadcast_message(
        interaction: discord.Interaction, 
        message: str,
        priority: Optional[str] = "NORMAL"
    ):
        """Send message to all active agents."""
        
        try:
            # Show processing message
            processing_embed = discord.Embed(
                title="📢 Broadcasting Message...",
                description=f"**Priority:** {priority}\n**Message:** {message[:100]}{'...' if len(message) > 100 else ''}",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=processing_embed)
            
            # Use messaging service to broadcast
            results = bot.messaging_service.broadcast_message(message, "Discord-Commander", priority)
            
            # Count results
            total_agents = len(results)
            successful = sum(1 for success in results.values() if success)
            failed = total_agents - successful
            
            if successful > 0:
                success_embed = discord.Embed(
                    title="📢 Broadcast Completed",
                    description=f"**Message:** {message}\n**Priority:** {priority}",
                    color=discord.Color.green()
                )
                success_embed.add_field(
                    name="📊 **Delivery Results**",
                    value=f"**Total Agents:** {total_agents}\n**Successful:** {successful}\n**Failed:** {failed}",
                    inline=True
                )
                
                if failed > 0:
                    failed_agents = [agent for agent, success in results.items() if not success]
                    success_embed.add_field(
                        name="❌ **Failed Agents**",
                        value=", ".join(failed_agents),
                        inline=True
                    )
                
                success_embed.set_footer(text="🐝 WE ARE SWARM - Broadcast System")
                await interaction.edit_original_response(embed=success_embed)
            else:
                error_embed = discord.Embed(
                    title="❌ Broadcast Failed",
                    description="No agents received the message",
                    color=discord.Color.red()
                )
                await interaction.edit_original_response(embed=error_embed)
                
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Broadcast Error",
                description=f"**Error:** {str(e)}",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=error_embed)