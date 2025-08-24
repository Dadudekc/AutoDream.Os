"""
Market Sentiment Analysis Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides comprehensive market sentiment analysis, news analysis, and market psychology insights.
Now uses modular architecture for better maintainability and SRP compliance.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Import the new modular components
from .sentiment import (
    TextAnalyzer,
    DataAnalyzer,
    SentimentAggregator,
    SentimentDataManager
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketSentimentService:
    """Advanced market sentiment analysis and psychology service using modular architecture"""

    def __init__(self, market_data_service=None, data_dir: str = "market_sentiment"):
        self.market_data_service = market_data_service
        
        # Initialize modular components
        self.text_analyzer = TextAnalyzer()
        self.data_analyzer = DataAnalyzer()
        self.sentiment_aggregator = SentimentAggregator()
        self.data_manager = SentimentDataManager(data_dir)

        # Load existing data
        self.data_manager.load_data()

    def analyze_text_sentiment(self, text: str) -> Tuple[float, float]:
        """Analyze text sentiment using TextAnalyzer module"""
        return self.text_analyzer.analyze_text_sentiment(text)

    def analyze_news_sentiment(
        self, articles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from news articles using TextAnalyzer module"""
        return self.text_analyzer.analyze_news_sentiment(articles)



    def analyze_social_media_sentiment(
        self, social_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from social media data using TextAnalyzer module"""
        return self.text_analyzer.analyze_social_media_sentiment(social_data)

    def analyze_analyst_ratings(
        self, ratings_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from analyst ratings using DataAnalyzer module"""
        return self.data_analyzer.analyze_analyst_ratings(ratings_data)

    def analyze_options_flow_sentiment(
        self, options_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from options flow data using DataAnalyzer module"""
        return self.data_analyzer.analyze_options_flow_sentiment(options_data)

    def aggregate_sentiment(
        self, symbol: str, time_window: timedelta = timedelta(days=7)
    ) -> Dict[str, Any]:
        """Aggregate sentiment data for a symbol using SentimentAggregator module"""
        sentiment_data = self.data_manager.get_sentiment_data(symbol, time_window)
        aggregate = self.sentiment_aggregator.aggregate_sentiment(symbol, sentiment_data, time_window)
        
        if aggregate:
            # Convert to dict for storage
            aggregate_dict = {
                "symbol": aggregate.symbol,
                "overall_sentiment": aggregate.overall_sentiment,
                "sentiment_score": aggregate.sentiment_score,
                "confidence": aggregate.confidence,
                "source_breakdown": aggregate.source_breakdown,
                "sentiment_trend": aggregate.sentiment_trend,
                "volatility": aggregate.volatility,
                "momentum": aggregate.momentum,
                "last_updated": aggregate.last_updated
            }
            self.data_manager.update_sentiment_aggregate(symbol, aggregate_dict)
            return aggregate_dict
        
        return None

    def calculate_market_psychology(self, symbols: List[str]) -> Dict[str, Any]:
        """Calculate overall market psychology indicators using SentimentAggregator module"""
        sentiment_aggregates = []
        for symbol in symbols:
            aggregate = self.data_manager.get_sentiment_aggregate(symbol)
            if aggregate:
                sentiment_aggregates.append(aggregate)
        
        psychology = self.sentiment_aggregator.calculate_market_psychology(sentiment_aggregates)
        
        if psychology:
            # Convert to dict for storage
            psychology_dict = {
                "fear_greed_index": psychology.fear_greed_index,
                "volatility_regime": psychology.volatility_regime,
                "momentum_bias": psychology.momentum_bias,
                "contrarian_signals": psychology.contrarian_signals,
                "crowd_sentiment": psychology.crowd_sentiment,
                "market_regime": psychology.market_regime,
                "last_updated": psychology.last_updated
            }
            self.data_manager.update_market_psychology(psychology_dict)
            return psychology_dict
        
        return None

    def get_sentiment_signals(self, symbol: str) -> List[Dict[str, Any]]:
        """Get trading signals based on sentiment analysis using SentimentAggregator module"""
        aggregate = self.data_manager.get_sentiment_aggregate(symbol)
        if aggregate:
            return self.sentiment_aggregator.get_sentiment_signals(aggregate)
        return []

    def add_sentiment_data(
        self, symbol: str, sentiment_data: List[Dict[str, Any]]
    ) -> None:
        """Add sentiment data for a symbol using SentimentDataManager"""
        self.data_manager.add_sentiment_data(symbol, sentiment_data)
        # Recalculate aggregate
        self.aggregate_sentiment(symbol)

    def save_data(self):
        """Save sentiment data using SentimentDataManager"""
        return self.data_manager.save_data()

    def load_data(self):
        """Load sentiment data using SentimentDataManager"""
        return self.data_manager.load_data()

    def get_service_summary(self) -> Dict[str, Any]:
        """Get comprehensive service summary"""
        try:
            data_summary = self.data_manager.get_data_summary()
            return {
                "total_symbols": data_summary.get("total_symbols", 0),
                "total_sentiment_data_points": data_summary.get("total_sentiment_data_points", 0),
                "total_news_articles": data_summary.get("total_news_articles", 0),
                "sentiment_aggregates_count": data_summary.get("sentiment_aggregates_count", 0),
                "has_market_psychology": data_summary.get("has_market_psychology", False),
                "text_analysis_capabilities": self.text_analyzer.get_analysis_summary(),
                "data_analysis_capabilities": self.data_analyzer.get_analysis_summary(),
                "aggregation_capabilities": self.sentiment_aggregator.get_aggregation_summary(),
                "storage_info": self.data_manager.get_storage_info(),
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating service summary: {e}")
            return {}


# Example usage and testing
if __name__ == "__main__":
    # Create market sentiment service
    mss = MarketSentimentService()

    # Test text sentiment analysis
    test_text = (
        "The company reported strong earnings growth and exceeded analyst expectations."
    )
    score, confidence = mss.analyze_text_sentiment(test_text)

    print(f"Sentiment Score: {score:.3f}")
    print(f"Confidence: {confidence:.3f}")

    # Test news sentiment analysis
    test_article = {
        "title": "Company Beats Earnings Expectations",
        "content": "The company reported quarterly earnings that exceeded analyst estimates by 15%.",
        "source": "Financial News",
        "url": "https://example.com",
        "published_at": datetime.now(),
        "symbol": "TEST",
    }

    sentiment_data = mss.analyze_news_sentiment([test_article])
    print(f"News Sentiment: {sentiment_data[0]['sentiment_type']}")

    print("Market Sentiment Service initialized successfully")
