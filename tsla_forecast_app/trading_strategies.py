"""
Trading Strategy Engine
V2 Compliant trading strategy implementation
"""

import numpy as np
from typing import List, Optional
from .trading_models import MarketData, TradingSignal, TradingMetrics


class TradingStrategy:
    """Base trading strategy class"""
    
    def __init__(self, name: str):
        """Initialize strategy"""
        self.name = name
        self.parameters = {}
        
    def calculate_signal(self, market_data: List[MarketData]) -> TradingSignal:
        """Calculate trading signal"""
        raise NotImplementedError
        
    def update_parameters(self, params: dict):
        """Update strategy parameters"""
        self.parameters.update(params)


class MovingAverageStrategy(TradingStrategy):
    """Moving average crossover strategy"""
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        """Initialize MA strategy"""
        super().__init__("Moving Average Crossover")
        self.short_window = short_window
        self.long_window = long_window
        
    def calculate_signal(self, market_data: List[MarketData]) -> TradingSignal:
        """Calculate MA crossover signal"""
        if len(market_data) < self.long_window:
            return TradingSignal.HOLD
            
        prices = [data.close for data in market_data[-self.long_window:]]
        
        short_ma = np.mean(prices[-self.short_window:])
        long_ma = np.mean(prices)
        
        if short_ma > long_ma:
            return TradingSignal.BUY
        elif short_ma < long_ma:
            return TradingSignal.SELL
        else:
            return TradingSignal.HOLD


class RSITradingStrategy(TradingStrategy):
    """RSI-based trading strategy"""
    
    def __init__(self, rsi_period: int = 14, oversold: float = 30, overbought: float = 70):
        """Initialize RSI strategy"""
        super().__init__("RSI Strategy")
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_signal(self, market_data: List[MarketData]) -> TradingSignal:
        """Calculate RSI signal"""
        if len(market_data) < self.rsi_period + 1:
            return TradingSignal.HOLD
            
        prices = [data.close for data in market_data[-self.rsi_period-1:]]
        rsi = self._calculate_rsi(prices)
        
        if rsi < self.oversold:
            return TradingSignal.BUY
        elif rsi > self.overbought:
            return TradingSignal.SELL
        else:
            return TradingSignal.HOLD
    
    def _calculate_rsi(self, prices: List[float]) -> float:
        """Calculate RSI indicator"""
        if len(prices) < 2:
            return 50.0
            
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100.0
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
