# 🔧 Discord Bot Restart & Shutdown Commands - Technical Specification

**Lead:** Agent-2 (Architecture & Design Specialist)  
**Implementer:** Agent-6 (Co-Captain - Execution)  
**Priority:** 🚨 CRITICAL (General's specific request)  
**Effort:** 3-5 hours  
**Date:** 2025-10-15

---

## 🎯 REQUIREMENTS (General's Directive)

**"we need to add a restart and shutdown command to the discord bot"**

**Use Cases:**
1. **Graceful Shutdown:** Stop bot without killing process
2. **Graceful Restart:** Restart bot to load new code/config
3. **Emergency Stop:** Quick shutdown if needed
4. **Maintenance Mode:** Restart for updates

---

## 🏗️ ARCHITECTURE DESIGN

### **Command 1: !shutdown**

**Purpose:** Gracefully stop the Discord bot

**Behavior:**
1. Announce shutdown to Discord
2. Complete any pending operations
3. Save state (if any)
4. Close connections
5. Exit process

**Implementation:**
```python
# src/discord_commander/unified_discord_bot.py (enhanced)

@bot.command(name='shutdown')
@commands.has_permissions(administrator=True)
async def shutdown_command(ctx):
    """Gracefully shutdown the Discord bot"""
    
    # Confirm with user
    embed = discord.Embed(
        title="🛑 Shutdown Requested",
        description="Are you sure you want to shutdown the bot?",
        color=discord.Color.red()
    )
    
    # Confirmation buttons
    view = ConfirmShutdownView()
    message = await ctx.send(embed=embed, view=view)
    
    # Wait for confirmation
    await view.wait()
    
    if view.confirmed:
        # Announce shutdown
        embed = discord.Embed(
            title="👋 Bot Shutting Down",
            description="Gracefully closing connections...",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        
        # Graceful shutdown
        logger.info("🛑 Shutdown command received - closing bot")
        
        # Close bot
        await bot.close()
    else:
        await message.edit(content="❌ Shutdown cancelled", embed=None, view=None)


class ConfirmShutdownView(discord.ui.View):
    """Confirmation view for shutdown"""
    
    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False
    
    @discord.ui.button(label="✅ Confirm Shutdown", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.confirmed = True
        await interaction.response.send_message("✅ Shutdown confirmed", ephemeral=True)
        self.stop()
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()
```

---

### **Command 2: !restart**

**Purpose:** Restart the bot (shutdown + restart script)

**Behavior:**
1. Announce restart to Discord
2. Graceful shutdown
3. Trigger restart script
4. Bot comes back online

**Implementation:**
```python
@bot.command(name='restart')
@commands.has_permissions(administrator=True)
async def restart_command(ctx):
    """Restart the Discord bot"""
    
    # Confirm
    embed = discord.Embed(
        title="🔄 Restart Requested",
        description="Bot will shutdown and restart. Continue?",
        color=discord.Color.blue()
    )
    
    view = ConfirmRestartView()
    message = await ctx.send(embed=embed, view=view)
    
    await view.wait()
    
    if view.confirmed:
        # Announce restart
        embed = discord.Embed(
            title="🔄 Bot Restarting",
            description="Shutting down... Will be back in 5-10 seconds!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        logger.info("🔄 Restart command received - restarting bot")
        
        # Create restart flag file
        with open('.discord_bot_restart', 'w') as f:
            f.write('RESTART_REQUESTED')
        
        # Shutdown
        await bot.close()
        
        # Note: Restart logic handled by run script


class ConfirmRestartView(discord.ui.View):
    """Confirmation view for restart"""
    
    def __init__(self):
        super().__init__(timeout=30)
        self.confirmed = False
    
    @discord.ui.button(label="🔄 Confirm Restart", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.confirmed = True
        await interaction.response.send_message("✅ Restart confirmed", ephemeral=True)
        self.stop()
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.confirmed = False
        await interaction.response.send_message("❌ Cancelled", ephemeral=True)
        self.stop()
```

---

### **Restart Script Enhancement:**

**File:** `run_unified_discord_bot.py` (enhanced)

```python
#!/usr/bin/env python3
"""
Run Discord bot with auto-restart support
"""
import os
import sys
import time

def main():
    while True:
        # Run bot
        exit_code = run_bot()
        
        # Check for restart flag
        if os.path.exists('.discord_bot_restart'):
            os.remove('.discord_bot_restart')
            print("🔄 Restart requested - restarting in 3 seconds...")
            time.sleep(3)
            continue  # Restart loop
        
        # Normal exit
        print("👋 Bot shutdown complete")
        break

def run_bot():
    """Run the Discord bot"""
    try:
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
        
        # Load config
        token = os.getenv('DISCORD_TOKEN')
        channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
        
        # Create and run bot
        bot = UnifiedDiscordBot(token=token, channel_id=channel_id)
        bot.run(token)
        
        return 0
    except KeyboardInterrupt:
        print("\n⚠️ Bot interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Bot error: {e}")
        return 1

if __name__ == "__main__":
    main()
```

---

## 🎯 IMPLEMENTATION STEPS

### **Step 1: Add Commands to Bot (2 hours)**

**Files to Modify:**
- `src/discord_commander/unified_discord_bot.py`

**Changes:**
1. Add `@bot.command(name='shutdown')` handler
2. Add `@bot.command(name='restart')` handler
3. Create confirmation views
4. Add admin permission checks

---

### **Step 2: Enhance Run Script (1 hour)**

**Files to Modify:**
- `run_unified_discord_bot.py` (or equivalent)

**Changes:**
1. Add restart loop
2. Check for `.discord_bot_restart` flag file
3. Auto-restart if flag present
4. Clean exit if no flag

---

### **Step 3: Testing (1-2 hours)**

**Test Cases:**
1. ✅ !shutdown with confirmation → Bot stops
2. ✅ !shutdown with cancel → Bot continues
3. ✅ !restart with confirmation → Bot restarts
4. ✅ !restart with cancel → Bot continues
5. ✅ Only admins can use commands
6. ✅ Non-admins get permission error

---

## 🚨 SAFETY CONSIDERATIONS

### **Permission Control:**
```python
@commands.has_permissions(administrator=True)
```
**Why:** Only admins should shutdown/restart bot

### **Graceful Shutdown:**
```python
await bot.close()  # Not sys.exit()
```
**Why:** Clean disconnect, no zombie processes

### **Confirmation Required:**
- User must click "Confirm" button
- 30-second timeout if no response
- Prevents accidental shutdowns

### **State Preservation:**
- Save any critical state before shutdown
- Ensure no data loss
- Clean reconnection on restart

---

## 📊 SUCCESS METRICS

**Functional:**
- [ ] !shutdown stops bot cleanly
- [ ] !restart restarts bot successfully
- [ ] Confirmations work correctly
- [ ] Only admins can execute
- [ ] No errors in logs

**User Experience:**
- [ ] Commands are intuitive
- [ ] Confirmations are clear
- [ ] Feedback messages helpful
- [ ] Restart time <10 seconds

---

## 🚀 QUICK START (For Implementation)

**Agent-6, to implement:**

1. Read this spec (5 min)
2. Add shutdown command to `unified_discord_bot.py` (30 min)
3. Add restart command (30 min)
4. Create confirmation views (20 min)
5. Enhance run script (15 min)
6. Test all commands (30 min)
7. Document usage (15 min)

**Total:** 2.5-3 hours

**Expected Result:** !shutdown and !restart commands working with confirmations

---

**Agent-2 (LEAD)**  
*Ready for Agent-6 to implement per this spec!*

**WE. ARE. SWARM.** 🐝⚡

