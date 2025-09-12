"""
Risk Management System for Trading Robot
"""

from datetime import datetime, time
from typing import Any

from config.settings import config
from loguru import logger


class RiskManager:
    """Comprehensive risk management system"""

    def __init__(self):
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.portfolio_value = config.initial_balance
        self.daily_start_value = config.initial_balance
        self.max_daily_loss = config.daily_loss_limit_pct * config.initial_balance
        self.max_daily_trades = config.max_daily_trades
        self.positions = {}
        self.trade_history = []

    def validate_trade(
        self, symbol: str, quantity: int, price: float, side: str, order_type: str = "market"
    ) -> tuple[bool, str]:
        """Validate if a trade meets risk management criteria"""

        # Check daily loss limit
        if self.daily_pnl <= -self.max_daily_loss:
            return False, "Daily loss limit exceeded"

        # Check maximum daily trades
        if self.daily_trades >= self.max_daily_trades:
            return False, "Maximum daily trades reached"

        # Check position limits
        if symbol in self.positions:
            current_qty = self.positions[symbol]["quantity"]
            if side == "buy":
                new_qty = current_qty + quantity
            else:
                new_qty = current_qty - quantity

            if abs(new_qty) > self._calculate_max_position_size(price):
                return False, "Position size exceeds limit"

        # Check portfolio risk
        trade_value = quantity * price
        if trade_value > self.portfolio_value * config.max_position_size_pct:
            return False, "Trade value exceeds position size limit"

        # Check minimum order value
        if trade_value < config.min_order_value:
            return False, "Order value below minimum"

        # Check maximum order value
        if trade_value > config.max_order_value:
            return False, "Order value above maximum"

        return True, "Trade approved"

    def calculate_position_size(self, price: float, stop_loss_pct: float = None) -> int:
        """Calculate safe position size based on risk management"""
        if stop_loss_pct is None:
            stop_loss_pct = config.default_stop_loss_pct

        # Risk per trade (1% of portfolio)
        risk_per_trade = self.portfolio_value * 0.01

        # Position size based on stop loss
        risk_per_share = price * stop_loss_pct
        position_size = int(risk_per_trade / risk_per_share)

        # Apply maximum position size limit
        max_position_size = self._calculate_max_position_size(price)
        position_size = min(position_size, max_position_size)

        return max(1, position_size)

    def _calculate_max_position_size(self, price: float) -> int:
        """Calculate maximum position size for a symbol"""
        max_value = self.portfolio_value * config.max_position_size_pct
        return int(max_value / price)

    def update_portfolio_value(self, new_value: float):
        """Update portfolio value and check for emergency stops"""
        old_value = self.portfolio_value
        self.portfolio_value = new_value

        # Calculate daily P&L
        if self.daily_start_value > 0:
            self.daily_pnl = self.portfolio_value - self.daily_start_value

        # Emergency stop check
        if config.emergency_stop_enabled:
            self._check_emergency_stop()

        logger.debug(
            f"💰 Portfolio value: ${self.portfolio_value:.2f} (Daily P&L: ${self.daily_pnl:.2f})"
        )

    def _check_emergency_stop(self):
        """Check for emergency stop conditions"""
        # Daily loss limit
        if self.daily_pnl <= -self.max_daily_loss:
            logger.critical("🚨 EMERGENCY STOP: Daily loss limit exceeded")
            self._trigger_emergency_stop("Daily loss limit exceeded")

        # Portfolio emergency stop
        emergency_loss = self.portfolio_value - config.initial_balance
        if emergency_loss <= -config.emergency_stop_loss_pct * config.initial_balance:
            logger.critical("🚨 EMERGENCY STOP: Portfolio emergency loss threshold reached")
            self._trigger_emergency_stop("Portfolio emergency loss threshold")

    def _trigger_emergency_stop(self, reason: str):
        """Trigger emergency stop procedure"""
        logger.critical(f"🚨 EMERGENCY STOP ACTIVATED: {reason}")

        # This would integrate with the main trading engine to:
        # 1. Cancel all open orders
        # 2. Close all positions
        # 3. Stop all trading activity
        # 4. Send emergency notifications

        # For now, just log the emergency
        # In production, this would trigger actual emergency procedures

    def record_trade(self, symbol: str, side: str, quantity: int, price: float, pnl: float = 0.0):
        """Record a completed trade"""
        self.daily_trades += 1

        trade_record = {
            "timestamp": datetime.now(),
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "pnl": pnl,
            "portfolio_value": self.portfolio_value,
        }

        self.trade_history.append(trade_record)

        # Update positions
        if symbol not in self.positions:
            self.positions[symbol] = {"quantity": 0, "avg_price": 0.0}

        current_qty = self.positions[symbol]["quantity"]
        current_avg_price = self.positions[symbol]["avg_price"]

        if side == "buy":
            # Update average price for long positions
            total_value = (current_qty * current_avg_price) + (quantity * price)
            new_qty = current_qty + quantity
            new_avg_price = total_value / new_qty if new_qty > 0 else 0

            self.positions[symbol]["quantity"] = new_qty
            self.positions[symbol]["avg_price"] = new_avg_price

        elif side == "sell":
            # Reduce position
            new_qty = current_qty - quantity
            if new_qty <= 0:
                del self.positions[symbol]
            else:
                self.positions[symbol]["quantity"] = new_qty

        logger.info(f"📊 Trade recorded: {side} {quantity} {symbol} @ ${price:.2f}")

    def get_portfolio_risk_metrics(self) -> dict[str, Any]:
        """Get current portfolio risk metrics"""
        total_exposure = 0.0
        position_count = len(self.positions)
        largest_position = 0.0

        for symbol, position in self.positions.items():
            position_value = position["quantity"] * position["avg_price"]
            total_exposure += position_value
            largest_position = max(largest_position, position_value)

        concentration_pct = (
            (largest_position / self.portfolio_value) * 100 if self.portfolio_value > 0 else 0
        )
        exposure_pct = (
            (total_exposure / self.portfolio_value) * 100 if self.portfolio_value > 0 else 0
        )

        return {
            "total_exposure": total_exposure,
            "exposure_percentage": exposure_pct,
            "position_count": position_count,
            "concentration_percentage": concentration_pct,
            "daily_pnl": self.daily_pnl,
            "daily_pnl_percentage": (
                (self.daily_pnl / self.daily_start_value) * 100 if self.daily_start_value > 0 else 0
            ),
            "daily_trades": self.daily_trades,
            "remaining_daily_trades": max(0, self.max_daily_trades - self.daily_trades),
        }

    def check_market_hours(self) -> bool:
        """Check if current time is within trading hours"""
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime("%A")

        # Check if it's a trading day
        if current_day not in config.trading_days:
            return False

        # Check if it's within trading hours
        market_open = time(config.market_open_hour, 0)
        market_close = time(config.market_close_hour, 0)

        return market_open <= current_time <= market_close

    def calculate_stop_loss_price(
        self, entry_price: float, side: str, stop_loss_pct: float = None
    ) -> float:
        """Calculate stop loss price"""
        if stop_loss_pct is None:
            stop_loss_pct = config.default_stop_loss_pct

        if side == "buy":
            return entry_price * (1 - stop_loss_pct)
        else:
            return entry_price * (1 + stop_loss_pct)

    def calculate_take_profit_price(
        self, entry_price: float, side: str, take_profit_pct: float = None
    ) -> float:
        """Calculate take profit price"""
        if take_profit_pct is None:
            take_profit_pct = config.default_take_profit_pct

        if side == "buy":
            return entry_price * (1 + take_profit_pct)
        else:
            return entry_price * (1 - take_profit_pct)

    def reset_daily_counters(self):
        """Reset daily counters (call this at market open)"""
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.daily_start_value = self.portfolio_value
        logger.info("🔄 Daily risk counters reset")

    def get_risk_report(self) -> str:
        """Generate risk management report"""
        metrics = self.get_portfolio_risk_metrics()

        report = f"""
RISK MANAGEMENT REPORT
======================
Portfolio Value: ${self.portfolio_value:.2f}
Daily P&L: ${metrics["daily_pnl"]:.2f} ({metrics["daily_pnl_percentage"]:.2f}%)

Position Metrics:
- Total Exposure: ${metrics["total_exposure"]:.2f}
- Exposure %: {metrics["exposure_percentage"]:.1f}%
- Position Count: {metrics["position_count"]}
- Largest Position: {metrics["concentration_percentage"]:.1f}%

Trading Limits:
- Daily Trades: {metrics["daily_trades"]}/{self.max_daily_trades}
- Remaining Trades: {metrics["remaining_daily_trades"]}
- Daily Loss Limit: ${self.max_daily_loss:.2f}

Risk Status: {"⚠️ HIGH RISK" if metrics["exposure_percentage"] > 50 else "✅ NORMAL"}
        """

        return report.strip()


class RiskMonitor:
    """Real-time risk monitoring system"""

    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
        self.alerts = []
        self.monitoring = False

    def start_monitoring(self):
        """Start risk monitoring"""
        self.monitoring = True
        logger.info("👁️ Risk monitoring started")

    def stop_monitoring(self):
        """Stop risk monitoring"""
        self.monitoring = False
        logger.info("👁️ Risk monitoring stopped")

    def check_risk_limits(self) -> list[str]:
        """Check all risk limits and return alerts"""
        alerts = []
        metrics = self.risk_manager.get_portfolio_risk_metrics()

        # Check exposure limits
        if metrics["exposure_percentage"] > 80:
            alerts.append("🚨 HIGH EXPOSURE: Portfolio exposure above 80%")

        # Check concentration limits
        if metrics["concentration_percentage"] > 20:
            alerts.append("⚠️ HIGH CONCENTRATION: Single position above 20%")

        # Check daily loss limits
        if metrics["daily_pnl_percentage"] < -3:
            alerts.append(f"⚠️ DAILY LOSS: {metrics['daily_pnl_percentage']:.1f}% loss today")

        # Check trading frequency
        if metrics["daily_trades"] >= self.risk_manager.max_daily_trades * 0.8:
            alerts.append(
                f"⚠️ HIGH TRADING FREQUENCY: {metrics['daily_trades']}/{self.risk_manager.max_daily_trades} trades"
            )

        # Check market hours
        if not self.risk_manager.check_market_hours():
            alerts.append("ℹ️ OUTSIDE TRADING HOURS")

        return alerts

    def log_alerts(self, alerts: list[str]):
        """Log risk alerts"""
        for alert in alerts:
            logger.warning(alert)
            self.alerts.append(
                {
                    "timestamp": datetime.now(),
                    "alert": alert,
                    "level": "WARNING" if "⚠️" in alert else "CRITICAL" if "🚨" in alert else "INFO",
                }
            )
