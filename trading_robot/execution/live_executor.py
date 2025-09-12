"""
Live Trading Executor
"""

import asyncio
from datetime import datetime, time
from typing import Any

# AGGRESSIVE LAZY LOADING - CRITICAL PERFORMANCE OPTIMIZATION
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.aggressive_lazy_loader import lazy_import

# Lazy load heavy modules for 30%+ performance improvement
pd = lazy_import('pandas', 'pd')

from loguru import logger
from strategies.base_strategy import Signal, StrategyManager

from core.alpaca_client import AlpacaClient
from core.risk_manager import RiskManager


class LiveExecutor:
    """Live trading execution engine"""

    def __init__(
        self,
        alpaca_client: AlpacaClient,
        risk_manager: RiskManager,
        strategy_manager: StrategyManager,
    ):
        self.alpaca_client = alpaca_client
        self.risk_manager = risk_manager
        self.strategy_manager = strategy_manager
        self.is_running = False
        self.symbols_to_trade = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # Default symbols
        self.trading_intervals = {}  # Track last trade time per symbol
        self.min_trade_interval = 300  # 5 minutes between trades for same symbol

    async def start(self):
        """Start live trading execution"""
        try:
            self.is_running = True
            logger.info("🚀 Starting live trading executor")

            # Start monitoring tasks
            asyncio.create_task(self._market_monitor())
            asyncio.create_task(self._position_monitor())
            asyncio.create_task(self._risk_monitor())

            # Reset daily counters if it's a new trading day
            await self._check_new_trading_day()

        except Exception as e:
            logger.error(f"❌ Failed to start live executor: {e}")
            raise

    async def stop(self):
        """Stop live trading execution"""
        try:
            self.is_running = False
            logger.info("🛑 Stopping live trading executor")

            # Cancel all pending orders
            await self._cancel_all_orders()

        except Exception as e:
            logger.error(f"❌ Error stopping live executor: {e}")

    async def _market_monitor(self):
        """Monitor market conditions and execute trades"""
        while self.is_running:
            try:
                # Check if market is open
                if not self.risk_manager.check_market_hours():
                    await asyncio.sleep(60)  # Check every minute when closed
                    continue

                # Scan symbols for trading opportunities
                for symbol in self.symbols_to_trade:
                    try:
                        await self._evaluate_symbol(symbol)
                    except Exception as e:
                        logger.error(f"❌ Error evaluating {symbol}: {e}")

                    await asyncio.sleep(1)  # Small delay between symbols

                # Wait before next market scan
                await asyncio.sleep(60)  # Scan every minute during market hours

            except Exception as e:
                logger.error(f"❌ Error in market monitor: {e}")
                await asyncio.sleep(30)

    async def _evaluate_symbol(self, symbol: str):
        """Evaluate a symbol for trading opportunities"""
        try:
            # Check if we can trade this symbol
            if not self.risk_manager.can_trade_symbol(symbol):
                return

            # Check trade interval
            now = datetime.now().timestamp()
            last_trade = self.trading_intervals.get(symbol, 0)
            if now - last_trade < self.min_trade_interval:
                return

            # Get recent market data
            market_data = self.alpaca_client.get_historical_data(
                symbol=symbol, timeframe="1Min", limit=100
            )

            if market_data.empty:
                logger.warning(f"⚠️ No market data available for {symbol}")
                return

            # Analyze with all strategies
            strategy_results = self.strategy_manager.analyze_symbol(symbol, market_data)

            # Get consensus signal
            consensus_signal, confidence = self.strategy_manager.get_consensus_signal(
                strategy_results
            )

            if consensus_signal == Signal.HOLD or confidence < 0.7:
                return  # Not confident enough

            # Execute trade if signal is strong
            await self._execute_signal(symbol, consensus_signal, confidence, market_data.iloc[-1])

        except Exception as e:
            logger.error(f"❌ Error evaluating symbol {symbol}: {e}")

    async def _execute_signal(
        self, symbol: str, signal: Signal, confidence: float, current_bar: pd.Series
    ):
        """Execute a trading signal"""
        try:
            current_price = current_bar["close"]

            # Calculate position size
            if signal == Signal.BUY:
                quantity = self.risk_manager.calculate_position_size(current_price)
                side = "buy"
            elif signal == Signal.SELL:
                # Check if we have position to sell
                positions = self.alpaca_client.get_positions()
                symbol_position = next((p for p in positions if p["symbol"] == symbol), None)

                if not symbol_position or symbol_position["qty"] <= 0:
                    return  # No position to sell

                quantity = min(
                    symbol_position["qty"], self.risk_manager.calculate_position_size(current_price)
                )
                side = "sell"
            else:
                return

            # Validate trade with risk manager
            is_valid, reason = self.risk_manager.validate_trade(
                symbol=symbol, quantity=quantity, price=current_price, side=side
            )

            if not is_valid:
                logger.warning(f"⚠️ Trade rejected for {symbol}: {reason}")
                return

            # Execute trade
            if side == "buy":
                order = self.alpaca_client.submit_market_order(symbol, quantity, side)
            else:
                order = self.alpaca_client.submit_market_order(symbol, quantity, side)

            if order:
                # Record trade
                self.risk_manager.record_trade(
                    symbol=symbol, side=side, quantity=quantity, price=current_price
                )

                # Update trade interval
                self.trading_intervals[symbol] = datetime.now().timestamp()

                logger.info(
                    f"✅ Trade executed: {side} {quantity} {symbol} @ ${current_price:.2f} (confidence: {confidence:.2f})"
                )

        except Exception as e:
            logger.error(f"❌ Error executing signal for {symbol}: {e}")

    async def _position_monitor(self):
        """Monitor positions and manage risk"""
        while self.is_running:
            try:
                positions = self.alpaca_client.get_positions()

                # Update risk manager with current positions
                for position in positions:
                    # Check for stop loss/take profit levels
                    await self._check_position_levels(position)

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"❌ Error in position monitor: {e}")
                await asyncio.sleep(30)

    async def _check_position_levels(self, position: dict[str, Any]):
        """Check stop loss and take profit levels for a position"""
        try:
            symbol = position["symbol"]
            current_price = position["current_price"]
            avg_entry_price = position["avg_entry_price"]
            quantity = position["qty"]

            # Calculate stop loss and take profit prices
            stop_loss_price = self.risk_manager.calculate_stop_loss_price(avg_entry_price, "buy")
            take_profit_price = self.risk_manager.calculate_take_profit_price(
                avg_entry_price, "buy"
            )

            # Check stop loss
            if current_price <= stop_loss_price:
                logger.warning(f"🛑 Stop loss triggered for {symbol} @ ${current_price:.2f}")
                await self._close_position(symbol, quantity, "Stop loss")

            # Check take profit
            elif current_price >= take_profit_price:
                logger.info(f"🎯 Take profit triggered for {symbol} @ ${current_price:.2f}")
                await self._close_position(symbol, quantity, "Take profit")

        except Exception as e:
            logger.error(f"❌ Error checking position levels for {position['symbol']}: {e}")

    async def _close_position(self, symbol: str, quantity: int, reason: str):
        """Close a position"""
        try:
            order = self.alpaca_client.submit_market_order(symbol, quantity, "sell")
            if order:
                logger.info(f"📈 Position closed: {symbol} ({reason})")

                # Record the closing trade
                current_price = await self._get_current_price(symbol)
                self.risk_manager.record_trade(
                    symbol=symbol, side="sell", quantity=quantity, price=current_price
                )

        except Exception as e:
            logger.error(f"❌ Error closing position for {symbol}: {e}")

    async def _get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            bars = self.alpaca_client.get_historical_data(symbol, "1Min", limit=1)
            if not bars.empty:
                return bars.iloc[-1]["close"]
            return 0.0
        except Exception as e:
            logger.error(f"❌ Error getting current price for {symbol}: {e}")
            return 0.0

    async def _risk_monitor(self):
        """Monitor risk levels and generate alerts"""
        while self.is_running:
            try:
                # Check risk limits
                alerts = self.risk_manager.check_risk_limits()

                if alerts:
                    for alert in alerts:
                        logger.warning(alert)

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"❌ Error in risk monitor: {e}")
                await asyncio.sleep(60)

    async def _cancel_all_orders(self):
        """Cancel all open orders"""
        try:
            orders = self.alpaca_client.get_orders(status="open")
            for order in orders:
                try:
                    self.alpaca_client.cancel_order(order["id"])
                    logger.info(f"❌ Order cancelled: {order['id']}")
                except Exception as e:
                    logger.error(f"❌ Error cancelling order {order['id']}: {e}")

        except Exception as e:
            logger.error(f"❌ Error getting orders: {e}")

    async def _check_new_trading_day(self):
        """Check if it's a new trading day and reset counters"""
        try:
            # This is a simplified check - in production, you'd want more sophisticated logic
            current_time = datetime.now().time()
            market_open = time(9, 30)  # Assuming 9:30 AM market open

            if (
                current_time.hour == market_open.hour
                and current_time.minute <= market_open.minute + 5
            ):
                self.risk_manager.reset_daily_counters()
                logger.info("🌅 New trading day detected - daily counters reset")

        except Exception as e:
            logger.error(f"❌ Error checking new trading day: {e}")

    def add_symbol(self, symbol: str):
        """Add a symbol to the trading list"""
        if symbol not in self.symbols_to_trade:
            self.symbols_to_trade.append(symbol)
            logger.info(f"➕ Symbol added to trading list: {symbol}")

    def remove_symbol(self, symbol: str):
        """Remove a symbol from the trading list"""
        if symbol in self.symbols_to_trade:
            self.symbols_to_trade.remove(symbol)
            logger.info(f"➖ Symbol removed from trading list: {symbol}")

    def get_trading_symbols(self) -> list[str]:
        """Get list of symbols being traded"""
        return self.symbols_to_trade.copy()

    def get_executor_status(self) -> dict[str, Any]:
        """Get executor status"""
        return {
            "is_running": self.is_running,
            "symbols_trading": len(self.symbols_to_trade),
            "trading_symbols": self.symbols_to_trade,
            "last_update": datetime.now().isoformat(),
        }
