import logging
logger = logging.getLogger(__name__)
"""
Agent Summary Handlers - Discord Commands for Agent Status
==========================================================

Discord command handlers for requesting agent summaries via PyAutoGUI.

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""
from __future__ import annotations
import discord
from discord.ext import commands


class AgentSummary(commands.Cog):
    """Discord cog for agent summary commands"""

    def __init__(self, bot: commands.Bot, gateway):
        """Initialize agent summary handler"""
        self.bot = bot
        self.gateway = gateway

    async def _send_and_ack(self, ctx: commands.Context, agent_key: str,
        context: (str | None)=None):
        """Send summary request and acknowledge via Discord"""
        try:
            result = self.gateway.request_agent_summary(agent_key,
                requested_by=str(ctx.author), context=context)
            embed = discord.Embed(title=f'📊 Summary Request → {agent_key}',
                description=
                'Delivered via **PyAutoGUI** using Unified Messaging.',
                color=65416, timestamp=discord.utils.utcnow())
            embed.add_field(name='🎯 Requested By', value=
                f'{ctx.author.mention}', inline=True)
            embed.add_field(name='📝 Context', value=context or
                'General status update', inline=True)
            embed.add_field(name='⚡ Status', value=
                '✅ Request sent successfully', inline=True)
            embed.set_footer(text=
                f'V2_SWARM - Agent coordination via {agent_key}')
            await ctx.reply(embed=embed, mention_author=False)
            logger.info(f'✅ Summary request sent to {agent_key} via PyAutoGUI')
        except Exception as e:
            error_embed = discord.Embed(title=
                f'❌ Summary Request Failed → {agent_key}', description=
                f'Error: `{str(e)}`', color=16729156, timestamp=discord.
                utils.utcnow())
            await ctx.reply(embed=error_embed, mention_author=False)
            logger.info(f'❌ Failed to send summary request to {agent_key}: {e}'
                )

    @commands.command(name='summary1', help=
        'Request status summary from Agent-1')
    async def summary1(self, ctx: commands.Context, *, context: str=''):
        """Request summary from Agent-1"""
        await self._send_and_ack(ctx, 'Agent-1', context or None)

    @commands.command(name='summary2', help=
        'Request status summary from Agent-2')
    async def summary2(self, ctx: commands.Context, *, context: str=''):
        """Request summary from Agent-2"""
        await self._send_and_ack(ctx, 'Agent-2', context or None)

    @commands.command(name='summary3', help=
        'Request status summary from Agent-3')
    async def summary3(self, ctx: commands.Context, *, context: str=''):
        """Request summary from Agent-3"""
        await self._send_and_ack(ctx, 'Agent-3', context or None)

    @commands.command(name='summary_agent4', help=
        'Request status summary from Agent-4')
    async def summary_agent4(self, ctx: commands.Context, *, context: str=''):
        """Request summary from Agent-4"""
        await self._send_and_ack(ctx, 'Agent-4', context or None)

    @commands.command(name='summary', help=
        'Request summary from specific agent (!summary <agent_number> [context])'
        )
    async def summary_general(self, ctx: commands.Context, agent_number:
        int, *, context: str=''):
        """General summary command for any agent number"""
        if 1 <= agent_number <= 4:
            agent_key = f'Agent-{agent_number}'
            await self._send_and_ack(ctx, agent_key, context or None)
        else:
            await ctx.reply('❌ Invalid agent number. Use 1-4.',
                mention_author=False)

    @commands.command(name='agentsummary', help=
        'List available summary commands')
    async def list_commands(self, ctx: commands.Context):
        """List all available summary commands"""
        embed = discord.Embed(title='📊 Agent Summary Commands', description
            ='Request status summaries from agents via PyAutoGUI', color=
            39423, timestamp=discord.utils.utcnow())
        embed.add_field(name='🎯 Individual Commands', value=
            """`!summary1 [context]` - Agent-1 summary
`!summary2 [context]` - Agent-2 summary
`!summary3 [context]` - Agent-3 summary
`!summary_agent4 [context]` - Agent-4 summary"""
            , inline=False)
        embed.add_field(name='⚡ General Command', value=
            '`!summary <number> [context]` - Request from any agent (1-4)',
            inline=False)
        embed.add_field(name='📝 Context Parameter', value=
            'Optional context for the summary request (e.g., `working on discord integration`)'
            , inline=False)
        embed.set_footer(text='V2_SWARM - Discord to PyAutoGUI coordination')
        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot, gateway):
    """Setup function for Discord cog"""
    await bot.add_cog(AgentSummary(bot, gateway))
    logger.info('✅ Agent Summary commands registered with Discord bot')
