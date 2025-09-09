# 🐝 Alpaca Trading Robot

A comprehensive algorithmic trading robot built with Python, FastAPI, and the Alpaca trading API. Features advanced risk management, multiple trading strategies, real-time monitoring, and production-ready deployment.

## 🚀 Features

### Core Trading Features
- **Real-time Trading**: Execute trades based on live market data
- **Multiple Strategies**: Trend following, mean reversion, and custom strategies
- **Risk Management**: Comprehensive position sizing, stop losses, and portfolio protection
- **Backtesting**: Historical performance analysis and strategy validation
- **Paper Trading**: Safe strategy testing before live deployment

### Technical Features
- **Alpaca Integration**: Full Alpaca API support for stocks and options
- **Web Dashboard**: Real-time monitoring and control interface
- **Technical Indicators**: 20+ indicators (RSI, MACD, Bollinger Bands, etc.)
- **Position Management**: Automated position sizing and rebalancing
- **Order Types**: Market, limit, stop-loss, and trailing stop orders

### Risk & Safety Features
- **Emergency Stops**: Automatic shutdown on excessive losses
- **Daily Loss Limits**: Prevent catastrophic daily losses
- **Position Limits**: Maximum position sizes and portfolio exposure
- **Circuit Breakers**: Emergency shutdown procedures
- **Trade Frequency Limits**: Prevent over-trading

### Monitoring & Analytics
- **Real-time Dashboard**: Live portfolio and position monitoring
- **Performance Analytics**: Detailed trade analysis and statistics
- **Risk Metrics**: Exposure, concentration, and drawdown tracking
- **Trade Logging**: Comprehensive audit trail
- **Alert System**: Email and system notifications

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Alpaca account (Paper trading recommended for testing)
- PostgreSQL (optional, SQLite for development)

### Quick Start

1. **Clone and setup**:
```bash
git clone <repository-url>
cd trading_robot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your Alpaca API credentials
```

4. **Run the trading robot**:
```bash
python main.py
```

5. **Access dashboard**:
Open http://localhost:8000 in your browser

## 📊 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALPACA_API_KEY` | Your Alpaca API key | Required |
| `ALPACA_SECRET_KEY` | Your Alpaca secret key | Required |
| `ALPACA_BASE_URL` | Alpaca API URL | `https://paper-api.alpaca.markets` |
| `WEB_PORT` | Dashboard port | `8000` |
| `MAX_POSITIONS` | Maximum concurrent positions | `10` |
| `DAILY_LOSS_LIMIT_PCT` | Daily loss limit | `0.03` |

### Trading Configuration

```python
# Example strategy configuration
strategy_config = {
    'fast_period': 10,
    'slow_period': 20,
    'rsi_period': 14,
    'stop_loss_pct': 0.02,
    'take_profit_pct': 0.04
}
```

## 🎯 Trading Strategies

### Built-in Strategies

1. **Trend Following**
   - Uses moving averages and RSI
   - Identifies and follows market trends
   - Configurable fast/slow periods

2. **Mean Reversion**
   - Uses RSI and Bollinger Bands
   - Trades against extreme price movements
   - Automatic entry/exit signals

3. **Custom Strategies**
   - Framework for building custom strategies
   - Access to 20+ technical indicators
   - Flexible signal generation

### Strategy Example

```python
from strategies.base_strategy import TrendFollowingStrategy

# Initialize strategy
strategy = TrendFollowingStrategy({
    'fast_period': 10,
    'slow_period': 20,
    'rsi_period': 14
})

# Analyze market data
result = strategy.analyze(market_data, "AAPL")
print(f"Signal: {result.signal}, Confidence: {result.confidence}")
```

## 📈 Backtesting

### Running Backtests

```python
from backtesting.backtester import Backtester
from strategies.base_strategy import TrendFollowingStrategy

# Initialize backtester
backtester = Backtester(initial_balance=100000)
strategy = TrendFollowingStrategy()

# Run backtest
result = backtester.run_backtest(strategy, historical_data, "AAPL")

# View results
result.print_summary()
```

### Performance Metrics

- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / gross loss
- **Max Drawdown**: Largest peak-to-valley decline
- **Sharpe Ratio**: Risk-adjusted returns
- **Total Return**: Overall portfolio performance

## 🚀 Production Deployment

### Docker Deployment

1. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

2. **Access services**:
- Trading Dashboard: http://localhost:8000
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

### Manual Production Setup

1. **Database setup**:
```bash
createdb trading_robot
```

2. **Environment configuration**:
```bash
export ALPACA_API_KEY="your_key"
export ALPACA_SECRET_KEY="your_secret"
export DATABASE_URL="postgresql://user:pass@localhost/trading_robot"
```

3. **Start services**:
```bash
python main.py
```

## 📊 API Endpoints

### Trading Endpoints

- `GET /api/status` - Get system status
- `GET /api/portfolio` - Get portfolio information
- `GET /api/market_data/{symbol}` - Get market data
- `POST /api/trade/{symbol}/{side}` - Execute trade
- `GET /api/stop_trading` - Emergency stop

### WebSocket

- `ws://localhost:8000/ws/updates` - Real-time updates

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_trading_robot.py::TestRiskManager::test_validate_trade
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Backtesting Tests**: Strategy performance validation
- **Risk Management Tests**: Safety mechanism validation

## 📋 Risk Management

### Safety Features

1. **Position Limits**
   - Maximum position size per trade
   - Maximum portfolio exposure
   - Concentration limits

2. **Loss Protection**
   - Daily loss limits
   - Emergency stop losses
   - Circuit breaker system

3. **Trade Controls**
   - Minimum/maximum order values
   - Maximum daily trade frequency
   - Trading hour restrictions

### Emergency Procedures

```python
# Emergency stop
from core.risk_manager import RiskManager

risk_manager = RiskManager()
risk_manager._trigger_emergency_stop("Manual emergency stop")
```

## 📊 Monitoring & Alerts

### Dashboard Features

- **Real-time Portfolio**: Live P&L and positions
- **Risk Metrics**: Exposure and concentration tracking
- **Trade History**: Complete audit trail
- **Performance Charts**: Visual analytics
- **System Health**: Component status monitoring

### Alert System

- **Email Alerts**: Trade notifications and warnings
- **System Alerts**: Risk limit breaches
- **Emergency Alerts**: Critical system events

## 🔧 Development

### Project Structure

```
trading_robot/
├── core/                 # Core trading components
│   ├── alpaca_client.py  # Alpaca API wrapper
│   ├── trading_engine.py # Main trading engine
│   └── risk_manager.py   # Risk management system
├── strategies/           # Trading strategies
│   ├── base_strategy.py  # Strategy framework
│   └── indicators.py     # Technical indicators
├── backtesting/          # Backtesting system
│   └── backtester.py     # Backtesting engine
├── execution/            # Live execution
│   └── live_executor.py  # Live trading executor
├── web/                  # Web dashboard
│   └── dashboard.py      # FastAPI dashboard
├── tests/                # Test suite
├── config/               # Configuration
├── data/                 # Data storage
├── logs/                 # Log files
└── docs/                 # Documentation
```

### Adding New Strategies

1. **Create strategy class**:
```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def analyze(self, data, symbol):
        # Your strategy logic here
        return StrategyResult(symbol, signal, confidence)
```

2. **Register strategy**:
```python
from strategies.base_strategy import StrategyManager

manager = StrategyManager()
manager.add_strategy(MyStrategy())
```

## 📈 Performance Optimization

### Best Practices

1. **Strategy Selection**: Backtest thoroughly before live trading
2. **Risk Management**: Never risk more than 1-2% per trade
3. **Position Sizing**: Use proper position sizing algorithms
4. **Diversification**: Spread risk across multiple symbols
5. **Monitoring**: Regular performance review and adjustment

### Performance Metrics

- **Sharpe Ratio**: > 1.5 considered good
- **Win Rate**: > 55% typically profitable
- **Profit Factor**: > 1.5 indicates good risk-reward
- **Max Drawdown**: < 20% preferable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This trading robot is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always test strategies thoroughly and use proper risk management.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: Wiki
- **Community**: GitHub Discussions

---

**🐝 Built with swarm intelligence and precision trading algorithms**
