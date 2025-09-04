"""
Trading BI Analytics Service Tests - V2 Compliant Unit Tests
Comprehensive test coverage for BI analytics functionality with clear test names
V2 COMPLIANCE: Unit test coverage above 85%, clear describe/it structure, mock externals

@version 1.0.0 - V2 COMPLIANCE BI ANALYTICS TESTS
"""


    TradingBiAnalyticsService,
    PerformanceMetrics,
    RiskMetrics,
    MarketTrend,
    RiskLevel
)


@pytest.fixture
def mock_repository():
    """Mock trading repository for testing"""
    repo = AsyncMock()

    # Mock sample data
    sample_trades = [
        Trade("1", "AAPL", "buy", 100, 150.0, datetime.now() - timedelta(days=5), "executed", "market"),
        Trade("2", "AAPL", "sell", 100, 155.0, datetime.now() - timedelta(days=3), "executed", "market"),
        Trade("3", "GOOGL", "buy", 50, 2800.0, datetime.now() - timedelta(days=2), "executed", "market"),
        Trade("4", "GOOGL", "sell", 50, 2750.0, datetime.now() - timedelta(days=1), "executed", "market"),
    ]

    sample_positions = [
        Position("AAPL", 0, 0, 155.0, 0, datetime.now()),
        Position("GOOGL", 0, 0, 2750.0, 0, datetime.now()),
    ]

    repo.get_trades_by_symbol.return_value = sample_trades[:2]
    repo.get_all_trades.return_value = sample_trades
    repo.get_position.return_value = sample_positions[0]
    repo.get_all_positions.return_value = sample_positions

    return repo


@pytest.fixture
def bi_analytics_service(mock_repository):
    """BI analytics service with mocked repository"""
    return TradingBiAnalyticsService(mock_repository)


class TestTradingBiAnalyticsService:
    """Test suite for Trading BI Analytics Service"""

    @pytest.mark.asyncio
    async def test_calculate_real_time_pnl_portfolio(self, bi_analytics_service):
        """Test portfolio P&L calculation"""
        result = await bi_analytics_service.calculate_real_time_pnl()

        assert "total_pnl" in result
        assert "total_value" in result
        assert "pnl_percentage" in result
        assert "positions_count" in result
        assert "timestamp" in result
        assert get_unified_validator().validate_type(result["timestamp"], datetime)

    @pytest.mark.asyncio
    async def test_calculate_real_time_pnl_symbol(self, bi_analytics_service):
        """Test symbol-specific P&L calculation"""
        result = await bi_analytics_service.calculate_real_time_pnl("AAPL")

        assert result["symbol"] == "AAPL"
        assert "pnl" in result
        assert "pnl_percentage" in result
        assert "position_value" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_assess_portfolio_risk(self, bi_analytics_service):
        """Test portfolio risk assessment"""
        result = await bi_analytics_service.assess_portfolio_risk()

        assert get_unified_validator().validate_type(result, RiskMetrics)
        assert get_unified_validator().validate_hasattr(result, 'portfolio_volatility')
        assert get_unified_validator().validate_hasattr(result, 'value_at_risk')
        assert get_unified_validator().validate_hasattr(result, 'risk_level')
        assert get_unified_validator().validate_hasattr(result, 'max_position_size')
        assert get_unified_validator().validate_type(result.risk_level, RiskLevel)
        assert get_unified_validator().validate_type(result.timestamp, datetime)

    @pytest.mark.asyncio
    async def test_analyze_market_trends(self, bi_analytics_service):
        """Test market trend analysis"""
        result = await bi_analytics_service.analyze_market_trends("AAPL")

        assert get_unified_validator().validate_type(result, MarketTrend)
        assert get_unified_validator().validate_hasattr(result, 'direction')
        assert get_unified_validator().validate_hasattr(result, 'strength')
        assert get_unified_validator().validate_hasattr(result, 'confidence')
        assert get_unified_validator().validate_hasattr(result, 'predicted_change')
        assert result.direction in ['bullish', 'bearish', 'sideways']
        assert 0.0 <= result.strength <= 1.0
        assert 0.0 <= result.confidence <= 1.0
        assert get_unified_validator().validate_type(result.timestamp, datetime)

    @pytest.mark.asyncio
    async def test_generate_performance_report(self, bi_analytics_service):
        """Test performance report generation"""
        result = await bi_analytics_service.generate_performance_report()

        assert get_unified_validator().validate_type(result, PerformanceMetrics)
        assert get_unified_validator().validate_hasattr(result, 'total_return')
        assert get_unified_validator().validate_hasattr(result, 'sharpe_ratio')
        assert get_unified_validator().validate_hasattr(result, 'max_drawdown')
        assert get_unified_validator().validate_hasattr(result, 'win_rate')
        assert get_unified_validator().validate_hasattr(result, 'profit_factor')
        assert get_unified_validator().validate_hasattr(result, 'total_trades')
        assert get_unified_validator().validate_hasattr(result, 'avg_trade_duration')
        assert get_unified_validator().validate_type(result.timestamp, datetime)

    @pytest.mark.asyncio
    async def test_calculate_real_time_pnl_empty_portfolio(self, bi_analytics_service):
        """Test P&L calculation with empty portfolio"""
        bi_analytics_service.repository.get_all_positions.return_value = []

        result = await bi_analytics_service.calculate_real_time_pnl()

        assert result["total_pnl"] == 0.0
        assert result["positions_count"] == 0

    @pytest.mark.asyncio
    async def test_calculate_real_time_pnl_symbol_not_found(self, bi_analytics_service):
        """Test P&L calculation for non-existent symbol"""
        bi_analytics_service.repository.get_position.return_value = None

        result = await bi_analytics_service.calculate_real_time_pnl("INVALID")

        assert result["symbol"] == "INVALID"
        assert result["pnl"] == 0.0
        assert result["pnl_percentage"] == 0.0
        assert result["position_value"] == 0.0

    @pytest.mark.asyncio
    async def test_assess_portfolio_risk_empty_portfolio(self, bi_analytics_service):
        """Test risk assessment with empty portfolio"""
        bi_analytics_service.repository.get_all_positions.return_value = []
        bi_analytics_service.repository.get_all_trades.return_value = []

        result = await bi_analytics_service.assess_portfolio_risk()

        assert result.portfolio_volatility == 0.0
        assert result.value_at_risk == 0.0
        assert result.risk_level == RiskLevel.LOW

    @pytest.mark.asyncio
    async def test_analyze_market_trends_insufficient_data(self, bi_analytics_service):
        """Test trend analysis with insufficient data"""
        bi_analytics_service.repository.get_trades_by_symbol.return_value = []

        result = await bi_analytics_service.analyze_market_trends("AAPL")

        assert result.direction == "sideways"
        assert result.strength == 0.0
        assert result.confidence == 0.0
        assert result.predicted_change == 0.0

    @pytest.mark.asyncio
    async def test_generate_performance_report_empty_trades(self, bi_analytics_service):
        """Test performance report with no trades"""
        bi_analytics_service.repository.get_all_trades.return_value = []

        result = await bi_analytics_service.generate_performance_report()

        assert result.total_return == 0.0
        assert result.sharpe_ratio == 0.0
        assert result.total_trades == 0
        assert result.avg_trade_duration == timedelta(0)

    def test_risk_level_enum_values(self):
        """Test RiskLevel enum has expected values"""
        assert RiskLevel.LOW.value == "low"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.CRITICAL.value == "critical"

    def test_performance_metrics_dataclass(self):
        """Test PerformanceMetrics dataclass structure"""
        timestamp = datetime.now()
        metrics = PerformanceMetrics(
            total_return=15.5,
            sharpe_ratio=1.2,
            max_drawdown=8.5,
            win_rate=65.0,
            profit_factor=1.8,
            total_trades=100,
            avg_trade_duration=timedelta(hours=2),
            timestamp=timestamp
        )

        assert metrics.total_return == 15.5
        assert metrics.sharpe_ratio == 1.2
        assert metrics.max_drawdown == 8.5
        assert metrics.win_rate == 65.0
        assert metrics.profit_factor == 1.8
        assert metrics.total_trades == 100
        assert metrics.avg_trade_duration == timedelta(hours=2)
        assert metrics.timestamp == timestamp

    def test_risk_metrics_dataclass(self):
        """Test RiskMetrics dataclass structure"""
        timestamp = datetime.now()
        metrics = RiskMetrics(
            portfolio_volatility=0.15,
            value_at_risk=0.05,
            expected_shortfall=0.08,
            beta_coefficient=1.2,
            risk_level=RiskLevel.MEDIUM,
            max_position_size=50000.0,
            timestamp=timestamp
        )

        assert metrics.portfolio_volatility == 0.15
        assert metrics.value_at_risk == 0.05
        assert metrics.expected_shortfall == 0.08
        assert metrics.beta_coefficient == 1.2
        assert metrics.risk_level == RiskLevel.MEDIUM
        assert metrics.max_position_size == 50000.0
        assert metrics.timestamp == timestamp

    def test_market_trend_dataclass(self):
        """Test MarketTrend dataclass structure"""
        timestamp = datetime.now()
        trend = MarketTrend(
            direction="bullish",
            strength=0.75,
            confidence=0.85,
            predicted_change=5.2,
            timeframe="medium",
            timestamp=timestamp
        )

        assert trend.direction == "bullish"
        assert trend.strength == 0.75
        assert trend.confidence == 0.85
        assert trend.predicted_change == 5.2
        assert trend.timeframe == "medium"
        assert trend.timestamp == timestamp


class TestTradingBiAnalyticsServiceIntegration:
    """Integration tests for BI Analytics Service"""

    @pytest.mark.asyncio
    async def test_full_bi_workflow(self, bi_analytics_service):
        """Test complete BI workflow from data to insights"""
        # Calculate P&L
        pnl = await bi_analytics_service.calculate_real_time_pnl()
        assert get_unified_validator().validate_type(pnl, dict)

        # Assess risk
        risk = await bi_analytics_service.assess_portfolio_risk()
        assert get_unified_validator().validate_type(risk, RiskMetrics)

        # Analyze trends
        trend = await bi_analytics_service.analyze_market_trends("AAPL")
        assert get_unified_validator().validate_type(trend, MarketTrend)

        # Generate performance report
        performance = await bi_analytics_service.generate_performance_report()
        assert get_unified_validator().validate_type(performance, PerformanceMetrics)

    @pytest.mark.asyncio
    async def test_error_handling(self, bi_analytics_service):
        """Test error handling in BI analytics"""
        # Simulate repository error
        bi_analytics_service.repository.get_all_positions.side_effect = Exception("Database error")

        result = await bi_analytics_service.calculate_real_time_pnl()

        assert "error" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, bi_analytics_service):
        """Test concurrent BI operations"""

        # Run multiple operations concurrently
        tasks = [
            bi_analytics_service.calculate_real_time_pnl(),
            bi_analytics_service.assess_portfolio_risk(),
            bi_analytics_service.generate_performance_report()
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        assert all(get_unified_validator().validate_type(r, (dict, RiskMetrics, PerformanceMetrics)) for r in results)


# Test coverage metrics
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.trading_robot.services.trading_bi_analytics", "--cov-report=term-missing"])
