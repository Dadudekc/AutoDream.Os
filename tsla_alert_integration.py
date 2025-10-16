#!/usr/bin/env python3
"""
TSLA Alert System Integration
Dream.OS Tactical Trading Complete Integration

This file integrates all components:
- TradingView webhook processing
- Risk management
- Discord notifications
- Position tracking
- Alert routing
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from tsla_premarket_alert_system import TSLAAlertSystem
from tsla_risk_management import TSLARiskManager
from tsla_discord_integration import TSLADiscordBot, DiscordConfig, AlertData, AlertSeverity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tsla_alerts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TSLATradingSystem:
    def __init__(self, discord_webhook_url: str, portfolio_value: float = 10000.0):
        self.alert_system = TSLAAlertSystem(discord_webhook_url=discord_webhook_url)
        self.risk_manager = TSLARiskManager(portfolio_value=portfolio_value)
        
        # Discord configuration
        discord_config = DiscordConfig(webhook_url=discord_webhook_url)
        self.discord_bot = TSLADiscordBot(discord_config)
        
        # System state
        self.is_running = False
        self.last_price_update = None
        self.active_positions = {}
        
    async def initialize(self):
        """Initialize the trading system"""
        logger.info("🚀 Initializing TSLA Trading System...")
        
        # Initialize Discord bot
        await self.discord_bot.__aenter__()
        
        # Send startup notification
        await self._send_system_status("initializing", "System starting up...")
        
        self.is_running = True
        logger.info("✅ TSLA Trading System initialized successfully")
    
    async def shutdown(self):
        """Shutdown the trading system"""
        logger.info("🛑 Shutting down TSLA Trading System...")
        
        # Send shutdown notification
        await self._send_system_status("shutdown", "System shutting down...")
        
        # Close Discord bot
        await self.discord_bot.__aexit__(None, None, None)
        
        self.is_running = False
        logger.info("✅ TSLA Trading System shutdown complete")
    
    async def process_tradingview_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming TradingView webhook"""
        try:
            logger.info(f"📨 Processing TradingView webhook: {webhook_data.get('alert_type', 'unknown')}")
            
            # Process through alert system
            alert_processed = self.alert_system.process_tradingview_webhook(webhook_data)
            
            if not alert_processed:
                return {"status": "error", "message": "Failed to process alert"}
            
            # Extract key data
            alert_type = webhook_data.get('alert_type')
            price = float(webhook_data.get('price', 0))
            symbol = webhook_data.get('symbol', 'TSLA')
            
            # Create alert data for Discord
            alert_data = AlertData(
                alert_type=alert_type,
                symbol=symbol,
                price=price,
                message=webhook_data.get('message', 'No message'),
                severity=self._get_alert_severity(alert_type),
                timestamp=datetime.now(),
                additional_data=webhook_data
            )
            
            # Send Discord alert
            discord_sent = await self.discord_bot.send_alert(alert_data)
            
            # Handle position management based on alert type
            position_result = await self._handle_position_management(alert_type, price, webhook_data)
            
            return {
                "status": "success",
                "alert_processed": alert_processed,
                "discord_sent": discord_sent,
                "position_result": position_result
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing webhook: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _handle_position_management(self, alert_type: str, price: float, webhook_data: Dict) -> Dict:
        """Handle position management based on alert type"""
        try:
            if alert_type == "bear_confirmed":
                # Create new put position
                position = self.risk_manager.create_position(
                    symbol="TSLA",
                    entry_price=price,
                    position_type="put",
                    current_price=price
                )
                
                if position:
                    self.active_positions[position.symbol] = position
                    
                    # Send position update to Discord
                    position_data = {
                        "symbol": position.symbol,
                        "position_type": position.position_type,
                        "quantity": position.quantity,
                        "entry_price": position.entry_price,
                        "current_price": position.current_price,
                        "unrealized_pnl": position.unrealized_pnl,
                        "status": "opened"
                    }
                    
                    await self.discord_bot.send_position_update(position_data)
                    
                    return {"action": "position_created", "position_id": id(position)}
                else:
                    return {"action": "position_creation_failed"}
            
            elif alert_type == "fakeout_filter":
                # Cancel any open positions
                cancelled_positions = []
                for symbol, position in list(self.active_positions.items()):
                    if position.status.value == "monitoring":
                        position.status = "cancelled"
                        cancelled_positions.append(symbol)
                        del self.active_positions[symbol]
                
                return {"action": "positions_cancelled", "count": len(cancelled_positions)}
            
            else:
                return {"action": "no_position_action"}
                
        except Exception as e:
            logger.error(f"❌ Error in position management: {e}")
            return {"action": "error", "message": str(e)}
    
    def _get_alert_severity(self, alert_type: str) -> AlertSeverity:
        """Get alert severity based on type"""
        severity_map = {
            "rug_pull_watch": AlertSeverity.WARNING,
            "bear_confirmed": AlertSeverity.CRITICAL,
            "fakeout_filter": AlertSeverity.INFO,
            "macd_signal": AlertSeverity.WARNING,
            "volume_spike": AlertSeverity.INFO
        }
        return severity_map.get(alert_type, AlertSeverity.INFO)
    
    async def update_positions(self, current_price: float) -> Dict:
        """Update all active positions with current price"""
        try:
            updated_positions = []
            
            for symbol, position in self.active_positions.items():
                update_result = self.risk_manager.update_position(position, current_price)
                updated_positions.append({
                    "symbol": symbol,
                    "result": update_result
                })
                
                # Send position update if status changed
                if update_result.get("status") == "closed":
                    position_data = {
                        "symbol": position.symbol,
                        "position_type": position.position_type,
                        "quantity": position.quantity,
                        "entry_price": position.entry_price,
                        "current_price": position.current_price,
                        "unrealized_pnl": position.unrealized_pnl,
                        "status": "closed"
                    }
                    
                    await self.discord_bot.send_position_update(position_data)
                    
                    # Remove from active positions
                    del self.active_positions[symbol]
            
            return {"updated_positions": updated_positions}
            
        except Exception as e:
            logger.error(f"❌ Error updating positions: {e}")
            return {"error": str(e)}
    
    async def _send_system_status(self, status: str, message: str):
        """Send system status update to Discord"""
        try:
            status_data = {
                "status": status,
                "uptime": "N/A",  # Would calculate actual uptime
                "alerts_sent": len(self.alert_system.alert_history),
                "message": message
            }
            
            await self.discord_bot.send_system_status(status_data)
            
        except Exception as e:
            logger.error(f"❌ Error sending system status: {e}")
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        risk_summary = self.risk_manager.get_risk_summary()
        alert_summary = self.alert_system.get_alert_summary()
        discord_summary = self.discord_bot.get_alert_summary()
        
        return {
            "system_running": self.is_running,
            "active_positions": len(self.active_positions),
            "risk_management": risk_summary,
            "alert_system": alert_summary,
            "discord_bot": discord_summary,
            "last_price_update": self.last_price_update
        }

# Flask web server for webhook handling
app = Flask(__name__)
trading_system = None

@app.route('/webhook/tradingview', methods=['POST'])
async def tradingview_webhook():
    """Handle TradingView webhook requests"""
    try:
        webhook_data = request.get_json()
        
        if not webhook_data:
            return jsonify({"status": "error", "message": "No data received"}), 400
        
        logger.info(f"📨 Received TradingView webhook: {webhook_data}")
        
        # Process webhook
        result = await trading_system.process_tradingview_webhook(webhook_data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get system status"""
    try:
        status = trading_system.get_system_status()
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"❌ Status error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/positions', methods=['GET'])
def get_positions():
    """Get current positions"""
    try:
        positions = []
        for symbol, position in trading_system.active_positions.items():
            positions.append({
                "symbol": position.symbol,
                "type": position.position_type,
                "quantity": position.quantity,
                "entry_price": position.entry_price,
                "current_price": position.current_price,
                "unrealized_pnl": position.unrealized_pnl,
                "status": position.status.value
            })
        
        return jsonify({"positions": positions})
        
    except Exception as e:
        logger.error(f"❌ Positions error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

async def main():
    """Main function to run the trading system"""
    global trading_system
    
    # Configuration
    DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
    PORTFOLIO_VALUE = 10000.0
    
    # Initialize trading system
    trading_system = TSLATradingSystem(
        discord_webhook_url=DISCORD_WEBHOOK_URL,
        portfolio_value=PORTFOLIO_VALUE
    )
    
    # Initialize system
    await trading_system.initialize()
    
    # Start Flask app
    logger.info("🌐 Starting Flask web server...")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    asyncio.run(main())