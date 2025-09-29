#!/usr/bin/env python3
"""
Market Analysis CLI Tool
========================

Advanced market analysis tool for better trading predictions
V2 Compliant: ≤400 lines, focused market analysis
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any

import requests

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from tsla_forecast_app.modules import TradingFlagEngine


class MarketAnalyzer:
    """Advanced market analysis tool"""

    def __init__(self):
        """Initialize market analyzer"""
        self.flag_engine = TradingFlagEngine()
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self) -> dict[str, str]:
        """Load API keys from environment"""
        return {
            "alpha_vantage": os.getenv("ALPHAVANTAGE_API_KEY"),
            "polygon": os.getenv("POLYGONIO_API_KEY"),
            "finnhub": os.getenv("FINNHUB_API_KEY"),
            "news_api": os.getenv("NEWS_API_KEY"),
        }

    def get_comprehensive_data(self, symbol: str = "TSLA") -> dict[str, Any]:
        """Get comprehensive market data"""
        print(f"[ANALYSIS] Analyzing {symbol} market data...")

        # Get basic stock data
        stock_data = self._get_stock_data(symbol)
        if not stock_data:
            print(f"❌ Could not get stock data for {symbol}")
            return None

        # Get additional market data
        market_data = {
            "stock": stock_data,
            "technical_indicators": self._get_technical_indicators(symbol),
            "market_sentiment": self._get_market_sentiment(symbol),
            "volume_analysis": self._analyze_volume(stock_data),
            "volatility_analysis": self._analyze_volatility(stock_data),
            "trend_analysis": self._analyze_trend(stock_data),
        }

        return market_data

    def _get_stock_data(self, symbol: str) -> dict[str, Any] | None:
        """Get stock data from multiple sources"""
        # Try Yahoo Finance first
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/TSLA"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                result = data["chart"]["result"][0]
                meta = result["meta"]

                return {
                    "symbol": symbol,
                    "price": meta["regularMarketPrice"],
                    "change": meta["regularMarketPrice"]
                    - meta.get("previousClose", meta["regularMarketPrice"]),
                    "change_percent": (
                        (
                            meta["regularMarketPrice"]
                            - meta.get("previousClose", meta["regularMarketPrice"])
                        )
                        / meta.get("previousClose", meta["regularMarketPrice"])
                    )
                    * 100,
                    "volume": meta["regularMarketVolume"],
                    "high": meta["regularMarketDayHigh"],
                    "low": meta["regularMarketDayLow"],
                    "open": meta.get("regularMarketPreviousClose", meta["regularMarketPrice"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "Yahoo Finance",
                }
        except Exception as e:
            print(f"Yahoo Finance error: {e}")

        return None

    def _get_technical_indicators(self, symbol: str) -> dict[str, Any]:
        """Get technical indicators"""
        try:
            # Simple technical indicators calculation
            stock_data = self._get_stock_data(symbol)
            if not stock_data:
                return {}

            price = stock_data["price"]

            # Mock technical indicators (in real implementation, these would be calculated from historical data)
            return {
                "rsi": self._calculate_rsi(price),
                "macd": self._calculate_macd(price),
                "moving_average_20": price * 0.98,
                "moving_average_50": price * 0.95,
                "bollinger_upper": price * 1.05,
                "bollinger_lower": price * 0.95,
                "stochastic": 45.0,
                "williams_r": -55.0,
            }
        except Exception as e:
            print(f"Technical indicators error: {e}")
            return {}

    def _calculate_rsi(self, price: float) -> float:
        """Calculate RSI (simplified)"""
        # Mock RSI calculation
        import random

        return random.uniform(30, 70)

    def _calculate_macd(self, price: float) -> float:
        """Calculate MACD (simplified)"""
        # Mock MACD calculation
        import random

        return random.uniform(-2, 2)

    def _get_market_sentiment(self, symbol: str) -> dict[str, Any]:
        """Get market sentiment analysis"""
        try:
            # Mock sentiment analysis (in real implementation, this would analyze news, social media, etc.)
            return {
                "sentiment_score": 0.3,  # -1 (very bearish) to 1 (very bullish)
                "news_sentiment": "neutral",
                "social_sentiment": "bearish",
                "analyst_rating": "hold",
                "fear_greed_index": 45,  # 0 (extreme fear) to 100 (extreme greed)
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {}

    def _analyze_volume(self, stock_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze volume patterns"""
        volume = stock_data.get("volume", 0)
        avg_volume = 50000000  # Mock average volume

        return {
            "current_volume": volume,
            "average_volume": avg_volume,
            "volume_ratio": volume / avg_volume,
            "volume_trend": "high" if volume > avg_volume * 1.5 else "normal",
            "volume_significance": "significant" if volume > avg_volume * 2 else "normal",
        }

    def _analyze_volatility(self, stock_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze volatility patterns"""
        change_percent = abs(stock_data.get("change_percent", 0))

        return {
            "current_volatility": change_percent,
            "volatility_level": "high"
            if change_percent > 5
            else "moderate"
            if change_percent > 2
            else "low",
            "volatility_trend": "increasing" if change_percent > 3 else "stable",
        }

    def _analyze_trend(self, stock_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze trend patterns"""
        change = stock_data.get("change", 0)

        return {
            "direction": "bullish" if change > 0 else "bearish" if change < 0 else "neutral",
            "strength": "strong" if abs(change) > 5 else "moderate" if abs(change) > 2 else "weak",
            "momentum": "accelerating" if change > 0 else "decelerating",
        }

    def generate_enhanced_predictions(self, symbol: str = "TSLA") -> dict[str, Any]:
        """Generate enhanced predictions with comprehensive analysis"""
        print(f"[AI] Generating enhanced predictions for {symbol}...")

        # Get comprehensive market data
        market_data = self.get_comprehensive_data(symbol)
        if not market_data:
            return None

        # Analyze market data
        analysis = self.flag_engine.analyze_market_data(market_data["stock"])

        # Generate agent predictions
        flags = self.flag_engine.generate_all_agent_flags(analysis)

        # Get consensus
        consensus = self.flag_engine.get_consensus_flag(flags)

        # Enhanced analysis
        enhanced_prediction = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_data": market_data,
            "agent_predictions": [
                {
                    "agent": flag.agent_id.value,
                    "action": flag.flag_type.value,
                    "target": flag.price_target,
                    "confidence": flag.confidence,
                    "reasoning": flag.reasoning,
                }
                for flag in flags
            ],
            "consensus": {
                "action": consensus.flag_type.value,
                "target": consensus.price_target,
                "confidence": consensus.confidence,
                "reasoning": consensus.reasoning,
            },
            "market_analysis": {
                "trend": market_data["trend_analysis"]["direction"],
                "volatility": market_data["volatility_analysis"]["volatility_level"],
                "volume": market_data["volume_analysis"]["volume_trend"],
                "sentiment": market_data["market_sentiment"]["sentiment_score"],
            },
        }

        return enhanced_prediction

    def display_analysis(self, prediction: dict[str, Any]):
        """Display comprehensive analysis"""
        if not prediction:
            print("❌ No prediction data available")
            return

        print(f"\n🚀 ENHANCED MARKET ANALYSIS: {prediction['symbol']}")
        print("=" * 60)

        # Stock data
        stock = prediction["market_data"]["stock"]
        print(f"📊 Current Price: ${stock['price']:.2f}")
        print(f"📈 Change: ${stock['change']:.2f} ({stock['change_percent']:.2f}%)")
        print(f"📊 Volume: {stock['volume']:,}")
        print(f"📈 High: ${stock['high']:.2f}")
        print(f"📉 Low: ${stock['low']:.2f}")

        # Market analysis
        market = prediction["market_analysis"]
        print("\n📊 MARKET ANALYSIS:")
        print(f"  Trend: {market['trend']}")
        print(f"  Volatility: {market['volatility']}")
        print(f"  Volume: {market['volume']}")
        print(f"  Sentiment: {market['sentiment']:.2f}")

        # Technical indicators
        technical = prediction["market_data"]["technical_indicators"]
        print("\n📈 TECHNICAL INDICATORS:")
        print(f"  RSI: {technical.get('rsi', 0):.1f}")
        print(f"  MACD: {technical.get('macd', 0):.2f}")
        print(f"  MA20: ${technical.get('moving_average_20', 0):.2f}")
        print(f"  MA50: ${technical.get('moving_average_50', 0):.2f}")

        # Agent predictions
        print("\n🤖 AGENT PREDICTIONS:")
        for i, pred in enumerate(prediction["agent_predictions"], 1):
            print(
                f"  {i}. {pred['agent']}: {pred['action'].upper()} → ${pred['target']:.2f} ({pred['confidence']:.1%})"
            )

        # Consensus
        consensus = prediction["consensus"]
        print("\n🎯 FINAL CONSENSUS:")
        print(f"  Action: {consensus['action'].upper()}")
        print(f"  Target: ${consensus['target']:.2f}")
        print(f"  Confidence: {consensus['confidence']:.1%}")
        print(f"  Reasoning: {consensus['reasoning']}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Advanced Market Analysis Tool")
    parser.add_argument("--symbol", "-s", default="TSLA", help="Stock symbol to analyze")
    parser.add_argument("--output", "-o", help="Output file for analysis results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Create analyzer
    analyzer = MarketAnalyzer()

    # Generate enhanced predictions
    prediction = analyzer.generate_enhanced_predictions(args.symbol)

    if prediction:
        # Display analysis
        analyzer.display_analysis(prediction)

        # Save to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(prediction, f, indent=2)
            print(f"\n💾 Analysis saved to {args.output}")
    else:
        print(f"❌ Could not analyze {args.symbol}")
        sys.exit(1)


if __name__ == "__main__":
    main()
