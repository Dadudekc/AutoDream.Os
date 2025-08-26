"""
Test script for the extracted sentiment analysis modules
"""

import sys
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, 'src')

def test_text_analyzer():
    """Test the TextAnalyzer module"""
    print("Testing TextAnalyzer...")
    
    try:
        from services.financial.sentiment.text_analyzer import TextAnalyzer
        
        analyzer = TextAnalyzer()
        
        # Test text sentiment analysis
        test_text = "The company reported strong earnings growth and exceeded analyst expectations."
        score, confidence = analyzer.analyze_text_sentiment(test_text)
        print(f"  ✓ Text sentiment analysis: score={score:.3f}, confidence={confidence:.3f}")
        
        # Test news sentiment analysis
        test_article = {
            "title": "Company Beats Earnings Expectations",
            "content": "The company reported quarterly earnings that exceeded analyst estimates by 15%.",
            "source": "Financial News",
            "url": "https://example.com",
            "published_at": datetime.now(),
            "symbol": "TEST",
        }
        
        sentiment_data = analyzer.analyze_news_sentiment([test_article])
        print(f"  ✓ News sentiment analysis: {len(sentiment_data)} articles processed")
        
        # Test social media sentiment analysis
        social_data = [{
            "text": "Great earnings report! Stock is going to the moon! 🚀",
            "timestamp": datetime.now().isoformat(),
            "symbol": "TEST",
            "platform": "twitter",
            "likes": 100,
            "retweets": 50,
            "replies": 25
        }]
        
        sentiment_data = analyzer.analyze_social_media_sentiment(social_data)
        print(f"  ✓ Social media sentiment analysis: {len(sentiment_data)} posts processed")
        
        # Test analysis summary
        summary = analyzer.get_analysis_summary()
        print(f"  ✓ Analysis summary: {summary['supported_content_types']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ TextAnalyzer test failed: {e}")
        return False

def test_data_analyzer():
    """Test the DataAnalyzer module"""
    print("Testing DataAnalyzer...")
    
    try:
        from services.financial.sentiment.data_analyzer import DataAnalyzer
        
        analyzer = DataAnalyzer()
        
        # Test analyst ratings analysis
        ratings_data = [{
            "rating": "strong_buy",
            "analyst": "John Doe",
            "firm": "Goldman Sachs",
            "price_target": 150.0,
            "current_price": 100.0,
            "analyst_track_record": 0.8,
            "timestamp": datetime.now().isoformat(),
            "symbol": "TEST"
        }]
        
        sentiment_data = analyzer.analyze_analyst_ratings(ratings_data)
        print(f"  ✓ Analyst ratings analysis: {len(sentiment_data)} ratings processed")
        
        # Test options flow analysis
        options_data = [{
            "call_volume": 1000,
            "put_volume": 500,
            "unusual_activity": True,
            "strike": 100.0,
            "expiration": "2024-01-19",
            "timestamp": datetime.now().isoformat(),
            "symbol": "TEST"
        }]
        
        sentiment_data = analyzer.analyze_options_flow_sentiment(options_data)
        print(f"  ✓ Options flow analysis: {len(sentiment_data)} options processed")
        
        # Test insider trading analysis
        insider_data = [{
            "trade_type": "buy",
            "trade_size": 10000,
            "current_price": 100.0,
            "insider": "CEO Smith",
            "filing_date": "2024-01-19",
            "timestamp": datetime.now().isoformat(),
            "symbol": "TEST"
        }]
        
        sentiment_data = analyzer.analyze_insider_trading_sentiment(insider_data)
        print(f"  ✓ Insider trading analysis: {len(sentiment_data)} trades processed")
        
        # Test analysis summary
        summary = analyzer.get_analysis_summary()
        print(f"  ✓ Analysis summary: {summary['supported_data_sources']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ DataAnalyzer test failed: {e}")
        return False

def test_sentiment_aggregator():
    """Test the SentimentAggregator module"""
    print("Testing SentimentAggregator...")
    
    try:
        from services.financial.sentiment.aggregator import SentimentAggregator
        
        aggregator = SentimentAggregator()
        
        # Test sentiment aggregation
        sentiment_data = [
            {
                "source": "NEWS",
                "sentiment_type": "BULLISH",
                "confidence": 0.8,
                "score": 0.7,
                "text": "Positive news article",
                "timestamp": datetime.now(),
                "symbol": "TEST",
                "weight": 1.0,
                "metadata": {}
            },
            {
                "source": "SOCIAL_MEDIA",
                "sentiment_type": "BULLISH",
                "confidence": 0.6,
                "score": 0.5,
                "text": "Positive social media post",
                "timestamp": datetime.now(),
                "symbol": "TEST",
                "weight": 0.8,
                "metadata": {}
            }
        ]
        
        aggregate = aggregator.aggregate_sentiment("TEST", sentiment_data, timedelta(days=7))
        if aggregate:
            print(f"  ✓ Sentiment aggregation: {aggregate['overall_sentiment']} with score {aggregate['sentiment_score']:.3f}")
        else:
            print("  ✗ Sentiment aggregation failed")
            return False
        
        # Test market psychology calculation
        psychology = aggregator.calculate_market_psychology([aggregate])
        if psychology:
            print(f"  ✓ Market psychology: {psychology['crowd_sentiment']} with fear-greed index {psychology['fear_greed_index']:.1f}")
        else:
            print("  ✗ Market psychology calculation failed")
            return False
        
        # Test sentiment signals
        signals = aggregator.get_sentiment_signals(aggregate)
        print(f"  ✓ Sentiment signals: {len(signals)} signals generated")
        
        # Test aggregation summary
        summary = aggregator.get_aggregation_summary()
        print(f"  ✓ Aggregation summary: {summary['supported_aggregation_methods']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ SentimentAggregator test failed: {e}")
        return False

def test_sentiment_data_manager():
    """Test the SentimentDataManager module"""
    print("Testing SentimentDataManager...")
    
    try:
        from services.financial.sentiment.data_manager import SentimentDataManager
        
        manager = SentimentDataManager("test_sentiment_data")
        
        # Test adding sentiment data
        sentiment_data = [{
            "source": "NEWS",
            "sentiment_type": "BULLISH",
            "confidence": 0.8,
            "score": 0.7,
            "text": "Test sentiment data",
            "timestamp": datetime.now(),
            "symbol": "TEST",
            "weight": 1.0,
            "metadata": {}
        }]
        
        manager.add_sentiment_data("TEST", sentiment_data)
        print("  ✓ Added sentiment data")
        
        # Test retrieving sentiment data
        retrieved_data = manager.get_sentiment_data("TEST")
        print(f"  ✓ Retrieved sentiment data: {len(retrieved_data)} data points")
        
        # Test data summary
        summary = manager.get_data_summary()
        print(f"  ✓ Data summary: {summary['total_symbols']} symbols")
        
        # Test storage info
        storage_info = manager.get_storage_info()
        print(f"  ✓ Storage info: {storage_info['total_size_mb']} MB")
        
        # Test cleanup
        cleaned_count = manager.cleanup_old_data()
        print(f"  ✓ Cleanup: {cleaned_count} old data points removed")
        
        return True
        
    except Exception as e:
        print(f"  ✗ SentimentDataManager test failed: {e}")
        return False

def test_integration():
    """Test the integrated MarketSentimentService"""
    print("Testing integrated MarketSentimentService...")
    
    try:
        from services.financial.market_sentiment_service import MarketSentimentService
        
        service = MarketSentimentService()
        
        # Test text sentiment analysis
        test_text = "The company reported strong earnings growth and exceeded analyst expectations."
        score, confidence = service.analyze_text_sentiment(test_text)
        print(f"  ✓ Service text analysis: score={score:.3f}, confidence={confidence:.3f}")
        
        # Test service summary
        summary = service.get_service_summary()
        print(f"  ✓ Service summary: {summary['total_symbols']} symbols")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Sentiment Analysis Modules")
    print("=" * 50)
    
    tests = [
        test_text_analyzer,
        test_data_analyzer,
        test_sentiment_aggregator,
        test_sentiment_data_manager,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The sentiment analysis modules are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


