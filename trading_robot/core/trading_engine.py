"""
Core Trading Engine for Alpaca Trading Robot
"""
import asyncio
from datetime import datetime, time
from typing import Dict, List, Optional, Any
from decimal import Decimal
import alpaca_trade_api as tradeapi
from loguru import logger

from config.settings import config


class TradingEngine:
    """Core trading engine managing Alpaca API interactions"""

    def __init__(self):
        self.api = None
        self.account = None
        self.positions = {}
        self.orders = {}
        self.is_running = False
        self.market_open = False

    async def initialize(self):
        """Initialize Alpaca API connection"""
        try:
            logger.info("🔗 Connecting to Alpaca API...")

            # Initialize Alpaca API
            self.api = tradeapi.REST(
                key_id=config.alpaca_api_key,
                secret_key=config.alpaca_secret_key,
                base_url=config.alpaca_base_url,
                api_version='v2'
            )

            # Test connection
            await self._test_connection()

            # Get account information
            await self._update_account_info()

            logger.info("✅ Alpaca API connection established")

        except Exception as e:
            logger.error(f"❌ Failed to initialize Alpaca API: {e}")
            raise

    async def _test_connection(self):
        """Test Alpaca API connection"""
        try:
            # Test API connectivity
            clock = self.api.get_clock()
            logger.info(f"🕒 Market clock: {clock}")

            # Check if market is open
            self.market_open = clock.is_open

        except Exception as e:
            logger.error(f"❌ Alpaca API connection test failed: {e}")
            raise

    async def _update_account_info(self):
        """Update account information"""
        try:
            self.account = self.api.get_account()
            logger.info(f"💰 Account: {self.account.cash} cash, {self.account.portfolio_value} portfolio value")

        except Exception as e:
            logger.error(f"❌ Failed to get account info: {e}")
            raise

    async def start(self):
        """Start the trading engine"""
        try:
            logger.info("🚀 Starting trading engine...")
            self.is_running = True

            # Start market monitoring
            asyncio.create_task(self._monitor_market_status())

            # Start position monitoring
            asyncio.create_task(self._monitor_positions())

            logger.info("✅ Trading engine started")

        except Exception as e:
            logger.error(f"❌ Failed to start trading engine: {e}")
            raise

    async def stop(self):
        """Stop the trading engine"""
        try:
            logger.info("🛑 Stopping trading engine...")
            self.is_running = False

            # Cancel all open orders
            await self._cancel_all_orders()

            logger.info("✅ Trading engine stopped")

        except Exception as e:
            logger.error(f"❌ Error stopping trading engine: {e}")

    async def _monitor_market_status(self):
        """Monitor market open/close status"""
        while self.is_running:
            try:
                clock = self.api.get_clock()
                market_was_open = self.market_open
                self.market_open = clock.is_open

                if market_was_open != self.market_open:
                    status = "🟢 OPEN" if self.market_open else "🔴 CLOSED"
                    logger.info(f"📊 Market status changed: {status}")

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"❌ Error monitoring market status: {e}")
                await asyncio.sleep(30)

    async def _monitor_positions(self):
        """Monitor current positions"""
        while self.is_running:
            try:
                positions = self.api.list_positions()
                self.positions = {pos.symbol: pos for pos in positions}

                if positions:
                    logger.debug(f"📊 Current positions: {[f'{p.symbol}:{p.qty}' for p in positions]}")

                await asyncio.sleep(30)  # Update every 30 seconds

            except Exception as e:
                logger.error(f"❌ Error monitoring positions: {e}")
                await asyncio.sleep(30)

    async def get_market_data(self, symbol: str, timeframe: str = "1Min", limit: int = 100):
        """Get market data for a symbol"""
        try:
            bars = self.api.get_bars(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit,
                adjustment='raw'
            )

            return [{
                'timestamp': bar.t,
                'open': bar.o,
                'high': bar.h,
                'low': bar.l,
                'close': bar.c,
                'volume': bar.v
            } for bar in bars]

        except Exception as e:
            logger.error(f"❌ Error getting market data for {symbol}: {e}")
            return []

    async def place_order(self, symbol: str, qty: int, side: str, order_type: str = "market",
                         time_in_force: str = "gtc", limit_price: Optional[float] = None):
        """Place a trading order"""
        try:
            if not self.market_open and order_type != "limit":
                logger.warning(f"⚠️ Market is closed, placing limit order for {symbol}")
                order_type = "limit"
                limit_price = limit_price or await self._get_current_price(symbol)

            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force,
                limit_price=limit_price
            )

            self.orders[order.id] = order
            logger.info(f"📋 Order placed: {side} {qty} {symbol} @ {order_type}")

            return order

        except Exception as e:
            logger.error(f"❌ Error placing order for {symbol}: {e}")
            return None

    async def _get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            bars = await self.get_market_data(symbol, limit=1)
            if bars:
                return bars[0]['close']
            return 0.0
        except Exception as e:
            logger.error(f"❌ Error getting current price for {symbol}: {e}")
            return 0.0

    async def cancel_order(self, order_id: str):
        """Cancel an order"""
        try:
            self.api.cancel_order(order_id)
            if order_id in self.orders:
                del self.orders[order_id]
            logger.info(f"❌ Order cancelled: {order_id}")

        except Exception as e:
            logger.error(f"❌ Error cancelling order {order_id}: {e}")

    async def _cancel_all_orders(self):
        """Cancel all open orders"""
        try:
            orders = self.api.list_orders(status="open")
            for order in orders:
                await self.cancel_order(order.id)
            logger.info("❌ All open orders cancelled")

        except Exception as e:
            logger.error(f"❌ Error cancelling all orders: {e}")

    async def get_portfolio_value(self) -> float:
        """Get current portfolio value"""
        try:
            await self._update_account_info()
            return float(self.account.portfolio_value)
        except Exception as e:
            logger.error(f"❌ Error getting portfolio value: {e}")
            return 0.0

    async def get_account_balance(self) -> float:
        """Get account cash balance"""
        try:
            await self._update_account_info()
            return float(self.account.cash)
        except Exception as e:
            logger.error(f"❌ Error getting account balance: {e}")
            return 0.0

    def is_market_open(self) -> bool:
        """Check if market is currently open"""
        return self.market_open

    def can_trade_symbol(self, symbol: str) -> bool:
        """Check if we can trade a symbol"""
        # Add your trading restrictions here
        return symbol not in ["", None]  # Basic check
