"""
Comprehensive Test Suite for Trading Robot
"""
import os
import sys
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtesting.backtester import Backtester, BacktestResult
from config.settings import config
from core.alpaca_client import AlpacaClient
from core.risk_manager import RiskManager
from strategies.base_strategy import MeanReversionStrategy, TrendFollowingStrategy


class TestAlpacaClient:
    """Test Alpaca API client"""

    @pytest.fixture
    def mock_api(self):
        """Mock Alpaca API"""
        with patch('core.alpaca_client.tradeapi') as mock_tradeapi:
            mock_api_instance = Mock()
            mock_tradeapi.REST.return_value = mock_api_instance
            mock_api_instance.get_account.return_value = {
                'cash': 100000,
                'portfolio_value': 100000,
                'buying_power': 200000
            }
            yield mock_api_instance

    def test_client_initialization(self, mock_api):
        """Test client initialization"""
        client = AlpacaClient()
        client.connect()

        assert client.is_connected()
        mock_api.get_account.assert_called_once()

    def test_get_account_info(self, mock_api):
        """Test getting account information"""
        client = AlpacaClient()
        client.connect()

        account_info = client.get_account_info()

        assert 'cash' in account_info
        assert 'portfolio_value' in account_info
        assert account_info['cash'] == 100000

    def test_get_positions(self, mock_api):
        """Test getting positions"""
        mock_api.list_positions.return_value = [
            Mock(symbol='AAPL', qty=100, avg_entry_price=150.0, current_price=155.0,
                 market_value=15500.0, unrealized_pl=500.0, unrealized_plpc=0.0333)
        ]

        client = AlpacaClient()
        client._connected = True
        client.api = mock_api

        positions = client.get_positions()

        assert len(positions) == 1
        assert positions[0]['symbol'] == 'AAPL'
        assert positions[0]['qty'] == 100


class TestRiskManager:
    """Test risk management system"""

    @pytest.fixture
    def risk_manager(self):
        """Create risk manager instance"""
        return RiskManager()

    def test_initialization(self, risk_manager):
        """Test risk manager initialization"""
        assert risk_manager.daily_pnl == 0.0
        assert risk_manager.daily_trades == 0
        assert risk_manager.portfolio_value == config.initial_balance

    def test_validate_trade_success(self, risk_manager):
        """Test successful trade validation"""
        is_valid, reason = risk_manager.validate_trade(
            symbol='AAPL',
            quantity=10,
            price=150.0,
            side='buy'
        )

        assert is_valid
        assert reason == "Trade approved"

    def test_validate_trade_daily_loss_limit(self, risk_manager):
        """Test trade rejection due to daily loss limit"""
        risk_manager.daily_pnl = -4000  # Below limit

        is_valid, reason = risk_manager.validate_trade(
            symbol='AAPL',
            quantity=10,
            price=150.0,
            side='buy'
        )

        assert not is_valid
        assert "Daily loss limit" in reason

    def test_calculate_position_size(self, risk_manager):
        """Test position size calculation"""
        position_size = risk_manager.calculate_position_size(100.0, 0.02)

        assert isinstance(position_size, int)
        assert position_size > 0

    def test_stop_loss_calculation(self, risk_manager):
        """Test stop loss price calculation"""
        stop_price = risk_manager.calculate_stop_loss_price(100.0, "buy", 0.02)

        assert stop_price == 98.0  # 2% below entry

    def test_take_profit_calculation(self, risk_manager):
        """Test take profit price calculation"""
        profit_price = risk_manager.calculate_take_profit_price(100.0, "buy", 0.04)

        assert profit_price == 104.0  # 4% above entry


class TestTradingStrategies:
    """Test trading strategies"""

    @pytest.fixture
    def sample_data(self):
        """Create sample market data"""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)

        # Generate realistic price data
        base_price = 100.0
        prices = []
        for i in range(100):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
            base_price *= (1 + change)
            prices.append(base_price)

        return pd.DataFrame({
            'open': prices,
            'high': [p * 1.01 for p in prices],  # High is 1% above close
            'low': [p * 0.99 for p in prices],   # Low is 1% below close
            'close': prices,
            'volume': np.random.randint(1000000, 5000000, 100)
        }, index=dates)

    def test_trend_following_strategy(self, sample_data):
        """Test trend following strategy"""
        strategy = TrendFollowingStrategy()

        # Test with valid data
        result = strategy.analyze(sample_data, "TEST")

        assert hasattr(result, 'signal')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'symbol')
        assert result.symbol == "TEST"

    def test_mean_reversion_strategy(self, sample_data):
        """Test mean reversion strategy"""
        strategy = MeanReversionStrategy()

        result = strategy.analyze(sample_data, "TEST")

        assert hasattr(result, 'signal')
        assert hasattr(result, 'confidence')
        assert result.symbol == "TEST"

    def test_data_validation(self, sample_data):
        """Test data validation in strategies"""
        strategy = TrendFollowingStrategy()

        # Test with insufficient data
        small_data = sample_data.head(10)
        result = strategy.analyze(small_data, "TEST")

        assert result.signal.name == "HOLD"


class TestBacktester:
    """Test backtesting system"""

    @pytest.fixture
    def sample_data(self):
        """Create sample market data for backtesting"""
        dates = pd.date_range(start='2023-01-01', periods=252, freq='D')  # 1 year
        np.random.seed(123)

        # Generate trending price data
        base_price = 100.0
        prices = []
        trend = 0.001  # Upward trend

        for i in range(252):
            change = np.random.normal(trend, 0.02)
            base_price *= (1 + change)
            prices.append(base_price)

        return pd.DataFrame({
            'open': prices,
            'high': [p * 1.01 for p in prices],
            'low': [p * 0.99 for p in prices],
            'close': prices,
            'volume': np.random.randint(1000000, 5000000, 252)
        }, index=dates)

    def test_backtest_initialization(self, sample_data):
        """Test backtester initialization"""
        backtester = Backtester(initial_balance=100000)

        assert backtester.current_balance == 100000
        assert backtester.positions == {}

    @pytest.mark.asyncio
    async def test_run_backtest(self, sample_data):
        """Test running a backtest"""
        strategy = TrendFollowingStrategy()
        backtester = Backtester(initial_balance=100000)

        result = backtester.run_backtest(strategy, sample_data, "TEST")

        assert isinstance(result, BacktestResult)
        assert hasattr(result, 'total_trades')
        assert hasattr(result, 'win_rate')
        assert hasattr(result, 'total_return')

    def test_calculate_metrics(self):
        """Test performance metrics calculation"""
        result = BacktestResult()

        # Mock some trades
        result.trades = [
            {'pnl': 1000, 'symbol': 'TEST'},
            {'pnl': -500, 'symbol': 'TEST'},
            {'pnl': 800, 'symbol': 'TEST'}
        ]

        result.calculate_metrics()

        assert result.total_trades == 3
        assert result.winning_trades == 2
        assert result.losing_trades == 1
        assert result.win_rate == 2/3


class TestIntegration:
    """Integration tests"""

    @pytest.mark.asyncio
    async def test_full_trading_workflow(self):
        """Test complete trading workflow"""
        # This would be a comprehensive integration test
        # For now, just ensure components can be imported and initialized

        from core.alpaca_client import AlpacaClient
        from core.risk_manager import RiskManager
        from strategies.base_strategy import TrendFollowingStrategy

        # Test component initialization
        client = AlpacaClient()
        risk_manager = RiskManager()
        strategy = TrendFollowingStrategy()

        assert client is not None
        assert risk_manager is not None
        assert strategy is not None


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")


# Test utilities
def create_mock_market_data(symbol: str, periods: int = 100) -> pd.DataFrame:
    """Create mock market data for testing"""
    dates = pd.date_range(start='2023-01-01', periods=periods, freq='D')
    np.random.seed(42)

    base_price = 100.0
    prices = []

    for i in range(periods):
        change = np.random.normal(0, 0.02)
        base_price *= (1 + change)
        prices.append(base_price)

    return pd.DataFrame({
        'open': prices,
        'high': [p * 1.01 for p in prices],
        'low': [p * 0.99 for p in prices],
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, periods)
    }, index=dates)


def run_all_tests():
    """Run all tests"""
    import subprocess
    import sys

    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--cov=.",
            "--cov-report=html"
        ], capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")

        return result.returncode == 0

    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Running Trading Robot Test Suite...")
    success = run_all_tests()

    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
