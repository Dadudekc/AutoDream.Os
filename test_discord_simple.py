#!/usr/bin/env python3
"""
Simple Discord Bot Test
Just connects and responds to !ping
"""

import os
from pathlib import Path

import discord
from discord.ext import commands

# Load .env
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

# Get token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("❌ No DISCORD_BOT_TOKEN found!")
    exit(1)

# Create bot with ALL intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot connected: {bot.user}")
    print(f"   Guilds: {len(bot.guilds)}")
    for guild in bot.guilds:
        print(f"   - {guild.name}")


@bot.command()
async def ping(ctx):
    """Simple ping command"""
    await ctx.send("🏓 Pong! Bot is working!")
    print(f"✅ Responded to ping from {ctx.author}")


@bot.command()
async def test(ctx):
    """Test command"""
    await ctx.send("✅ Test successful! Commands are working!")
    print(f"✅ Responded to test from {ctx.author}")


print("🤖 Starting simple Discord bot...")
print("   Try these commands in Discord:")
print("   !ping")
print("   !test")
bot.run(TOKEN)
