# 🚀 TSLA Pre-Market Bearish Alert System (V1.3)

**Dream.OS Tactical Trading System** - Automated TSLA bearish bias alerts for pre-market and open session trading.

## 🎯 Overview

This system provides automated alert conditions and triggers for TSLA pre-market and open-session trading, designed to detect 440 rejection or 430 break, alert the swarm, and execute trade logic under a 5-minute confirmation rule.

## ⚙️ Core Parameters

- **Symbol**: TSLA
- **Bias**: Bearish
- **Session**: Pre-market → Open
- **Alert Engine**: TradingView / Dream.OS AlertBridge
- **Confirmation Rule**: 1 full 5m candle close at key level
- **Risk Management**: Stop loss 430, target zones 440→437, 431→425
- **Max Exposure**: 1 contract @ $100 premium

## 🧩 Alert Conditions

### 1. Rug Pull Watch
- **Trigger**: Price ≥ 439.50, RSI(5m) > 60, MACD histogram flattening
- **Action**: Send alert, arm put entry
- **Message**: "🚨 TSLA rug setup forming — 440 rejection zone heating up."

### 2. Bear Confirmed
- **Trigger**: Price < 434.50, volume increasing, RSI < 50, MACD cross down
- **Action**: Execute put trade, set trailing stop
- **Message**: "💀 Breakdown active under 434.50 — volume confirmed."

### 3. Fakeout Filter
- **Trigger**: Price drops below 434.50 then closes above 435.50
- **Action**: Cancel open puts, log event
- **Message**: "🧩 Fakeout detected. Trade canceled for safety."

## 🧠 Signal Stack (Confirmers)

- **VWAP Alignment**: Below VWAP = Bearish
- **EMA Cross**: 20 below 50 = Bearish
- **QQQ Correlation**: Positive divergence detection
- **Timeframe Sync**: 30m, 15m, 5m alignment

## 📁 File Structure

```
tsla_alert_system/
├── tsla_premarket_alert_system.py    # Main alert system
├── tsla_tradingview_webhook_schema.json  # TradingView webhook schema
├── tsla_signal_stack_indicators.pine     # Pine Script indicators
├── tsla_risk_management.py               # Risk management system
├── tsla_discord_integration.py           # Discord bot integration
├── tsla_alert_integration.py             # Complete system integration
└── README.md                             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests aiohttp flask
```

### 2. Configure Discord Webhook

1. Create a Discord webhook in your server
2. Update the webhook URL in `tsla_alert_integration.py`:

```python
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
```

### 3. Set Up TradingView Alerts

1. Copy the Pine Script from `tsla_signal_stack_indicators.pine`
2. Create a new indicator in TradingView
3. Set up webhook alerts using the schema from `tsla_tradingview_webhook_schema.json`
4. Configure webhook URL to point to your server: `http://your-server:5000/webhook/tradingview`

### 4. Run the System

```bash
python tsla_alert_integration.py
```

## 🔧 Configuration

### Risk Management Parameters

```python
# In tsla_risk_management.py
@dataclass
class RiskParameters:
    max_portfolio_risk: float = 0.02      # 2% of portfolio
    max_position_risk: float = 0.01       # 1% per position
    stop_loss_pct: float = 0.15           # 15% stop loss
    trailing_stop_pct: float = 0.015      # 1.5% trailing stop
    target_risk_reward: float = 2.0       # 2:1 risk/reward minimum
    max_daily_loss: float = 0.05          # 5% max daily loss
```

### Alert Levels

```python
# Key price levels
rug_pull_level = 439.50      # Rug pull watch level
breakdown_level = 434.50     # Breakdown confirmation level
fakeout_recovery = 435.50    # Fakeout recovery level
```

## 📊 TradingView Integration

### Pine Script Setup

1. **Copy the complete Pine Script** from `tsla_signal_stack_indicators.pine`
2. **Create new indicator** in TradingView
3. **Apply to TSLA chart** with 5-minute timeframe
4. **Set up alerts** for each condition

### Webhook Configuration

```json
{
  "webhook_url": "http://your-server:5000/webhook/tradingview",
  "alert_conditions": [
    "rug_pull_watch",
    "bear_confirmed", 
    "fakeout_filter"
  ]
}
```

## 🤖 Discord Integration

### Rich Embed Format

The system sends beautifully formatted Discord messages with:

- **Color-coded alerts** based on severity
- **Real-time price data** and technical indicators
- **Position tracking** with P&L updates
- **Risk management** status updates
- **System health** monitoring

### Alert Types

- 🚨 **Rug Pull Watch** - Orange warning
- 💀 **Bear Confirmed** - Red critical
- 🧩 **Fakeout Filter** - Yellow info
- ⚠️ **MACD Signal** - Orange warning
- 📈 **Volume Spike** - Blue info

## 🛡️ Risk Management

### Position Sizing

- **Dynamic sizing** based on volatility
- **Risk-adjusted** position limits
- **Daily trade limits** (max 5 trades)
- **Correlation limits** between positions

### Stop Loss Management

- **Dynamic stop loss** based on market conditions
- **Trailing stops** for profit protection
- **Volatility adjustment** for stop levels
- **Trend strength** consideration

### Target Zones

- **Multiple target levels** for profit taking
- **Risk/reward ratio** minimum 2:1
- **Partial profit taking** at each zone
- **Trailing stop** activation

## 📈 API Endpoints

### Webhook Endpoint
```
POST /webhook/tradingview
```
Receives TradingView webhook data and processes alerts.

### Status Endpoint
```
GET /status
```
Returns current system status and metrics.

### Positions Endpoint
```
GET /positions
```
Returns current active positions.

## 🔍 Monitoring & Logging

### Log Files
- `tsla_alerts.log` - System logs
- Alert history tracking
- Position performance metrics
- Error logging and debugging

### Metrics Tracked
- Alert delivery success rate
- Position P&L performance
- Risk management effectiveness
- System uptime and health

## ⚠️ Important Notes

### Trading Disclaimer
This system is for educational and informational purposes only. Trading involves substantial risk of loss and is not suitable for all investors.

### Risk Warnings
- **Never risk more than you can afford to lose**
- **Test thoroughly in paper trading first**
- **Monitor system performance regularly**
- **Have manual override capabilities**

### System Requirements
- Python 3.8+
- Stable internet connection
- Discord webhook access
- TradingView Pro account (for webhooks)

## 🚀 Advanced Features

### Signal Stack Confirmation
- **Multi-timeframe analysis** (30m, 15m, 5m)
- **VWAP alignment** confirmation
- **EMA cross** validation
- **Volume spike** detection
- **Correlation analysis** with QQQ

### Adaptive Risk Management
- **Volatility-based** position sizing
- **Market regime** detection
- **Dynamic stop loss** adjustment
- **Correlation limits** between positions

### Real-time Monitoring
- **Live position tracking**
- **P&L monitoring**
- **Risk metrics** dashboard
- **Alert performance** analytics

## 📞 Support

For issues or questions:
1. Check the logs in `tsla_alerts.log`
2. Verify webhook configuration
3. Test with paper trading first
4. Monitor system status via `/status` endpoint

## 🔄 Updates

### Version 1.3 Features
- ✅ Complete TradingView webhook integration
- ✅ Advanced signal stack confirmation
- ✅ Dynamic risk management system
- ✅ Rich Discord notifications
- ✅ Real-time position tracking
- ✅ Comprehensive logging and monitoring

---

**Ready for integration with Dream.OS/alert_bridge.py or TradingView webhook template!** 🎯