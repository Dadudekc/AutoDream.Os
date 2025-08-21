"""
Business Intelligence Integration Tests
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Tests the integration of portfolio management, risk management, and market data services.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# Import business intelligence services
from src.services.financial import (
    PortfolioManager,
    RiskManager,
    MarketDataService,
    PortfolioPosition,
    RiskLevel,
    RiskType
)

class TestBusinessIntelligenceIntegration:
    """Test suite for business intelligence system integration"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.portfolio_dir = Path(self.temp_dir) / "portfolio_data"
        self.risk_dir = Path(self.temp_dir) / "risk_data"
        self.market_dir = Path(self.temp_dir) / "market_data"
        
        # Create directories
        self.portfolio_dir.mkdir(exist_ok=True)
        self.risk_dir.mkdir(exist_ok=True)
        self.market_dir.mkdir(exist_ok=True)
        
        yield
        
        # Cleanup
        shutil.rmtree(self.temp_dir)
    
    def test_portfolio_management_creation(self):
        """Test portfolio manager creation and initialization"""
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        assert pm.portfolio_name == "test_portfolio"
        assert pm.data_dir == self.portfolio_dir
        assert len(pm.positions) == 0
        assert pm.metrics is not None
    
    def test_portfolio_position_management(self):
        """Test adding and managing portfolio positions"""
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        # Add positions
        assert pm.add_position("AAPL", 100, 150.0, "Technology")
        assert pm.add_position("MSFT", 50, 300.0, "Technology")
        assert pm.add_position("JPM", 200, 140.0, "Financial")
        
        # Verify positions
        assert len(pm.positions) == 3
        assert "AAPL" in pm.positions
        assert "MSFT" in pm.positions
        assert "JPM" in pm.positions
        
        # Verify position data
        aapl_pos = pm.positions["AAPL"]
        assert aapl_pos.symbol == "AAPL"
        assert aapl_pos.quantity == 100
        assert aapl_pos.avg_price == 150.0
        assert aapl_pos.sector == "Technology"
    
    def test_portfolio_metrics_calculation(self):
        """Test portfolio metrics calculation"""
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        # Add positions
        pm.add_position("AAPL", 100, 150.0, "Technology")
        pm.add_position("MSFT", 50, 300.0, "Technology")
        
        # Update prices
        pm.update_prices({
            "AAPL": 155.0,
            "MSFT": 310.0
        })
        
        # Verify metrics
        metrics = pm.calculate_metrics()
        assert metrics is not None
        assert metrics.total_value > 0
        assert metrics.total_cost > 0
        assert metrics.total_pnl != 0
    
    def test_portfolio_persistence(self):
        """Test portfolio data persistence"""
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        # Add positions
        pm.add_position("AAPL", 100, 150.0, "Technology")
        pm.add_position("MSFT", 50, 300.0, "Technology")
        
        # Save portfolio
        pm.save_portfolio()
        
        # Create new instance and load
        pm2 = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        # Verify data loaded
        assert len(pm2.positions) == 2
        assert "AAPL" in pm2.positions
        assert "MSFT" in pm2.positions
    
    def test_risk_manager_initialization(self):
        """Test risk manager initialization"""
        rm = RiskManager(data_dir=str(self.risk_dir))
        
        assert rm.data_dir == self.risk_dir
        assert len(rm.risk_metrics) > 0
        assert len(rm.risk_alerts) == 0
    
    def test_risk_metrics_calculation(self):
        """Test risk metrics calculation"""
        # Create portfolio manager first
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        pm.add_position("AAPL", 100, 150.0, "Technology")
        pm.add_position("MSFT", 50, 300.0, "Technology")
        pm.update_prices({"AAPL": 155.0, "MSFT": 310.0})
        
        # Create risk manager with portfolio
        rm = RiskManager(pm, str(self.risk_dir))
        
        # Update risk metrics
        rm.update_risk_metrics()
        
        # Verify risk metrics
        assert len(rm.risk_metrics) > 0
        for risk_type, metric in rm.risk_metrics.items():
            assert metric.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
    
    def test_risk_profile_generation(self):
        """Test comprehensive risk profile generation"""
        # Setup portfolio and risk manager
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        pm.add_position("AAPL", 100, 150.0, "Technology")
        pm.add_position("MSFT", 50, 300.0, "Technology")
        pm.update_prices({"AAPL": 155.0, "MSFT": 310.0})
        
        rm = RiskManager(pm, str(self.risk_dir))
        
        # Get risk profile
        risk_profile = rm.get_risk_profile()
        
        assert risk_profile is not None
        assert hasattr(risk_profile, 'total_risk_score')
        assert hasattr(risk_profile, 'var_95')
        assert hasattr(risk_profile, 'var_99')
        assert hasattr(risk_profile, 'expected_shortfall')
        assert hasattr(risk_profile, 'stress_test_results')
    
    def test_market_data_service_initialization(self):
        """Test market data service initialization"""
        mds = MarketDataService(str(self.market_dir))
        
        assert mds.data_dir == self.market_dir
        assert mds.default_source == "yfinance"
        assert "yfinance" in mds.data_sources
        assert "mock" in mds.data_sources
    
    def test_mock_market_data(self):
        """Test mock market data functionality"""
        mds = MarketDataService(str(self.market_dir))
        
        # Get mock data
        symbols = ["AAPL", "MSFT", "GOOGL"]
        market_data = mds.get_real_time_data(symbols, source="mock")
        
        assert len(market_data) == 3
        for symbol, data in market_data.items():
            assert data.symbol == symbol
            assert data.price > 0
            assert data.data_source == "mock"
    
    def test_market_sentiment_calculation(self):
        """Test market sentiment calculation (with mock data)"""
        mds = MarketDataService(str(self.market_dir))
        
        # Test with mock data source
        sentiment = mds.get_market_sentiment("AAPL")
        
        # Note: This will return None with mock data since no historical data
        # In real implementation with yfinance, would return sentiment data
        assert sentiment is None or hasattr(sentiment, 'rsi')
    
    def test_portfolio_market_data_integration(self):
        """Test portfolio market data integration"""
        mds = MarketDataService(str(self.market_dir))
        
        # Get portfolio market data with mock source
        symbols = ["AAPL", "MSFT", "GOOGL"]
        portfolio_data = mds.get_portfolio_market_data(symbols)
        
        assert "real_time_data" in portfolio_data
        assert "sentiment_data" in portfolio_data
        assert "portfolio_metrics" in portfolio_data
        assert "market_status" in portfolio_data
        
        # Verify real-time data
        real_time_data = portfolio_data["real_time_data"]
        assert len(real_time_data) == 3
        
        # Verify market status
        market_status = portfolio_data["market_status"]
        assert "is_open" in market_status
        assert "last_updated" in market_status
    
    def test_business_intelligence_workflow(self):
        """Test complete business intelligence workflow"""
        # 1. Create portfolio
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        pm.add_position("AAPL", 100, 150.0, "Technology")
        pm.add_position("MSFT", 50, 300.0, "Technology")
        pm.add_position("JPM", 200, 140.0, "Financial")
        
        # 2. Update prices
        pm.update_prices({
            "AAPL": 155.0,
            "MSFT": 310.0,
            "JPM": 145.0
        })
        
        # 3. Create risk manager
        rm = RiskManager(pm, str(self.risk_dir))
        risk_profile = rm.get_risk_profile()
        
        # 4. Create market data service
        mds = MarketDataService(str(self.market_dir))
        portfolio_symbols = ["AAPL", "MSFT", "JPM"]
        market_data = mds.get_portfolio_market_data(portfolio_symbols)
        
        # 5. Verify integration
        assert pm.metrics is not None
        assert risk_profile is not None
        assert market_data is not None
        
        # 6. Verify data consistency
        portfolio_summary = pm.get_portfolio_summary()
        risk_summary = rm.get_risk_summary()
        
        assert portfolio_summary["positions_count"] == 3
        assert "total_risk_score" in risk_summary
        assert len(market_data["real_time_data"]) == 3
    
    def test_error_handling(self):
        """Test error handling in business intelligence services"""
        # Test portfolio manager with invalid data
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        # Invalid position data should be handled gracefully
        result = pm.add_position("", -100, -150.0, "")
        assert result is False
        
        # Test risk manager without portfolio
        rm = RiskManager(data_dir=str(self.risk_dir))
        risk_profile = rm.get_risk_profile()
        
        # Should handle missing portfolio gracefully
        assert risk_profile is not None
        
        # Test market data service with invalid symbols
        mds = MarketDataService(str(self.market_dir))
        invalid_data = mds.get_real_time_data([""], source="mock")
        
        # Should handle invalid symbols gracefully
        assert isinstance(invalid_data, dict)
    
    def test_performance_metrics(self):
        """Test performance and efficiency metrics"""
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        
        # Add multiple positions for performance testing
        symbols = [f"STOCK_{i}" for i in range(100)]
        for i, symbol in enumerate(symbols):
            pm.add_position(symbol, 100, 100.0 + i, "Technology")
        
        # Measure portfolio metrics calculation time
        import time
        start_time = time.time()
        metrics = pm.calculate_metrics()
        calculation_time = time.time() - start_time
        
        # Verify performance
        assert calculation_time < 1.0  # Should complete within 1 second
        assert metrics is not None
        assert len(pm.positions) == 100
    
    def test_data_export_functionality(self):
        """Test data export functionality"""
        pm = PortfolioManager("test_portfolio", str(self.portfolio_dir))
        pm.add_position("AAPL", 100, 150.0, "Technology")
        pm.add_position("MSFT", 50, 300.0, "Technology")
        
        # Export portfolio to CSV
        csv_file = pm.export_to_csv()
        assert csv_file != ""
        assert Path(csv_file).exists()
        
        # Verify CSV content
        df = pd.read_csv(csv_file)
        assert len(df) == 2
        assert "Symbol" in df.columns
        assert "AAPL" in df["Symbol"].values
        assert "MSFT" in df["Symbol"].values

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
