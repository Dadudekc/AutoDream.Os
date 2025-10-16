#!/usr/bin/env python3
"""
TSLA Alert System Demo
Demonstrates the complete TSLA pre-market bearish alert system
"""

import json
import asyncio
from datetime import datetime
from tsla_premarket_alert_system import TSLAAlertSystem
from tsla_risk_management import TSLARiskManager
from tsla_discord_integration import TSLADiscordBot, DiscordConfig, AlertData, AlertSeverity

async def demo_alert_system():
    """Demonstrate the complete TSLA alert system"""
    print("🚀 TSLA Pre-Market Alert System Demo")
    print("=" * 50)
    
    # Initialize components
    alert_system = TSLAAlertSystem()
    risk_manager = TSLARiskManager(portfolio_value=10000.0)
    
    # Discord config (using placeholder URL for demo)
    discord_config = DiscordConfig(webhook_url="https://discord.com/api/webhooks/placeholder")
    discord_bot = TSLADiscordBot(discord_config)
    
    print("\n📋 System Components Initialized:")
    print("  ✅ Alert System")
    print("  ✅ Risk Manager")
    print("  ✅ Discord Bot")
    
    # Generate TradingView webhook schema
    print("\n🔧 Generating TradingView Webhook Schema...")
    webhook_schema = alert_system.generate_tradingview_webhook_schema()
    
    # Save schema
    with open('tsla_tradingview_webhook_schema.json', 'w') as f:
        json.dump(webhook_schema, f, indent=2)
    print("  ✅ Schema saved to tsla_tradingview_webhook_schema.json")
    
    # Simulate webhook data
    print("\n📨 Simulating TradingView Webhook Data...")
    
    # Rug Pull Watch Alert
    rug_pull_data = {
        "symbol": "TSLA",
        "alert_type": "rug_pull_watch",
        "price": "439.50",
        "rsi": "65.2",
        "macd_histogram": "-0.15",
        "volume": "1250000",
        "timestamp": "1640995200",
        "message": "🚨 TSLA rug setup forming — 440 rejection zone heating up."
    }
    
    print("  📤 Processing Rug Pull Watch Alert...")
    result = alert_system.process_tradingview_webhook(rug_pull_data)
    print(f"  ✅ Alert processed: {result}")
    
    # Bear Confirmed Alert
    bear_confirmed_data = {
        "symbol": "TSLA",
        "alert_type": "bear_confirmed",
        "price": "432.00",
        "rsi": "45.8",
        "macd_cross": "true",
        "volume": "1800000",
        "timestamp": "1640995800",
        "message": "💀 Breakdown active under 434.50 — volume confirmed."
    }
    
    print("\n  📤 Processing Bear Confirmed Alert...")
    result = alert_system.process_tradingview_webhook(bear_confirmed_data)
    print(f"  ✅ Alert processed: {result}")
    
    # Create position
    print("\n📈 Creating TSLA Put Position...")
    position = risk_manager.create_position(
        symbol="TSLA",
        entry_price=432.0,
        position_type="put",
        current_price=432.0
    )
    
    if position:
        print(f"  ✅ Position created: {position.quantity} contracts")
        print(f"  💰 Entry Price: ${position.entry_price}")
        print(f"  🛑 Stop Loss: ${position.stop_loss}")
        print(f"  🎯 Target Zones: {position.target_zones}")
        
        # Simulate price movement
        print("\n📊 Simulating Price Movement...")
        prices = [430.0, 428.0, 425.0, 422.0, 420.0]
        
        for i, price in enumerate(prices):
            print(f"  📉 Price: ${price}")
            update_result = risk_manager.update_position(position, price)
            print(f"  💰 Unrealized P&L: ${position.unrealized_pnl:.2f}")
            
            if update_result.get("status") == "closed":
                print(f"  🔒 Position closed: {update_result.get('reason', 'unknown')}")
                break
    else:
        print("  ❌ Position creation failed")
    
    # Fakeout Filter Alert
    fakeout_data = {
        "symbol": "TSLA",
        "alert_type": "fakeout_filter",
        "price": "436.00",
        "fakeout_low": "431.50",
        "timestamp": "1640996400",
        "message": "🧩 Fakeout detected. Trade canceled for safety."
    }
    
    print("\n  📤 Processing Fakeout Filter Alert...")
    result = alert_system.process_tradingview_webhook(fakeout_data)
    print(f"  ✅ Alert processed: {result}")
    
    # Display system status
    print("\n📊 System Status Summary:")
    alert_summary = alert_system.get_alert_summary()
    risk_summary = risk_manager.get_risk_summary()
    
    print(f"  📈 Active Alerts: {alert_summary['active_alerts']}")
    print(f"  📨 Total Alerts Sent: {alert_summary['total_alerts_sent']}")
    print(f"  💰 Daily P&L: ${risk_summary['daily_pnl']:.2f}")
    print(f"  📊 Active Positions: {risk_summary['active_positions']}")
    print(f"  🛡️ Risk Level: {risk_summary['risk_level']}")
    
    # Display TradingView webhook schema
    print("\n🔧 TradingView Webhook Schema:")
    print("  📋 Alert Conditions:")
    for condition in webhook_schema['webhook_schema']['conditions']:
        print(f"    • {condition['name']} ({condition['id']})")
    
    print("\n  🧠 Signal Stack:")
    signal_stack = webhook_schema['webhook_schema']['signal_stack']
    for key, value in signal_stack.items():
        print(f"    • {key}: {value}")
    
    print("\n  🛡️ Risk Management:")
    risk_mgmt = webhook_schema['webhook_schema']['risk_management']
    print(f"    • Stop Loss: ${risk_mgmt['stop_loss']}")
    print(f"    • Max Exposure: ${risk_mgmt['max_exposure']}")
    print(f"    • Target Zones: {risk_mgmt['target_zones']}")
    
    print("\n✅ Demo Complete!")
    print("\n🎯 Next Steps:")
    print("  1. Set up Discord webhook URL")
    print("  2. Configure TradingView alerts")
    print("  3. Deploy webhook server")
    print("  4. Start monitoring TSLA pre-market")

def main():
    """Main demo function"""
    asyncio.run(demo_alert_system())

if __name__ == "__main__":
    main()