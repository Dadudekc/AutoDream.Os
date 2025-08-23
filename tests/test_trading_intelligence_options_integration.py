"""
Trading Intelligence & Options Trading Integration Tests
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Tests the integration of trading intelligence, options trading, and financial analytics services.
"""

import pytest
import json
import tempfile
import shutil
import uuid
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import business intelligence services
from src.services.financial import (
    TradingIntelligenceService,
    OptionsTradingService,
    StrategyType,
    SignalType,
    SignalStrength,
    OptionType,
    OptionStrategy,
    Greeks,
)
from src.services.financial.analytics import (
    FinancialAnalyticsService,
)


class TestTradingIntelligenceOptionsIntegration:
    """Test suite for trading intelligence and options trading system integration"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        # Create temporary directories in organized structure
        self.temp_dir = Path("data/test_outputs") / f"test_{uuid.uuid4().hex[:8]}"
        self.trading_dir = self.temp_dir / "trading_intelligence"
        self.options_dir = self.temp_dir / "options_trading"
        self.analytics_dir = self.temp_dir / "financial_analytics"

        # Create directories
        self.trading_dir.mkdir(exist_ok=True)
        self.options_dir.mkdir(exist_ok=True)
        self.analytics_dir.mkdir(exist_ok=True)

        yield

        # Cleanup
        shutil.rmtree(self.temp_dir)

    def test_trading_intelligence_service_initialization(self):
        """Test trading intelligence service initialization"""
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))

        assert tis.data_dir == self.trading_dir
        assert len(tis.strategies) > 0
        assert len(tis.performance_metrics) > 0
        assert len(tis.active_signals) == 0

    def test_options_trading_service_initialization(self):
        """Test options trading service initialization"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        assert ots.data_dir == self.options_dir
        assert len(ots.options_chains) == 0
        assert len(ots.active_strategies) == 0
        assert len(ots.strategy_performance) == 0

    def test_financial_analytics_service_initialization(self):
        """Test financial analytics service initialization"""
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        assert fas.data_dir == self.analytics_dir
        assert len(fas.backtest_results) == 0
        assert len(fas.performance_metrics) == 0
        assert len(fas.risk_analyses) == 0

    def test_trading_strategies_initialization(self):
        """Test trading strategies initialization"""
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))

        # Check that all strategy types are initialized
        expected_strategies = [
            StrategyType.MOMENTUM,
            StrategyType.MEAN_REVERSION,
            StrategyType.BREAKOUT,
            StrategyType.SCALPING,
            StrategyType.PAIRS_TRADING,
            StrategyType.GRID_TRADING,
        ]

        for strategy_type in expected_strategies:
            assert strategy_type in tis.strategies
            assert callable(tis.strategies[strategy_type])

    def test_momentum_strategy(self):
        """Test momentum trading strategy"""
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))

        # Create test data
        test_data = pd.DataFrame(
            {
                "Close": [
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                ],
                "Volume": [1000000] * 21,
                "High": [
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                    121,
                ],
                "Low": [
                    99,
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                ],
            }
        )

        # Test momentum strategy
        signal = tis.momentum_strategy("TEST", test_data)

        # Should generate a signal due to strong momentum
        assert signal is not None
        assert signal.symbol == "TEST"
        assert signal.strategy == StrategyType.MOMENTUM
        assert signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY]
        assert signal.confidence > 0

    def test_mean_reversion_strategy(self):
        """Test mean reversion trading strategy"""
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))

        # Create test data with extreme values
        test_data = pd.DataFrame(
            {
                "Close": [
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                    121,
                    122,
                    123,
                    124,
                    125,
                    126,
                    127,
                    128,
                    129,
                    130,
                    131,
                    132,
                    133,
                    134,
                    135,
                    136,
                    137,
                    138,
                    139,
                    140,
                    141,
                    142,
                    143,
                    144,
                    145,
                    146,
                    147,
                    148,
                    149,
                    150,
                    151,
                    152,
                    153,
                    154,
                    155,
                    156,
                    157,
                    158,
                    159,
                    160,
                ]
            }
        )

        # Test mean reversion strategy
        signal = tis.mean_reversion_strategy("TEST", test_data)

        # Should generate a signal due to extreme values
        assert signal is not None
        assert signal.symbol == "TEST"
        assert signal.strategy == StrategyType.MEAN_REVERSION
        assert signal.signal_type in [SignalType.SELL, SignalType.STRONG_SELL]
        assert signal.confidence > 0

    def test_black_scholes_calculation(self):
        """Test Black-Scholes option pricing"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Test parameters
        S = 100.0  # Current stock price
        K = 100.0  # Strike price
        T = 0.25  # Time to expiration (3 months)
        r = 0.02  # Risk-free rate
        sigma = 0.3  # Volatility

        # Calculate call option
        call_result = ots.calculate_black_scholes(S, K, T, r, sigma, OptionType.CALL)

        assert "price" in call_result
        assert "delta" in call_result
        assert "gamma" in call_result
        assert "theta" in call_result
        assert "vega" in call_result
        assert "rho" in call_result

        # Validate results
        assert call_result["price"] > 0
        assert 0 < call_result["delta"] < 1
        assert call_result["gamma"] > 0
        assert call_result["theta"] < 0  # Time decay
        assert call_result["vega"] > 0

        # Calculate put option
        put_result = ots.calculate_black_scholes(S, K, T, r, sigma, OptionType.PUT)

        assert "price" in put_result
        assert put_result["price"] > 0
        assert -1 < put_result["delta"] < 0  # Put delta is negative

    def test_implied_volatility_calculation(self):
        """Test implied volatility calculation"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Test parameters
        S = 100.0  # Current stock price
        K = 100.0  # Strike price
        T = 0.25  # Time to expiration
        r = 0.02  # Risk-free rate
        market_price = 5.0  # Market price of option

        # Calculate implied volatility
        iv = ots.calculate_implied_volatility(market_price, S, K, T, r, OptionType.CALL)

        assert iv > 0
        assert iv < 5.0  # Reasonable bounds

    def test_long_call_strategy_creation(self):
        """Test long call strategy creation"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Create strategy parameters
        symbol = "AAPL"
        strike = 150.0
        expiration = datetime.now() + timedelta(days=30)
        underlying_price = 155.0
        option_price = 8.0

        # Create strategy
        strategy = ots.create_long_call_strategy(
            symbol, strike, expiration, underlying_price, option_price
        )

        assert strategy is not None
        assert strategy.strategy_type == OptionStrategy.LONG_CALL
        assert strategy.symbol == symbol
        assert len(strategy.contracts) == 1
        assert strategy.max_loss == option_price
        assert strategy.max_profit == float("inf")
        assert len(strategy.break_even_points) == 1
        assert strategy.probability_profit > 0
        assert strategy.risk_reward_ratio > 0

    def test_covered_call_strategy_creation(self):
        """Test covered call strategy creation"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Create strategy parameters
        symbol = "AAPL"
        strike = 160.0
        expiration = datetime.now() + timedelta(days=30)
        underlying_price = 155.0
        option_price = 3.0
        shares_owned = 100

        # Create strategy
        strategy = ots.create_covered_call_strategy(
            symbol, strike, expiration, underlying_price, option_price, shares_owned
        )

        assert strategy is not None
        assert strategy.strategy_type == OptionStrategy.COVERED_CALL
        assert strategy.symbol == symbol
        assert len(strategy.contracts) == 1
        assert strategy.max_profit > 0
        assert strategy.max_loss < 0
        assert len(strategy.break_even_points) == 1
        assert strategy.probability_profit > 0

    def test_iron_condor_strategy_creation(self):
        """Test iron condor strategy creation"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Create strategy parameters
        symbol = "AAPL"
        short_call_strike = 160.0
        long_call_strike = 165.0
        short_put_strike = 150.0
        long_put_strike = 145.0
        expiration = datetime.now() + timedelta(days=30)
        underlying_price = 155.0
        net_premium = 0.02

        # Create strategy
        strategy = ots.create_iron_condor_strategy(
            symbol,
            short_call_strike,
            long_call_strike,
            short_put_strike,
            long_put_strike,
            expiration,
            underlying_price,
            net_premium,
        )

        assert strategy is not None
        assert strategy.strategy_type == OptionStrategy.IRON_CONDOR
        assert strategy.symbol == symbol
        assert len(strategy.contracts) == 4  # 4 option contracts
        assert strategy.max_profit == net_premium
        assert strategy.max_loss < 0
        assert len(strategy.break_even_points) == 2
        assert strategy.probability_profit > 0

    def test_options_opportunity_scanning(self):
        """Test options opportunity scanning"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Create mock options chain
        mock_chain = {
            "symbol": "AAPL",
            "underlying_price": 155.0,
            "expiration_dates": [datetime.now() + timedelta(days=30)],
            "call_options": {},
            "put_options": {},
        }

        # Add mock options
        expiration = datetime.now() + timedelta(days=30)

        # ATM call option
        atm_call = {
            "symbol": "AAPL",
            "strike": 155.0,
            "expiration": expiration,
            "option_type": OptionType.CALL,
            "last_price": 8.0,
            "bid": 7.8,
            "ask": 8.2,
            "volume": 1000,
            "open_interest": 5000,
            "implied_volatility": 0.25,
            "delta": 0.6,
            "gamma": 0.02,
            "theta": -0.05,
            "vega": 0.1,
            "rho": 0.01,
            "underlying_price": 155.0,
        }

        # ATM put option
        atm_put = {
            "symbol": "AAPL",
            "strike": 155.0,
            "expiration": expiration,
            "option_type": OptionType.PUT,
            "last_price": 7.5,
            "bid": 7.3,
            "ask": 7.7,
            "volume": 1000,
            "open_interest": 5000,
            "implied_volatility": 0.28,
            "delta": -0.4,
            "gamma": 0.02,
            "theta": -0.04,
            "vega": 0.1,
            "rho": -0.01,
            "underlying_price": 155.0,
        }

        # Create options chain
        chain = ots.options_chains["AAPL"] = type(
            "OptionsChain",
            (),
            {
                "symbol": "AAPL",
                "underlying_price": 155.0,
                "expiration_dates": [expiration],
                "call_options": {155.0: type("OptionContract", (), atm_call)()},
                "put_options": {155.0: type("OptionContract", (), atm_put)()},
                "get_atm_options": lambda exp=None: (
                    type("OptionContract", (), atm_call)(),
                    type("OptionContract", (), atm_put)(),
                ),
                "get_implied_volatility_smile": lambda exp=None: {
                    "strikes": [155.0],
                    "call_ivs": [0.25],
                    "put_ivs": [0.28],
                },
            },
        )()

        # Test opportunity scanning
        opportunities = ots.scan_for_opportunities(["AAPL"])

        # Should find opportunities
        assert len(opportunities) > 0
        assert opportunities[0]["symbol"] == "AAPL"
        assert "recommendations" in opportunities[0]

    def test_financial_metrics_calculation(self):
        """Test financial metrics calculation"""
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Create test returns
        test_returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.015] * 50)

        # Calculate basic metrics
        sharpe = fas.calculate_sharpe_ratio(test_returns)
        sortino = fas.calculate_sortino_ratio(test_returns)
        var_95 = fas.calculate_value_at_risk(test_returns)
        conditional_var = fas.calculate_conditional_var(test_returns)

        assert sharpe > 0
        assert sortino > 0
        assert var_95 > 0
        assert conditional_var > 0

        # Test comprehensive metrics
        metrics = fas.calculate_comprehensive_metrics(test_returns)

        assert metrics is not None
        assert hasattr(metrics, "returns")
        assert hasattr(metrics, "cumulative_returns")
        assert hasattr(metrics, "drawdown")
        assert hasattr(metrics, "sharpe_ratio")
        assert hasattr(metrics, "sortino_ratio")
        assert hasattr(metrics, "value_at_risk")
        assert hasattr(metrics, "conditional_var")

    def test_backtesting_functionality(self):
        """Test backtesting functionality"""
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Create test data
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        prices = pd.Series([100 + i * 0.1 for i in range(len(dates))], index=dates)

        # Create simple signals
        signals = pd.DataFrame(
            {"signal": ["BUY"] * 100 + ["SELL"] * 100 + ["HOLD"] * (len(dates) - 200)},
            index=dates,
        )

        # Run backtest
        result = fas.run_backtest(
            "Test Strategy", signals, prices, initial_capital=10000
        )

        assert result is not None
        assert result.strategy_name == "Test Strategy"
        assert result.total_trades > 0
        assert result.total_return != 0
        assert result.sharpe_ratio != 0
        assert result.max_drawdown <= 0
        assert result.win_rate >= 0
        assert result.profit_factor > 0

    def test_risk_analysis(self):
        """Test risk analysis functionality"""
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Create test returns
        test_returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.015] * 100)

        # Perform risk analysis
        risk_analysis = fas.perform_risk_analysis(test_returns)

        assert risk_analysis is not None
        assert "volatility_analysis" in risk_analysis.__dict__
        assert "drawdown_analysis" in risk_analysis.__dict__
        assert "var_analysis" in risk_analysis.__dict__
        assert "correlation_analysis" in risk_analysis.__dict__
        assert "stress_test_results" in risk_analysis.__dict__
        assert "scenario_analysis" in risk_analysis.__dict__
        assert "risk_decomposition" in risk_analysis.__dict__

    def test_performance_report_generation(self):
        """Test performance report generation"""
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Create test data and run backtest first
        dates = pd.date_range(start="2023-01-01", end="2023-06-30", freq="D")
        prices = pd.Series([100 + i * 0.05 for i in range(len(dates))], index=dates)

        signals = pd.DataFrame(
            {"signal": ["BUY"] * 50 + ["SELL"] * 50 + ["HOLD"] * (len(dates) - 100)},
            index=dates,
        )

        result = fas.run_backtest(
            "Report Test Strategy", signals, prices, initial_capital=10000
        )

        # Generate performance report
        report = fas.generate_performance_report("Report Test Strategy")

        assert "error" not in report
        assert "summary" in report
        assert "risk_metrics" in report
        assert "trade_analysis" in report
        assert "recommendations" in report

        # Verify summary data
        summary = report["summary"]
        assert "total_return" in summary
        assert "annualized_return" in summary
        assert "sharpe_ratio" in summary
        assert "max_drawdown" in summary
        assert "win_rate" in summary
        assert "profit_factor" in summary

    def test_trading_intelligence_integration(self):
        """Test trading intelligence service integration"""
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))

        # Test market conditions analysis
        symbols = ["AAPL", "MSFT", "GOOGL"]

        # Mock market data service
        class MockMarketDataService:
            def get_real_time_data(self, symbols):
                return {
                    "AAPL": type(
                        "MarketData", (), {"change_pct": 0.02, "volume": 1000000}
                    )(),
                    "MSFT": type(
                        "MarketData", (), {"change_pct": 0.015, "volume": 800000}
                    )(),
                    "GOOGL": type(
                        "MarketData", (), {"change_pct": 0.025, "volume": 1200000}
                    )(),
                }

        tis.market_data_service = MockMarketDataService()

        # Analyze market conditions
        market_conditions = tis.analyze_market_conditions(symbols)

        assert market_conditions is not None
        assert hasattr(market_conditions, "volatility_regime")
        assert hasattr(market_conditions, "trend_direction")
        assert hasattr(market_conditions, "market_sentiment")
        assert hasattr(market_conditions, "liquidity_condition")

    def test_options_trading_integration(self):
        """Test options trading service integration"""
        ots = OptionsTradingService(data_dir=str(self.options_dir))

        # Test strategy execution
        symbol = "AAPL"
        strike = 150.0
        expiration = datetime.now() + timedelta(days=30)
        underlying_price = 155.0
        option_price = 8.0

        # Create strategy
        strategy = ots.create_long_call_strategy(
            symbol, strike, expiration, underlying_price, option_price
        )

        # Execute strategy
        success = ots.execute_strategy(strategy)

        assert success is True
        assert len(ots.active_strategies) == 1
        assert ots.active_strategies[0].strategy_type == OptionStrategy.LONG_CALL

        # Test strategy monitoring
        updates = ots.monitor_strategies()

        # Should have monitoring updates
        assert isinstance(updates, list)

    def test_financial_analytics_integration(self):
        """Test financial analytics service integration"""
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Test data persistence
        test_returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.015] * 50)

        # Calculate metrics
        metrics = fas.calculate_comprehensive_metrics(test_returns)
        risk_analysis = fas.perform_risk_analysis(test_returns)

        # Store in service
        fas.performance_metrics["test_strategy"] = metrics
        fas.risk_analyses["test_strategy"] = risk_analysis

        # Save data
        fas.save_data()

        # Verify files were created
        assert fas.results_file.exists()
        assert fas.metrics_file.exists()
        assert fas.risk_file.exists()

    def test_complete_workflow_integration(self):
        """Test complete workflow integration"""
        # Initialize all services
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))
        ots = OptionsTradingService(data_dir=str(self.options_dir))
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Create test data
        test_data = pd.DataFrame(
            {
                "Close": [
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                ],
                "Volume": [1000000] * 21,
                "High": [
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                    121,
                ],
                "Low": [
                    99,
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                ],
            }
        )

        # 1. Generate trading signals
        momentum_signal = tis.momentum_strategy("AAPL", test_data)
        assert momentum_signal is not None

        # 2. Create options strategy
        if momentum_signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
            options_strategy = ots.create_long_call_strategy(
                "AAPL", 150, datetime.now() + timedelta(days=30), 155, 8.0
            )
            assert options_strategy is not None

            # 3. Execute strategy
            success = ots.execute_strategy(options_strategy)
            assert success is True

            # 4. Create backtest data
            dates = pd.date_range(start="2023-01-01", end="2023-06-30", freq="D")
            prices = pd.Series([155 + i * 0.1 for i in range(len(dates))], index=dates)

            signals = pd.DataFrame(
                {
                    "signal": ["BUY"] * 50
                    + ["SELL"] * 50
                    + ["HOLD"] * (len(dates) - 100)
                },
                index=dates,
            )

            # 5. Run backtest
            backtest_result = fas.run_backtest("Integration Test", signals, prices)
            assert backtest_result is not None

            # 6. Generate performance report
            report = fas.generate_performance_report("Integration Test")
            assert "error" not in report

            # 7. Verify integration
            assert len(ots.active_strategies) > 0
            assert len(fas.backtest_results) > 0
            assert len(tis.active_signals) == 0  # No signals added yet

    def test_error_handling(self):
        """Test error handling in integrated services"""
        # Test with invalid data
        tis = TradingIntelligenceService(data_dir=str(self.trading_dir))
        ots = OptionsTradingService(data_dir=str(self.options_dir))
        fas = FinancialAnalyticsService(data_dir=str(self.analytics_dir))

        # Test trading intelligence with empty data
        empty_data = pd.DataFrame()
        signal = tis.momentum_strategy("TEST", empty_data)
        assert signal is None

        # Test options trading with invalid parameters
        invalid_strategy = ots.create_long_call_strategy(
            "", -100, datetime.now(), -155, -8.0
        )
        assert invalid_strategy is None

        # Test financial analytics with empty returns
        empty_returns = pd.Series()
        metrics = fas.calculate_comprehensive_metrics(empty_returns)
        assert metrics is None

        # Test backtesting with invalid data
        invalid_signals = pd.DataFrame()
        invalid_prices = pd.Series()
        result = fas.run_backtest("Invalid", invalid_signals, invalid_prices)
        assert result is None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
