#!/usr/bin/env python3
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
