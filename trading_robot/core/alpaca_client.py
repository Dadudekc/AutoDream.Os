"""
Alpaca API Client Wrapper
"""
from datetime import datetime, timedelta
from typing import Any

import alpaca_trade_api as tradeapi
import pandas as pd
from config.settings import config
from loguru import logger


class AlpacaClient:
    """Wrapper for Alpaca API interactions"""

    def __init__(self):
        self.api = None
        self._connected = False

    def connect(self):
        """Establish connection to Alpaca API"""
        try:
            self.api = tradeapi.REST(
                key_id=config.alpaca_api_key,
                secret_key=config.alpaca_secret_key,
                base_url=config.alpaca_base_url,
                api_version='v2'
            )

            # Test connection
            self.api.get_account()
            self._connected = True
            logger.info("✅ Connected to Alpaca API")

        except Exception as e:
            logger.error(f"❌ Failed to connect to Alpaca API: {e}")
            raise

    def is_connected(self) -> bool:
        """Check if connected to Alpaca API"""
        return self._connected

    def get_account_info(self) -> dict[str, Any]:
        """Get account information"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            account = self.api.get_account()
            return {
                'id': account.id,
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'buying_power': float(account.buying_power),
                'daytrade_count': account.daytrade_count,
                'status': account.status
            }
        except Exception as e:
            logger.error(f"❌ Error getting account info: {e}")
            return {}

    def get_positions(self) -> list[dict[str, Any]]:
        """Get current positions"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            positions = self.api.list_positions()
            return [{
                'symbol': pos.symbol,
                'qty': int(pos.qty),
                'avg_entry_price': float(pos.avg_entry_price),
                'current_price': float(pos.current_price),
                'market_value': float(pos.market_value),
                'unrealized_pl': float(pos.unrealized_pl),
                'unrealized_plpc': float(pos.unrealized_plpc)
            } for pos in positions]
        except Exception as e:
            logger.error(f"❌ Error getting positions: {e}")
            return []

    def get_orders(self, status: str = "open") -> list[dict[str, Any]]:
        """Get orders by status"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            orders = self.api.list_orders(status=status)
            return [{
                'id': order.id,
                'symbol': order.symbol,
                'qty': order.qty,
                'side': order.side,
                'type': order.type,
                'status': order.status,
                'submitted_at': order.submitted_at,
                'filled_at': order.filled_at,
                'filled_qty': order.filled_qty,
                'filled_avg_price': order.filled_avg_price
            } for order in orders]
        except Exception as e:
            logger.error(f"❌ Error getting orders: {e}")
            return []

    def get_historical_data(self, symbol: str, timeframe: str = "1Min",
                           start: datetime | None = None, end: datetime | None = None,
                           limit: int = 1000) -> pd.DataFrame:
        """Get historical market data"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            # Set default time range if not provided
            if end is None:
                end = datetime.now()
            if start is None:
                start = end - timedelta(days=30)

            bars = self.api.get_bars(
                symbol=symbol,
                timeframe=timeframe,
                start=start.isoformat(),
                end=end.isoformat(),
                limit=limit,
                adjustment='raw'
            )

            # Convert to DataFrame
            data = [{
                'timestamp': bar.t,
                'open': bar.o,
                'high': bar.h,
                'low': bar.l,
                'close': bar.c,
                'volume': bar.v
            } for bar in bars]

            df = pd.DataFrame(data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.set_index('timestamp', inplace=True)

            return df

        except Exception as e:
            logger.error(f"❌ Error getting historical data for {symbol}: {e}")
            return pd.DataFrame()

    def submit_market_order(self, symbol: str, qty: int, side: str,
                           time_in_force: str = "gtc") -> dict[str, Any]:
        """Submit a market order"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type="market",
                time_in_force=time_in_force
            )

            logger.info(f"📋 Market order submitted: {side} {qty} {symbol}")
            return {
                'id': order.id,
                'symbol': order.symbol,
                'qty': order.qty,
                'side': order.side,
                'type': order.type,
                'status': order.status
            }

        except Exception as e:
            logger.error(f"❌ Error submitting market order for {symbol}: {e}")
            raise

    def submit_limit_order(self, symbol: str, qty: int, side: str,
                          limit_price: float, time_in_force: str = "gtc") -> dict[str, Any]:
        """Submit a limit order"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type="limit",
                limit_price=limit_price,
                time_in_force=time_in_force
            )

            logger.info(f"📋 Limit order submitted: {side} {qty} {symbol} @ {limit_price}")
            return {
                'id': order.id,
                'symbol': order.symbol,
                'qty': order.qty,
                'side': order.side,
                'type': order.type,
                'limit_price': limit_price,
                'status': order.status
            }

        except Exception as e:
            logger.error(f"❌ Error submitting limit order for {symbol}: {e}")
            raise

    def cancel_order(self, order_id: str):
        """Cancel an order"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            self.api.cancel_order(order_id)
            logger.info(f"❌ Order cancelled: {order_id}")
        except Exception as e:
            logger.error(f"❌ Error cancelling order {order_id}: {e}")
            raise

    def get_market_clock(self) -> dict[str, Any]:
        """Get market clock information"""
        if not self._connected:
            raise ConnectionError("Not connected to Alpaca API")

        try:
            clock = self.api.get_clock()
            return {
                'timestamp': clock.timestamp,
                'is_open': clock.is_open,
                'next_open': clock.next_open,
                'next_close': clock.next_close
            }
        except Exception as e:
            logger.error(f"❌ Error getting market clock: {e}")
            return {}
