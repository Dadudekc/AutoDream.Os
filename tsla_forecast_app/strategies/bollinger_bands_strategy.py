#!/usr/bin/env python3
"""
Bollinger Bands Strategy - V2 Compliant
=======================================

Bollinger Bands trading strategy following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from .base_strategy import TradingStrategy


class BollingerBandsStrategy(TradingStrategy):
    """Bollinger Bands Strategy."""
    
    def __init__(self):
        """Initialize Bollinger Bands strategy."""
        super().__init__(
            "Bollinger Bands", 
            "Buy when price touches lower band, Sell when price touches upper band"
        )
        self.price_history: List[float] = []
        self.bb_period = 20
        self.bb_std = 2
        self.touch_threshold = 0.01  # 1% threshold for band touch
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: int = 2) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return None, None, None
        
        sma = np.mean(prices[-period:])
        std = np.std(prices[-period:])
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using Bollinger Bands."""
        current_price = data['current_price']
        self.price_history.append(current_price)
        
        if len(self.price_history) < self.bb_period:
            return {
                'action': 'HOLD', 
                'confidence': 0.0, 
                'reason': 'Insufficient data for Bollinger Bands'
            }
        
        upper, middle, lower = self.calculate_bollinger_bands(
            self.price_history, self.bb_period, self.bb_std
        )
        
        if upper is None or lower is None:
            return {
                'action': 'HOLD', 
                'confidence': 0.0, 
                'reason': 'Unable to calculate Bollinger Bands'
            }
        
        # Check for band touches with threshold
        lower_threshold = lower * (1 + self.touch_threshold)
        upper_threshold = upper * (1 - self.touch_threshold)
        
        if current_price <= lower_threshold:
            return {
                'action': 'BUY', 
                'confidence': 0.85, 
                'reason': f'Price at lower band: ${current_price:.2f} <= ${lower:.2f}'
            }
        elif current_price >= upper_threshold:
            return {
                'action': 'SELL', 
                'confidence': 0.85, 
                'reason': f'Price at upper band: ${current_price:.2f} >= ${upper:.2f}'
            }
        
        return {
            'action': 'HOLD', 
            'confidence': 0.5, 
            'reason': f'Price within bands: ${lower:.2f} < ${current_price:.2f} < ${upper:.2f}'
        }
    
    def set_parameters(self, period: int, std_dev: int, touch_threshold: float) -> None:
        """Set strategy parameters."""
        self.bb_period = period
        self.bb_std = std_dev
        self.touch_threshold = touch_threshold
    
    def get_current_bands(self) -> Dict[str, float]:
        """Get current Bollinger Bands values."""
        if len(self.price_history) < self.bb_period:
            return {}
        
        upper, middle, lower = self.calculate_bollinger_bands(
            self.price_history, self.bb_period, self.bb_std
        )
        
        if upper is None or lower is None:
            return {}
        
        return {
            'upper_band': upper,
            'middle_band': middle,
            'lower_band': lower,
            'current_price': self.price_history[-1],
            'band_width': upper - lower
        }
    
    def get_band_position(self) -> float:
        """Get current position within bands (0-1 scale)."""
        bands = self.get_current_bands()
        if not bands:
            return 0.5
        
        current_price = bands['current_price']
        lower_band = bands['lower_band']
        upper_band = bands['upper_band']
        
        if upper_band == lower_band:
            return 0.5
        
        return (current_price - lower_band) / (upper_band - lower_band)