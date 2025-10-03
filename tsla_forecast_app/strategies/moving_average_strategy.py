#!/usr/bin/env python3
"""
Moving Average Crossover Strategy - V2 Compliant
===============================================

Moving Average Crossover trading strategy following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import numpy as np
from typing import Dict, Any, List
from .base_strategy import TradingStrategy


class MovingAverageStrategy(TradingStrategy):
    """Moving Average Crossover Strategy."""
    
    def __init__(self):
        """Initialize Moving Average strategy."""
        super().__init__(
            "Moving Average Crossover", 
            "Buy when short MA crosses above long MA"
        )
        self.short_period = 10
        self.long_period = 30
        self.price_history: List[float] = []
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using moving average crossover."""
        current_price = data['current_price']
        self.price_history.append(current_price)
        
        # Keep only last 50 prices
        if len(self.price_history) > 50:
            self.price_history = self.price_history[-50:]
        
        if len(self.price_history) < self.long_period:
            return {
                'action': 'HOLD', 
                'confidence': 0.0, 
                'reason': 'Insufficient data'
            }
        
        # Calculate moving averages
        short_ma = np.mean(self.price_history[-self.short_period:])
        long_ma = np.mean(self.price_history[-self.long_period:])
        prev_short_ma = np.mean(self.price_history[-self.short_period-1:-1])
        prev_long_ma = np.mean(self.price_history[-self.long_period-1:-1])
        
        # Check for crossover
        if prev_short_ma <= prev_long_ma and short_ma > long_ma:
            return {
                'action': 'BUY', 
                'confidence': 0.8, 
                'reason': f'Golden Cross: MA{self.short_period} > MA{self.long_period}'
            }
        elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
            return {
                'action': 'SELL', 
                'confidence': 0.8, 
                'reason': f'Death Cross: MA{self.short_period} < MA{self.long_period}'
            }
        
        return {
            'action': 'HOLD', 
            'confidence': 0.5, 
            'reason': f'MA{self.short_period}={short_ma:.2f}, MA{self.long_period}={long_ma:.2f}'
        }
    
    def set_parameters(self, short_period: int, long_period: int) -> None:
        """Set strategy parameters."""
        self.short_period = short_period
        self.long_period = long_period
    
    def get_current_indicators(self) -> Dict[str, float]:
        """Get current indicator values."""
        if len(self.price_history) < self.long_period:
            return {}
        
        short_ma = np.mean(self.price_history[-self.short_period:])
        long_ma = np.mean(self.price_history[-self.long_period:])
        
        return {
            'short_ma': short_ma,
            'long_ma': long_ma,
            'current_price': self.price_history[-1]
        }