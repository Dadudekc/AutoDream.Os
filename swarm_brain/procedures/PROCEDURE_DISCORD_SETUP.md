# PROCEDURE: Discord Integration Setup

**Category**: Setup & Configuration  
**Author**: Agent-5 (extracted from scripts/setup_enhanced_discord.py)  
**Date**: 2025-10-14  
**Tags**: discord, setup, communication, integration

---

## 🎯 WHEN TO USE

**Trigger**: Setting up Discord integration for swarm communication OR upgrading Discord features

**Who**: Agent-3 (Infrastructure Specialist) or designated setup agent

---

## 📋 PREREQUISITES

- Discord server created
- Bot token obtained from Discord Developer Portal
- Webhook URLs ready (for channels)
- Python environment with discord.py installed
- Channel IDs identified

---

## 🔄 PROCEDURE STEPS

### **Step 1: Run Setup Script**

```bash
python scripts/setup_enhanced_discord.py
```

### **Step 2: Provide Configuration**

The script will prompt for:
1. **Discord Bot Token** - From Discord Developer Portal
2. **Webhook URLs** - For each channel (devlog, status, etc.)
3. **Channel IDs** - Individual agent channels
4. **Server ID** - Discord server ID

### **Step 3: Verify Configuration**

Script creates:
- `config/discord_channels.json` - Channel configuration
- `config/discord_config.json` - Bot configuration
- Coordination file for agent handoff

### **Step 4: Test Discord Integration**

```bash
# Test with sample message
python scripts/test_enhanced_discord.py
```

Should see:
- ✅ Message posted to Discord
- ✅ Bot responsive
- ✅ Channels accessible

---

## ✅ SUCCESS CRITERIA

- [ ] `config/discord_channels.json` created
- [ ] `config/discord_config.json` configured  
- [ ] Bot token validated
- [ ] Webhook URLs working
- [ ] Test message posts successfully
- [ ] All agent channels accessible

---

## 🔄 ROLLBACK

If setup fails:

```bash
# Remove configuration files
rm config/discord_channels.json
rm config/discord_config.json

# Re-run setup
python scripts/setup_enhanced_discord.py
```

---

## 📝 EXAMPLES

**Example 1: Successful Setup**

```bash
$ python scripts/setup_enhanced_discord.py
🎯 Enhanced Discord Integration Setup
============================================================
Setting up individual agent channels for V2_SWARM

✅ Prerequisites check passed
✅ Configuration created
✅ Channels configured:
   - #devlog
   - #agent-status
   - #agent-1
   - #agent-2
   ...

✅ Setup complete!
Test with: python scripts/test_enhanced_discord.py
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_DISCORD_BOT_DEPLOYMENT (deploying bot)
- PROCEDURE_DISCORD_CHANNEL_MANAGEMENT (managing channels)
- PROCEDURE_MESSAGING_SYSTEM_SETUP (related messaging)

---

## ⚠️ COMMON ISSUES

**Issue 1: Invalid Bot Token**
```
Error: 401 Unauthorized
```
**Solution**: Check bot token in Discord Developer Portal, regenerate if needed

**Issue 2: Webhook URL Not Working**
```
Error: 404 Not Found
```
**Solution**: Verify webhook URL is correct, recreate webhook in Discord if needed

**Issue 3: Missing Permissions**
```
Error: 403 Forbidden
```
**Solution**: Check bot permissions in Discord server settings

---

**Agent-5 - Procedure Documentation** 📚

