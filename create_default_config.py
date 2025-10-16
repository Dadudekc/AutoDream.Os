#!/usr/bin/env python3
"""
Create default configuration for TSLA Alert System
"""

import json

def create_default_config():
    """Create default configuration file"""
    config = {
        "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
        "portfolio_value": 10000.0,
        "max_daily_loss_pct": 5.0,
        "max_position_risk_pct": 1.0,
        "rug_pull_level": 439.50,
        "breakdown_level": 434.50,
        "fakeout_recovery": 435.50,
        "server_host": "0.0.0.0",
        "server_port": 5000
    }
    
    with open("tsla_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Default configuration created: tsla_config.json")
    return config

def create_startup_script():
    """Create startup script"""
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
    
    print("✅ Startup script created: start_tsla_alerts.py")

def main():
    """Main function"""
    print("🔧 Creating TSLA Alert System Configuration")
    print("=" * 50)
    
    # Create default config
    config = create_default_config()
    
    # Create startup script
    create_startup_script()
    
    print("\n✅ Configuration files created!")
    print("\n📋 Files created:")
    print("  • tsla_config.json - System configuration")
    print("  • start_tsla_alerts.py - Startup script")
    
    print("\n🎯 Next Steps:")
    print("  1. Edit tsla_config.json to add your Discord webhook URL")
    print("  2. Set up TradingView alerts using the Pine Script")
    print("  3. Start the system: python3 start_tsla_alerts.py")
    print("  4. Test alerts and monitor performance")

if __name__ == "__main__":
    main()