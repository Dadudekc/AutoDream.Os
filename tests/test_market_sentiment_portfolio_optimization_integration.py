"""
Market Sentiment & Portfolio Optimization Integration Tests
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Tests the integration of market sentiment analysis and portfolio optimization services.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import business intelligence services
from src.services.financial import (
    MarketSentimentService,
    PortfolioOptimizationService,
    SentimentData,
    SentimentAggregate,
    NewsArticle,
    MarketPsychology,
    SentimentSource,
    SentimentType,
    OptimizationResult,
    RebalancingSignal,
    PortfolioAllocation,
    OptimizationMethod,
    RebalancingFrequency,
    OptimizationConstraint
)

class TestMarketSentimentPortfolioOptimizationIntegration:
    """Test market sentiment analysis and portfolio optimization integration"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.sentiment_dir = Path(self.temp_dir) / "market_sentiment"
        self.optimization_dir = Path(self.temp_dir) / "portfolio_optimization"
        
        # Create services
        self.market_sentiment_service = MarketSentimentService(data_dir=str(self.sentiment_dir))
        self.portfolio_optimization_service = PortfolioOptimizationService(data_dir=str(self.optimization_dir))
        
        yield
        
        # Cleanup
        shutil.rmtree(self.temp_dir)
    
    def test_market_sentiment_service_initialization(self):
        """Test market sentiment service initialization"""
        assert self.market_sentiment_service is not None
        assert self.market_sentiment_service.data_dir.exists()
        assert len(self.market_sentiment_service.sentiment_params) > 0
        assert len(self.market_sentiment_service.bullish_keywords) > 0
        assert len(self.market_sentiment_service.bearish_keywords) > 0
    
    def test_portfolio_optimization_service_initialization(self):
        """Test portfolio optimization service initialization"""
        assert self.portfolio_optimization_service is not None
        assert self.portfolio_optimization_service.data_dir.exists()
        assert len(self.portfolio_optimization_service.optimization_params) > 0
        assert len(self.portfolio_optimization_service.sector_classifications) > 0
        assert len(self.portfolio_optimization_service.market_cap_classifications) > 0
    
    def test_text_sentiment_analysis(self):
        """Test text sentiment analysis functionality"""
        # Test bullish text
        bullish_text = "The company reported strong earnings growth and exceeded analyst expectations."
        score, confidence = self.market_sentiment_service.analyze_text_sentiment(bullish_text)
        
        assert score > 0
        assert confidence > 0
        assert confidence <= 1.0
        
        # Test bearish text
        bearish_text = "The company missed earnings estimates and reported declining revenue."
        score, confidence = self.market_sentiment_service.analyze_text_sentiment(bearish_text)
        
        assert score < 0
        assert confidence > 0
        assert confidence <= 1.0
        
        # Test neutral text
        neutral_text = "The company reported quarterly results in line with expectations."
        score, confidence = self.market_sentiment_service.analyze_text_sentiment(neutral_text)
        
        assert abs(score) < 0.2
        assert confidence > 0
    
    def test_news_sentiment_analysis(self):
        """Test news sentiment analysis functionality"""
        # Create test news articles
        test_articles = [
            NewsArticle(
                title="Company Beats Earnings Expectations",
                content="The company reported quarterly earnings that exceeded analyst estimates by 15%.",
                source="Financial News",
                url="https://example.com",
                published_at=datetime.now(),
                symbol="TEST1"
            ),
            NewsArticle(
                title="Company Reports Revenue Decline",
                content="The company reported declining revenue and missed analyst expectations.",
                source="Financial News",
                url="https://example.com",
                published_at=datetime.now(),
                symbol="TEST2"
            )
        ]
        
        # Analyze sentiment
        sentiment_data = self.market_sentiment_service.analyze_news_sentiment(test_articles)
        
        assert len(sentiment_data) == 2
        assert sentiment_data[0].sentiment_type == SentimentType.BULLISH
        assert sentiment_data[1].sentiment_type == SentimentType.BEARISH
        assert sentiment_data[0].source == SentimentSource.NEWS
        assert sentiment_data[1].source == SentimentSource.NEWS
    
    def test_social_media_sentiment_analysis(self):
        """Test social media sentiment analysis functionality"""
        # Create test social media data
        social_data = [
            {
                "text": "Great earnings report! This stock is going to the moon! 🚀",
                "timestamp": datetime.now().isoformat(),
                "symbol": "TEST",
                "likes": 100,
                "retweets": 50,
                "replies": 25,
                "platform": "twitter",
                "author_followers": 1000
            },
            {
                "text": "Terrible quarter, selling everything",
                "timestamp": datetime.now().isoformat(),
                "symbol": "TEST",
                "likes": 10,
                "retweets": 5,
                "replies": 2,
                "platform": "twitter",
                "author_followers": 100
            }
        ]
        
        # Analyze sentiment
        sentiment_data = self.market_sentiment_service.analyze_social_media_sentiment(social_data)
        
        assert len(sentiment_data) == 2
        assert sentiment_data[0].sentiment_type == SentimentType.BULLISH
        assert sentiment_data[1].sentiment_type == SentimentType.BEARISH
        assert sentiment_data[0].source == SentimentSource.SOCIAL_MEDIA
        assert sentiment_data[1].source == SentimentSource.SOCIAL_MEDIA
    
    def test_analyst_ratings_sentiment_analysis(self):
        """Test analyst ratings sentiment analysis functionality"""
        # Create test analyst ratings data
        ratings_data = [
            {
                "rating": "strong_buy",
                "analyst": "John Doe",
                "firm": "Test Bank",
                "price_target": 150.0,
                "current_price": 100.0,
                "analyst_track_record": 0.8,
                "timestamp": datetime.now().isoformat(),
                "symbol": "TEST"
            },
            {
                "rating": "sell",
                "analyst": "Jane Smith",
                "firm": "Test Securities",
                "price_target": 80.0,
                "current_price": 100.0,
                "analyst_track_record": 0.7,
                "timestamp": datetime.now().isoformat(),
                "symbol": "TEST"
            }
        ]
        
        # Analyze sentiment
        sentiment_data = self.market_sentiment_service.analyze_analyst_ratings(ratings_data)
        
        assert len(sentiment_data) == 2
        assert sentiment_data[0].sentiment_type == SentimentType.BULLISH
        assert sentiment_data[1].sentiment_type == SentimentType.BEARISH
        assert sentiment_data[0].source == SentimentSource.ANALYST_RATINGS
        assert sentiment_data[1].source == SentimentSource.ANALYST_RATINGS
    
    def test_options_flow_sentiment_analysis(self):
        """Test options flow sentiment analysis functionality"""
        # Create test options flow data
        options_data = [
            {
                "call_volume": 1000,
                "put_volume": 200,
                "unusual_activity": True,
                "strike": 100.0,
                "expiration": "2024-01-19",
                "timestamp": datetime.now().isoformat(),
                "symbol": "TEST"
            },
            {
                "call_volume": 200,
                "put_volume": 1000,
                "unusual_activity": False,
                "strike": 100.0,
                "expiration": "2024-01-19",
                "timestamp": datetime.now().isoformat(),
                "symbol": "TEST"
            }
        ]
        
        # Analyze sentiment
        sentiment_data = self.market_sentiment_service.analyze_options_flow_sentiment(options_data)
        
        assert len(sentiment_data) == 2
        assert sentiment_data[0].sentiment_type == SentimentType.BULLISH
        assert sentiment_data[1].sentiment_type == SentimentType.BEARISH
        assert sentiment_data[0].source == SentimentSource.OPTIONS_FLOW
        assert sentiment_data[1].source == SentimentSource.OPTIONS_FLOW
    
    def test_sentiment_aggregation(self):
        """Test sentiment aggregation functionality"""
        # Add sentiment data (need at least 5 data points for aggregation)
        test_symbol = "TEST"
        sentiment_data = [
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.8,
                score=0.7,
                text="Positive news 1",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.SOCIAL_MEDIA,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.6,
                score=0.5,
                text="Positive social sentiment 1",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.ANALYST_RATINGS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.9,
                score=0.8,
                text="Analyst upgrade",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.OPTIONS_FLOW,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.7,
                score=0.6,
                text="Options flow bullish",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.8,
                score=0.7,
                text="Positive news 2",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            )
        ]
        
        self.market_sentiment_service.add_sentiment_data(test_symbol, sentiment_data)
        
        # Aggregate sentiment
        aggregate = self.market_sentiment_service.aggregate_sentiment(test_symbol)
        
        assert aggregate is not None
        assert aggregate.symbol == test_symbol
        assert aggregate.overall_sentiment == SentimentType.BULLISH
        assert aggregate.sentiment_score > 0
        assert aggregate.confidence > 0
        assert len(aggregate.source_breakdown) > 0
    
    def test_market_psychology_calculation(self):
        """Test market psychology calculation functionality"""
        # Add sentiment data for multiple symbols (need at least 5 data points per symbol)
        symbols = ["TEST1", "TEST2", "TEST3"]
        
        for symbol in symbols:
            sentiment_data = [
                SentimentData(
                    source=SentimentSource.NEWS,
                    sentiment_type=SentimentType.BULLISH,
                    confidence=0.7,
                    score=0.6,
                    text="Positive sentiment 1",
                    timestamp=datetime.now(),
                    symbol=symbol,
                    weight=1.0
                ),
                SentimentData(
                    source=SentimentSource.SOCIAL_MEDIA,
                    sentiment_type=SentimentType.BULLISH,
                    confidence=0.6,
                    score=0.5,
                    text="Positive sentiment 2",
                    timestamp=datetime.now(),
                    symbol=symbol,
                    weight=1.0
                ),
                SentimentData(
                    source=SentimentSource.ANALYST_RATINGS,
                    sentiment_type=SentimentType.BULLISH,
                    confidence=0.8,
                    score=0.7,
                    text="Positive sentiment 3",
                    timestamp=datetime.now(),
                    symbol=symbol,
                    weight=1.0
                ),
                SentimentData(
                    source=SentimentSource.OPTIONS_FLOW,
                    sentiment_type=SentimentType.BULLISH,
                    confidence=0.7,
                    score=0.6,
                    text="Positive sentiment 4",
                    timestamp=datetime.now(),
                    symbol=symbol,
                    weight=1.0
                ),
                SentimentData(
                    source=SentimentSource.NEWS,
                    sentiment_type=SentimentType.BULLISH,
                    confidence=0.7,
                    score=0.6,
                    text="Positive sentiment 5",
                    timestamp=datetime.now(),
                    symbol=symbol,
                    weight=1.0
                )
            ]
            self.market_sentiment_service.add_sentiment_data(symbol, sentiment_data)
        
        # Calculate market psychology
        psychology = self.market_sentiment_service.calculate_market_psychology(symbols)
        
        assert psychology is not None
        assert psychology.fear_greed_index > 50  # Should be bullish
        assert psychology.volatility_regime in ["LOW", "MEDIUM", "HIGH", "EXTREME"]
        assert psychology.momentum_bias in ["BULLISH", "BEARISH", "NEUTRAL"]
        assert len(psychology.contrarian_signals) >= 0
    
    def test_sentiment_signals_generation(self):
        """Test sentiment trading signals generation"""
        # Add strong sentiment data
        test_symbol = "TEST"
        sentiment_data = [
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.9,
                score=0.8,
                text="Very positive news",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.5
            )
        ]
        
        self.market_sentiment_service.add_sentiment_data(test_symbol, sentiment_data)
        
        # Generate signals
        signals = self.market_sentiment_service.get_sentiment_signals(test_symbol)
        
        assert len(signals) > 0
        assert any(signal["type"] == "STRONG_BULLISH_SENTIMENT" for signal in signals)
    
    def test_portfolio_optimization_constraints(self):
        """Test portfolio optimization constraints"""
        # Create test constraints
        constraints = [
            OptimizationConstraint(
                constraint_type="SECTOR_LIMIT",
                sector="TECHNOLOGY",
                max_sector_weight=0.3
            ),
            OptimizationConstraint(
                constraint_type="WEIGHT_LIMIT",
                symbol="TEST",
                min_weight=0.01,
                max_weight=0.1
            )
        ]
        
        assert len(constraints) == 2
        assert constraints[0].constraint_type == "SECTOR_LIMIT"
        assert constraints[1].constraint_type == "WEIGHT_LIMIT"
    
    def test_portfolio_optimization_methods(self):
        """Test portfolio optimization methods"""
        # Test available methods
        methods = [method.value for method in OptimizationMethod]
        
        assert "SHARPE_RATIO" in methods
        assert "MINIMUM_VARIANCE" in methods
        assert "MAXIMUM_RETURN" in methods
        assert "BLACK_LITTERMAN" in methods
        assert "RISK_PARITY" in methods
        assert "MEAN_VARIANCE" in methods
    
    def test_rebalancing_frequency_options(self):
        """Test rebalancing frequency options"""
        # Test available frequencies
        frequencies = [freq.value for freq in RebalancingFrequency]
        
        assert "DAILY" in frequencies
        assert "WEEKLY" in frequencies
        assert "MONTHLY" in frequencies
        assert "QUARTERLY" in frequencies
        assert "SEMI_ANNUALLY" in frequencies
        assert "ANNUALLY" in frequencies
        assert "ON_SIGNAL" in frequencies
    
    def test_rebalancing_signals_generation(self):
        """Test rebalancing signals generation"""
        # Create test portfolio data
        current_portfolio = {"AAPL": 0.3, "MSFT": 0.4, "GOOGL": 0.3}
        target_weights = {"AAPL": 0.25, "MSFT": 0.35, "GOOGL": 0.4}
        
        # Generate rebalancing signals
        signals = self.portfolio_optimization_service.generate_rebalancing_signals(
            current_portfolio, target_weights
        )
        
        assert len(signals) > 0
        
        # Check signal properties
        for signal in signals:
            assert signal.symbol in current_portfolio
            assert signal.action in ["BUY", "SELL", "HOLD"]
            assert signal.priority in ["HIGH", "MEDIUM", "LOW"]
            assert signal.reason in ["SIGNIFICANT_DRIFT", "MODERATE_DRIFT", "MINOR_DRIFT"]
    
    def test_portfolio_allocation_analysis(self):
        """Test portfolio allocation analysis"""
        # Create test portfolio positions
        portfolio_positions = [
            {
                "symbol": "AAPL",
                "weight": 0.3,
                "shares": 100,
                "purchase_price": 150.0
            },
            {
                "symbol": "MSFT",
                "weight": 0.4,
                "shares": 80,
                "purchase_price": 200.0
            }
        ]
        
        target_weights = {"AAPL": 0.25, "MSFT": 0.35, "GOOGL": 0.4}
        
        # Analyze allocation
        allocations = self.portfolio_optimization_service.analyze_portfolio_allocation(
            portfolio_positions, target_weights
        )
        
        assert len(allocations) == 2
        assert "AAPL" in allocations
        assert "MSFT" in allocations
        
        # Check allocation properties
        for symbol, allocation in allocations.items():
            assert allocation.symbol == symbol
            assert allocation.sector in ["TECHNOLOGY", "UNKNOWN"]
            assert allocation.market_cap in ["LARGE_CAP", "MID_CAP", "SMALL_CAP", "MICRO_CAP", "UNKNOWN"]
            assert allocation.style in ["GROWTH", "VALUE", "BLEND"]
            assert allocation.risk_level in ["LOW", "MEDIUM", "HIGH"]
    
    def test_optimization_recommendations(self):
        """Test optimization recommendations generation"""
        # Create test optimization result
        optimization_result = OptimizationResult(
            method=OptimizationMethod.SHARPE_RATIO,
            optimal_weights={"AAPL": 0.3, "MSFT": 0.4, "GOOGL": 0.3},
            expected_return=0.08,
            expected_volatility=0.20,
            sharpe_ratio=0.4,
            risk_metrics={
                "var_95": -0.05,
                "cvar_95": -0.08,
                "max_drawdown": 0.15,
                "beta": 1.1,
                "correlation": 0.65
            },
            constraints_satisfied=True,
            optimization_time=1.5
        )
        
        # Get recommendations
        recommendations = self.portfolio_optimization_service.get_optimization_recommendations(
            optimization_result
        )
        
        assert len(recommendations) > 0
        
        # Check for specific recommendations
        recommendation_texts = [rec for rec in recommendations]
        assert any("HIGH_VOLATILITY" in rec for rec in recommendation_texts)
        assert any("LOW_SHARPE_RATIO" in rec for rec in recommendation_texts)
    
    def test_data_persistence(self):
        """Test data persistence functionality"""
        # Add test data (need at least 5 data points for aggregation)
        test_symbol = "TEST"
        sentiment_data = [
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.8,
                score=0.7,
                text="Test sentiment 1",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.SOCIAL_MEDIA,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.7,
                score=0.6,
                text="Test sentiment 2",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.ANALYST_RATINGS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.9,
                score=0.8,
                text="Test sentiment 3",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.OPTIONS_FLOW,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.7,
                score=0.6,
                text="Test sentiment 4",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.8,
                score=0.7,
                text="Test sentiment 5",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            )
        ]
        
        self.market_sentiment_service.add_sentiment_data(test_symbol, sentiment_data)
        
        # Test portfolio optimization data
        current_portfolio = {"AAPL": 0.3, "MSFT": 0.4, "GOOGL": 0.3}
        target_weights = {"AAPL": 0.25, "MSFT": 0.35, "GOOGL": 0.4}
        
        signals = self.portfolio_optimization_service.generate_rebalancing_signals(
            current_portfolio, target_weights
        )
        
        # Save data
        self.market_sentiment_service.save_data()
        self.portfolio_optimization_service.save_data()
        
        # Verify files exist
        assert (self.sentiment_dir / "sentiment_data.json").exists()
        assert (self.sentiment_dir / "sentiment_aggregates.json").exists()
        assert (self.optimization_dir / "rebalancing_signals.json").exists()
    
    def test_integration_workflow(self):
        """Test complete integration workflow"""
        # 1. Add sentiment data (need at least 5 data points for aggregation)
        test_symbol = "INTEGRATION_TEST"
        sentiment_data = [
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.8,
                score=0.7,
                text="Integration test sentiment 1",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.SOCIAL_MEDIA,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.7,
                score=0.6,
                text="Integration test sentiment 2",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.ANALYST_RATINGS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.9,
                score=0.8,
                text="Integration test sentiment 3",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.OPTIONS_FLOW,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.7,
                score=0.6,
                text="Integration test sentiment 4",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            ),
            SentimentData(
                source=SentimentSource.NEWS,
                sentiment_type=SentimentType.BULLISH,
                confidence=0.8,
                score=0.7,
                text="Integration test sentiment 5",
                timestamp=datetime.now(),
                symbol=test_symbol,
                weight=1.0
            )
        ]
        
        self.market_sentiment_service.add_sentiment_data(test_symbol, sentiment_data)
        
        # 2. Aggregate sentiment
        aggregate = self.market_sentiment_service.aggregate_sentiment(test_symbol)
        assert aggregate is not None
        
        # 3. Generate sentiment signals
        signals = self.market_sentiment_service.get_sentiment_signals(test_symbol)
        assert len(signals) > 0
        
        # 4. Create portfolio optimization scenario
        current_portfolio = {"AAPL": 0.3, "MSFT": 0.4, "GOOGL": 0.3}
        target_weights = {"AAPL": 0.25, "MSFT": 0.35, "GOOGL": 0.4}
        
        # 5. Generate rebalancing signals
        rebalancing_signals = self.portfolio_optimization_service.generate_rebalancing_signals(
            current_portfolio, target_weights
        )
        assert len(rebalancing_signals) > 0
        
        # 6. Analyze portfolio allocation
        portfolio_positions = [
            {"symbol": "AAPL", "weight": 0.3, "shares": 100, "purchase_price": 150.0},
            {"symbol": "MSFT", "weight": 0.4, "shares": 80, "purchase_price": 200.0},
            {"symbol": "GOOGL", "weight": 0.3, "shares": 60, "purchase_price": 250.0}
        ]
        
        allocations = self.portfolio_optimization_service.analyze_portfolio_allocation(
            portfolio_positions, target_weights
        )
        assert len(allocations) == 3
        
        # 7. Save all data
        self.market_sentiment_service.save_data()
        self.portfolio_optimization_service.save_data()
        
        # Verify integration success
        assert len(self.market_sentiment_service.sentiment_data) > 0
        assert len(self.portfolio_optimization_service.rebalancing_signals) > 0
        assert len(self.portfolio_optimization_service.portfolio_allocations) > 0
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        # Test empty data handling
        empty_signals = self.market_sentiment_service.get_sentiment_signals("NONEXISTENT")
        assert len(empty_signals) == 0
        
        # Test invalid sentiment data
        invalid_sentiment = self.market_sentiment_service.analyze_text_sentiment("")
        assert invalid_sentiment == (0.0, 0.0)
        
        # Test portfolio optimization with empty data
        empty_rebalancing = self.portfolio_optimization_service.generate_rebalancing_signals({}, {})
        assert len(empty_rebalancing) == 0
        
        # Test allocation analysis with empty data
        empty_allocations = self.portfolio_optimization_service.analyze_portfolio_allocation([], {})
        assert len(empty_allocations) == 0

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
