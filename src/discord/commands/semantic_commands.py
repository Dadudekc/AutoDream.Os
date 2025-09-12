"""
Discord commands: /route and /similar_status
Assumes discord.py app_commands setup with a running Bot/Tree.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discord.ext import commands

    import discord
    from discord import app_commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

    # Create dummy classes for type hints when discord is not available
    class discord:
        class Interaction:
            pass

    class app_commands:
        class command:
            def __init__(self, **kwargs):
                pass

        class describe:
            def __init__(self, **kwargs):
                pass

    class commands:
        class Cog:
            pass

        class Bot:
            pass


from src.core.semantic.router_hooks import route_message, similar_status


class SemanticCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="route", description="Semantic route a task to best agent(s)")
    @app_commands.describe(task="Natural language task description")
    async def route(self, interaction: discord.Interaction, task: str):
        if not DISCORD_AVAILABLE:
            return

        await interaction.response.defer(thinking=True)
        res = route_message(task)
        # Compact pretty-print
        view = {
            "priority": res.get("priority"),
            "agent_suggestions": [
                {"agent": x["agent"], "score": round(float(x["score"]), 3)}
                for x in res.get("agent_suggestions", [])[:3]
            ],
            "context_hits": [
                {"id": x["id"], "score": round(float(x["score"]), 3), "meta": x.get("meta", {})}
                for x in res.get("context_hits", [])[:3]
            ],
        }
        await interaction.followup.send(f"```json\n{json.dumps(view, indent=2)}\n```")

    @app_commands.command(
        name="similar_status", description="Find similar agent statuses (text or JSON)"
    )
    @app_commands.describe(query="Text query or JSON blob")
    async def similar_status_cmd(self, interaction: discord.Interaction, query: str):
        if not DISCORD_AVAILABLE:
            return

        await interaction.response.defer(thinking=True)
        try:
            payload = json.loads(query)
        except Exception:
            payload = query
        res = similar_status(payload)
        # top-3 only
        res["results"] = res.get("results", [])[:3]
        await interaction.followup.send(f"```json\n{json.dumps(res, indent=2)}\n```")


async def setup_semantic_commands(bot: commands.Bot):
    if DISCORD_AVAILABLE:
        await bot.add_cog(SemanticCommands(bot))
    # If using CommandTree directly, ensure sync elsewhere
