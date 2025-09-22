#!/usr/bin/env python3
"""
Discord Social Media Commands
=============================

Extends the existing Discord bot with ChatMate social media integration commands.
Provides cross-platform analytics, sentiment analysis, and community management through Discord.

V2 Compliance: ≤400 lines, modular design, Discord integration
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from src.services.social_media_integration import get_social_media_service

logger = logging.getLogger(__name__)


class SocialMediaCommands(commands.Cog):
    """
    Discord commands for ChatMate social media integration.

    Commands:
    - /social_stats: Get cross-platform community statistics
    - /sentiment_analysis: Analyze sentiment of text
    - /community_dashboard: View unified community dashboard
    - /platform_status: Check platform connection status
    """

    def __init__(self, bot):
        """Initialize the social media commands cog."""
        self.bot = bot
        self.social_service = None
        self.logger = logging.getLogger(f"{__name__}.SocialMediaCommands")

    async def get_social_service(self):
        """Get or initialize the social media service."""
        if self.social_service is None:
            self.social_service = get_social_media_service()
            await self.social_service.initialize_integration()
        return self.social_service

    @app_commands.command(name="social_stats", description="Get cross-platform community statistics")
    async def social_stats(self, interaction: discord.Interaction):
        """Get cross-platform social media statistics."""
        await interaction.response.defer()

        try:
            service = await self.get_social_service()
            analytics = await service.get_cross_platform_analytics()

            if not analytics["platforms"]:
                await interaction.followup.send("❌ No social media platforms connected yet.")
                return

            # Create embed with analytics
            embed = discord.Embed(
                title="🌐 Cross-Platform Social Analytics",
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )

            # Summary section
            summary = analytics["summary"]
            embed.add_field(
                name="📊 Summary",
                value=f"**Active Platforms:** {summary['active_platforms']}\n"
                      f"**Total Engagement:** {summary['total_engagement']:,}\n"
                      f"**Avg Sentiment:** {summary['average_sentiment']:.2f}",
                inline=False
            )

            # Platform breakdown
            platform_text = ""
            for platform, data in analytics["platforms"].items():
                platform_text += f"**{platform.title()}:** {data.get('engagement', 0):,} engagement\n"

            embed.add_field(
                name="📱 Platforms",
                value=platform_text,
                inline=False
            )

            # Insights
            if analytics["insights"]:
                insights_text = ""
                for insight in analytics["insights"][:3]:  # Show top 3 insights
                    insights_text += f"• {insight['message']}\n"

                embed.add_field(
                    name="💡 Key Insights",
                    value=insights_text,
                    inline=False
                )

            embed.set_footer(text="ChatMate Social Integration | WE ARE SWARM")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            self.logger.error(f"❌ Failed to get social stats: {e}")
            await interaction.followup.send(f"❌ Error getting social statistics: {str(e)}")

    @app_commands.command(name="sentiment_analysis", description="Analyze sentiment of text")
    @app_commands.describe(text="Text to analyze for sentiment")
    async def sentiment_analysis(self, interaction: discord.Interaction, text: str):
        """Analyze sentiment of provided text."""
        await interaction.response.defer()

        try:
            service = await self.get_social_service()
            sentiment = await service.analyze_sentiment(text, "discord")

            # Create embed with sentiment analysis
            embed = discord.Embed(
                title="🧠 Sentiment Analysis",
                color=self._get_sentiment_color(sentiment["sentiment_score"]),
                timestamp=datetime.utcnow()
            )

            embed.add_field(
                name="📝 Text Sample",
                value=sentiment["text"],
                inline=False
            )

            embed.add_field(
                name="🎭 Sentiment",
                value=f"**Label:** {sentiment['sentiment_label'].title()}\n"
                      f"**Score:** {sentiment['sentiment_score']:.2f}\n"
                      f"**Confidence:** {sentiment['confidence']:.2f}",
                inline=True
            )

            # Detailed scores if available
            if "detailed_scores" in sentiment:
                detailed = sentiment["detailed_scores"]
                embed.add_field(
                    name="📊 Detailed Scores",
                    value=f"**Positive:** {detailed.get('pos', 0):.2f}\n"
                          f"**Negative:** {detailed.get('neg', 0):.2f}\n"
                          f"**Neutral:** {detailed.get('neu', 0):.2f}",
                    inline=True
                )

            embed.set_footer(text="ChatMate Sentiment Analysis | WE ARE SWARM")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            self.logger.error(f"❌ Failed to analyze sentiment: {e}")
            await interaction.followup.send(f"❌ Error analyzing sentiment: {str(e)}")

    def _get_sentiment_color(self, score: float) -> int:
        """Get Discord color based on sentiment score."""
        if score > 0.2:
            return 0x00ff00  # Green (positive)
        elif score < -0.2:
            return 0xff0000  # Red (negative)
        else:
            return 0xffff00  # Yellow (neutral)

    @app_commands.command(name="community_dashboard", description="View unified community dashboard")
    async def community_dashboard(self, interaction: discord.Interaction):
        """Get unified community dashboard data."""
        await interaction.response.defer()

        try:
            service = await self.get_social_service()
            dashboard_data = await service.get_community_dashboard_data()

            embed = discord.Embed(
                title="📊 Unified Community Dashboard",
                color=0x0099ff,
                timestamp=datetime.utcnow()
            )

            # Integration status
            status = dashboard_data["integration_status"]
            embed.add_field(
                name="🔗 Integration Status",
                value=f"**Active:** {'✅' if status['integration_active'] else '❌'}\n"
                      f"**Platforms:** {len(status['enabled_platforms'])}\n"
                      f"**Last Update:** {status['last_update'][:19]}",
                inline=False
            )

            # Platform status
            enabled = status["enabled_platforms"]
            if enabled:
                platforms_text = ", ".join(p.title() for p in enabled)
                embed.add_field(
                    name="📱 Connected Platforms",
                    value=platforms_text,
                    inline=False
                )

            # Insights
            if "cross_platform_insights" in dashboard_data:
                insights = dashboard_data["cross_platform_insights"]
                if insights:
                    insights_text = ""
                    for insight in insights[:2]:  # Show top 2 insights
                        insights_text += f"• {insight['message']}\n"

                    embed.add_field(
                        name="💡 Insights",
                        value=insights_text,
                        inline=False
                    )

            # Recommendations
            if "recommendations" in dashboard_data:
                recommendations = dashboard_data["recommendations"]
                if recommendations:
                    recs_text = ""
                    for rec in recommendations[:2]:  # Show top 2 recommendations
                        recs_text += f"• **{rec['priority'].title()}**: {rec['message']}\n"

                    embed.add_field(
                        name="🎯 Recommendations",
                        value=recs_text,
                        inline=False
                    )

            embed.set_footer(text="ChatMate Community Dashboard | WE ARE SWARM")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            self.logger.error(f"❌ Failed to get community dashboard: {e}")
            await interaction.followup.send(f"❌ Error getting community dashboard: {str(e)}")

    @app_commands.command(name="platform_status", description="Check platform connection status")
    async def platform_status(self, interaction: discord.Interaction):
        """Check the status of all social media platforms."""
        await interaction.response.defer()

        try:
            service = await self.get_social_service()

            embed = discord.Embed(
                title="🔌 Platform Connection Status",
                color=0x00ff00 if service.is_integrated else 0xff0000,
                timestamp=datetime.utcnow()
            )

            # Overall status
            embed.add_field(
                name="📊 Overall Status",
                value=f"**Integration:** {'✅ Active' if service.is_integrated else '❌ Inactive'}\n"
                      f"**Platforms:** {len(service.enabled_platforms)} enabled",
                inline=False
            )

            # Individual platform status
            if service.enabled_platforms:
                platforms_text = ""
                for platform in service.enabled_platforms:
                    platforms_text += f"✅ {platform.title()}\n"

                embed.add_field(
                    name="📱 Enabled Platforms",
                    value=platforms_text,
                    inline=False
                )
            else:
                embed.add_field(
                    name="⚠️ No Platforms",
                    value="No social media platforms are currently connected.\n"
                          "Use `/social_setup` to configure platforms.",
                    inline=False
                )

            # Setup instructions
            embed.add_field(
                name="🔧 Setup Help",
                value="To add platforms, configure the following environment variables:\n"
                      "• `TWITTER_API_KEY`, `TWITTER_API_SECRET`, etc.\n"
                      "• `FACEBOOK_APP_ID`, `FACEBOOK_ACCESS_TOKEN`\n"
                      "• `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`",
                inline=False
            )

            embed.set_footer(text="ChatMate Platform Status | WE ARE SWARM")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            self.logger.error(f"❌ Failed to get platform status: {e}")
            await interaction.followup.send(f"❌ Error checking platform status: {str(e)}")


async def setup(bot):
    """Setup function to add the social media commands cog to the bot."""
    await bot.add_cog(SocialMediaCommands(bot))
