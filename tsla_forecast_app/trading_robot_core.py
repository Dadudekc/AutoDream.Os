#!/usr/bin/env python3
"""
Trading Robot Core - V2 Compliant
=================================

Core trading robot functionality following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

from strategies import (
    MovingAverageStrategy, 
    RSIMeanReversionStrategy, 
    BollingerBandsStrategy
)

# Load environment variables
load_dotenv()


class TradingRobotCore:
    """Core trading robot functionality."""
    
    def __init__(self):
        """Initialize trading robot core."""
        self.stock_data = {}
        self.portfolio = {
            'cash': 100000.0,  # Starting cash
            'shares': 0,
            'total_value': 100000.0,
            'trades': [],
            'daily_pnl': 0.0,
            'total_pnl': 0.0
        }
        self.strategies = {
            'ma_crossover': MovingAverageStrategy(),
            'rsi_mean_reversion': RSIMeanReversionStrategy(),
            'bollinger_bands': BollingerBandsStrategy()
        }
        self.active_strategies = []
        self.trading_enabled = False
        self.risk_management = {
            'max_position_size': 0.1,  # 10% of portfolio
            'stop_loss_pct': 0.05,     # 5% stop loss
            'take_profit_pct': 0.10,   # 10% take profit
            'max_daily_loss': 0.02     # 2% max daily loss
        }
        self.data_worker_thread = None
        self.running = False
    
    def start_data_worker(self):
        """Start data collection worker thread."""
        if self.data_worker_thread is None or not self.data_worker_thread.is_alive():
            self.running = True
            self.data_worker_thread = threading.Thread(target=self._data_worker)
            self.data_worker_thread.daemon = True
            self.data_worker_thread.start()
    
    def stop_data_worker(self):
        """Stop data collection worker thread."""
        self.running = False
        if self.data_worker_thread:
            self.data_worker_thread.join(timeout=5)
    
    def _data_worker(self):
        """Data collection worker thread."""
        while self.running:
            try:
                self._fetch_stock_data()
                if self.trading_enabled:
                    self._process_trading_signals()
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"Data worker error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _fetch_stock_data(self):
        """Fetch current stock data."""
        try:
            # Simulate stock data (replace with real API)
            current_price = 250.0 + (time.time() % 100) - 50  # Simulate price movement
            
            self.stock_data = {
                'symbol': 'TSLA',
                'current_price': current_price,
                'timestamp': datetime.now(),
                'volume': 1000000,
                'change': current_price - 250.0,
                'change_percent': ((current_price - 250.0) / 250.0) * 100
            }
            
            # Update portfolio value
            self._update_portfolio_value()
            
        except Exception as e:
            print(f"Error fetching stock data: {e}")
    
    def _update_portfolio_value(self):
        """Update portfolio total value."""
        if 'current_price' in self.stock_data:
            stock_value = self.portfolio['shares'] * self.stock_data['current_price']
            self.portfolio['total_value'] = self.portfolio['cash'] + stock_value
    
    def _process_trading_signals(self):
        """Process trading signals from active strategies."""
        if not self.stock_data:
            return
        
        for strategy_name, strategy in self.strategies.items():
            if strategy.enabled and strategy_name in self.active_strategies:
                try:
                    signal = strategy.analyze(self.stock_data)
                    if signal['action'] != 'HOLD':
                        self._execute_trade_signal(strategy_name, signal)
                except Exception as e:
                    print(f"Error processing signal from {strategy_name}: {e}")
    
    def _execute_trade_signal(self, strategy_name: str, signal: Dict[str, Any]):
        """Execute trade based on signal."""
        action = signal['action']
        confidence = signal['confidence']
        reason = signal['reason']
        
        # Risk management checks
        if not self._risk_check_passed(action, confidence):
            return
        
        current_price = self.stock_data['current_price']
        quantity = self._calculate_position_size(action, current_price)
        
        if quantity <= 0:
            return
        
        # Execute trade
        trade = {
            'timestamp': datetime.now(),
            'action': action,
            'price': current_price,
            'quantity': quantity,
            'strategy': strategy_name,
            'reason': reason,
            'confidence': confidence
        }
        
        if action == 'BUY':
            cost = current_price * quantity
            if cost <= self.portfolio['cash']:
                self.portfolio['cash'] -= cost
                self.portfolio['shares'] += quantity
                trade['profit'] = 0  # Will be calculated on sell
            else:
                return  # Insufficient funds
        
        elif action == 'SELL':
            if quantity <= self.portfolio['shares']:
                proceeds = current_price * quantity
                self.portfolio['cash'] += proceeds
                self.portfolio['shares'] -= quantity
                
                # Calculate profit (simplified)
                trade['profit'] = proceeds - (quantity * 250.0)  # Assume avg buy price
                self.portfolio['total_pnl'] += trade['profit']
        
        self.portfolio['trades'].append(trade)
        self._update_portfolio_value()
        
        # Update strategy performance
        self.strategies[strategy_name].update_performance(trade)
    
    def _risk_check_passed(self, action: str, confidence: float) -> bool:
        """Check if trade passes risk management rules."""
        # Check daily loss limit
        if self.portfolio['daily_pnl'] < -self.portfolio['total_value'] * self.risk_management['max_daily_loss']:
            return False
        
        # Check confidence threshold
        if confidence < 0.7:
            return False
        
        return True
    
    def _calculate_position_size(self, action: str, price: float) -> int:
        """Calculate position size based on risk management."""
        max_position_value = self.portfolio['total_value'] * self.risk_management['max_position_size']
        
        if action == 'BUY':
            available_cash = self.portfolio['cash']
            position_value = min(max_position_value, available_cash)
            return int(position_value / price)
        
        elif action == 'SELL':
            available_shares = self.portfolio['shares']
            max_shares = int(max_position_value / price)
            return min(available_shares, max_shares)
        
        return 0
    
    def enable_strategy(self, strategy_name: str):
        """Enable a trading strategy."""
        if strategy_name in self.strategies:
            self.strategies[strategy_name].enabled = True
            if strategy_name not in self.active_strategies:
                self.active_strategies.append(strategy_name)
    
    def disable_strategy(self, strategy_name: str):
        """Disable a trading strategy."""
        if strategy_name in self.strategies:
            self.strategies[strategy_name].enabled = False
            if strategy_name in self.active_strategies:
                self.active_strategies.remove(strategy_name)
    
    def start_trading(self):
        """Start automated trading."""
        self.trading_enabled = True
    
    def stop_trading(self):
        """Stop automated trading."""
        self.trading_enabled = False
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary."""
        return {
            'total_value': self.portfolio['total_value'],
            'cash': self.portfolio['cash'],
            'shares': self.portfolio['shares'],
            'daily_pnl': self.portfolio['daily_pnl'],
            'total_pnl': self.portfolio['total_pnl'],
            'total_trades': len(self.portfolio['trades']),
            'active_strategies': len(self.active_strategies)
        }
    
    def get_strategy_performance(self) -> Dict[str, Any]:
        """Get strategy performance summary."""
        performance = {}
        for name, strategy in self.strategies.items():
            performance[name] = strategy.get_performance_summary()
        return performance