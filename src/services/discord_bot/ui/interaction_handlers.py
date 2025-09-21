#!/usr/bin/env python3
"""
Interaction Handlers
===================

Discord interaction handlers for buttons, selects, and other UI components.
"""

import logging
import asyncio
from typing import Dict, Callable, Any, Optional
import discord
from discord import app_commands

logger = logging.getLogger(__name__)


class InteractionHandler:
    """Handles Discord interactions for UI components."""
    
    def __init__(self):
        self.button_handlers: Dict[str, Callable] = {}
        self.select_handlers: Dict[str, Callable] = {}
        self.modal_handlers: Dict[str, Callable] = {}
    
    def register_button_handler(self, custom_id: str, handler: Callable):
        """Register a button click handler."""
        self.button_handlers[custom_id] = handler
        logger.debug(f"Registered button handler for: {custom_id}")
    
    def register_select_handler(self, custom_id: str, handler: Callable):
        """Register a select menu handler."""
        self.select_handlers[custom_id] = handler
        logger.debug(f"Registered select handler for: {custom_id}")
    
    def register_modal_handler(self, custom_id: str, handler: Callable):
        """Register a modal submit handler."""
        self.modal_handlers[custom_id] = handler
        logger.debug(f"Registered modal handler for: {custom_id}")
    
    async def handle_interaction(self, interaction: discord.Interaction):
        """Handle Discord interactions."""
        try:
            custom_id = interaction.data.get('custom_id', '')
            
            if custom_id in self.button_handlers:
                handler = self.button_handlers[custom_id]
                if callable(handler):
                    await handler(interaction)
            
            elif custom_id in self.select_handlers:
                handler = self.select_handlers[custom_id]
                if callable(handler):
                    await handler(interaction)
            
            elif custom_id in self.modal_handlers:
                handler = self.modal_handlers[custom_id]
                if callable(handler):
                    await handler(interaction)
            
        except Exception as e:
            logger.error(f"❌ Error handling interaction: {e}")
            try:
                await interaction.response.send_message(
                    "❌ Error processing interaction. Please try again.",
                    ephemeral=True
                )
            except:
                logger.error("Failed to send error response")


class ButtonFactory:
    """Factory for creating Discord buttons."""
    
    @staticmethod
    def create_button(
        label: str,
        style: discord.ButtonStyle = discord.ButtonStyle.primary,
        emoji: Optional[str] = None,
        disabled: bool = False,
        url: Optional[str] = None
    ) -> discord.ui.Button:
        """Create a Discord button."""
        return discord.ui.Button(
            label=label,
            style=style,
            emoji=emoji,
            disabled=disabled,
            url=url
        )
    
    @staticmethod
    def create_success_button(label: str, custom_id: str) -> discord.ui.Button:
        """Create a success button."""
        button = discord.ui.Button(
            label=label,
            style=discord.ButtonStyle.success,
            custom_id=custom_id
        )
        return button
    
    @staticmethod
    def create_danger_button(label: str, custom_id: str) -> discord.ui.Button:
        """Create a danger button."""
        button = discord.ui.Button(
            label=label,
            style=discord.ButtonStyle.danger,
            custom_id=custom_id
        )
        return button
