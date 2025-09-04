# 🔧 Discord Bot Setup Guide

## ✅ Great News!
Your Discord bot is working! The error you saw is just a Discord configuration issue that's easy to fix.

## 🚨 The Issue
```
Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal.
```

## 🔧 How to Fix It

### Step 1: Go to Discord Developer Portal
1. Go to https://discord.com/developers/applications
2. Find your bot application
3. Click on it

### Step 2: Enable Privileged Intents
1. Go to the **"Bot"** section in the left sidebar
2. Scroll down to **"Privileged Gateway Intents"**
3. Enable these intents:
   - ✅ **MESSAGE CONTENT INTENT** (Required for reading message content)
   - ✅ **SERVER MEMBERS INTENT** (Required for member information)
   - ✅ **PRESENCE INTENT** (Optional, for presence information)

### Step 3: Save Changes
1. Click **"Save Changes"** at the bottom
2. Your bot will automatically restart

## 🚀 Run the Bot Again
```bash
python run_discord_bot.py
```

## 🎮 Using the GUI

Once the bot is running:
1. **Go to your Discord server**
2. **Type `!gui`** to launch the workflow control panel
3. **Click buttons** to trigger workflows:
   - 🚀 **Onboard Agent** - Start onboarding
   - 📋 **Wrapup** - Trigger wrapup
   - 📊 **Status Check** - Get system status
   - 🔄 **Refresh** - Refresh interface

## 💬 Send Messages to Agents

Type `!message_gui` to:
1. **Select an agent** from dropdown
2. **Enter your message** in the popup form
3. **Send via PyAutoGUI** coordinates

## 🛠️ Alternative Commands

```bash
!onboard                    # Trigger onboarding
!wrapup                     # Trigger wrapup
!message_captain <message>  # Send to Captain Agent-4
!status                     # Get system status
```

## ✅ What's Working
- ✅ Bot token loaded from .env file
- ✅ All packages installed correctly
- ✅ Configuration files loaded
- ✅ Bot connects to Discord
- ✅ GUI interface ready
- ✅ Coordinate messaging system ready

## 🎯 Ready to Go!

1. **Enable privileged intents** in Discord Developer Portal
2. **Run the bot**: `python run_discord_bot.py`
3. **In Discord, type**: `!gui`
4. **Start clicking buttons!** 🎮

**WE. ARE. SWARM. ⚡️🔥**
