#!/usr/bin/env python3
"""
Trading Backtest Position Management Engine
==========================================

Position management engine for trading strategy backtesting.
Handles position sizing, entry/exit execution, and trade tracking.
V2 COMPLIANT: Focused position management under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR POSITION MANAGEMENT
@license MIT
"""

import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from .signal_detection_engine import TradeSide


@dataclass
class Trade:
    """Individual trade record"""
    entry_time: datetime
    exit_time: Optional[datetime]
    side: TradeSide
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    stop_price: float
    target_price: float
    pnl: float = 0.0
    pnl_percent: float = 0.0
    commission: float = 0.0
    status: str = "open"


@dataclass
class PositionConfig:
    """Configuration for position management"""
    initial_capital: float = 100000.0
    risk_percent: float = 0.5
    commission_bps: float = 2.0
    slippage_ticks: int = 1
    min_position_size: float = 0.1


class PositionManagementEngine:
    """Position management engine for trading backtesting"""
    
    def __init__(self, config: PositionConfig):
        """Initialize position management engine with configuration"""
        self.config = config
        self.trades: List[Trade] = []
        self.current_capital = config.initial_capital
        self.position_size = 0.0
        self.position_avg_price = 0.0
        self.position_side: Optional[TradeSide] = None
        self.current_trade: Optional[Trade] = None
    
    def calculate_position_size(self, entry_price: float, stop_distance: float, 
                              point_value: float = 1.0) -> float:
        """Calculate position size based on risk management"""
        try:
            risk_amount = self.current_capital * (self.config.risk_percent / 100)
            qty_raw = risk_amount / (stop_distance * point_value)
            qty = max(self.config.min_position_size, qty_raw)
            return qty
        except (ZeroDivisionError, ValueError):
            return self.config.min_position_size
    
    def enter_position(self, side: TradeSide, entry_price: float, stop_distance: float,
                      target_distance: float, bar_time: datetime, point_value: float = 1.0) -> bool:
        """Enter a new position"""
        try:
            # Calculate position size
            qty = self.calculate_position_size(entry_price, stop_distance, point_value)
            
            # Check if we have enough capital
            cost = qty * entry_price
            if cost > self.current_capital:
                qty = self.current_capital / entry_price
                if qty < self.config.min_position_size:
                    return False
            
            # Calculate stop and target prices
            if side == TradeSide.LONG:
                stop_price = entry_price - stop_distance
                target_price = entry_price + target_distance
                position_qty = qty
            else:
                stop_price = entry_price + stop_distance
                target_price = entry_price - target_distance
                position_qty = -qty
            
            # Update position state
            self.position_size = position_qty
            self.position_avg_price = entry_price
            self.position_side = side
            
            # Create trade record
            trade = Trade(
                entry_time=bar_time,
                exit_time=None,
                side=side,
                entry_price=entry_price,
                exit_price=None,
                quantity=abs(position_qty),
                stop_price=stop_price,
                target_price=target_price,
                status="open"
            )
            
            self.trades.append(trade)
            self.current_trade = trade
            
            return True
            
        except Exception as e:
            print(f"Error entering position: {e}")
            return False
    
    def exit_position(self, exit_price: float, exit_reason: str, bar_time: datetime) -> bool:
        """Exit current position"""
        try:
            if self.position_size == 0 or not self.current_trade:
                return False
            
            # Calculate P&L
            if self.position_side == TradeSide.LONG:
                pnl = (exit_price - self.position_avg_price) * abs(self.position_size)
            else:
                pnl = (self.position_avg_price - exit_price) * abs(self.position_size)
            
            # Calculate commission
            commission = self._calculate_commission(exit_price, abs(self.position_size))
            pnl -= commission
            
            # Calculate P&L percentage
            pnl_percent = (pnl / (self.position_avg_price * abs(self.position_size))) * 100
            
            # Update trade record
            self.current_trade.exit_time = bar_time
            self.current_trade.exit_price = exit_price
            self.current_trade.pnl = pnl
            self.current_trade.pnl_percent = pnl_percent
            self.current_trade.commission = commission
            self.current_trade.status = "closed"
            
            # Update capital
            self.current_capital += pnl
            
            # Reset position state
            self.position_size = 0.0
            self.position_avg_price = 0.0
            self.position_side = None
            self.current_trade = None
            
            return True
            
        except Exception as e:
            print(f"Error exiting position: {e}")
            return False
    
    def _calculate_commission(self, price: float, quantity: float) -> float:
        """Calculate commission for a trade"""
        trade_value = price * quantity
        commission = trade_value * (self.config.commission_bps / 10000)
        return commission
    
    def get_position_status(self) -> Dict[str, Any]:
        """Get current position status"""
        return {
            'has_position': self.position_size != 0,
            'position_size': self.position_size,
            'position_side': self.position_side.value if self.position_side else None,
            'position_avg_price': self.position_avg_price,
            'current_capital': self.current_capital,
            'current_trade_id': len(self.trades) if self.current_trade else None
        }
    
    def get_trade_statistics(self) -> Dict[str, Any]:
        """Get comprehensive trade statistics"""
        if not self.trades:
            return {"error": "No trades executed"}
        
        closed_trades = [t for t in self.trades if t.status == "closed"]
        open_trades = [t for t in self.trades if t.status == "open"]
        
        if not closed_trades:
            return {
                "total_trades": len(self.trades),
                "closed_trades": 0,
                "open_trades": len(open_trades),
                "current_capital": self.current_capital
            }
        
        # Basic statistics
        total_trades = len(closed_trades)
        winning_trades = [t for t in closed_trades if t.pnl > 0]
        losing_trades = [t for t in closed_trades if t.pnl < 0]
        
        # P&L metrics
        total_pnl = sum(t.pnl for t in closed_trades)
        gross_profit = sum(t.pnl for t in winning_trades)
        gross_loss = abs(sum(t.pnl for t in losing_trades))
        
        # Win rate and profit factor
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Average metrics
        avg_win = gross_profit / len(winning_trades) if winning_trades else 0
        avg_loss = gross_loss / len(losing_trades) if losing_trades else 0
        avg_trade = total_pnl / total_trades if total_trades > 0 else 0
        
        return {
            "total_trades": total_trades,
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "open_trades": len(open_trades),
            "win_rate": win_rate,
            "total_pnl": total_pnl,
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "profit_factor": profit_factor,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "avg_trade": avg_trade,
            "current_capital": self.current_capital,
            "total_return_pct": ((self.current_capital - self.config.initial_capital) / self.config.initial_capital) * 100
        }
    
    def get_trade_log(self) -> List[Dict[str, Any]]:
        """Get detailed trade log"""
        trade_log = []
        
        for i, trade in enumerate(self.trades):
            trade_data = {
                'trade_id': i + 1,
                'entry_time': trade.entry_time.isoformat() if trade.entry_time else None,
                'exit_time': trade.exit_time.isoformat() if trade.exit_time else None,
                'side': trade.side.value,
                'entry_price': trade.entry_price,
                'exit_price': trade.exit_price,
                'quantity': trade.quantity,
                'stop_price': trade.stop_price,
                'target_price': trade.target_price,
                'pnl': trade.pnl,
                'pnl_percent': trade.pnl_percent,
                'commission': trade.commission,
                'status': trade.status
            }
            trade_log.append(trade_data)
        
        return trade_log
    
    def clear_trades(self):
        """Clear all trade history"""
        self.trades.clear()
        self.current_trade = None
        self.position_size = 0.0
        self.position_avg_price = 0.0
        self.position_side = None
    
    def reset_capital(self, new_capital: Optional[float] = None):
        """Reset capital to initial or specified amount"""
        self.current_capital = new_capital or self.config.initial_capital
    
    def get_equity_curve(self) -> List[float]:
        """Get equity curve data"""
        equity_curve = [self.config.initial_capital]
        running_capital = self.config.initial_capital
        
        for trade in self.trades:
            if trade.status == "closed":
                running_capital += trade.pnl
                equity_curve.append(running_capital)
        
        return equity_curve


# Factory function for dependency injection
def create_position_management_engine(config: PositionConfig) -> PositionManagementEngine:
    """Factory function to create position management engine with configuration"""
    return PositionManagementEngine(config)


# Export for DI
__all__ = ['PositionManagementEngine', 'PositionConfig', 'Trade', 'create_position_management_engine']
