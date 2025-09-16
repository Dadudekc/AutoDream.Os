import logging
logger = logging.getLogger(__name__)
"""
Dynamic Agent Commands (V2)
- One source of truth (config/agent_aliases.json)
- Auto-register prefix aliases (!captain, !agent4, !a1, etc.)
- Single slash command: /agent (agent autocomplete, summary toggle)
- Uses MessagingGateway for Agents 1-4 (PyAutoGUI), engine inbox for others
"""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
SUMMARY_PROMPT = """- 3 bullets: (1) current task, (2) blockers, (3) ETA.
- This is a message from the GENERAL to the core agents.
"""


def _load_alias_map() ->tuple[dict[str, str], dict[str, list[str]]]:
    cfg = Path('config/agent_aliases.json')
    if not cfg.exists():
        data = {f'Agent-{i}': [f'agent{i}', f'a{i}'] for i in range(1, 9)}
    else:
        data = json.loads(cfg.read_text(encoding='utf-8'))
    alias_to_agent: dict[str, str] = {}
    for agent, aliases in data.items():
        for alias in aliases:
            alias_to_agent[alias.lower()] = agent
        alias_to_agent[agent.lower()] = agent
    return alias_to_agent, data


async def _send_to_agent(bot: commands.Bot, agent_id: str, message: str,
    author_tag: str, request_summary: bool=True, message_type: str=
    'general_to_agent') ->str:
    """Route message via MessagingGateway (Agents 1-4) else engine inbox."""
    payload = message
    if request_summary:
        payload = f'{message}\n\n{SUMMARY_PROMPT}'
    meta = {'source': 'discord', 'message_type': message_type, 'author_tag':
        author_tag}
    try:
        idx = int(agent_id.split('-')[-1])
    except Exception:
        idx = 0
    if getattr(bot, 'messaging_gateway', None) and 1 <= idx <= 4:
        result = await bot.messaging_gateway.send(agent_id, payload, meta=meta)
        return (
            f"🖥️ PyAutoGUI gateway → **{agent_id}**: {result.get('status', 'sent')}"
            )
    if getattr(bot, 'agent_engine', None):
        await bot.agent_engine.send_to_agent_inbox(agent_id, payload,
            author_tag)
        return f'📬 Inbox drop → **{agent_id}**: queued'
    raise RuntimeError('No messaging backend available')


def _mk_ok_embed(title: str, desc: str) ->discord.Embed:
    e = discord.Embed(title=title, description=desc, colour=discord.Colour.
        green())
    return e


def _mk_err_embed(title: str, desc: str) ->discord.Embed:
    e = discord.Embed(title=title, description=desc, colour=discord.Colour.
        red())
    return e


async def _agent_autocomplete(interaction: discord.Interaction, current: str
    ) ->list[app_commands.Choice[str]]:
    alias_to_agent, by_agent = _load_alias_map()
    seen = set()
    out: list[app_commands.Choice[str]] = []
    q = current.lower()
    for ag in sorted(by_agent.keys()):
        if q in ag.lower():
            out.append(app_commands.Choice(name=ag, value=ag))
            seen.add(ag.lower())
    for alias, ag in alias_to_agent.items():
        if q in alias and ag.lower() not in seen:
            out.append(app_commands.Choice(name=f'{alias} → {ag}', value=ag))
            seen.add(ag.lower())
        if len(out) >= 20:
            break
    return out


urgent_message_cache: dict[str, dict] = {}


async def handle_keyboard_shortcut(message: discord.Message, bot: commands.Bot
    ):
    """Handle keyboard shortcuts for high-priority messaging."""
    alias_to_agent, by_agent = _load_alias_map()
    content = message.content.strip()
    if content.upper().startswith(('URGENT:', '!URGENT')):
        parts = content.replace('URGENT:', '').replace('!urgent', '').strip(
            ).split(' ', 1)
        if len(parts) >= 2:
            agent_name = parts[0]
            urgent_content = parts[1]
            ag = alias_to_agent.get(agent_name.lower(), agent_name)
            if ag in [f'Agent-{i}' for i in range(1, 9)
                ] or ag in alias_to_agent.values():
                try:
                    urgent_message = f'🚨 URGENT KEYBOARD: {urgent_content}'
                    status = await _send_to_agent(bot, ag, urgent_message,
                        author_tag=f'Discord:{message.author.id}',
                        request_summary=False, message_type=
                        'urgent_keyboard_to_agent')
                    embed = _mk_ok_embed('🚨 URGENT Keyboard to Agent Message',
                        f"""**Agent:** {ag}
**Status:** {status}

**Message:** {urgent_message}

*Type: Urgent Keyboard to Agent*
*Triggered by keyboard shortcut*"""
                        )
                    await message.reply(embed=embed, mention_author=False)
                    return True
                except Exception as e:
                    embed = _mk_err_embed('🚨 Urgent Keyboard Shortcut Failed',
                        str(e))
                    await message.reply(embed=embed, mention_author=False)
                    return True
    return False


async def setup_dynamic_agent_commands(bot: commands.Bot):
    alias_to_agent, by_agent = _load_alias_map()

    @bot.tree.command(name='urgent', description=
        'Send URGENT high-priority message to agent (Ctrl+Enter delivery).')
    @app_commands.describe(agent='Agent or alias (autocomplete)', message=
        'Urgent message to send immediately')
    @app_commands.autocomplete(agent=_agent_autocomplete)
    async def urgent_cmd(interaction: discord.Interaction, agent: str,
        message: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        ag = alias_to_agent.get(agent.lower(), agent)
        try:
            urgent_message = f'🚨 URGENT: {message}'
            status = await _send_to_agent(bot, ag, urgent_message,
                author_tag=f'Discord:{interaction.user.id}',
                request_summary=False, message_type='urgent_to_agent')
            await interaction.followup.send(embed=_mk_ok_embed(
                '🚨 URGENT to Agent Message Dispatched',
                f"""**Agent:** {ag}
**Status:** {status}

**Message:** {urgent_message}

*Type: Urgent to Agent*
*Delivered via Ctrl+Enter priority system*"""
                ), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=_mk_err_embed(
                '🚨 Urgent Dispatch Failed', str(e)), ephemeral=True)

    @bot.tree.command(name='agent', description=
        'Send a message to an agent (summary toggle).')
    @app_commands.describe(agent='Agent or alias (autocomplete)', message=
        'What to send', summary='Ask the agent to reply with a 3-bullet status'
        )
    @app_commands.autocomplete(agent=_agent_autocomplete)
    async def agent_cmd(interaction: discord.Interaction, agent: str,
        message: str, summary: bool=True):
        await interaction.response.defer(ephemeral=True, thinking=True)
        alias_to_agent, by_agent = _load_alias_map()
        ag = alias_to_agent.get(agent.lower(), agent)
        try:
            status = await _send_to_agent(bot, ag, message, author_tag=
                f'Discord:{interaction.user.id}', request_summary=summary,
                message_type='general_to_agent')
            await interaction.followup.send(embed=_mk_ok_embed(
                '📨 General to Agent Message Dispatched',
                f"""{status}

**Message:** {message}

*Type: General to Agent*"""
                ), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=_mk_err_embed(
                'Dispatch failed', str(e)), ephemeral=True)

    @bot.tree.command(name='summary_core', description=
        'Request quick summaries from Agents 1-4.')
    async def summary_core(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        tasks = []
        for i in range(1, 5):
            tasks.append(_send_to_agent(bot, f'Agent-{i}',
                'Status check requested.', author_tag=
                f'Discord:{interaction.user.id}', request_summary=True))
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            lines = []
            for i, r in enumerate(results, start=1):
                if isinstance(r, Exception):
                    lines.append(f'Agent-{i}: ❌ {r}')
                else:
                    lines.append(f'{r}')
            await interaction.followup.send(embed=_mk_ok_embed(
                'Core summaries requested', '\n'.join(lines)), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=_mk_err_embed(
                'Summary request failed', str(e)), ephemeral=True)

    async def _dispatch_prefix(ctx: commands.Context, target_agent: str,
        msg: str):
        if not msg.strip():
            await ctx.reply(embed=_mk_err_embed('Missing message',
                'Usage: `!<alias> <message>`'))
            return
        try:
            status = await _send_to_agent(bot, target_agent, msg,
                author_tag=f'Discord:{ctx.author.id}', request_summary=True)
            await ctx.reply(embed=_mk_ok_embed('Message dispatched',
                f"""{status}

**Message:** {msg}"""))
        except Exception as e:
            await ctx.reply(embed=_mk_err_embed('Dispatch failed', str(e)))
    for agent_id, aliases in by_agent.items():
        for alias in aliases:

            @bot.command(name=alias)
            async def _alias_cmd(ctx: commands.Context, *, message: str,
                _agent=agent_id):
                await _dispatch_prefix(ctx, _agent, message)

    @bot.command(name='agent')
    async def generic_agent(ctx: commands.Context, who: str, *, message: str):
        ag = alias_to_agent.get(who.lower(), who)
        await _dispatch_prefix(ctx, ag, message)

    @bot.command(name='summary4')
    async def summary4(ctx: commands.Context):
        tasks = []
        for i in range(1, 5):
            tasks.append(_send_to_agent(bot, f'Agent-{i}',
                'Status check requested.', author_tag=
                f'Discord:{ctx.author.id}', request_summary=True))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        lines = []
        for i, r in enumerate(results, start=1):
            if isinstance(r, Exception):
                lines.append(f'Agent-{i}: ❌ {r}')
            else:
                lines.append(f'{r}')
        await ctx.reply(embed=_mk_ok_embed('Core summaries requested', '\n'
            .join(lines)))
    try:
        await bot.tree.sync()
    except Exception as e:
        logger.info(f'⚠️ Slash sync warning: {e}')
