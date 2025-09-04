# 🚀 Quick Start Guide - Discord GUI Interface

## ✅ What's Working
- All required packages are installed ✅
- Discord webhook URL is configured ✅
- Setup script is working ✅
- .env file is configured ✅

## ❌ What You Need to Do

### 1. Get a Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Give it a name (e.g., "Agent Swarm Bot")
4. Go to "Bot" section
5. Click "Add Bot"
6. Copy the bot token

### 2. Update .env File
Edit your `.env` file and replace `your_bot_token_here` with your actual bot token:
```
DISCORD_BOT_TOKEN=your_actual_bot_token_here
```

### 3. Run the Bot
```bash
python run_discord_bot.py
```

## 🎮 Using the GUI

Once the bot is running:
1. Go to your Discord server
2. Type `!gui` to launch the workflow control panel
3. Click buttons to trigger workflows:
   - 🚀 **Onboard Agent** - Start onboarding
   - 📋 **Wrapup** - Trigger wrapup
   - 📊 **Status Check** - Get system status
   - 🔄 **Refresh** - Refresh interface

## 💬 Send Messages to Agents

Type `!message_gui` to:
1. Select an agent from dropdown
2. Enter your message
3. Send via PyAutoGUI coordinates

## 🔧 Alternative Commands

```bash
!onboard                    # Trigger onboarding
!wrapup                     # Trigger wrapup
!message_captain <message>  # Send to Captain Agent-4
!status                     # Get system status
```

## 🛠️ Troubleshooting

**Bot not responding?**
- Check if token is correct
- Make sure bot is invited to your server
- Verify bot has proper permissions

**PyAutoGUI not working?**
- System will fallback to inbox delivery
- Check coordinate configuration

## 🎯 Ready to Go!

1. Set your bot token: `$env:DISCORD_BOT_TOKEN="your_token"`
2. Run the bot: `python run_discord_bot.py`
3. In Discord, type: `!gui`
4. Start clicking buttons! 🎮

**WE. ARE. SWARM. ⚡️🔥**
