#!/usr/bin/env python3
"""
TSLA Discord Integration
Dream.OS Tactical Trading Discord Bot

Features:
- Real-time alert delivery
- Rich embed formatting
- Position tracking
- Risk management updates
- Webhook management
"""

import json
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"

class MessageType(Enum):
    ALERT = "alert"
    POSITION_UPDATE = "position_update"
    RISK_UPDATE = "risk_update"
    SYSTEM_STATUS = "system_status"
    TRADE_SIGNAL = "trade_signal"

@dataclass
class DiscordConfig:
    webhook_url: str
    bot_token: Optional[str] = None
    channel_id: Optional[str] = None
    guild_id: Optional[str] = None
    username: str = "TSLA Alert Bot"
    avatar_url: str = "https://cdn.discordapp.com/emojis/📈.png"

@dataclass
class AlertData:
    alert_type: str
    symbol: str
    price: float
    message: str
    severity: AlertSeverity
    timestamp: datetime
    additional_data: Dict[str, Any] = None

class TSLADiscordBot:
    def __init__(self, config: DiscordConfig):
        self.config = config
        self.session = None
        self.alert_history = []
        self.rate_limits = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_color(self, severity: AlertSeverity) -> int:
        """Get Discord embed color based on severity"""
        colors = {
            AlertSeverity.INFO: 0x3498db,      # Blue
            AlertSeverity.WARNING: 0xf39c12,   # Orange
            AlertSeverity.CRITICAL: 0xe74c3c,  # Red
            AlertSeverity.SUCCESS: 0x2ecc71    # Green
        }
        return colors.get(severity, 0x95a5a6)  # Default gray
    
    def _get_emoji(self, alert_type: str) -> str:
        """Get emoji based on alert type"""
        emojis = {
            "rug_pull_watch": "🚨",
            "bear_confirmed": "💀",
            "fakeout_filter": "🧩",
            "macd_signal": "⚠️",
            "volume_spike": "📈",
            "position_opened": "✅",
            "position_closed": "🔒",
            "stop_loss": "🛑",
            "target_hit": "🎯",
            "risk_warning": "⚠️"
        }
        return emojis.get(alert_type, "📊")
    
    def _format_price(self, price: float) -> str:
        """Format price with proper precision"""
        return f"${price:.2f}"
    
    def _format_percentage(self, value: float) -> str:
        """Format percentage with proper precision"""
        return f"{value:.2f}%"
    
    def _format_timestamp(self, timestamp: datetime) -> str:
        """Format timestamp for Discord"""
        return f"<t:{int(timestamp.timestamp())}:F>"
    
    async def send_alert(self, alert_data: AlertData) -> bool:
        """Send alert to Discord"""
        try:
            embed = self._create_alert_embed(alert_data)
            payload = {
                "username": self.config.username,
                "avatar_url": self.config.avatar_url,
                "embeds": [embed]
            }
            
            async with self.session.post(self.config.webhook_url, json=payload) as response:
                if response.status == 204:
                    print(f"✅ Alert sent: {alert_data.message}")
                    self.alert_history.append(alert_data)
                    return True
                else:
                    print(f"❌ Failed to send alert: {response.status}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error sending alert: {e}")
            return False
    
    def _create_alert_embed(self, alert_data: AlertData) -> Dict:
        """Create Discord embed for alert"""
        emoji = self._get_emoji(alert_data.alert_type)
        color = self._get_color(alert_data.severity)
        
        embed = {
            "title": f"{emoji} TSLA {alert_data.alert_type.replace('_', ' ').title()}",
            "description": alert_data.message,
            "color": color,
            "timestamp": alert_data.timestamp.isoformat(),
            "fields": [
                {
                    "name": "Symbol",
                    "value": alert_data.symbol,
                    "inline": True
                },
                {
                    "name": "Price",
                    "value": self._format_price(alert_data.price),
                    "inline": True
                },
                {
                    "name": "Severity",
                    "value": alert_data.severity.value.upper(),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Dream.OS Tactical Trading System",
                "icon_url": "https://cdn.discordapp.com/emojis/🤖.png"
            }
        }
        
        # Add additional data fields
        if alert_data.additional_data:
            for key, value in alert_data.additional_data.items():
                if isinstance(value, (int, float)):
                    if "pct" in key.lower() or "rate" in key.lower():
                        value = self._format_percentage(value)
                    elif "price" in key.lower() or "amount" in key.lower():
                        value = self._format_price(value)
                
                embed["fields"].append({
                    "name": key.replace("_", " ").title(),
                    "value": str(value),
                    "inline": True
                })
        
        return embed
    
    async def send_position_update(self, position_data: Dict) -> bool:
        """Send position update to Discord"""
        try:
            embed = self._create_position_embed(position_data)
            payload = {
                "username": self.config.username,
                "avatar_url": self.config.avatar_url,
                "embeds": [embed]
            }
            
            async with self.session.post(self.config.webhook_url, json=payload) as response:
                return response.status == 204
                
        except Exception as e:
            print(f"❌ Error sending position update: {e}")
            return False
    
    def _create_position_embed(self, position_data: Dict) -> Dict:
        """Create Discord embed for position update"""
        status = position_data.get("status", "unknown")
        emoji = "✅" if status == "opened" else "🔒" if status == "closed" else "📊"
        
        embed = {
            "title": f"{emoji} TSLA Position Update",
            "color": 0x3498db if status == "opened" else 0xe74c3c if status == "closed" else 0x95a5a6,
            "timestamp": datetime.now().isoformat(),
            "fields": [
                {
                    "name": "Symbol",
                    "value": position_data.get("symbol", "TSLA"),
                    "inline": True
                },
                {
                    "name": "Type",
                    "value": position_data.get("position_type", "Unknown").upper(),
                    "inline": True
                },
                {
                    "name": "Quantity",
                    "value": str(position_data.get("quantity", 0)),
                    "inline": True
                },
                {
                    "name": "Entry Price",
                    "value": self._format_price(position_data.get("entry_price", 0)),
                    "inline": True
                },
                {
                    "name": "Current Price",
                    "value": self._format_price(position_data.get("current_price", 0)),
                    "inline": True
                },
                {
                    "name": "P&L",
                    "value": self._format_price(position_data.get("unrealized_pnl", 0)),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Dream.OS Position Tracker",
                "icon_url": "https://cdn.discordapp.com/emojis/📊.png"
            }
        }
        
        return embed
    
    async def send_risk_update(self, risk_data: Dict) -> bool:
        """Send risk management update to Discord"""
        try:
            embed = self._create_risk_embed(risk_data)
            payload = {
                "username": self.config.username,
                "avatar_url": self.config.avatar_url,
                "embeds": [embed]
            }
            
            async with self.session.post(self.config.webhook_url, json=payload) as response:
                return response.status == 204
                
        except Exception as e:
            print(f"❌ Error sending risk update: {e}")
            return False
    
    def _create_risk_embed(self, risk_data: Dict) -> Dict:
        """Create Discord embed for risk update"""
        risk_level = risk_data.get("risk_level", "medium")
        color = 0x2ecc71 if risk_level == "low" else 0xf39c12 if risk_level == "medium" else 0xe74c3c
        
        embed = {
            "title": "🛡️ Risk Management Update",
            "color": color,
            "timestamp": datetime.now().isoformat(),
            "fields": [
                {
                    "name": "Portfolio Value",
                    "value": self._format_price(risk_data.get("portfolio_value", 0)),
                    "inline": True
                },
                {
                    "name": "Daily P&L",
                    "value": self._format_price(risk_data.get("daily_pnl", 0)),
                    "inline": True
                },
                {
                    "name": "Risk Level",
                    "value": risk_level.upper(),
                    "inline": True
                },
                {
                    "name": "Active Positions",
                    "value": str(risk_data.get("active_positions", 0)),
                    "inline": True
                },
                {
                    "name": "Total Exposure",
                    "value": self._format_percentage(risk_data.get("exposure_pct", 0)),
                    "inline": True
                },
                {
                    "name": "Daily Trades",
                    "value": f"{risk_data.get('daily_trades', 0)}/{risk_data.get('max_daily_trades', 0)}",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Dream.OS Risk Manager",
                "icon_url": "https://cdn.discordapp.com/emojis/🛡️.png"
            }
        }
        
        return embed
    
    async def send_system_status(self, status_data: Dict) -> bool:
        """Send system status update to Discord"""
        try:
            embed = {
                "title": "🤖 System Status Update",
                "color": 0x2ecc71 if status_data.get("status") == "healthy" else 0xe74c3c,
                "timestamp": datetime.now().isoformat(),
                "fields": [
                    {
                        "name": "Status",
                        "value": status_data.get("status", "Unknown").upper(),
                        "inline": True
                    },
                    {
                        "name": "Uptime",
                        "value": status_data.get("uptime", "Unknown"),
                        "inline": True
                    },
                    {
                        "name": "Alerts Sent",
                        "value": str(status_data.get("alerts_sent", 0)),
                        "inline": True
                    },
                    {
                        "name": "Last Update",
                        "value": self._format_timestamp(datetime.now()),
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Dream.OS System Monitor",
                    "icon_url": "https://cdn.discordapp.com/emojis/🤖.png"
                }
            }
            
            payload = {
                "username": self.config.username,
                "avatar_url": self.config.avatar_url,
                "embeds": [embed]
            }
            
            async with self.session.post(self.config.webhook_url, json=payload) as response:
                return response.status == 204
                
        except Exception as e:
            print(f"❌ Error sending system status: {e}")
            return False
    
    def get_alert_summary(self) -> Dict:
        """Get summary of sent alerts"""
        total_alerts = len(self.alert_history)
        alerts_by_type = {}
        alerts_by_severity = {}
        
        for alert in self.alert_history:
            alert_type = alert.alert_type
            severity = alert.severity.value
            
            alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1
            alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "alerts_by_type": alerts_by_type,
            "alerts_by_severity": alerts_by_severity,
            "last_alert": self.alert_history[-1] if self.alert_history else None
        }

async def main():
    """Demonstrate Discord integration"""
    print("🤖 TSLA Discord Integration Demo")
    print("=" * 40)
    
    # Configuration (replace with your actual webhook URL)
    config = DiscordConfig(
        webhook_url="YOUR_DISCORD_WEBHOOK_URL_HERE",
        username="TSLA Alert Bot",
        avatar_url="https://cdn.discordapp.com/emojis/📈.png"
    )
    
    async with TSLADiscordBot(config) as bot:
        # Send sample alert
        alert_data = AlertData(
            alert_type="rug_pull_watch",
            symbol="TSLA",
            price=439.50,
            message="🚨 TSLA rug setup forming — 440 rejection zone heating up.",
            severity=AlertSeverity.CRITICAL,
            timestamp=datetime.now(),
            additional_data={
                "rsi": 65.2,
                "macd_histogram": -0.15,
                "volume": 1250000,
                "vwap_alignment": "bearish"
            }
        )
        
        print("📤 Sending sample alert...")
        success = await bot.send_alert(alert_data)
        
        if success:
            print("✅ Alert sent successfully!")
        else:
            print("❌ Failed to send alert")
        
        # Send position update
        position_data = {
            "symbol": "TSLA",
            "position_type": "put",
            "quantity": 5,
            "entry_price": 435.0,
            "current_price": 432.0,
            "unrealized_pnl": 15.0,
            "status": "opened"
        }
        
        print("\n📊 Sending position update...")
        success = await bot.send_position_update(position_data)
        
        if success:
            print("✅ Position update sent successfully!")
        else:
            print("❌ Failed to send position update")
        
        # Get alert summary
        summary = bot.get_alert_summary()
        print(f"\n📋 Alert Summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())