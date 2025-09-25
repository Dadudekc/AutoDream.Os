#!/usr/bin/env python3
"""
News Sentiment Analyzer CLI Tool
================================

Analyze news sentiment for better trading predictions
V2 Compliant: ≤400 lines, focused news analysis
"""

import argparse
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys
import os
import re

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


class NewsSentimentAnalyzer:
    """News sentiment analysis tool"""

    def __init__(self):
        """Initialize news analyzer"""
        self.api_keys = self._load_api_keys()
        self.sentiment_keywords = self._load_sentiment_keywords()

    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment"""
        return {
            'news_api': os.getenv('NEWS_API_KEY'),
            'alpha_vantage': os.getenv('ALPHAVANTAGE_API_KEY')
        }

    def _load_sentiment_keywords(self) -> Dict[str, List[str]]:
        """Load sentiment analysis keywords"""
        return {
            'positive': [
                'bullish', 'surge', 'rally', 'gain', 'rise', 'up', 'strong', 'growth',
                'profit', 'earnings', 'beat', 'exceed', 'outperform', 'upgrade',
                'breakthrough', 'innovation', 'success', 'win', 'positive', 'optimistic'
            ],
            'negative': [
                'bearish', 'decline', 'fall', 'drop', 'down', 'weak', 'loss', 'miss',
                'disappoint', 'concern', 'risk', 'volatile', 'uncertain', 'negative',
                'pessimistic', 'crash', 'plunge', 'tumble', 'struggle', 'challenge'
            ],
            'neutral': [
                'stable', 'maintain', 'hold', 'steady', 'unchanged', 'flat', 'neutral',
                'mixed', 'uncertain', 'wait', 'observe', 'monitor', 'review'
            ]
        }

    def get_news_data(self, symbol: str = "TSLA", days: int = 7) -> List[Dict[str, Any]]:
        """Get news data for the symbol"""
        print(f"[NEWS] Fetching news for {symbol} (last {days} days)...")
        
        news_data = []
        
        # Try News API first
        if self.api_keys['news_api']:
            news_data.extend(self._get_news_api_data(symbol, days))
        
        # Try Alpha Vantage News
        if self.api_keys['alpha_vantage']:
            news_data.extend(self._get_alpha_vantage_news(symbol))
        
        # Mock news data if APIs fail
        if not news_data:
            news_data = self._get_mock_news_data(symbol)
        
        return news_data

    def _get_news_api_data(self, symbol: str, days: int) -> List[Dict[str, Any]]:
        """Get news from News API"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': f"{symbol} OR Tesla",
                'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'apiKey': self.api_keys['news_api'],
                'pageSize': 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'published_at': article['publishedAt'],
                        'source': article['source']['name']
                    }
                    for article in data.get('articles', [])
                ]
        except Exception as e:
            print(f"News API error: {e}")
        
        return []

    def _get_alpha_vantage_news(self, symbol: str) -> List[Dict[str, Any]]:
        """Get news from Alpha Vantage"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'NEWS_SENTIMENT',
                'tickers': symbol,
                'apikey': self.api_keys['alpha_vantage'],
                'limit': 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        'title': article['title'],
                        'summary': article['summary'],
                        'url': article['url'],
                        'published_at': article['time_published'],
                        'source': 'Alpha Vantage',
                        'sentiment_score': float(article.get('overall_sentiment_score', 0)),
                        'sentiment_label': article.get('overall_sentiment_label', 'neutral')
                    }
                    for article in data.get('feed', [])
                ]
        except Exception as e:
            print(f"Alpha Vantage News error: {e}")
        
        return []

    def _get_mock_news_data(self, symbol: str) -> List[Dict[str, Any]]:
        """Get mock news data for testing"""
        return [
            {
                'title': f'{symbol} Stock Shows Strong Performance',
                'description': f'{symbol} continues to show strong performance in the market',
                'url': 'https://example.com/news1',
                'published_at': datetime.now().isoformat(),
                'source': 'Mock News'
            },
            {
                'title': f'{symbol} Faces Market Volatility',
                'description': f'{symbol} experiences increased volatility in recent trading',
                'url': 'https://example.com/news2',
                'published_at': datetime.now().isoformat(),
                'source': 'Mock News'
            },
            {
                'title': f'{symbol} Reports Quarterly Earnings',
                'description': f'{symbol} reports better than expected quarterly earnings',
                'url': 'https://example.com/news3',
                'published_at': datetime.now().isoformat(),
                'source': 'Mock News'
            }
        ]

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in text_lower)
        neutral_count = sum(1 for word in self.sentiment_keywords['neutral'] if word in text_lower)
        
        total_words = positive_count + negative_count + neutral_count
        
        if total_words == 0:
            sentiment_score = 0
            sentiment_label = 'neutral'
        else:
            sentiment_score = (positive_count - negative_count) / total_words
            if sentiment_score > 0.1:
                sentiment_label = 'positive'
            elif sentiment_score < -0.1:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
        
        return {
            'score': sentiment_score,
            'label': sentiment_label,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'neutral_words': neutral_count,
            'total_sentiment_words': total_words
        }

    def analyze_news_sentiment(self, symbol: str = "TSLA", days: int = 7) -> Dict[str, Any]:
        """Analyze overall news sentiment"""
        print(f"[ANALYSIS] Analyzing news sentiment for {symbol}...")
        
        # Get news data
        news_data = self.get_news_data(symbol, days)
        
        if not news_data:
            print("❌ No news data available")
            return None
        
        # Analyze each news item
        analyzed_news = []
        total_sentiment_score = 0
        
        for news in news_data:
            # Combine title and description for analysis
            text = f"{news.get('title', '')} {news.get('description', '')} {news.get('summary', '')}"
            
            # Analyze sentiment
            sentiment = self.analyze_sentiment(text)
            
            # Use API sentiment if available
            if 'sentiment_score' in news:
                sentiment['score'] = news['sentiment_score']
                sentiment['label'] = news['sentiment_label']
            
            analyzed_news.append({
                'title': news.get('title', ''),
                'source': news.get('source', ''),
                'published_at': news.get('published_at', ''),
                'sentiment': sentiment,
                'url': news.get('url', '')
            })
            
            total_sentiment_score += sentiment['score']
        
        # Calculate overall sentiment
        avg_sentiment_score = total_sentiment_score / len(analyzed_news)
        
        if avg_sentiment_score > 0.1:
            overall_sentiment = 'positive'
        elif avg_sentiment_score < -0.1:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        # Count sentiment distribution
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        for news in analyzed_news:
            sentiment_counts[news['sentiment']['label']] += 1
        
        return {
            'symbol': symbol,
            'analysis_period': f"{days} days",
            'total_articles': len(analyzed_news),
            'overall_sentiment': overall_sentiment,
            'sentiment_score': avg_sentiment_score,
            'sentiment_distribution': sentiment_counts,
            'articles': analyzed_news,
            'timestamp': datetime.now().isoformat()
        }

    def display_sentiment_analysis(self, analysis: Dict[str, Any]):
        """Display sentiment analysis results"""
        if not analysis:
            print("❌ No sentiment analysis available")
            return
        
        print(f"\n📰 NEWS SENTIMENT ANALYSIS: {analysis['symbol']}")
        print("=" * 50)
        print(f"📊 Analysis Period: {analysis['analysis_period']}")
        print(f"📰 Total Articles: {analysis['total_articles']}")
        print(f"🎯 Overall Sentiment: {analysis['overall_sentiment'].upper()}")
        print(f"📈 Sentiment Score: {analysis['sentiment_score']:.3f}")
        
        # Sentiment distribution
        dist = analysis['sentiment_distribution']
        print(f"\n📊 Sentiment Distribution:")
        print(f"  Positive: {dist['positive']} articles")
        print(f"  Negative: {dist['negative']} articles")
        print(f"  Neutral: {dist['neutral']} articles")
        
        # Recent articles
        print(f"\n📰 Recent Articles:")
        for i, article in enumerate(analysis['articles'][:5], 1):
            sentiment = article['sentiment']
            print(f"  {i}. {article['title'][:60]}...")
            print(f"     Sentiment: {sentiment['label']} ({sentiment['score']:.3f})")
            print(f"     Source: {article['source']}")
            print()

    def get_sentiment_trading_signal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Convert sentiment analysis to trading signal"""
        if not analysis:
            return None
        
        sentiment_score = analysis['sentiment_score']
        sentiment_label = analysis['overall_sentiment']
        
        # Convert sentiment to trading signal
        if sentiment_score > 0.2:
            signal = 'strong_buy'
            confidence = min(0.9, 0.6 + abs(sentiment_score))
        elif sentiment_score > 0.1:
            signal = 'buy'
            confidence = min(0.8, 0.5 + abs(sentiment_score))
        elif sentiment_score < -0.2:
            signal = 'strong_sell'
            confidence = min(0.9, 0.6 + abs(sentiment_score))
        elif sentiment_score < -0.1:
            signal = 'sell'
            confidence = min(0.8, 0.5 + abs(sentiment_score))
        else:
            signal = 'hold'
            confidence = 0.5
        
        return {
            'signal': signal,
            'confidence': confidence,
            'sentiment_score': sentiment_score,
            'reasoning': f"News sentiment analysis shows {sentiment_label} sentiment with score {sentiment_score:.3f}"
        }


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="News Sentiment Analyzer")
    parser.add_argument("--symbol", "-s", default="TSLA", help="Stock symbol to analyze")
    parser.add_argument("--days", "-d", type=int, default=7, help="Number of days to analyze")
    parser.add_argument("--output", "-o", help="Output file for analysis results")
    parser.add_argument("--signal", action="store_true", help="Generate trading signal")
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = NewsSentimentAnalyzer()
    
    # Analyze sentiment
    analysis = analyzer.analyze_news_sentiment(args.symbol, args.days)
    
    if analysis:
        # Display analysis
        analyzer.display_sentiment_analysis(analysis)
        
        # Generate trading signal if requested
        if args.signal:
            signal = analyzer.get_sentiment_trading_signal(analysis)
            if signal:
                print(f"\n🎯 TRADING SIGNAL:")
                print(f"  Signal: {signal['signal'].upper()}")
                print(f"  Confidence: {signal['confidence']:.1%}")
                print(f"  Reasoning: {signal['reasoning']}")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"\n💾 Analysis saved to {args.output}")
    else:
        print(f"❌ Could not analyze news sentiment for {args.symbol}")
        sys.exit(1)


if __name__ == "__main__":
    main()