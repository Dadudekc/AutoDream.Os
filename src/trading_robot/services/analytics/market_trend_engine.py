#!/usr/bin/env python3
"""
Trading BI Market Trend Analysis Engine
======================================

Market trend analysis engine for trading business intelligence analytics.
Handles trend detection, confidence calculation, and market prediction.
V2 COMPLIANT: Focused trend analysis under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR TREND ENGINE
@license MIT
"""

import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime

from .trading_bi_models import MarketTrend, TrendAnalysisConfig
from ...repositories.trading_repository import Trade


class MarketTrendEngine:
    """Market trend analysis engine for trading market analysis"""
    
    def __init__(self, config: Optional[TrendAnalysisConfig] = None):
        """Initialize market trend engine with configuration"""
        self.config = config or TrendAnalysisConfig()
    
    def analyze_market_trend(self, trades: List[Trade], symbol: str, timeframe: str = "medium") -> MarketTrend:
        """Analyze market trends using technical indicators"""
        try:
            if not trades or len(trades) < self.config.min_trades_for_analysis:
                return self._create_default_trend(symbol, timeframe)
            
            # Calculate trend direction and strength
            direction, strength = self._calculate_trend_direction(trades)
            confidence = self._calculate_trend_confidence(trades)
            predicted_change = self._calculate_predicted_change(trades, direction)
            
            return MarketTrend(
                direction=direction,
                strength=strength,
                confidence=confidence,
                predicted_change=predicted_change,
                timeframe=timeframe,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            # Return default trend on error
            return self._create_default_trend(symbol, timeframe)
    
    def _calculate_trend_direction(self, trades: List[Trade]) -> tuple[str, float]:
        """Calculate trend direction and strength"""
        if len(trades) < 2:
            return "sideways", 0.0
        
        # Sort trades by timestamp
        trades_sorted = sorted(trades, key=lambda x: x.timestamp)
        
        # Calculate price changes
        price_changes = []
        for i in range(1, len(trades_sorted)):
            prev_price = trades_sorted[i-1].price
            curr_price = trades_sorted[i].price
            if prev_price > 0:
                change = (curr_price - prev_price) / prev_price
                price_changes.append(change)
        
        if not price_changes:
            return "sideways", 0.0
        
        # Calculate average change and volatility
        avg_change = statistics.mean(price_changes)
        volatility = statistics.stdev(price_changes) if len(price_changes) > 1 else 0.0
        
        # Determine direction based on average change
        if avg_change > 0.01:  # 1% threshold
            direction = "bullish"
        elif avg_change < -0.01:  # -1% threshold
            direction = "bearish"
        else:
            direction = "sideways"
        
        # Calculate strength based on magnitude and consistency
        strength = min(abs(avg_change) * 10, 1.0)  # Scale to 0-1
        
        # Adjust strength based on volatility (lower volatility = higher strength)
        if volatility > 0:
            consistency_factor = max(0.1, 1.0 - (volatility * 5))
            strength *= consistency_factor
        
        return direction, strength
    
    def _calculate_trend_confidence(self, trades: List[Trade]) -> float:
        """Calculate confidence in trend analysis"""
        if len(trades) < self.config.min_trades_for_analysis:
            return 0.0
        
        # More trades = higher confidence (up to a point)
        trade_count_factor = min(len(trades) / 50, 1.0)  # Max at 50 trades
        
        # Calculate price consistency
        trades_sorted = sorted(trades, key=lambda x: x.timestamp)
        price_changes = []
        
        for i in range(1, len(trades_sorted)):
            prev_price = trades_sorted[i-1].price
            curr_price = trades_sorted[i].price
            if prev_price > 0:
                change = (curr_price - prev_price) / prev_price
                price_changes.append(change)
        
        if not price_changes:
            return 0.0
        
        # Calculate consistency (lower volatility = higher confidence)
        volatility = statistics.stdev(price_changes) if len(price_changes) > 1 else 0.0
        consistency_factor = max(0.1, 1.0 - (volatility * 10))
        
        # Combine factors
        confidence = (trade_count_factor + consistency_factor) / 2
        
        return min(confidence, 1.0)
    
    def _calculate_predicted_change(self, trades: List[Trade], direction: str) -> float:
        """Calculate predicted price change based on trend"""
        if len(trades) < 2:
            return 0.0
        
        trades_sorted = sorted(trades, key=lambda x: x.timestamp)
        
        # Calculate recent average change
        recent_trades = trades_sorted[-min(10, len(trades_sorted)):]  # Last 10 trades
        price_changes = []
        
        for i in range(1, len(recent_trades)):
            prev_price = recent_trades[i-1].price
            curr_price = recent_trades[i].price
            if prev_price > 0:
                change = (curr_price - prev_price) / prev_price
                price_changes.append(change)
        
        if not price_changes:
            return 0.0
        
        avg_change = statistics.mean(price_changes)
        
        # Apply direction-based prediction
        if direction == "bullish":
            return abs(avg_change) * 100  # Convert to percentage
        elif direction == "bearish":
            return -abs(avg_change) * 100  # Convert to percentage
        else:
            return avg_change * 100
    
    def _create_default_trend(self, symbol: str, timeframe: str) -> MarketTrend:
        """Create default trend when analysis fails"""
        return MarketTrend(
            direction="sideways",
            strength=0.0,
            confidence=0.0,
            predicted_change=0.0,
            timeframe=timeframe,
            timestamp=datetime.now()
        )
    
    def get_trend_summary(self, trends: List[MarketTrend]) -> Dict[str, Any]:
        """Get summary of multiple trend analyses"""
        if not trends:
            return {"error": "No trends provided"}
        
        # Calculate aggregate metrics
        bullish_count = sum(1 for t in trends if t.direction == "bullish")
        bearish_count = sum(1 for t in trends if t.direction == "bearish")
        sideways_count = sum(1 for t in trends if t.direction == "sideways")
        
        avg_strength = statistics.mean(t.strength for t in trends)
        avg_confidence = statistics.mean(t.confidence for t in trends)
        avg_predicted_change = statistics.mean(t.predicted_change for t in trends)
        
        # Determine overall market sentiment
        total_trends = len(trends)
        if bullish_count > total_trends * 0.6:
            overall_sentiment = "bullish"
        elif bearish_count > total_trends * 0.6:
            overall_sentiment = "bearish"
        else:
            overall_sentiment = "mixed"
        
        return {
            "overall_sentiment": overall_sentiment,
            "bullish_count": bullish_count,
            "bearish_count": bearish_count,
            "sideways_count": sideways_count,
            "avg_strength": avg_strength,
            "avg_confidence": avg_confidence,
            "avg_predicted_change": avg_predicted_change,
            "total_analyses": total_trends,
            "timestamp": datetime.now()
        }


# Factory function for dependency injection
def create_market_trend_engine(config: Optional[TrendAnalysisConfig] = None) -> MarketTrendEngine:
    """Factory function to create market trend engine with optional configuration"""
    return MarketTrendEngine(config)


# Export for DI
__all__ = ['MarketTrendEngine', 'create_market_trend_engine']
