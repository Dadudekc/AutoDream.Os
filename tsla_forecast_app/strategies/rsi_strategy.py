#!/usr/bin/env python3
"""
RSI Mean Reversion Strategy - V2 Compliant
==========================================

RSI Mean Reversion trading strategy following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import numpy as np
from typing import Dict, Any, List
from .base_strategy import TradingStrategy


class RSIMeanReversionStrategy(TradingStrategy):
    """RSI Mean Reversion Strategy."""
    
    def __init__(self):
        """Initialize RSI Mean Reversion strategy."""
        super().__init__(
            "RSI Mean Reversion", 
            "Buy when RSI < 30, Sell when RSI > 70"
        )
        self.price_history: List[float] = []
        self.rsi_period = 14
        self.oversold_threshold = 30
        self.overbought_threshold = 70
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return 50
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using RSI mean reversion."""
        current_price = data['current_price']
        self.price_history.append(current_price)
        
        if len(self.price_history) < self.rsi_period + 1:
            return {
                'action': 'HOLD', 
                'confidence': 0.0, 
                'reason': 'Insufficient data for RSI'
            }
        
        rsi = self.calculate_rsi(self.price_history, self.rsi_period)
        
        if rsi < self.oversold_threshold:
            return {
                'action': 'BUY', 
                'confidence': 0.9, 
                'reason': f'RSI oversold: {rsi:.1f}'
            }
        elif rsi > self.overbought_threshold:
            return {
                'action': 'SELL', 
                'confidence': 0.9, 
                'reason': f'RSI overbought: {rsi:.1f}'
            }
        
        return {
            'action': 'HOLD', 
            'confidence': 0.5, 
            'reason': f'RSI neutral: {rsi:.1f}'
        }
    
    def set_parameters(self, period: int, oversold: int, overbought: int) -> None:
        """Set strategy parameters."""
        self.rsi_period = period
        self.oversold_threshold = oversold
        self.overbought_threshold = overbought
    
    def get_current_rsi(self) -> float:
        """Get current RSI value."""
        if len(self.price_history) < self.rsi_period + 1:
            return 50
        
        return self.calculate_rsi(self.price_history, self.rsi_period)
    
    def get_rsi_status(self) -> str:
        """Get RSI status description."""
        rsi = self.get_current_rsi()
        
        if rsi < self.oversold_threshold:
            return "Oversold"
        elif rsi > self.overbought_threshold:
            return "Overbought"
        else:
            return "Neutral"