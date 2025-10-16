#!/usr/bin/env python3
"""
TSLA Risk Management System
Dream.OS Tactical Trading Risk Controls

Features:
- Dynamic stop-loss management
- Position sizing based on volatility
- Target zone tracking
- Trailing stop implementation
- Risk-adjusted position sizing
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class PositionStatus(Enum):
    MONITORING = "monitoring"
    ENTRY_PENDING = "entry_pending"
    ACTIVE = "active"
    TRAILING = "trailing"
    STOPPED_OUT = "stopped_out"
    TARGET_HIT = "target_hit"
    CANCELLED = "cancelled"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Position:
    symbol: str
    entry_price: float
    entry_time: datetime
    position_type: str  # "put" or "call"
    quantity: int
    premium_paid: float
    stop_loss: float
    target_zones: List[Tuple[float, float]]
    status: PositionStatus = PositionStatus.MONITORING
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    trailing_stop: Optional[float] = None
    max_favorable_excursion: float = 0.0
    max_adverse_excursion: float = 0.0

@dataclass
class RiskParameters:
    max_portfolio_risk: float = 0.02  # 2% of portfolio
    max_position_risk: float = 0.01   # 1% per position
    stop_loss_pct: float = 0.15       # 15% stop loss
    trailing_stop_pct: float = 0.015  # 1.5% trailing stop
    target_risk_reward: float = 2.0   # 2:1 risk/reward minimum
    max_daily_loss: float = 0.05      # 5% max daily loss
    volatility_adjustment: bool = True
    correlation_limit: float = 0.7    # Max correlation between positions

@dataclass
class MarketConditions:
    volatility: float = 0.0
    trend_strength: float = 0.0
    volume_profile: str = "normal"
    market_regime: str = "normal"
    risk_level: RiskLevel = RiskLevel.MEDIUM

class TSLARiskManager:
    def __init__(self, portfolio_value: float = 10000.0):
        self.portfolio_value = portfolio_value
        self.risk_params = RiskParameters()
        self.market_conditions = MarketConditions()
        self.active_positions: List[Position] = []
        self.position_history: List[Position] = []
        self.daily_pnl: float = 0.0
        self.daily_trades: int = 0
        self.max_daily_trades: int = 5
        
        # TSLA-specific parameters
        self.tsla_volatility = 0.35  # Historical TSLA volatility
        self.tsla_atr_multiplier = 2.0
        self.tsla_support_levels = [430.0, 425.0, 420.0, 415.0]
        self.tsla_resistance_levels = [440.0, 445.0, 450.0, 455.0]
        
    def calculate_position_size(self, entry_price: float, stop_loss: float, 
                              risk_amount: float) -> int:
        """Calculate position size based on risk parameters"""
        risk_per_contract = abs(entry_price - stop_loss)
        if risk_per_contract == 0:
            return 0
            
        max_contracts = int(risk_amount / risk_per_contract)
        
        # Apply volatility adjustment
        if self.risk_params.volatility_adjustment:
            volatility_factor = min(1.0, 0.3 / self.tsla_volatility)
            max_contracts = int(max_contracts * volatility_factor)
        
        # Apply daily trade limit
        max_contracts = min(max_contracts, self.max_daily_trades - self.daily_trades)
        
        return max(0, max_contracts)
    
    def calculate_stop_loss(self, entry_price: float, position_type: str) -> float:
        """Calculate dynamic stop loss based on market conditions"""
        base_stop_pct = self.risk_params.stop_loss_pct
        
        # Adjust for volatility
        if self.market_conditions.volatility > 0.4:  # High volatility
            base_stop_pct *= 1.2
        elif self.market_conditions.volatility < 0.2:  # Low volatility
            base_stop_pct *= 0.8
            
        # Adjust for trend strength
        if self.market_conditions.trend_strength > 0.7:  # Strong trend
            base_stop_pct *= 0.9
        elif self.market_conditions.trend_strength < 0.3:  # Weak trend
            base_stop_pct *= 1.1
            
        if position_type == "put":
            return entry_price * (1 + base_stop_pct)
        else:
            return entry_price * (1 - base_stop_pct)
    
    def calculate_target_zones(self, entry_price: float, position_type: str) -> List[Tuple[float, float]]:
        """Calculate target zones based on risk/reward ratio"""
        stop_loss = self.calculate_stop_loss(entry_price, position_type)
        risk_amount = abs(entry_price - stop_loss)
        target_profit = risk_amount * self.risk_params.target_risk_reward
        
        if position_type == "put":
            target_price = entry_price - target_profit
            # Create multiple target zones
            zones = []
            for i in range(1, 4):
                zone_target = entry_price - (target_profit * i / 3)
                zone_stop = zone_target - (risk_amount * 0.5)
                zones.append((zone_target, zone_stop))
            return zones
        else:
            target_price = entry_price + target_profit
            zones = []
            for i in range(1, 4):
                zone_target = entry_price + (target_profit * i / 3)
                zone_stop = zone_target + (risk_amount * 0.5)
                zones.append((zone_target, zone_stop))
            return zones
    
    def create_position(self, symbol: str, entry_price: float, position_type: str, 
                       current_price: float) -> Optional[Position]:
        """Create a new position with risk management"""
        
        # Check daily limits
        if self.daily_trades >= self.max_daily_trades:
            print(f"❌ Daily trade limit reached: {self.daily_trades}")
            return None
            
        # Check daily loss limit
        if self.daily_pnl < -self.risk_params.max_daily_loss * self.portfolio_value:
            print(f"❌ Daily loss limit reached: {self.daily_pnl:.2f}")
            return None
            
        # Calculate risk amount
        risk_amount = self.portfolio_value * self.risk_params.max_position_risk
        
        # Calculate stop loss and targets
        stop_loss = self.calculate_stop_loss(entry_price, position_type)
        target_zones = self.calculate_target_zones(entry_price, position_type)
        
        # Calculate position size
        quantity = self.calculate_position_size(entry_price, stop_loss, risk_amount)
        
        if quantity == 0:
            print("❌ Position size too small or risk too high")
            return None
            
        # Estimate premium (simplified calculation)
        premium_per_contract = 2.50  # Estimated TSLA put premium
        total_premium = quantity * premium_per_contract
        
        # Check if premium exceeds max exposure
        if total_premium > self.risk_params.max_position_risk * self.portfolio_value:
            quantity = int((self.risk_params.max_position_risk * self.portfolio_value) / premium_per_contract)
            total_premium = quantity * premium_per_contract
            
        position = Position(
            symbol=symbol,
            entry_price=entry_price,
            entry_time=datetime.now(),
            position_type=position_type,
            quantity=quantity,
            premium_paid=total_premium,
            stop_loss=stop_loss,
            target_zones=target_zones,
            current_price=current_price,
            status=PositionStatus.ENTRY_PENDING
        )
        
        self.active_positions.append(position)
        self.daily_trades += 1
        
        print(f"✅ Position created: {quantity} contracts at ${entry_price:.2f}")
        print(f"   Stop Loss: ${stop_loss:.2f}")
        print(f"   Premium: ${total_premium:.2f}")
        print(f"   Target Zones: {target_zones}")
        
        return position
    
    def update_position(self, position: Position, current_price: float) -> Dict:
        """Update position with current market data"""
        position.current_price = current_price
        
        # Calculate unrealized P&L
        if position.position_type == "put":
            position.unrealized_pnl = (position.entry_price - current_price) * position.quantity
        else:
            position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
            
        # Update MFE/MAE
        if position.unrealized_pnl > position.max_favorable_excursion:
            position.max_favorable_excursion = position.unrealized_pnl
        if position.unrealized_pnl < position.max_adverse_excursion:
            position.max_adverse_excursion = position.unrealized_pnl
            
        # Check stop loss
        if self._check_stop_loss(position):
            return self._close_position(position, "stop_loss")
            
        # Check target zones
        target_hit = self._check_target_zones(position)
        if target_hit:
            return self._close_position(position, "target_hit")
            
        # Update trailing stop
        if position.status == PositionStatus.ACTIVE:
            self._update_trailing_stop(position)
            
        return {
            "status": "updated",
            "unrealized_pnl": position.unrealized_pnl,
            "current_price": current_price
        }
    
    def _check_stop_loss(self, position: Position) -> bool:
        """Check if stop loss has been hit"""
        if position.position_type == "put":
            return position.current_price >= position.stop_loss
        else:
            return position.current_price <= position.stop_loss
    
    def _check_target_zones(self, position: Position) -> bool:
        """Check if any target zone has been hit"""
        for target, stop in position.target_zones:
            if position.position_type == "put":
                if position.current_price <= target:
                    return True
            else:
                if position.current_price >= target:
                    return True
        return False
    
    def _update_trailing_stop(self, position: Position):
        """Update trailing stop based on favorable movement"""
        if position.position_type == "put":
            # For puts, trail down as price goes down
            if position.current_price < position.entry_price:
                new_trailing_stop = position.current_price * (1 + self.risk_params.trailing_stop_pct)
                if position.trailing_stop is None or new_trailing_stop < position.trailing_stop:
                    position.trailing_stop = new_trailing_stop
                    position.stop_loss = new_trailing_stop
        else:
            # For calls, trail up as price goes up
            if position.current_price > position.entry_price:
                new_trailing_stop = position.current_price * (1 - self.risk_params.trailing_stop_pct)
                if position.trailing_stop is None or new_trailing_stop > position.trailing_stop:
                    position.trailing_stop = new_trailing_stop
                    position.stop_loss = new_trailing_stop
    
    def _close_position(self, position: Position, reason: str) -> Dict:
        """Close position and update portfolio"""
        position.status = PositionStatus.STOPPED_OUT if reason == "stop_loss" else PositionStatus.TARGET_HIT
        
        # Calculate final P&L
        final_pnl = position.unrealized_pnl - position.premium_paid
        
        # Update daily P&L
        self.daily_pnl += final_pnl
        
        # Move to history
        self.position_history.append(position)
        self.active_positions.remove(position)
        
        print(f"🔒 Position closed: {reason}")
        print(f"   Final P&L: ${final_pnl:.2f}")
        print(f"   Daily P&L: ${self.daily_pnl:.2f}")
        
        return {
            "status": "closed",
            "reason": reason,
            "final_pnl": final_pnl,
            "daily_pnl": self.daily_pnl
        }
    
    def get_risk_summary(self) -> Dict:
        """Get current risk management summary"""
        total_exposure = sum(pos.premium_paid for pos in self.active_positions)
        total_unrealized = sum(pos.unrealized_pnl for pos in self.active_positions)
        
        return {
            "portfolio_value": self.portfolio_value,
            "daily_pnl": self.daily_pnl,
            "daily_trades": self.daily_trades,
            "active_positions": len(self.active_positions),
            "total_exposure": total_exposure,
            "exposure_pct": (total_exposure / self.portfolio_value) * 100,
            "total_unrealized": total_unrealized,
            "risk_level": self.market_conditions.risk_level.value,
            "max_daily_trades": self.max_daily_trades,
            "positions": [
                {
                    "symbol": pos.symbol,
                    "type": pos.position_type,
                    "quantity": pos.quantity,
                    "entry_price": pos.entry_price,
                    "current_price": pos.current_price,
                    "unrealized_pnl": pos.unrealized_pnl,
                    "status": pos.status.value
                }
                for pos in self.active_positions
            ]
        }
    
    def update_market_conditions(self, volatility: float, trend_strength: float, 
                               volume_profile: str = "normal"):
        """Update market conditions for risk adjustment"""
        self.market_conditions.volatility = volatility
        self.market_conditions.trend_strength = trend_strength
        self.market_conditions.volume_profile = volume_profile
        
        # Determine risk level
        if volatility > 0.4 or trend_strength < 0.3:
            self.market_conditions.risk_level = RiskLevel.HIGH
        elif volatility < 0.2 and trend_strength > 0.7:
            self.market_conditions.risk_level = RiskLevel.LOW
        else:
            self.market_conditions.risk_level = RiskLevel.MEDIUM
            
        print(f"📊 Market conditions updated:")
        print(f"   Volatility: {volatility:.2f}")
        print(f"   Trend Strength: {trend_strength:.2f}")
        print(f"   Risk Level: {self.market_conditions.risk_level.value}")

def main():
    """Demonstrate the risk management system"""
    print("🛡️ TSLA Risk Management System")
    print("=" * 40)
    
    # Initialize risk manager
    risk_manager = TSLARiskManager(portfolio_value=10000.0)
    
    # Update market conditions
    risk_manager.update_market_conditions(volatility=0.35, trend_strength=0.6)
    
    # Simulate creating a position
    print("\n📈 Creating TSLA Put Position...")
    position = risk_manager.create_position(
        symbol="TSLA",
        entry_price=435.0,
        position_type="put",
        current_price=435.0
    )
    
    if position:
        # Simulate price movement
        print("\n📊 Simulating price movement...")
        prices = [434.0, 432.0, 430.0, 428.0, 425.0]
        
        for price in prices:
            print(f"\nPrice: ${price}")
            result = risk_manager.update_position(position, price)
            print(f"Unrealized P&L: ${position.unrealized_pnl:.2f}")
            
            if result.get("status") == "closed":
                break
    
    # Display risk summary
    print("\n📋 Risk Summary:")
    summary = risk_manager.get_risk_summary()
    for key, value in summary.items():
        if key != "positions":
            print(f"   {key}: {value}")

if __name__ == "__main__":
    main()