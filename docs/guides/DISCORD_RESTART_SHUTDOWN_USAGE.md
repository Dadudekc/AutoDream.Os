# 📖 Discord Bot Restart & Shutdown Commands - Usage Guide

**Implementation:** Agent-6 (Co-Captain)  
**Spec:** Agent-2 (Architecture LEAD)  
**Request:** General  
**Date:** 2025-10-15  

---

## 🎯 OVERVIEW

The Discord bot now supports graceful restart and shutdown commands, allowing admins to control the bot remotely without accessing the server.

**Key Features:**
- ✅ Graceful shutdown (clean exit)
- ✅ Automatic restart (bot comes back online)
- ✅ Confirmation required (prevents accidents)
- ✅ Admin-only access (security)
- ✅ 30-second timeout (safety)

---

## 🚀 STARTING THE BOT

**With Auto-Restart Support:**
```bash
python run_unified_discord_bot_with_restart.py
```

**This enables:**
- Auto-restart when !restart is used
- Clean shutdown when !shutdown is used
- Automatic recovery from crashes (optional)

---

## 🛑 SHUTDOWN COMMAND

### **Usage:**
```
!shutdown
```

### **What Happens:**
1. Bot shows confirmation embed:
   ```
   🛑 Shutdown Requested
   Are you sure you want to shutdown the bot?
   
   [✅ Confirm Shutdown] [❌ Cancel]
   ```

2. Click "✅ Confirm Shutdown" to proceed
   - Bot announces shutdown
   - Bot gracefully closes connections
   - Runner script exits

3. Click "❌ Cancel" to abort
   - Bot stays online
   - No changes made

### **Requirements:**
- Must have **Administrator** permission in Discord
- Must confirm within 30 seconds

### **Use Cases:**
- Maintenance complete, shutting down for the day
- Emergency stop needed
- Bot misbehaving, need to stop

---

## 🔄 RESTART COMMAND

### **Usage:**
```
!restart
```

### **What Happens:**
1. Bot shows confirmation embed:
   ```
   🔄 Restart Requested
   Bot will shutdown and restart. Continue?
   
   [🔄 Confirm Restart] [❌ Cancel]
   ```

2. Click "🔄 Confirm Restart" to proceed
   - Bot announces restart
   - Bot gracefully closes
   - Creates restart flag file
   - Runner detects flag
   - Waits 3 seconds
   - Bot automatically restarts
   - Bot comes back online (5-10 seconds total)

3. Click "❌ Cancel" to abort
   - Bot stays online
   - No restart occurs

### **Requirements:**
- Must have **Administrator** permission in Discord
- Must confirm within 30 seconds

### **Use Cases:**
- Code updated, need to reload
- Configuration changed
- Bot acting strange, need fresh start
- Apply new Discord permissions

---

## 🔐 SECURITY

### **Admin-Only Access:**
Only users with **Administrator** permission can use these commands.

**Non-Admin Users:**
```
!shutdown
❌ Error: You do not have permission to use this command.
```

### **Confirmation Required:**
Both commands require explicit confirmation via button click.

**Safety Features:**
- 30-second timeout (auto-cancel if no response)
- Clear confirmation UI
- Separate confirm/cancel buttons
- Prevents accidental execution

---

## ⏱️ TIMEOUT BEHAVIOR

**If you don't respond within 30 seconds:**
- Buttons become inactive
- No action taken
- Bot stays running
- Confirmation expires

**Example:**
```
!shutdown
[Wait 30 seconds without clicking]
Buttons gray out → No shutdown occurs
```

---

## 📊 RESTART TIMING

**Expected Restart Time:**
- Shutdown announcement: <1 second
- Graceful close: <2 seconds
- Runner delay: 3 seconds
- Bot startup: 2-5 seconds

**Total:** ~5-10 seconds from !restart to bot online

---

## 🐛 TROUBLESHOOTING

### **Problem: !restart doesn't bring bot back**

**Possible Causes:**
1. Not using `run_unified_discord_bot_with_restart.py`
   - **Solution:** Use the restart-enabled runner script

2. Flag file not created
   - **Solution:** Check file permissions in project directory

3. Bot crashes on startup
   - **Solution:** Check logs for errors, fix issues

### **Problem: !shutdown doesn't work**

**Possible Causes:**
1. Not an admin user
   - **Solution:** Get Administrator permission in Discord

2. Confirmation timeout
   - **Solution:** Click confirm button within 30 seconds

3. Bot not responding
   - **Solution:** Check bot status, restart manually if needed

### **Problem: Commands not showing up**

**Possible Causes:**
1. Bot not fully started
   - **Solution:** Wait for "Bot ready" message in logs

2. Bot doesn't have permissions in channel
   - **Solution:** Give bot Send Messages permission

3. Wrong command prefix
   - **Solution:** Commands use `!` prefix: `!shutdown`, `!restart`

---

## 📝 EXAMPLES

### **Example 1: Graceful Shutdown**
```
Admin: !shutdown
Bot: 🛑 Shutdown Requested
     Are you sure you want to shutdown the bot?
     [✅ Confirm Shutdown] [❌ Cancel]

Admin: [Clicks ✅ Confirm Shutdown]
Bot: 👋 Bot Shutting Down
     Gracefully closing connections...
     
[Bot goes offline]
```

### **Example 2: Restart for Updates**
```
Admin: !restart
Bot: 🔄 Restart Requested
     Bot will shutdown and restart. Continue?
     [🔄 Confirm Restart] [❌ Cancel]

Admin: [Clicks 🔄 Confirm Restart]
Bot: 🔄 Bot Restarting
     Shutting down... Will be back in 5-10 seconds!

[Bot goes offline]
[3 seconds pass]
[Bot comes back online]

Bot: 🚀 Discord Commander - ONLINE
     Complete Agent Messaging System Access
```

### **Example 3: Cancelled Shutdown**
```
Admin: !shutdown
Bot: 🛑 Shutdown Requested
     Are you sure you want to shutdown the bot?
     [✅ Confirm Shutdown] [❌ Cancel]

Admin: [Clicks ❌ Cancel]
Bot: ❌ Shutdown cancelled

[Bot stays online]
```

---

## ✅ HELP COMMAND

**The !help command now includes restart/shutdown:**
```
!help
```

**Shows:**
```
📋 Main Commands
• !gui - Open interactive messaging GUI
• !status - View swarm status dashboard
• !message <agent> <msg> - Send direct message
• !broadcast <msg> - Broadcast to all agents
• !shutdown - Gracefully shutdown bot (admin only)
• !restart - Restart bot (admin only)
```

---

## 🎯 BEST PRACTICES

**When to Use !shutdown:**
- End of work day
- Maintenance complete
- Bot no longer needed
- Emergency stop

**When to Use !restart:**
- Code updated
- Configuration changed
- Bot acting strange
- Apply new features

**When NOT to Use:**
- During active operations (check with team first!)
- Without understanding impact
- Just to "test" (coordinate with team)

**Coordination:**
- Announce restarts to team
- Check for active operations first
- Use during low-activity periods
- Coordinate with Captain/General

---

## 🚀 QUICK REFERENCE

**Shutdown:**
```bash
!shutdown → Confirm → Bot stops → Runner exits
```

**Restart:**
```bash
!restart → Confirm → Bot stops → 3sec wait → Bot starts → Online
```

**Cancel:**
```bash
Click [❌ Cancel] → Bot stays running
```

**Timeout:**
```bash
Wait 30sec → Auto-cancel → Bot stays running
```

---

## 📚 RELATED DOCUMENTATION

- **Spec:** `docs/specs/DISCORD_RESTART_SHUTDOWN_COMMANDS_SPEC.md`
- **Testing:** `docs/testing/DISCORD_RESTART_SHUTDOWN_TESTS.md`
- **Implementation:** `src/discord_commander/unified_discord_bot.py`
- **Runner:** `run_unified_discord_bot_with_restart.py`

---

**WE. ARE. SWARM.** 🐝⚡

**General's request delivered with excellence!**

---

**#DISCORD_COMMANDS #USAGE_GUIDE #GENERAL_REQUEST #INFRASTRUCTURE**

