#!/usr/bin/env python3
"""
UI Embeds Manager V2
===================

V2 compliant UI embeds manager with modular architecture.
"""

import logging
from typing import Dict, Any, Optional, List
import discord
from discord import app_commands

from ..ui.embed_builder import EmbedBuilder
from ..ui.embed_types import EmbedType, EmbedConfig
from ..ui.interaction_handlers import InteractionHandler, ButtonFactory

logger = logging.getLogger(__name__)


class UIEmbedManager:
    """V2 compliant UI embed manager with modular design."""
    
    def __init__(self):
        self.embed_builder = EmbedBuilder()
        self.interaction_handler = InteractionHandler()
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Setup default interaction handlers."""
        # Register common button handlers
        self.interaction_handler.register_button_handler(
            "help_button", self._handle_help_button
        )
        self.interaction_handler.register_button_handler(
            "status_button", self._handle_status_button
        )
        self.interaction_handler.register_button_handler(
            "refresh_button", self._handle_refresh_button
        )
    
    async def _handle_help_button(self, interaction: discord.Interaction):
        """Handle help button click."""
        embed = self.embed_builder.create_embed(EmbedConfig(
            title="Help",
            description="Available commands and features",
            embed_type=EmbedType.HELP
        ))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _handle_status_button(self, interaction: discord.Interaction):
        """Handle status button click."""
        embed = self.embed_builder.create_embed(EmbedConfig(
            title="System Status",
            description="Current system status information",
            embed_type=EmbedType.SYSTEM_STATUS
        ))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _handle_refresh_button(self, interaction: discord.Interaction):
        """Handle refresh button click."""
        await interaction.response.defer()
        # Add refresh logic here
        await interaction.followup.send("✅ Refreshed!", ephemeral=True)
    
    def create_agent_status_view(self, agent_id: str, status: str) -> discord.ui.View:
        """Create a view for agent status display."""
        view = discord.ui.View()
        
        # Add status button
        status_button = ButtonFactory.create_success_button(
            "View Status", f"status_{agent_id}"
        )
        view.add_item(status_button)
        
        # Add refresh button
        refresh_button = ButtonFactory.create_button(
            "Refresh", discord.ButtonStyle.secondary, "🔄", 
            custom_id=f"refresh_{agent_id}"
        )
        view.add_item(refresh_button)
        
        return view
    
    def create_help_view(self) -> discord.ui.View:
        """Create a help view with navigation buttons."""
        view = discord.ui.View()
        
        # Add help sections
        sections = [
            ("Commands", "help_commands"),
            ("Agents", "help_agents"),
            ("System", "help_system")
        ]
        
        for label, custom_id in sections:
            button = ButtonFactory.create_button(
                label, discord.ButtonStyle.primary, custom_id=custom_id
            )
            view.add_item(button)
        
        return view
    
    async def handle_interaction(self, interaction: discord.Interaction):
        """Handle UI interactions."""
        await self.interaction_handler.handle_interaction(interaction)
    
    def create_success_message(self, title: str, message: str) -> discord.Embed:
        """Create a success message embed."""
        return self.embed_builder.create_success_embed(title, message)
    
    def create_error_message(self, title: str, message: str) -> discord.Embed:
        """Create an error message embed."""
        return self.embed_builder.create_error_embed(title, message)
    
    def create_agent_status_message(self, agent_id: str, status: str, details: str = "") -> discord.Embed:
        """Create an agent status message embed."""
        fields = {"Status": status}
        if details:
            fields["Details"] = details
            
        config = EmbedConfig(
            title=f"Agent {agent_id} Status",
            fields=fields,
            embed_type=EmbedType.AGENT_STATUS
        )
        return self.embed_builder.create_embed(config)
    
    def create_system_status_message(self, components: Dict[str, str]) -> discord.Embed:
        """Create a system status message embed."""
        config = EmbedConfig(
            title="System Status",
            fields=components,
            embed_type=EmbedType.SYSTEM_STATUS
        )
        return self.embed_builder.create_embed(config)
