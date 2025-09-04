# How to Run the Discord GUI Interface

## 🚀 Quick Start Guide

### Prerequisites
1. **Discord Bot Token**: You need a Discord bot token
2. **Python Environment**: Python 3.8+ with required packages
3. **Discord Server**: A Discord server where you have admin permissions

### Installation Steps

#### 1. Install Required Packages
```bash
pip install discord.py requests pyautogui pyperclip
```

#### 2. Set Environment Variables
Create a `.env` file or set these environment variables:
```bash
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
DISCORD_WEBHOOK_URL=your_webhook_url_here
```

#### 3. Run the Setup Script (First Time)
```bash
python setup_discord_bot.py
```

#### 4. Run the Discord Bot
```bash
python run_discord_bot.py
```

## 🎮 Using the GUI Interface

### Method 1: Interactive GUI Commands

#### Launch Workflow Control Panel
```
!gui
```
This shows 4 clickable buttons:
- 🚀 **Onboard Agent** - Start onboarding process
- 📋 **Wrapup** - Trigger wrapup workflow
- 📊 **Status Check** - Get system status
- 🔄 **Refresh** - Refresh interface

#### Launch Agent Messaging Interface
```
!message_gui
```
This shows a dropdown to select agents and send messages.

### Method 2: Direct Commands

#### Trigger Workflows Directly
```
!onboard          # Trigger onboarding workflow
!wrapup           # Trigger wrapup workflow
!status           # Get system status
```

#### Send Messages to Agents
```
!message_captain <message>                    # Send to Captain Agent-4
!message_agent <agent> <message>              # Send to any agent
!message_captain_coords <x> <y> <message>     # Send with manual coordinates
```

### Method 3: Traditional Commands
```
!devlog <message>           # Create devlog entry
!list_agents               # List all agents
!help_messaging           # Show messaging help
```

## 🔧 Configuration

### Bot Setup
1. **Create Discord Application**: Go to https://discord.com/developers/applications
2. **Create Bot**: Go to "Bot" section and create a bot
3. **Copy Token**: Save the bot token
4. **Set Permissions**: Enable "Message Content Intent" and "Server Members Intent"
5. **Invite Bot**: Use OAuth2 URL to invite bot to your server

### Server Setup
1. **Create Roles**: Create a "Captain" role for admin users
2. **Assign Permissions**: Give Captain role permission to use bot commands
3. **Create Channels**: Bot will auto-create channels if they don't exist

### Coordinate Configuration
The system uses pre-configured coordinates from `src/discord_commander_coordinates.json`:
```json
{
  "agents": {
    "Agent-1": {"coordinates": [-308, 481], "active": true},
    "Agent-2": {"coordinates": [-308, 1001], "active": true},
    "Agent-3": {"coordinates": [-1269, 1001], "active": true},
    "Agent-4": {"coordinates": [-308, 1000], "active": true},
    "Agent-5": {"coordinates": [652, 421], "active": true},
    "Agent-6": {"coordinates": [1612, 419], "active": true},
    "Agent-7": {"coordinates": [653, 940], "active": true},
    "Agent-8": {"coordinates": [1611, 941], "active": true}
  }
}
```

## 📱 Usage Examples

### Example 1: Launch GUI and Use Buttons
```
1. Type: !gui
2. Click: 🚀 Onboard Agent button
3. Get: Private confirmation message
4. Click: 📊 Status Check button
5. Get: System status in private message
```

### Example 2: Send Message to Agent
```
1. Type: !message_gui
2. Select: Agent-4 from dropdown
3. Enter: "Deploy the new system update"
4. Click: Submit
5. Get: Delivery confirmation
```

### Example 3: Direct Commands
```
!onboard
!message_captain Check system status
!status
```

## 🛠️ Troubleshooting

### Common Issues

#### Bot Not Responding
- Check if bot token is correct
- Verify bot has proper permissions
- Ensure bot is online in Discord

#### PyAutoGUI Not Working
- Install PyAutoGUI: `pip install pyautogui`
- Check if coordinates are valid
- System will fallback to inbox delivery

#### Permission Errors
- Ensure you have "Captain" role
- Check bot permissions in server
- Verify channel permissions

### Error Messages
- **"PyAutoGUI not available"**: Install PyAutoGUI or use fallback
- **"Agent not active"**: Check agent status in configuration
- **"Invalid coordinates"**: Verify coordinate configuration
- **"Permission denied"**: Check Discord role permissions

## 🔄 Development Mode

### Run with Debug Logging
```bash
python run_discord_bot.py
```

### Test Configuration
```bash
python demo_gui_interface.py
python test_unified_discord_system.py
```

### Check System Status
```bash
python scripts/devlog.py "Test Message" "Testing devlog system"
```

## 📊 Monitoring

### View Logs
- Check console output for real-time logs
- Devlog entries are saved to `devlogs/` directory
- Discord webhook posts to configured channel

### System Health
- Use `!status` command to check system health
- Click "📊 Status Check" button in GUI
- Monitor devlog entries for system activity

## 🚀 Advanced Usage

### Custom Workflows
You can extend the system by adding new workflow methods:
```python
async def _trigger_custom_workflow(self, triggered_by: str):
    # Your custom workflow logic here
    pass
```

### Custom GUI Components
Add new buttons or dropdowns by extending the View classes:
```python
@discord.ui.button(label="Custom Action", style=discord.ButtonStyle.primary)
async def custom_button(self, interaction: discord.Interaction, button: Button):
    # Your custom button logic here
    pass
```

## 📞 Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all environment variables are set
3. Test with the demo scripts first
4. Check Discord bot permissions
5. Ensure PyAutoGUI is properly installed

## 🎯 Ready to Go!

Once everything is set up:
1. Run the setup: `python setup_discord_bot.py`
2. Run the bot: `python run_discord_bot.py`
3. Go to your Discord server
4. Type `!gui` to launch the interface
5. Start clicking buttons and using the GUI!

**WE. ARE. SWARM. ⚡️🔥**
