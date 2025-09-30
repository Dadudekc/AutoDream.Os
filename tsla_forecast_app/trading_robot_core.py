"""
Tesla Trading Robot Core
V2 Compliant main trading robot implementation
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from .trading_models import MarketData, Order, Position, TradingSignal, TradingMetrics
from .trading_strategies import TradingStrategy, MovingAverageStrategy


class TradingRobot:
    """Main trading robot class - V2 Compliant"""
    
    def __init__(self, symbol: str = "TSLA"):
        """Initialize trading robot"""
        self.symbol = symbol
        self.strategies: List[TradingStrategy] = []
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.market_data: List[MarketData] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize default strategy
        self.add_strategy(MovingAverageStrategy())
        
    def add_strategy(self, strategy: TradingStrategy):
        """Add trading strategy"""
        self.strategies.append(strategy)
        self.logger.info(f"Added strategy: {strategy.name}")
        
    def update_market_data(self, data: MarketData):
        """Update market data"""
        self.market_data.append(data)
        # Keep only last 1000 data points
        if len(self.market_data) > 1000:
            self.market_data = self.market_data[-1000:]
            
    def generate_signals(self) -> List[TradingSignal]:
        """Generate trading signals from all strategies"""
        signals = []
        for strategy in self.strategies:
            try:
                signal = strategy.calculate_signal(self.market_data)
                signals.append(signal)
                self.logger.info(f"Strategy {strategy.name}: {signal.value}")
            except Exception as e:
                self.logger.error(f"Error in strategy {strategy.name}: {e}")
                
        return signals
        
    def execute_trade(self, signal: TradingSignal, quantity: int, price: Optional[float] = None):
        """Execute a trade"""
        if not self.market_data:
            self.logger.warning("No market data available")
            return
            
        latest_data = self.market_data[-1]
        
        order = Order(
            order_id=f"order_{len(self.orders) + 1}",
            symbol=self.symbol,
            order_type="market" if price is None else "limit",
            side=signal,
            quantity=quantity,
            price=price,
            status="pending",
            timestamp=datetime.now()
        )
        
        self.orders.append(order)
        self.logger.info(f"Executed trade: {signal.value} {quantity} shares at {latest_data.price}")
        
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary"""
        total_value = sum(pos.quantity * pos.current_price for pos in self.positions.values())
        total_pnl = sum(pos.unrealized_pnl + pos.realized_pnl for pos in self.positions.values())
        
        return {
            "symbol": self.symbol,
            "total_value": total_value,
            "total_pnl": total_pnl,
            "positions": len(self.positions),
            "orders": len(self.orders),
            "strategies": len(self.strategies)
        }
        
    def get_performance_metrics(self) -> TradingMetrics:
        """Get trading performance metrics"""
        filled_orders = [order for order in self.orders if order.status == "filled"]
        
        if not filled_orders:
            return TradingMetrics(
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0.0,
                total_pnl=0.0,
                max_drawdown=0.0,
                sharpe_ratio=0.0
            )
            
        total_trades = len(filled_orders)
        winning_trades = sum(1 for order in filled_orders if order.side == TradingSignal.BUY)
        losing_trades = total_trades - winning_trades
        win_rate = winning_trades / total_trades if total_trades > 0 else 0.0
        
        return TradingMetrics(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            total_pnl=0.0,  # Calculate from actual trades
            max_drawdown=0.0,  # Calculate from actual trades
            sharpe_ratio=0.0  # Calculate from actual trades
        )