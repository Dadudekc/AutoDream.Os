#!/usr/bin/env python3
"""
Trading Robot Strategies - Trading Strategy Implementations
===========================================================

Trading strategies extracted from trading_robot.py for V2 compliance.
Contains all trading strategy classes and market analysis algorithms.

Author: Agent-7 (Integration Specialist)
License: MIT
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional


class TradingStrategy:
    """Base class for trading strategies."""
    
    def __init__(self, name: str, description: str):
        """Initialize the trading strategy."""
        self.name = name
        self.description = description
        self.enabled = False
        self.positions = []
        self.performance = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0
        }
        
    def analyze(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Analyze market data and return trading signal.
        
        Args:
            data: Market data dictionary
            
        Returns:
            Trading signal: 'buy', 'sell', or None
        """
        raise NotImplementedError("Subclasses must implement analyze method")
        
    def execute_trade(self, action: str, price: float, quantity: int) -> bool:
        """
        Execute a trade and update performance metrics.
        
        Args:
            action: 'buy' or 'sell'
            price: Execution price
            quantity: Number of shares
            
        Returns:
            True if trade was successful
        """
        try:
            # Record the trade
            trade = {
                'action': action,
                'price': price,
                'quantity': quantity,
                'timestamp': pd.Timestamp.now()
            }
            self.positions.append(trade)
            
            # Update performance metrics
            self.performance['total_trades'] += 1
            
            # Calculate P&L (simplified)
            if action == 'sell' and len(self.positions) > 1:
                # Find matching buy position
                buy_positions = [p for p in self.positions if p['action'] == 'buy']
                if buy_positions:
                    buy_price = buy_positions[-1]['price']
                    pnl = (price - buy_price) * quantity
                    self.performance['total_pnl'] += pnl
                    
                    if pnl > 0:
                        self.performance['winning_trades'] += 1
                    else:
                        self.performance['losing_trades'] += 1
                        
            # Update win rate
            if self.performance['total_trades'] > 0:
                self.performance['win_rate'] = (
                    self.performance['winning_trades'] / 
                    self.performance['total_trades']
                )
                
            return True
            
        except Exception as e:
            print(f"Trade execution error: {e}")
            return False
            
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for the strategy."""
        return {
            'name': self.name,
            'enabled': self.enabled,
            'performance': self.performance.copy(),
            'active_positions': len([p for p in self.positions if p['action'] == 'buy'])
        }


class MovingAverageStrategy(TradingStrategy):
    """Moving Average Crossover Strategy."""
    
    def __init__(self):
        """Initialize the moving average strategy."""
        super().__init__(
            "Moving Average Crossover",
            "Buy when short MA crosses above long MA, sell when it crosses below"
        )
        self.short_period = 10
        self.long_period = 30
        self.price_history = []
        
    def analyze(self, data: Dict[str, Any]) -> Optional[str]:
        """Analyze using moving average crossover."""
        if not data or 'price' not in data:
            return None
            
        current_price = data['price']
        self.price_history.append(current_price)
        
        # Keep only recent history
        if len(self.price_history) > self.long_period * 2:
            self.price_history = self.price_history[-self.long_period * 2:]
            
        if len(self.price_history) < self.long_period:
            return None
            
        # Calculate moving averages
        short_ma = np.mean(self.price_history[-self.short_period:])
        long_ma = np.mean(self.price_history[-self.long_period:])
        
        # Previous values for crossover detection
        if len(self.price_history) >= self.long_period + 1:
            prev_short_ma = np.mean(self.price_history[-self.short_period-1:-1])
            prev_long_ma = np.mean(self.price_history[-self.long_period-1:-1])
            
            # Check for crossover
            if prev_short_ma <= prev_long_ma and short_ma > long_ma:
                return 'buy'  # Bullish crossover
            elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
                return 'sell'  # Bearish crossover
                
        return None


class RSIMeanReversionStrategy(TradingStrategy):
    """RSI Mean Reversion Strategy."""
    
    def __init__(self):
        """Initialize the RSI strategy."""
        super().__init__(
            "RSI Mean Reversion",
            "Buy when RSI is oversold (<30), sell when overbought (>70)"
        )
        self.rsi_period = 14
        self.oversold_threshold = 30
        self.overbought_threshold = 70
        self.price_history = []
        
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI
            
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    def analyze(self, data: Dict[str, Any]) -> Optional[str]:
        """Analyze using RSI mean reversion."""
        if not data or 'price' not in data:
            return None
            
        current_price = data['price']
        self.price_history.append(current_price)
        
        # Keep only recent history
        if len(self.price_history) > self.rsi_period * 3:
            self.price_history = self.price_history[-self.rsi_period * 3:]
            
        if len(self.price_history) < self.rsi_period + 1:
            return None
            
        # Calculate RSI
        rsi = self.calculate_rsi(self.price_history, self.rsi_period)
        
        # Generate signals
        if rsi < self.oversold_threshold:
            return 'buy'  # Oversold - potential buy signal
        elif rsi > self.overbought_threshold:
            return 'sell'  # Overbought - potential sell signal
            
        return None


class BollingerBandsStrategy(TradingStrategy):
    """Bollinger Bands Strategy."""
    
    def __init__(self):
        """Initialize the Bollinger Bands strategy."""
        super().__init__(
            "Bollinger Bands",
            "Buy when price touches lower band, sell when it touches upper band"
        )
        self.period = 20
        self.std_dev = 2.0
        self.price_history = []
        
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: float = 2.0) -> Dict[str, float]:
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return {'upper': 0, 'middle': 0, 'lower': 0}
            
        recent_prices = prices[-period:]
        middle = np.mean(recent_prices)
        std = np.std(recent_prices)
        
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        
        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }
        
    def analyze(self, data: Dict[str, Any]) -> Optional[str]:
        """Analyze using Bollinger Bands."""
        if not data or 'price' not in data:
            return None
            
        current_price = data['price']
        self.price_history.append(current_price)
        
        # Keep only recent history
        if len(self.price_history) > self.period * 2:
            self.price_history = self.price_history[-self.period * 2:]
            
        if len(self.price_history) < self.period:
            return None
            
        # Calculate Bollinger Bands
        bands = self.calculate_bollinger_bands(
            self.price_history, 
            self.period, 
            self.std_dev
        )
        
        # Generate signals
        if current_price <= bands['lower']:
            return 'buy'  # Price at lower band - potential buy
        elif current_price >= bands['upper']:
            return 'sell'  # Price at upper band - potential sell
            
        return None


class MomentumStrategy(TradingStrategy):
    """Momentum-based trading strategy."""
    
    def __init__(self):
        """Initialize the momentum strategy."""
        super().__init__(
            "Momentum Strategy",
            "Buy on strong upward momentum, sell on downward momentum"
        )
        self.lookback_period = 5
        self.momentum_threshold = 0.02  # 2% momentum threshold
        self.price_history = []
        
    def analyze(self, data: Dict[str, Any]) -> Optional[str]:
        """Analyze using momentum."""
        if not data or 'price' not in data:
            return None
            
        current_price = data['price']
        self.price_history.append(current_price)
        
        # Keep only recent history
        if len(self.price_history) > self.lookback_period * 2:
            self.price_history = self.price_history[-self.lookback_period * 2:]
            
        if len(self.price_history) < self.lookback_period:
            return None
            
        # Calculate momentum
        old_price = self.price_history[-self.lookback_period]
        momentum = (current_price - old_price) / old_price
        
        # Generate signals
        if momentum > self.momentum_threshold:
            return 'buy'  # Strong upward momentum
        elif momentum < -self.momentum_threshold:
            return 'sell'  # Strong downward momentum
            
        return None


class StrategyManager:
    """Manages multiple trading strategies."""
    
    def __init__(self):
        """Initialize the strategy manager."""
        self.strategies = {}
        self.voting_enabled = True
        self.vote_threshold = 0.6  # 60% agreement required
        
    def add_strategy(self, strategy: TradingStrategy):
        """Add a strategy to the manager."""
        self.strategies[strategy.name] = strategy
        
    def remove_strategy(self, name: str):
        """Remove a strategy from the manager."""
        if name in self.strategies:
            del self.strategies[name]
            
    def get_strategy(self, name: str) -> Optional[TradingStrategy]:
        """Get a strategy by name."""
        return self.strategies.get(name)
        
    def get_all_strategies(self) -> List[TradingStrategy]:
        """Get all strategies."""
        return list(self.strategies.values())
        
    def get_enabled_strategies(self) -> List[TradingStrategy]:
        """Get all enabled strategies."""
        return [s for s in self.strategies.values() if s.enabled]
        
    def analyze_market(self, data: Dict[str, Any]) -> Optional[str]:
        """Analyze market using all enabled strategies."""
        enabled_strategies = self.get_enabled_strategies()
        
        if not enabled_strategies:
            return None
            
        # Collect signals from all strategies
        signals = []
        for strategy in enabled_strategies:
            signal = strategy.analyze(data)
            if signal:
                signals.append(signal)
                
        if not signals:
            return None
            
        # If voting is enabled, use majority vote
        if self.voting_enabled:
            buy_votes = signals.count('buy')
            sell_votes = signals.count('sell')
            total_votes = len(signals)
            
            buy_ratio = buy_votes / total_votes
            sell_ratio = sell_votes / total_votes
            
            if buy_ratio >= self.vote_threshold:
                return 'buy'
            elif sell_ratio >= self.vote_threshold:
                return 'sell'
        else:
            # Return the first signal
            return signals[0]
            
        return None
        
    def get_strategy_performance(self) -> Dict[str, Any]:
        """Get performance summary for all strategies."""
        performance = {}
        for name, strategy in self.strategies.items():
            performance[name] = strategy.get_performance_summary()
        return performance
        
    def reset_all_performance(self):
        """Reset performance metrics for all strategies."""
        for strategy in self.strategies.values():
            strategy.performance = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0
            }
            strategy.positions = []




