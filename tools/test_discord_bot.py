#!/usr/bin/env python3
"""
Simple Discord bot test to verify basic functionality
"""

import asyncio
import discord
from discord.ext import commands

class TestBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f'✅ Test bot ready: {self.user}')
        
        # Send a test message to the first available channel
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == 'general' or 'general' in channel.name.lower():
                    try:
                        await channel.send("🤖 **Test Bot Online!**\n\nType `!test` to verify the bot is working.")
                        print(f"✅ Test message sent to {guild.name} in #{channel.name}")
                        return
                    except Exception as e:
                        print(f"❌ Failed to send test message: {e}")
                        continue

    @commands.command()
    async def test(self, ctx):
        """Simple test command."""
        embed = discord.Embed(
            title="✅ Bot Test Successful!",
            description="The Discord bot is working correctly.",
            color=discord.Color.green()
        )
        embed.add_field(name="Status", value="✅ Online and responsive", inline=True)
        embed.add_field(name="Commands", value="✅ Command system working", inline=True)
        await ctx.send(embed=embed)

async def main():
    # Load token from .env
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ No Discord bot token found in .env file")
        return
    
    bot = TestBot()
    try:
        await bot.start(token)
    except Exception as e:
        print(f"❌ Failed to start test bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
