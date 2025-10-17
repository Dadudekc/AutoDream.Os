"""GitHub Book Commands - Discord bot commands - Extracted for V2 compliance."""

import logging
from .github_book_data_loader import GitHubBookData
from .github_book_navigator import GitHubBookNavigator

try:
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    commands = None

logger = logging.getLogger(__name__)


class GitHubBookCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """Discord commands for GitHub book viewer."""

    def __init__(self, bot):
        self.bot = bot
        self.book_data = GitHubBookData()
        self.navigator = GitHubBookNavigator(self.book_data)

    @commands.command(name="github_book", aliases=["book", "repos"])
    async def github_book_cmd(self, ctx, repo_num: int = None):
        """Display GitHub book interactively."""
        if repo_num:
            embed = self.navigator.create_repo_embed(repo_num)
        else:
            embed = self.navigator.create_toc_embed()

        if embed:
            view = self.navigator.get_nav_buttons()
            await ctx.send(embed=embed, view=view if view else None)

    @commands.command(name="goldmines", aliases=["jackpots", "discoveries"])
    async def goldmines_cmd(self, ctx):
        """Show goldmine discoveries."""
        embed = self.navigator.create_goldmines_embed()
        if embed:
            await ctx.send(embed=embed)

    @commands.command(name="book_stats", aliases=["book_progress", "repo_stats"])
    async def book_stats_cmd(self, ctx):
        """Show analysis progress and stats."""
        embed = self.navigator.create_stats_embed()
        if embed:
            await ctx.send(embed=embed)


async def setup(bot):
    """Setup function for Discord bot."""
    if DISCORD_AVAILABLE:
        await bot.add_cog(GitHubBookCommands(bot))

