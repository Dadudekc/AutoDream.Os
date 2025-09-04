# 🤖 Discord Bot Invite & Setup Guide

## ✅ **Step 1: Get Your Bot Token**

### **If you already have a bot:**
1. Go to https://discord.com/developers/applications
2. Find your bot application
3. Go to **"Bot"** section
4. Copy the **"Token"** (this should already be in your `.env` file)

### **If you need to create a new bot:**
1. Go to https://discord.com/developers/applications
2. Click **"New Application"**
3. Give it a name (e.g., "Swarm Commander")
4. Go to **"Bot"** section
5. Click **"Add Bot"**
6. Copy the **"Token"**
7. Add to your `.env` file: `DISCORD_BOT_TOKEN=your_token_here`

---

## 🔗 **Step 2: Generate Invite Link**

### **Method 1: Use Discord Developer Portal (Recommended)**
1. Go to your bot application in https://discord.com/developers/applications
2. Go to **"OAuth2"** → **"URL Generator"**
3. Select **"bot"** in Scopes
4. Select these **Bot Permissions**:
   - ✅ **Send Messages**
   - ✅ **Use Slash Commands**
   - ✅ **Embed Links**
   - ✅ **Attach Files**
   - ✅ **Read Message History**
   - ✅ **Add Reactions**
   - ✅ **Use External Emojis**
   - ✅ **Manage Messages** (optional, for cleanup)
5. Copy the generated URL
6. Open the URL in your browser
7. Select your server and click **"Authorize"**

### **Method 2: Manual Invite Link**
Replace `YOUR_BOT_CLIENT_ID` with your bot's Client ID:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=2147483648&scope=bot
```

**To find your Client ID:**
1. Go to your bot application
2. Go to **"General Information"**
3. Copy the **"Application ID"** (this is your Client ID)

---

## ⚙️ **Step 3: Enable Required Intents**

### **In Discord Developer Portal:**
1. Go to your bot application
2. Go to **"Bot"** section
3. Scroll down to **"Privileged Gateway Intents"**
4. Enable these intents:
   - ✅ **MESSAGE CONTENT INTENT** (Required for reading message content)
   - ✅ **SERVER MEMBERS INTENT** (Required for member information)
   - ✅ **PRESENCE INTENT** (Optional, for presence information)
5. Click **"Save Changes"**

---

## 🔧 **Step 4: Set Up Environment Variables**

### **Add to your `.env` file:**
```bash
# Required
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=1412461118970138714

# Optional
DISCORD_GUILD_ID=your_server_id_here
DISCORD_WEBHOOK_URL=your_webhook_url_here
```

### **To find your Server ID:**
1. Enable **Developer Mode** in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on your server name
3. Click **"Copy Server ID"**

---

## 🎯 **Step 5: Create Required Roles**

### **Create the "Captain" role:**
1. Go to your Discord server
2. Go to **Server Settings** → **Roles**
3. Click **"Create Role"**
4. Name it **"Captain"**
5. Give it appropriate permissions
6. Assign it to users who should use the bot

---

## 🚀 **Step 6: Test the Bot**

### **Run the bot:**
```bash
python run_discord_bot.py
```

### **Test commands in the designated channel:**
```bash
!status                    # Check bot status
!list_agents              # List available agents
!gui                      # Launch GUI interface
```

---

## ❌ **Common Issues & Solutions**

### **"Bot is not responding"**
- ✅ Check if bot is online (green dot next to name)
- ✅ Verify bot token is correct
- ✅ Check console for error messages
- ✅ Ensure bot has proper permissions

### **"Missing Permissions"**
- ✅ Re-invite bot with correct permissions
- ✅ Check bot role position in server hierarchy
- ✅ Verify bot can see the command channel

### **"Commands not working"**
- ✅ Check if you're in the correct channel (ID: 1412461118970138714)
- ✅ Verify you have the "Captain" role
- ✅ Check if intents are enabled in Developer Portal

### **"Channel not found"**
- ✅ Verify `DISCORD_CHANNEL_ID` is correct
- ✅ Check if bot can see the channel
- ✅ Ensure channel ID is a number (no quotes)

---

## 📋 **Quick Checklist**

- [ ] Bot created in Discord Developer Portal
- [ ] Bot token added to `.env` file
- [ ] Bot invited to server with proper permissions
- [ ] Required intents enabled
- [ ] `DISCORD_CHANNEL_ID` set in `.env` file
- [ ] "Captain" role created and assigned
- [ ] Bot is online and responding
- [ ] Commands work in designated channel

---

## 🎮 **Ready to Use!**

Once everything is set up:

1. **Run the bot**: `python run_discord_bot.py`
2. **Go to your designated channel** (ID: 1412461118970138714)
3. **Type**: `!gui` to launch the interface
4. **Start using commands!**

**WE. ARE. SWARM. ⚡️🔥**
