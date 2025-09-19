#!/usr/bin/env python3
"""
Stall Discord Commands
======================

Agent stall/unstall control commands for Discord bot.
Provides emergency stop and resume functionality for agents.
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

import discord
import pyautogui
from discord import app_commands

logger = logging.getLogger(__name__)


def setup_stall_commands(bot):
    """Setup stall-related slash commands."""

    @bot.tree.command(name="stall", description="Stop an agent by sending Ctrl+Shift+Backspace")
    @app_commands.describe(
        agent="Select agent to stall",
        reason="Optional reason for stalling the agent"
    )
    @app_commands.choices(agent=[
        app_commands.Choice(name="Agent-1 (Infrastructure)", value="Agent-1"),
        app_commands.Choice(name="Agent-2 (Architecture)", value="Agent-2"),
        app_commands.Choice(name="Agent-3 (Infrastructure & DevOps)", value="Agent-3"),
        app_commands.Choice(name="Agent-4 (Captain)", value="Agent-4"),
        app_commands.Choice(name="Agent-5 (Business Intelligence)", value="Agent-5"),
        app_commands.Choice(name="Agent-6 (Coordination)", value="Agent-6"),
        app_commands.Choice(name="Agent-7 (Web Development)", value="Agent-7"),
        app_commands.Choice(name="Agent-8 (SSOT & Integration)", value="Agent-8"),
    ])
    async def stall_agent(interaction: discord.Interaction, agent: app_commands.Choice[str], reason: Optional[str] = None):
        """Stop an agent by sending Ctrl+Shift+Backspace to their chat input."""
        agent_id = agent.value
        
        # Validate agent ID
        if agent_id not in bot.agent_coordinates:
            await interaction.response.send_message(f"❌ Invalid agent ID: {agent_id}")
            return
            
        try:
            # Show stalling status
            await interaction.response.send_message(f"🛑 **Stalling {agent.name}...**")
            
            # Get agent coordinates
            coords = bot.agent_coordinates[agent_id]
            chat_coords = coords.get('chat_input_coordinates')
            
            if not chat_coords:
                await interaction.followup.send(f"❌ **No chat input coordinates found for {agent.name}**")
                return
            
            # Execute stall command
            success = _execute_stall_command(chat_coords)
            
            if success:
                reason_text = f"\n📝 **Reason:** {reason}" if reason else ""
                await interaction.followup.send(
                    f"🛑 **Agent Stalled Successfully!**\n\n"
                    f"🤖 **Agent:** {agent.name}\n"
                    f"📍 **Coordinates:** {chat_coords}\n"
                    f"⌨️ **Command:** Ctrl+Shift+Backspace{reason_text}\n\n"
                    f"🐝 **WE ARE SWARM** - Agent stopped!"
                )
            else:
                await interaction.followup.send(f"❌ **Failed to stall {agent.name}**\n\nPlease check coordinates and system status.")
                
        except Exception as e:
            logger.error(f"Error stalling agent {agent_id}: {e}")
            await interaction.followup.send(f"❌ **Error stalling agent:** {e}")

    @bot.tree.command(name="unstall", description="Resume an agent by sending Ctrl+Enter")
    @app_commands.describe(
        agent="Select agent to unstall",
        message="Optional message to send with unstall"
    )
    @app_commands.choices(agent=[
        app_commands.Choice(name="Agent-1 (Infrastructure)", value="Agent-1"),
        app_commands.Choice(name="Agent-2 (Architecture)", value="Agent-2"),
        app_commands.Choice(name="Agent-3 (Infrastructure & DevOps)", value="Agent-3"),
        app_commands.Choice(name="Agent-4 (Captain)", value="Agent-4"),
        app_commands.Choice(name="Agent-5 (Business Intelligence)", value="Agent-5"),
        app_commands.Choice(name="Agent-6 (Coordination)", value="Agent-6"),
        app_commands.Choice(name="Agent-7 (Web Development)", value="Agent-7"),
        app_commands.Choice(name="Agent-8 (SSOT & Integration)", value="Agent-8"),
    ])
    async def unstall_agent(interaction: discord.Interaction, agent: app_commands.Choice[str], message: Optional[str] = None):
        """Resume an agent by sending Ctrl+Enter to their chat input."""
        agent_id = agent.value
        
        # Validate agent ID
        if agent_id not in bot.agent_coordinates:
            await interaction.response.send_message(f"❌ Invalid agent ID: {agent_id}")
            return
            
        try:
            # Show unstalling status
            await interaction.response.send_message(f"▶️ **Unstalling {agent.name}...**")
            
            # Get agent coordinates
            coords = bot.agent_coordinates[agent_id]
            chat_coords = coords.get('chat_input_coordinates')
            
            if not chat_coords:
                await interaction.followup.send(f"❌ **No chat input coordinates found for {agent.name}**")
                return
            
            # Execute unstall command
            success = _execute_unstall_command(chat_coords, message)
            
            if success:
                message_text = f"\n💬 **Message:** {message}" if message else ""
                await interaction.followup.send(
                    f"▶️ **Agent Unstalled Successfully!**\n\n"
                    f"🤖 **Agent:** {agent.name}\n"
                    f"📍 **Coordinates:** {chat_coords}\n"
                    f"⌨️ **Command:** Ctrl+Enter{message_text}\n\n"
                    f"🐝 **WE ARE SWARM** - Agent resumed!"
                )
            else:
                await interaction.followup.send(f"❌ **Failed to unstall {agent.name}**\n\nPlease check coordinates and system status.")
                
        except Exception as e:
            logger.error(f"Error unstalling agent {agent_id}: {e}")
            await interaction.followup.send(f"❌ **Error unstalling agent:** {e}")

    @bot.tree.command(name="stall-status", description="Get stall status for all agents")
    async def stall_status(interaction: discord.Interaction):
        """Get stall status for all agents."""
        try:
            response = "**🛑 Agent Stall Status:**\n\n"
            
            for agent_id, coords in bot.agent_coordinates.items():
                chat_coords = coords.get('chat_input_coordinates')
                status_icon = "✅" if coords.get('active', True) else "❌"
                coords_text = f"({chat_coords[0]}, {chat_coords[1]})" if chat_coords else "No coordinates"
                
                response += f"{status_icon} **{agent_id}** - {coords_text}\n"
            
            response += "\n🐝 **WE ARE SWARM** - Stall system ready!"
            
            await interaction.response.send_message(response)
            
        except Exception as e:
            logger.error(f"Error getting stall status: {e}")
            await interaction.response.send_message(f"❌ Error getting stall status: {e}")

    @bot.tree.command(name="auto-stall", description="Automatically stall inactive agents")
    @app_commands.describe(
        check_hours="Hours to check for inactivity (default: 1)",
        dry_run="Show what would be stalled without actually stalling (default: true)"
    )
    async def auto_stall_inactive(interaction: discord.Interaction, check_hours: Optional[int] = 1, dry_run: Optional[bool] = True):
        """Automatically stall agents that haven't updated their status."""
        try:
            await interaction.response.send_message(f"🔍 **Checking for inactive agents (last {check_hours} hours)...**")
            
            # Get inactive agents
            inactive_agents = _get_inactive_agents(check_hours)
            
            if not inactive_agents:
                await interaction.followup.send("✅ **No inactive agents found!**\n\nAll active agents have updated their status recently.")
                return
            
            # Filter out disabled agents (5, 6, 7, 8 in 4-agent mode)
            active_inactive = [agent for agent in inactive_agents if agent not in ['Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']]
            
            if not active_inactive:
                await interaction.followup.send("✅ **No active agents need stalling!**\n\nInactive agents are disabled agents (5, 6, 7, 8) which are excluded from auto-stall.")
                return
            
            if dry_run:
                response = f"🔍 **DRY RUN - Inactive Agents Found:**\n\n"
                for agent_id in active_inactive:
                    last_update = _get_agent_last_update(agent_id)
                    response += f"🛑 **{agent_id}** - Last update: {last_update}\n"
                
                response += f"\n⚠️ **Would stall {len(active_inactive)} agents**\n"
                response += "Use `dry_run: false` to actually stall these agents."
                
                await interaction.followup.send(response)
            else:
                # Actually stall the inactive agents
                stalled_count = 0
                failed_count = 0
                
                for agent_id in active_inactive:
                    coords = bot.agent_coordinates.get(agent_id)
                    if coords and coords.get('chat_input_coordinates'):
                        success = _execute_stall_command(coords['chat_input_coordinates'])
                        if success:
                            stalled_count += 1
                        else:
                            failed_count += 1
                
                response = f"🛑 **Auto-Stall Complete!**\n\n"
                response += f"✅ **Stalled:** {stalled_count} agents\n"
                if failed_count > 0:
                    response += f"❌ **Failed:** {failed_count} agents\n"
                
                response += f"\n🐝 **WE ARE SWARM** - Inactive agents stalled!"
                await interaction.followup.send(response)
                
        except Exception as e:
            logger.error(f"Error in auto-stall: {e}")
            await interaction.followup.send(f"❌ **Error in auto-stall:** {e}")


def _execute_stall_command(coords: list) -> bool:
    """Execute stall command at specified coordinates."""
    try:
        x, y = coords[0], coords[1]
        
        # Move to coordinates
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.2)
        
        # Click to focus
        pyautogui.click()
        time.sleep(0.2)
        
        # Send Ctrl+Shift+Backspace
        pyautogui.hotkey('ctrl', 'shift', 'backspace')
        time.sleep(0.5)
        
        logger.info(f"Stall command executed at coordinates ({x}, {y})")
        return True
        
    except Exception as e:
        logger.error(f"Error executing stall command: {e}")
        return False


def _execute_unstall_command(coords: list, message: Optional[str] = None) -> bool:
    """Execute unstall command at specified coordinates."""
    try:
        x, y = coords[0], coords[1]
        
        # Move to coordinates
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.2)
        
        # Click to focus
        pyautogui.click()
        time.sleep(0.2)
        
        # Clear any existing content
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        
        # Type message if provided
        if message:
            pyautogui.typewrite(message, interval=0.01)
            time.sleep(0.2)
        
        # Send Ctrl+Enter
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(0.5)
        
        logger.info(f"Unstall command executed at coordinates ({x}, {y}) with message: {message}")
        return True
        
    except Exception as e:
        logger.error(f"Error executing unstall command: {e}")
        return False


def _get_inactive_agents(check_hours: int = 1) -> List[str]:
    """Get list of agents that haven't updated their status recently."""
    inactive_agents = []
    cutoff_time = datetime.now() - timedelta(hours=check_hours)
    
    # Check all agent workspaces
    for agent_id in ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']:
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        
        if not status_file.exists():
            inactive_agents.append(agent_id)
            continue
        
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
            
            last_updated_str = status_data.get('last_updated', '')
            if not last_updated_str:
                inactive_agents.append(agent_id)
                continue
            
            # Parse last updated time (handle multiple formats)
            try:
                # Try ISO format first
                if 'T' in last_updated_str and 'Z' in last_updated_str:
                    last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
                    # Convert to naive datetime for comparison
                    last_updated = last_updated.replace(tzinfo=None)
                else:
                    # Try standard format
                    last_updated = datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # If parsing fails, consider agent inactive
                inactive_agents.append(agent_id)
                continue
            
            if last_updated < cutoff_time:
                inactive_agents.append(agent_id)
                
        except Exception as e:
            logger.error(f"Error checking status for {agent_id}: {e}")
            inactive_agents.append(agent_id)
    
    return inactive_agents


def _get_agent_last_update(agent_id: str) -> str:
    """Get the last update time for an agent."""
    status_file = Path(f"agent_workspaces/{agent_id}/status.json")
    
    if not status_file.exists():
        return "No status file"
    
    try:
        with open(status_file, 'r') as f:
            status_data = json.load(f)
        
        return status_data.get('last_updated', 'Unknown')
        
    except Exception as e:
        logger.error(f"Error reading status for {agent_id}: {e}")
        return "Error reading status"
