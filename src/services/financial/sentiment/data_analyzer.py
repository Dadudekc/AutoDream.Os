"""
Data Analyzer Module - Sentiment Analysis Package

This module handles analysis of structured data sources including analyst ratings,
options flow data, and other market data. Extracted from MarketSentimentService
to improve maintainability and follow SRP principles.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

# Configure logging
logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Handles analysis of structured market data for sentiment analysis"""

    def __init__(self):
        # Rating score mappings
        self.rating_scores = {
            "strong_buy": 1.0,
            "buy": 0.7,
            "hold": 0.0,
            "sell": -0.7,
            "strong_sell": -1.0,
        }

        # Sentiment thresholds
        self.sentiment_thresholds = {
            "bullish": 0.5,
            "bearish": -0.5,
            "put_call_bullish": 0.5,
            "put_call_bearish": 2.0
        }

    def analyze_analyst_ratings(
        self, ratings_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from analyst ratings"""
        try:
            sentiment_data = []

            for rating in ratings_data:
                rating_type = rating.get("rating", "hold").lower()
                score = self.rating_scores.get(rating_type, 0.0)

                # Determine sentiment type
                if score > self.sentiment_thresholds["bullish"]:
                    sentiment_type = "BULLISH"
                elif score < self.sentiment_thresholds["bearish"]:
                    sentiment_type = "BEARISH"
                else:
                    sentiment_type = "NEUTRAL"

                # Calculate confidence based on analyst track record
                track_record = rating.get("analyst_track_record", 0.5)
                confidence = min(1.0, 0.6 + (track_record * 0.4))

                # Calculate weight based on price target and current price
                current_price = rating.get("current_price", 0)
                price_target = rating.get("price_target", 0)

                if current_price > 0 and price_target > 0:
                    price_change_pct = (price_target - current_price) / current_price
                    weight = 1.0 + abs(price_change_pct) * 2
                else:
                    weight = 1.0

                sentiment_data.append({
                    "source": "ANALYST_RATINGS",
                    "sentiment_type": sentiment_type,
                    "confidence": confidence,
                    "score": score,
                    "text": f"Analyst {rating.get('analyst', 'Unknown')}: {rating_type.upper()} - Target: ${price_target}",
                    "timestamp": datetime.fromisoformat(
                        rating.get("timestamp", datetime.now().isoformat())
                    ),
                    "symbol": rating.get("symbol", ""),
                    "weight": weight,
                    "metadata": {
                        "analyst": rating.get("analyst", "Unknown"),
                        "firm": rating.get("firm", "Unknown"),
                        "price_target": price_target,
                        "track_record": track_record,
                    },
                })

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing analyst ratings: {e}")
            return []

    def analyze_options_flow_sentiment(
        self, options_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from options flow data"""
        try:
            sentiment_data = []

            for option in options_data:
                # Calculate sentiment based on options flow
                call_volume = option.get("call_volume", 0)
                put_volume = option.get("put_volume", 0)
                total_volume = call_volume + put_volume

                if total_volume == 0:
                    continue

                # Calculate put-call ratio sentiment
                put_call_ratio = (
                    put_volume / call_volume if call_volume > 0 else float("inf")
                )

                # Lower put-call ratio indicates bullish sentiment
                if put_call_ratio < self.sentiment_thresholds["put_call_bullish"]:
                    sentiment_type = "BULLISH"
                    score = 0.8
                elif put_call_ratio > self.sentiment_thresholds["put_call_bearish"]:
                    sentiment_type = "BEARISH"
                    score = -0.8
                else:
                    sentiment_type = "NEUTRAL"
                    score = 0.0

                # Calculate confidence based on volume
                confidence = min(1.0, total_volume / 10000)

                # Calculate weight based on unusual activity
                unusual_activity = option.get("unusual_activity", False)
                weight = 1.5 if unusual_activity else 1.0

                sentiment_data.append({
                    "source": "OPTIONS_FLOW",
                    "sentiment_type": sentiment_type,
                    "confidence": confidence,
                    "score": score,
                    "text": f"Options Flow: Call Volume: {call_volume}, Put Volume: {put_volume}, PCR: {put_call_ratio:.2f}",
                    "timestamp": datetime.fromisoformat(
                        option.get("timestamp", datetime.now().isoformat())
                    ),
                    "symbol": option.get("symbol", ""),
                    "weight": weight,
                    "metadata": {
                        "call_volume": call_volume,
                        "put_volume": put_volume,
                        "put_call_ratio": put_call_ratio,
                        "unusual_activity": unusual_activity,
                        "strike": option.get("strike", 0),
                        "expiration": option.get("expiration", ""),
                    },
                })

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing options flow sentiment: {e}")
            return []

    def analyze_insider_trading_sentiment(
        self, insider_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from insider trading data"""
        try:
            sentiment_data = []

            for trade in insider_data:
                # Calculate sentiment based on trade type and size
                trade_type = trade.get("trade_type", "unknown").lower()
                trade_size = trade.get("trade_size", 0)
                current_price = trade.get("current_price", 0)

                # Determine sentiment based on trade type
                if trade_type in ["buy", "purchase"]:
                    sentiment_type = "BULLISH"
                    score = 0.7
                elif trade_type in ["sell", "sale"]:
                    sentiment_type = "BEARISH"
                    score = -0.7
                else:
                    sentiment_type = "NEUTRAL"
                    score = 0.0

                # Calculate confidence based on trade size
                confidence = min(1.0, trade_size / 100000)

                # Calculate weight based on trade significance
                weight = 1.0 + (trade_size / 1000000)

                sentiment_data.append({
                    "source": "INSIDER_TRADING",
                    "sentiment_type": sentiment_type,
                    "confidence": confidence,
                    "score": score,
                    "text": f"Insider {trade_type.upper()}: {trade_size} shares at ${current_price}",
                    "timestamp": datetime.fromisoformat(
                        trade.get("timestamp", datetime.now().isoformat())
                    ),
                    "symbol": trade.get("symbol", ""),
                    "weight": weight,
                    "metadata": {
                        "insider": trade.get("insider", "Unknown"),
                        "trade_type": trade_type,
                        "trade_size": trade_size,
                        "current_price": current_price,
                        "filing_date": trade.get("filing_date", ""),
                    },
                })

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing insider trading sentiment: {e}")
            return []

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of data analysis capabilities"""
        return {
            "supported_data_sources": [
                "analyst_ratings", "options_flow", "insider_trading"
            ],
            "rating_score_mappings": self.rating_scores,
            "sentiment_thresholds": self.sentiment_thresholds,
            "analysis_methods": ["rating_based", "volume_based", "activity_based"]
        }

