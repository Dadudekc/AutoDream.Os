#!/usr/bin/env python3
"""
TSLA Pre-Market Bearish Alert System (V1.3)
Dream.OS Tactical Trading Alert Engine

Core Parameters:
- Symbol: TSLA
- Bias: Bearish
- Session: Pre-market → Open
- Confirmation Rule: 1 full 5m candle close at key level
- Risk Management: Stop loss 430, target zones 440→437, 431→425
"""

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class AlertPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AlertType(Enum):
    RUG_PULL_WATCH = "rug_pull_watch"
    BEAR_CONFIRMED = "bear_confirmed"
    FAKEOUT_FILTER = "fakeout_filter"
    VOLUME_SPIKE = "volume_spike"
    MACD_SIGNAL = "macd_signal"

@dataclass
class AlertCondition:
    name: str
    trigger_conditions: Dict
    action: Dict
    priority: AlertPriority
    alert_type: AlertType

@dataclass
class RiskManagement:
    stop_loss: float = 430.0
    max_exposure: float = 100.0  # $100 premium
    trailing_stop_pct: float = 1.5
    target_zones: List[Tuple[float, float]] = None
    
    def __post_init__(self):
        if self.target_zones is None:
            self.target_zones = [(440.0, 437.0), (431.0, 425.0)]

class TSLAAlertSystem:
    def __init__(self, discord_webhook_url: str = None, tradingview_webhook_url: str = None):
        self.discord_webhook_url = discord_webhook_url
        self.tradingview_webhook_url = tradingview_webhook_url
        self.risk_management = RiskManagement()
        self.active_alerts = {}
        self.alert_history = []
        
        # Initialize alert conditions
        self.alert_conditions = self._initialize_alert_conditions()
        
    def _initialize_alert_conditions(self) -> List[AlertCondition]:
        """Initialize all TSLA alert conditions"""
        return [
            AlertCondition(
                name="Rug Pull Watch",
                trigger_conditions={
                    "price_gte": 439.50,
                    "rsi_5m_gt": 60,
                    "macd_histogram_flattening": True,
                    "volume_increasing": True
                },
                action={
                    "send_alert": "🚨 TSLA rug setup forming — 440 rejection zone heating up.",
                    "arm_put_entry": True,
                    "wait_for_confirmation": True
                },
                priority=AlertPriority.HIGH,
                alert_type=AlertType.RUG_PULL_WATCH
            ),
            
            AlertCondition(
                name="Bear Confirmed",
                trigger_conditions={
                    "price_lt": 434.50,
                    "volume_increasing": True,
                    "rsi_5m_lt": 50,
                    "macd_cross_down": True,
                    "candle_close_confirmed": True
                },
                action={
                    "send_alert": "💀 Breakdown active under 434.50 — volume confirmed.",
                    "execute_trade": "buy_put",
                    "set_trailing_stop": True
                },
                priority=AlertPriority.HIGH,
                alert_type=AlertType.BEAR_CONFIRMED
            ),
            
            AlertCondition(
                name="Fakeout Filter",
                trigger_conditions={
                    "price_drops_below": 434.50,
                    "then_closes_above": 435.50,
                    "within_timeframe_minutes": 15
                },
                action={
                    "send_alert": "🧩 Fakeout detected. Trade canceled for safety.",
                    "cancel_open_puts": True,
                    "log_event": True
                },
                priority=AlertPriority.MEDIUM,
                alert_type=AlertType.FAKEOUT_FILTER
            ),
            
            AlertCondition(
                name="MACD Signal",
                trigger_conditions={
                    "macd_histogram_turning_red": True,
                    "macd_signal_cross": True,
                    "price_above": 435.0
                },
                action={
                    "send_alert": "⚠️ TSLA 5m MACD curling down. Wait for candle close confirmation.",
                    "prepare_for_entry": True
                },
                priority=AlertPriority.MEDIUM,
                alert_type=AlertType.MACD_SIGNAL
            )
        ]
    
    def generate_tradingview_webhook_schema(self) -> Dict:
        """Generate TradingView webhook JSON schema for direct integration"""
        return {
            "webhook_schema": {
                "name": "TSLA Pre-Market Bearish Alert System",
                "version": "1.3",
                "description": "Automated TSLA bearish bias alerts for pre-market and open session",
                "conditions": [
                    {
                        "id": "rug_pull_watch",
                        "name": "Rug Pull Watch",
                        "pine_script": """
//@version=5
indicator("TSLA Rug Pull Watch", overlay=true)

// Parameters
rsi_length = input.int(14, "RSI Length")
macd_fast = input.int(12, "MACD Fast")
macd_slow = input.int(26, "MACD Slow")
macd_signal = input.int(9, "MACD Signal")

// Calculations
rsi = ta.rsi(close, rsi_length)
[macd_line, signal_line, histogram] = ta.macd(close, macd_fast, macd_slow, macd_signal)
volume_ma = ta.sma(volume, 20)

// Conditions
price_condition = close >= 439.50
rsi_condition = rsi > 60
macd_condition = histogram < histogram[1] and histogram[1] < histogram[2]
volume_condition = volume > volume_ma

// Alert condition
alert_condition = price_condition and rsi_condition and macd_condition and volume_condition

// Alert
if alert_condition
    alert("🚨 TSLA rug setup forming — 440 rejection zone heating up.", alert.freq_once_per_bar)
""",
                        "webhook_payload": {
                            "symbol": "TSLA",
                            "alert_type": "rug_pull_watch",
                            "price": "{{close}}",
                            "rsi": "{{rsi}}",
                            "macd_histogram": "{{macd_histogram}}",
                            "volume": "{{volume}}",
                            "timestamp": "{{time}}",
                            "message": "🚨 TSLA rug setup forming — 440 rejection zone heating up."
                        }
                    },
                    {
                        "id": "bear_confirmed",
                        "name": "Bear Confirmed",
                        "pine_script": """
//@version=5
indicator("TSLA Bear Confirmed", overlay=true)

// Parameters
rsi_length = input.int(14, "RSI Length")
macd_fast = input.int(12, "MACD Fast")
macd_slow = input.int(26, "MACD Slow")
macd_signal = input.int(9, "MACD Signal")

// Calculations
rsi = ta.rsi(close, rsi_length)
[macd_line, signal_line, histogram] = ta.macd(close, macd_fast, macd_slow, macd_signal)
volume_ma = ta.sma(volume, 20)

// Conditions
price_condition = close < 434.50
rsi_condition = rsi < 50
macd_cross = ta.crossunder(macd_line, signal_line)
volume_condition = volume > volume_ma * 1.2

// Alert condition
alert_condition = price_condition and rsi_condition and macd_cross and volume_condition

// Alert
if alert_condition
    alert("💀 Breakdown active under 434.50 — volume confirmed.", alert.freq_once_per_bar)
""",
                        "webhook_payload": {
                            "symbol": "TSLA",
                            "alert_type": "bear_confirmed",
                            "price": "{{close}}",
                            "rsi": "{{rsi}}",
                            "macd_cross": "{{macd_cross}}",
                            "volume": "{{volume}}",
                            "timestamp": "{{time}}",
                            "message": "💀 Breakdown active under 434.50 — volume confirmed."
                        }
                    },
                    {
                        "id": "fakeout_filter",
                        "name": "Fakeout Filter",
                        "pine_script": """
//@version=5
indicator("TSLA Fakeout Filter", overlay=true)

// Variables
var float fakeout_low = na
var bool fakeout_detected = false

// Track price below 434.50
if close < 434.50 and na(fakeout_low)
    fakeout_low := low

// Check for recovery above 435.50
if not na(fakeout_low) and close > 435.50
    fakeout_detected := true
    alert("🧩 Fakeout detected. Trade canceled for safety.", alert.freq_once_per_bar)
    fakeout_low := na

// Reset on new day
if ta.change(time("1D"))
    fakeout_detected := false
    fakeout_low := na
""",
                        "webhook_payload": {
                            "symbol": "TSLA",
                            "alert_type": "fakeout_filter",
                            "price": "{{close}}",
                            "fakeout_low": "{{fakeout_low}}",
                            "timestamp": "{{time}}",
                            "message": "🧩 Fakeout detected. Trade canceled for safety."
                        }
                    }
                ],
                "signal_stack": {
                    "vwap_alignment": "below",
                    "ema20_vs_ema50": "bearish_cross",
                    "qqq_correlation": "positive_divergence",
                    "timeframe_sync": ["30m", "15m", "5m"]
                },
                "risk_management": {
                    "stop_loss": 430.0,
                    "target_zones": [[440.0, 437.0], [431.0, 425.0]],
                    "max_exposure": 100.0,
                    "trailing_stop_pct": 1.5
                }
            }
        }
    
    def generate_discord_webhook_payload(self, alert_data: Dict) -> Dict:
        """Generate Discord webhook payload for alert delivery"""
        return {
            "username": "TSLA Alert Bot",
            "avatar_url": "https://cdn.discordapp.com/emojis/📈.png",
            "embeds": [{
                "title": f"🚨 TSLA Alert - {alert_data.get('alert_type', 'Unknown')}",
                "description": alert_data.get('message', 'No message'),
                "color": 0xff0000 if alert_data.get('priority') == 'high' else 0xffaa00,
                "fields": [
                    {
                        "name": "Price",
                        "value": f"${alert_data.get('price', 'N/A')}",
                        "inline": True
                    },
                    {
                        "name": "RSI (5m)",
                        "value": f"{alert_data.get('rsi', 'N/A')}",
                        "inline": True
                    },
                    {
                        "name": "Volume",
                        "value": f"{alert_data.get('volume', 'N/A'):,}",
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": f"<t:{int(datetime.now().timestamp())}:F>",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Dream.OS Tactical Trading System",
                    "icon_url": "https://cdn.discordapp.com/emojis/🤖.png"
                },
                "timestamp": datetime.now().isoformat()
            }]
        }
    
    def send_discord_alert(self, alert_data: Dict) -> bool:
        """Send alert to Discord webhook"""
        if not self.discord_webhook_url:
            print("Discord webhook URL not configured")
            return False
        
        try:
            payload = self.generate_discord_webhook_payload(alert_data)
            response = requests.post(self.discord_webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"✅ Discord alert sent: {alert_data.get('message')}")
            return True
        except Exception as e:
            print(f"❌ Failed to send Discord alert: {e}")
            return False
    
    def process_tradingview_webhook(self, webhook_data: Dict) -> bool:
        """Process incoming TradingView webhook data"""
        try:
            alert_type = webhook_data.get('alert_type')
            price = float(webhook_data.get('price', 0))
            
            # Log the alert
            self.alert_history.append({
                'timestamp': datetime.now().isoformat(),
                'alert_type': alert_type,
                'price': price,
                'raw_data': webhook_data
            })
            
            # Process based on alert type
            if alert_type == 'rug_pull_watch':
                return self._handle_rug_pull_watch(webhook_data)
            elif alert_type == 'bear_confirmed':
                return self._handle_bear_confirmed(webhook_data)
            elif alert_type == 'fakeout_filter':
                return self._handle_fakeout_filter(webhook_data)
            else:
                print(f"Unknown alert type: {alert_type}")
                return False
                
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return False
    
    def _handle_rug_pull_watch(self, data: Dict) -> bool:
        """Handle rug pull watch alert"""
        print("🔍 Rug pull setup detected - monitoring for confirmation...")
        self.active_alerts['rug_pull'] = {
            'timestamp': datetime.now(),
            'price': float(data.get('price', 0)),
            'status': 'monitoring'
        }
        return self.send_discord_alert(data)
    
    def _handle_bear_confirmed(self, data: Dict) -> bool:
        """Handle bear confirmed alert"""
        print("🐻 Bearish breakdown confirmed - executing trade logic...")
        self.active_alerts['bear_confirmed'] = {
            'timestamp': datetime.now(),
            'price': float(data.get('price', 0)),
            'status': 'executing'
        }
        return self.send_discord_alert(data)
    
    def _handle_fakeout_filter(self, data: Dict) -> bool:
        """Handle fakeout filter alert"""
        print("🛡️ Fakeout detected - canceling open positions...")
        if 'rug_pull' in self.active_alerts:
            del self.active_alerts['rug_pull']
        return self.send_discord_alert(data)
    
    def get_alert_summary(self) -> Dict:
        """Get current alert system status"""
        return {
            'active_alerts': len(self.active_alerts),
            'total_alerts_sent': len(self.alert_history),
            'risk_management': {
                'stop_loss': self.risk_management.stop_loss,
                'max_exposure': self.risk_management.max_exposure,
                'target_zones': self.risk_management.target_zones
            },
            'last_alert': self.alert_history[-1] if self.alert_history else None
        }

def main():
    """Main function to demonstrate the alert system"""
    print("🚀 TSLA Pre-Market Alert System (V1.3)")
    print("=" * 50)
    
    # Initialize the alert system
    alert_system = TSLAAlertSystem()
    
    # Generate TradingView webhook schema
    webhook_schema = alert_system.generate_tradingview_webhook_schema()
    
    # Save schema to file
    with open('tsla_tradingview_webhook_schema.json', 'w') as f:
        json.dump(webhook_schema, f, indent=2)
    
    print("✅ TradingView webhook schema generated: tsla_tradingview_webhook_schema.json")
    
    # Display alert conditions
    print("\n📋 Alert Conditions:")
    for condition in alert_system.alert_conditions:
        print(f"  • {condition.name} ({condition.priority.value})")
    
    # Display risk management
    print(f"\n🛡️ Risk Management:")
    print(f"  • Stop Loss: ${alert_system.risk_management.stop_loss}")
    print(f"  • Max Exposure: ${alert_system.risk_management.max_exposure}")
    print(f"  • Target Zones: {alert_system.risk_management.target_zones}")
    
    print("\n🎯 Ready for TradingView integration!")

if __name__ == "__main__":
    main()