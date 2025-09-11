# -*- coding: utf-8 -*-
"""
Dynamic Agent Commands (V2)
- One source of truth (config/agent_aliases.json)
- Auto-register prefix aliases (!captain, !agent4, !a1, etc.)
- Single slash command: /agent (agent autocomplete, summary toggle)
- Uses MessagingGateway for Agents 1-4 (PyAutoGUI), engine inbox for others
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Tuple
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

SUMMARY_PROMPT = (
    "🔎 QUICK STATUS PING:\n"
    "- 3 bullets: (1) current task, (2) blockers, (3) ETA.\n"
    "- Keep it under 60 seconds.\n"
)

def _load_alias_map() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    cfg = Path("config/agent_aliases.json")
    if not cfg.exists():
        # Defaults if missing
        data = {
            f"Agent-{i}": [f"agent{i}", f"a{i}"] for i in range(1, 9)
        }
    else:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    alias_to_agent: Dict[str, str] = {}
    for agent, aliases in data.items():
        for alias in aliases:
            alias_to_agent[alias.lower()] = agent
        # also map canonical name as alias
        alias_to_agent[agent.lower()] = agent
    return alias_to_agent, data

async def _send_to_agent(
    bot: commands.Bot,
    agent_id: str,
    message: str,
    author_tag: str,
    request_summary: bool = True,
) -> str:
    """Route message via MessagingGateway (Agents 1-4) else engine inbox."""
    payload = message
    if request_summary:
        payload = f"{message}\n\n{SUMMARY_PROMPT}"

    # Prefer MessagingGateway for Agents 1-4
    try:
        idx = int(agent_id.split("-")[-1])
    except Exception:
        idx = 0

    if getattr(bot, "messaging_gateway", None) and 1 <= idx <= 4:
        result = await bot.messaging_gateway.send(agent_id, payload, meta={"source": "discord"})
        return f"🖥️ PyAutoGUI gateway → **{agent_id}**: {result.get('status','sent')}"
    # Fallback to engine inbox
    if getattr(bot, "agent_engine", None):
        await bot.agent_engine.send_to_agent_inbox(agent_id, payload, author_tag)
        return f"📬 Inbox drop → **{agent_id}**: queued"
    raise RuntimeError("No messaging backend available")

def _mk_ok_embed(title: str, desc: str) -> discord.Embed:
    e = discord.Embed(title=title, description=desc, colour=discord.Colour.green())
    return e

def _mk_err_embed(title: str, desc: str) -> discord.Embed:
    e = discord.Embed(title=title, description=desc, colour=discord.Colour.red())
    return e

async def _agent_autocomplete(
    interaction: discord.Interaction, current: str
) -> List[app_commands.Choice[str]]:
    alias_to_agent, by_agent = _load_alias_map()
    seen = set()
    out: List[app_commands.Choice[str]] = []
    q = current.lower()
    # Prefer canonical names, then aliases
    for ag in sorted(by_agent.keys()):
        if q in ag.lower():
            out.append(app_commands.Choice(name=ag, value=ag))
            seen.add(ag.lower())
    for alias, ag in alias_to_agent.items():
        if q in alias and ag.lower() not in seen:
            out.append(app_commands.Choice(name=f"{alias} → {ag}", value=ag))
            seen.add(ag.lower())
        if len(out) >= 20:
            break
    return out

async def setup_dynamic_agent_commands(bot: commands.Bot):
    alias_to_agent, by_agent = _load_alias_map()

    # ---------- Slash command: /agent ----------
    @bot.tree.command(name="agent", description="Send a message to an agent (summary toggle).")
    @app_commands.describe(agent="Agent or alias (autocomplete)", message="What to send",
                           summary="Ask the agent to reply with a 3-bullet status")
    @app_commands.autocomplete(agent=_agent_autocomplete)
    async def agent_cmd(
        interaction: discord.Interaction,
        agent: str,
        message: str,
        summary: bool = True,
    ):
        await interaction.response.defer(ephemeral=True, thinking=True)
        ag = alias_to_agent.get(agent.lower(), agent)
        try:
            status = await _send_to_agent(
                bot, ag, message, author_tag=f"Discord:{interaction.user.id}", request_summary=summary
            )
            await interaction.followup.send(
                embed=_mk_ok_embed("Message dispatched",
                                   f"{status}\n\n**Message:** {message}"),
                ephemeral=True,
            )
        except Exception as e:
            await interaction.followup.send(
                embed=_mk_err_embed("Dispatch failed", str(e)), ephemeral=True
            )

    # ---------- Slash command: /summary_core (Agents 1-4) ----------
    @bot.tree.command(name="summary_core", description="Request quick summaries from Agents 1-4.")
    async def summary_core(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        tasks = []
        for i in range(1, 5):
            tasks.append(_send_to_agent(
                bot, f"Agent-{i}", "Status check requested.", author_tag=f"Discord:{interaction.user.id}", request_summary=True
            ))
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            lines = []
            for i, r in enumerate(results, start=1):
                if isinstance(r, Exception):
                    lines.append(f"Agent-{i}: ❌ {r}")
                else:
                    lines.append(f"{r}")
            await interaction.followup.send(
                embed=_mk_ok_embed("Core summaries requested", "\n".join(lines)),
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                embed=_mk_err_embed("Summary request failed", str(e)), ephemeral=True
            )

    # ---------- Prefix aliases: !captain Hello, etc. ----------
    async def _dispatch_prefix(ctx: commands.Context, target_agent: str, msg: str):
        if not msg.strip():
            await ctx.reply(embed=_mk_err_embed("Missing message", "Usage: `!<alias> <message>`"))
            return
        try:
            status = await _send_to_agent(
                bot, target_agent, msg, author_tag=f"Discord:{ctx.author.id}", request_summary=True
            )
            await ctx.reply(embed=_mk_ok_embed("Message dispatched", f"{status}\n\n**Message:** {msg}"))
        except Exception as e:
            await ctx.reply(embed=_mk_err_embed("Dispatch failed", str(e)))

    # Create one command per alias without repetition
    for agent_id, aliases in by_agent.items():
        for alias in aliases:
            @bot.command(name=alias)  # capture with default arg
            async def _alias_cmd(ctx: commands.Context, *, message: str, _agent=agent_id):
                await _dispatch_prefix(ctx, _agent, message)

    # Generic fallback: !agent <who> <message>
    @bot.command(name="agent")
    async def generic_agent(ctx: commands.Context, who: str, *, message: str):
        ag = alias_to_agent.get(who.lower(), who)
        await _dispatch_prefix(ctx, ag, message)

    # Core shortcut: !summary4
    @bot.command(name="summary4")
    async def summary4(ctx: commands.Context):
        tasks = []
        for i in range(1, 5):
            tasks.append(_send_to_agent(bot, f"Agent-{i}", "Status check requested.", author_tag=f"Discord:{ctx.author.id}", request_summary=True))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        lines = []
        for i, r in enumerate(results, start=1):
            if isinstance(r, Exception):
                lines.append(f"Agent-{i}: ❌ {r}")
            else:
                lines.append(f"{r}")
        await ctx.reply(embed=_mk_ok_embed("Core summaries requested", "\n".join(lines)))

    # Sync slash commands
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"⚠️ Slash sync warning: {e}")
