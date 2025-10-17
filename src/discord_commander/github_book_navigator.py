"""GitHub Book Navigator - Interactive UI - Extracted for V2 compliance."""

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None


class GitHubBookNavigator:
    """Interactive navigation for GitHub book."""

    def __init__(self, book_data):
        self.book_data = book_data
        self.current_page = 1

    def create_toc_embed(self) -> any:
        """Create table of contents embed."""
        if not DISCORD_AVAILABLE:
            return None
        embed = discord.Embed(
            title="📚 GitHub 75 Repos - Comprehensive Analysis Book",
            description=f"Analyzed: {self.book_data.get_analyzed_count()}/75 repos",
            color=discord.Color.purple(),
        )
        embed.add_field(
            name="📖 Navigation",
            value="Use buttons to browse repos, or !github_book [num] to jump!",
            inline=False,
        )
        return embed

    def create_repo_embed(self, repo_num: int) -> any:
        """Create repo chapter embed."""
        if not DISCORD_AVAILABLE:
            return None
        repo = self.book_data.get_repo(repo_num)
        if not repo:
            return None
        color = discord.Color.gold() if repo.get("goldmine") else discord.Color.blue()
        embed = discord.Embed(
            title=f"📖 Repo #{repo_num}: {repo.get('name', 'Unknown')}",
            description=repo.get("purpose", "No description"),
            color=color,
        )
        if repo.get("agent"):
            embed.add_field(name="Analyst", value=repo["agent"], inline=True)
        if repo.get("roi"):
            embed.add_field(name="ROI", value=repo["roi"], inline=True)
        if repo.get("quality_rating"):
            embed.add_field(name="Quality", value=repo["quality_rating"], inline=True)
        return embed

    def create_goldmines_embed(self) -> any:
        """Create goldmines showcase embed."""
        if not DISCORD_AVAILABLE:
            return None
        goldmines = self.book_data.get_goldmines()
        embed = discord.Embed(
            title="💎 GOLDMINE DISCOVERIES",
            description=f"Found {len(goldmines)} high-value repositories!",
            color=discord.Color.gold(),
        )
        for gm in goldmines[:10]:
            embed.add_field(
                name=f"#{gm['num']}: {gm.get('name', 'Unknown')}",
                value=f"ROI: {gm.get('roi', 'Unknown')} | {gm.get('recommendations', 'Unknown')}",
                inline=False,
            )
        return embed

    def create_stats_embed(self) -> any:
        """Create statistics embed."""
        if not DISCORD_AVAILABLE:
            return None
        analyzed = self.book_data.get_analyzed_count()
        goldmines = len(self.book_data.get_goldmines())
        embed = discord.Embed(
            title="📊 GitHub Book Statistics",
            description=f"Analysis Progress: {analyzed}/75 repos",
            color=discord.Color.green(),
        )
        embed.add_field(name="Analyzed", value=f"{analyzed}/75", inline=True)
        embed.add_field(name="Goldmines", value=str(goldmines), inline=True)
        embed.add_field(
            name="Completion",
            value=f"{int(analyzed / 75 * 100)}%",
            inline=True,
        )
        return embed

    def get_nav_buttons(self) -> any:
        """Get navigation button view."""
        if not DISCORD_AVAILABLE:
            return None

        class NavView(discord.ui.View):
            def __init__(self, navigator):
                super().__init__(timeout=300)
                self.navigator = navigator

            @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.primary)
            async def prev_button(self, interaction, button):
                await interaction.response.defer()

            @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.primary)
            async def next_button(self, interaction, button):
                await interaction.response.defer()

            @discord.ui.button(label="💎 Goldmines", style=discord.ButtonStyle.success)
            async def goldmines_button(self, interaction, button):
                await interaction.response.defer()

            @discord.ui.button(label="📑 Contents", style=discord.ButtonStyle.secondary)
            async def toc_button(self, interaction, button):
                await interaction.response.defer()

        return NavView(self)

