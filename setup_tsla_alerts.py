#!/usr/bin/env python3
"""
TSLA Alert System Setup Script
Quick setup and configuration for the TSLA pre-market alert system
"""

import json
import os
import sys
from pathlib import Path

def create_config_file():
    """Create configuration file with user inputs"""
    print("🔧 TSLA Alert System Setup")
    print("=" * 40)
    
    config = {}
    
    # Discord webhook configuration
    print("\n📱 Discord Configuration:")
    discord_webhook = input("Enter Discord webhook URL (or press Enter to skip): ").strip()
    if discord_webhook:
        config['discord_webhook_url'] = discord_webhook
    else:
        config['discord_webhook_url'] = "YOUR_DISCORD_WEBHOOK_URL_HERE"
    
    # Portfolio configuration
    print("\n💰 Portfolio Configuration:")
    try:
        portfolio_value = float(input("Enter portfolio value (default: 10000): ") or "10000")
        config['portfolio_value'] = portfolio_value
    except ValueError:
        config['portfolio_value'] = 10000.0
        print("  Using default portfolio value: $10,000")
    
    # Risk management configuration
    print("\n🛡️ Risk Management Configuration:")
    try:
        max_daily_loss = float(input("Enter max daily loss % (default: 5.0): ") or "5.0")
        config['max_daily_loss_pct'] = max_daily_loss
    except ValueError:
        config['max_daily_loss_pct'] = 5.0
    
    try:
        max_position_risk = float(input("Enter max position risk % (default: 1.0): ") or "1.0")
        config['max_position_risk_pct'] = max_position_risk
    except ValueError:
        config['max_position_risk_pct'] = 1.0
    
    # Alert levels configuration
    print("\n📊 Alert Levels Configuration:")
    try:
        rug_pull_level = float(input("Enter rug pull watch level (default: 439.50): ") or "439.50")
        config['rug_pull_level'] = rug_pull_level
    except ValueError:
        config['rug_pull_level'] = 439.50
    
    try:
        breakdown_level = float(input("Enter breakdown level (default: 434.50): ") or "434.50")
        config['breakdown_level'] = breakdown_level
    except ValueError:
        config['breakdown_level'] = 434.50
    
    try:
        fakeout_recovery = float(input("Enter fakeout recovery level (default: 435.50): ") or "435.50")
        config['fakeout_recovery'] = fakeout_recovery
    except ValueError:
        config['fakeout_recovery'] = 435.50
    
    # Server configuration
    print("\n🌐 Server Configuration:")
    server_host = input("Enter server host (default: 0.0.0.0): ").strip() or "0.0.0.0"
    config['server_host'] = server_host
    
    try:
        server_port = int(input("Enter server port (default: 5000): ") or "5000")
        config['server_port'] = server_port
    except ValueError:
        config['server_port'] = 5000
    
    # Save configuration
    config_file = "tsla_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to {config_file}")
    return config

def create_startup_script(config):
    """Create startup script with configuration"""
    startup_script = """#!/usr/bin/env python3
'''
TSLA Alert System Startup Script
Auto-generated startup script with your configuration
'''

import json
import asyncio
from tsla_alert_integration import TSLATradingSystem

async def main():
    # Load configuration
    with open('tsla_config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize trading system
    trading_system = TSLATradingSystem(
        discord_webhook_url=config['discord_webhook_url'],
        portfolio_value=config['portfolio_value']
    )
    
    # Initialize system
    await trading_system.initialize()
    
    print("🚀 TSLA Alert System Started!")
    print(f"📱 Discord: {'✅ Configured' if 'YOUR_DISCORD_WEBHOOK_URL_HERE' not in config['discord_webhook_url'] else '❌ Not configured'}")
    print(f"💰 Portfolio: ${config['portfolio_value']:,.2f}")
    print(f"🛡️ Max Daily Loss: {config['max_daily_loss_pct']}%")
    print(f"📊 Rug Pull Level: ${config['rug_pull_level']}")
    print(f"📉 Breakdown Level: ${config['breakdown_level']}")
    print(f"🌐 Server: {config['server_host']}:{config['server_port']}")
    
    # Start Flask app
    from tsla_alert_integration import app
    app.run(host=config['server_host'], port=config['server_port'], debug=False)

if __name__ == "__main__":
    asyncio.run(main())
"""
    
    with open("start_tsla_alerts.py", 'w') as f:
        f.write(startup_script)
    
    # Make executable
    os.chmod("start_tsla_alerts.py", 0o755)
    print("✅ Startup script created: start_tsla_alerts.py")

def create_tradingview_instructions():
    """Create TradingView setup instructions"""
    instructions = """# TradingView Setup Instructions

## 1. Copy Pine Script Code

Copy the complete Pine Script from `tsla_signal_stack_indicators.pine` and create a new indicator in TradingView.

## 2. Set Up Alerts

For each alert condition, create a webhook alert:

### Rug Pull Watch Alert
- **Condition**: When the indicator shows rug pull setup
- **Webhook URL**: `http://your-server:5000/webhook/tradingview`
- **Message**: 
```json
{
  "symbol": "TSLA",
  "alert_type": "rug_pull_watch",
  "price": "{{close}}",
  "rsi": "{{rsi}}",
  "macd_histogram": "{{macd_histogram}}",
  "volume": "{{volume}}",
  "timestamp": "{{time}}",
  "message": "🚨 TSLA rug setup forming — 440 rejection zone heating up."
}
```

### Bear Confirmed Alert
- **Condition**: When the indicator shows bearish breakdown
- **Webhook URL**: `http://your-server:5000/webhook/tradingview`
- **Message**:
```json
{
  "symbol": "TSLA",
  "alert_type": "bear_confirmed",
  "price": "{{close}}",
  "rsi": "{{rsi}}",
  "macd_cross": "{{macd_cross}}",
  "volume": "{{volume}}",
  "timestamp": "{{time}}",
  "message": "💀 Breakdown active under 434.50 — volume confirmed."
}
```

### Fakeout Filter Alert
- **Condition**: When the indicator detects fakeout
- **Webhook URL**: `http://your-server:5000/webhook/tradingview`
- **Message**:
```json
{
  "symbol": "TSLA",
  "alert_type": "fakeout_filter",
  "price": "{{close}}",
  "fakeout_low": "{{fakeout_low}}",
  "timestamp": "{{time}}",
  "message": "🧩 Fakeout detected. Trade canceled for safety."
}
```

## 3. Test Alerts

1. Start your TSLA alert system: `python3 start_tsla_alerts.py`
2. Test each alert condition in TradingView
3. Verify alerts are received in Discord
4. Check system logs for any errors

## 4. Monitor Performance

- Check system status: `curl http://localhost:5000/status`
- View positions: `curl http://localhost:5000/positions`
- Monitor logs: `tail -f tsla_alerts.log`
"""
    
    with open("TRADINGVIEW_SETUP.md", 'w') as f:
        f.write(instructions)
    
    print("✅ TradingView setup instructions created: TRADINGVIEW_SETUP.md")

def main():
    """Main setup function"""
    print("🚀 TSLA Pre-Market Alert System Setup")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        "tsla_premarket_alert_system.py",
        "tsla_risk_management.py", 
        "tsla_discord_integration.py",
        "tsla_alert_integration.py"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all TSLA alert system files are present.")
        sys.exit(1)
    
    print("✅ All required files found")
    
    # Create configuration
    config = create_config_file()
    
    # Create startup script
    create_startup_script(config)
    
    # Create TradingView instructions
    create_tradingview_instructions()
    
    print("\n🎯 Setup Complete!")
    print("\n📋 Next Steps:")
    print("  1. Review configuration in tsla_config.json")
    print("  2. Set up Discord webhook if not done already")
    print("  3. Follow TradingView setup instructions")
    print("  4. Start the system: python3 start_tsla_alerts.py")
    print("  5. Test alerts and monitor performance")
    
    print("\n📚 Documentation:")
    print("  • README.md - Complete system documentation")
    print("  • TRADINGVIEW_SETUP.md - TradingView configuration guide")
    print("  • tsla_tradingview_webhook_schema.json - Webhook schema reference")

if __name__ == "__main__":
    main()