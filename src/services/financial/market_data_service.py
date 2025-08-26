"""
Market Data Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides real-time market data, historical data analysis, and market intelligence.
"""

from __future__ import annotations

import asyncio
import json

from src.utils.stability_improvements import stability_manager, safe_import
from src.utils.unified_logging_manager import get_logger
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path

pd = safe_import("pandas")
np = safe_import("numpy")
yf = safe_import("yfinance")
from concurrent.futures import ThreadPoolExecutor
import time

# Configure logging
logger = get_logger(__name__)


@dataclass
class MarketData:
    """Market data structure"""

    symbol: str
    price: float
    change: float
    change_pct: float
    volume: int
    market_cap: float
    pe_ratio: float
    dividend_yield: float
    timestamp: datetime
    data_source: str = "yfinance"


@dataclass
class HistoricalData:
    """Historical market data"""

    symbol: str
    data: pd.DataFrame
    start_date: datetime
    end_date: datetime
    interval: str
    last_updated: datetime


@dataclass
class MarketSentiment:
    """Market sentiment indicators"""

    symbol: str
    rsi: float  # Relative Strength Index
    macd: float  # MACD line
    macd_signal: float  # MACD signal line
    bollinger_upper: float
    bollinger_lower: float
    bollinger_middle: float
    timestamp: datetime


class MarketDataService:
    """Advanced market data and intelligence service"""

    def __init__(self, data_dir: str = "market_data", cache_duration: int = 300):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.cache_duration = cache_duration  # Cache duration in seconds
        self.market_data_cache: Dict[str, Dict[str, Any]] = {}
        self.historical_data_cache: Dict[str, HistoricalData] = {}

        # Data source configuration
        self.data_sources = {
            "yfinance": self._get_yfinance_data,
            "mock": self._get_mock_data,
        }

        # Default data source
        self.default_source = "yfinance"

        # Market hours (simplified - would be more complex in production)
        self.market_hours = {
            "start": "09:30",
            "end": "16:00",
            "timezone": "America/New_York",
        }

        logger.info("Market Data Service initialized")

    def is_market_open(self) -> bool:
        """Check if market is currently open"""
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            # Simple check - in production would use proper timezone handling
            return (
                self.market_hours["start"] <= current_time <= self.market_hours["end"]
            )

        except Exception as e:
            logger.error(f"Error checking market hours: {e}")
            return False

    def get_real_time_data(
        self, symbols: List[str], source: str = None
    ) -> Dict[str, MarketData]:
        """Get real-time market data for symbols"""
        try:
            source = source or self.default_source
            if source not in self.data_sources:
                raise ValueError(f"Unsupported data source: {source}")

            # Check cache first
            cached_data = {}
            symbols_to_fetch = []

            for symbol in symbols:
                symbol_upper = symbol.upper()
                if (
                    symbol_upper in self.market_data_cache
                    and time.time()
                    - self.market_data_cache[symbol_upper].get("timestamp", 0)
                    < self.cache_duration
                ):
                    cached_data[symbol_upper] = self.market_data_cache[symbol_upper][
                        "data"
                    ]
                else:
                    symbols_to_fetch.append(symbol_upper)

            # Fetch new data for uncached symbols
            if symbols_to_fetch:
                new_data = self.data_sources[source](symbols_to_fetch)

                # Update cache and results
                for symbol, data in new_data.items():
                    self.market_data_cache[symbol] = {
                        "data": data,
                        "timestamp": time.time(),
                    }
                    cached_data[symbol] = data

            return cached_data

        except Exception as e:
            logger.error(f"Error getting real-time data: {e}")
            return {}

    def get_historical_data(
        self, symbol: str, period: str = "1y", interval: str = "1d"
    ) -> Optional[HistoricalData]:
        """Get historical market data"""
        try:
            symbol_upper = symbol.upper()
            cache_key = f"{symbol_upper}_{period}_{interval}"

            # Check cache first
            if cache_key in self.historical_data_cache:
                cached_data = self.historical_data_cache[cache_key]
                if (
                    datetime.now() - cached_data.last_updated
                ).seconds < self.cache_duration:
                    return cached_data

            # Fetch new data
            ticker = yf.Ticker(symbol_upper)
            hist_data = ticker.history(period=period, interval=interval)

            if hist_data.empty:
                logger.warning(f"No historical data found for {symbol_upper}")
                return None

            # Create historical data object
            historical_data = HistoricalData(
                symbol=symbol_upper,
                data=hist_data,
                start_date=hist_data.index[0].to_pydatetime(),
                end_date=hist_data.index[-1].to_pydatetime(),
                interval=interval,
                last_updated=datetime.now(),
            )

            # Update cache
            self.historical_data_cache[cache_key] = historical_data

            return historical_data

        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {e}")
            return None

    def get_market_sentiment(
        self, symbol: str, period: str = "1y"
    ) -> Optional[MarketSentiment]:
        """Calculate market sentiment indicators"""
        try:
            historical_data = self.get_historical_data(symbol, period)
            if not historical_data or historical_data.data.empty:
                return None

            # Calculate technical indicators
            data = historical_data.data.copy()

            # RSI calculation
            delta = data["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            # MACD calculation
            exp1 = data["Close"].ewm(span=12, adjust=False).mean()
            exp2 = data["Close"].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            macd_signal = macd.ewm(span=9, adjust=False).mean()

            # Bollinger Bands
            sma = data["Close"].rolling(window=20).mean()
            std = data["Close"].rolling(window=20).std()
            bollinger_upper = sma + (std * 2)
            bollinger_lower = sma - (std * 2)
            bollinger_middle = sma

            # Get latest values
            latest_rsi = rsi.iloc[-1] if not rsi.empty else 50.0
            latest_macd = macd.iloc[-1] if not macd.empty else 0.0
            latest_macd_signal = macd_signal.iloc[-1] if not macd_signal.empty else 0.0
            latest_bb_upper = (
                bollinger_upper.iloc[-1] if not bollinger_upper.empty else 0.0
            )
            latest_bb_lower = (
                bollinger_lower.iloc[-1] if not bollinger_lower.empty else 0.0
            )
            latest_bb_middle = (
                bollinger_middle.iloc[-1] if not bollinger_middle.empty else 0.0
            )

            return MarketSentiment(
                symbol=symbol.upper(),
                rsi=latest_rsi,
                macd=latest_macd,
                macd_signal=latest_macd_signal,
                bollinger_upper=latest_bb_upper,
                bollinger_lower=latest_bb_lower,
                bollinger_middle=latest_bb_middle,
                timestamp=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Error calculating market sentiment for {symbol}: {e}")
            return None

    def get_portfolio_market_data(self, portfolio_symbols: List[str]) -> Dict[str, Any]:
        """Get comprehensive market data for portfolio symbols"""
        try:
            # Get real-time data
            real_time_data = self.get_real_time_data(portfolio_symbols)

            # Get sentiment data
            sentiment_data = {}
            for symbol in portfolio_symbols:
                sentiment = self.get_market_sentiment(symbol)
                if sentiment:
                    sentiment_data[symbol.upper()] = asdict(sentiment)

            # Calculate portfolio market metrics
            portfolio_metrics = self._calculate_portfolio_market_metrics(real_time_data)

            return {
                "real_time_data": {
                    symbol: asdict(data) for symbol, data in real_time_data.items()
                },
                "sentiment_data": sentiment_data,
                "portfolio_metrics": portfolio_metrics,
                "market_status": {
                    "is_open": self.is_market_open(),
                    "last_updated": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"Error getting portfolio market data: {e}")
            return {}

    def _calculate_portfolio_market_metrics(
        self, market_data: Dict[str, MarketData]
    ) -> Dict[str, Any]:
        """Calculate portfolio-level market metrics"""
        try:
            if not market_data:
                return {}

            total_market_cap = sum(
                data.market_cap for data in market_data.values() if data.market_cap
            )
            avg_pe_ratio = np.mean(
                [data.pe_ratio for data in market_data.values() if data.pe_ratio]
            )
            avg_dividend_yield = np.mean(
                [
                    data.dividend_yield
                    for data in market_data.values()
                    if data.dividend_yield
                ]
            )

            # Calculate sector distribution (simplified)
            sectors = {}
            for data in market_data.values():
                # In real implementation, would get sector from company info
                sector = "Unknown"
                if sector not in sectors:
                    sectors[sector] = 0
                sectors[sector] += data.market_cap or 0

            return {
                "total_market_cap": total_market_cap,
                "avg_pe_ratio": avg_pe_ratio,
                "avg_dividend_yield": avg_dividend_yield,
                "sector_distribution": sectors,
                "symbols_count": len(market_data),
            }

        except Exception as e:
            logger.error(f"Error calculating portfolio market metrics: {e}")
            return {}

    def _get_yfinance_data(self, symbols: List[str]) -> Dict[str, MarketData]:
        """Get market data from Yahoo Finance"""
        try:
            market_data = {}

            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info

                    # Get current price
                    current_price = (
                        ticker.history(period="1d")["Close"].iloc[-1]
                        if not ticker.history(period="1d").empty
                        else 0
                    )

                    # Get previous close for change calculation
                    hist_data = ticker.history(period="2d")
                    if len(hist_data) >= 2:
                        prev_close = hist_data["Close"].iloc[-2]
                        change = current_price - prev_close
                        change_pct = (
                            (change / prev_close) * 100 if prev_close > 0 else 0
                        )
                    else:
                        change = 0
                        change_pct = 0

                    # Get volume
                    volume = hist_data["Volume"].iloc[-1] if not hist_data.empty else 0

                    # Get additional info
                    market_cap = info.get("marketCap", 0)
                    pe_ratio = info.get("trailingPE", 0)
                    dividend_yield = (
                        info.get("dividendYield", 0) * 100
                        if info.get("dividendYield")
                        else 0
                    )

                    market_data[symbol] = MarketData(
                        symbol=symbol,
                        price=current_price,
                        change=change,
                        change_pct=change_pct,
                        volume=volume,
                        market_cap=market_cap,
                        pe_ratio=pe_ratio,
                        dividend_yield=dividend_yield,
                        timestamp=datetime.now(),
                    )

                    # Rate limiting to avoid API issues
                    time.sleep(0.1)

                except Exception as e:
                    logger.warning(f"Error getting data for {symbol}: {e}")
                    continue

            return market_data

        except Exception as e:
            logger.error(f"Error getting Yahoo Finance data: {e}")
            return {}

    def _get_mock_data(self, symbols: List[str]) -> Dict[str, MarketData]:
        """Get mock market data for testing"""
        try:
            market_data = {}

            for symbol in symbols:
                # Generate mock data
                base_price = 100 + (hash(symbol) % 900)  # Pseudo-random base price
                change = (hash(symbol + str(time.time())) % 20) - 10  # Random change
                change_pct = (change / base_price) * 100

                market_data[symbol] = MarketData(
                    symbol=symbol,
                    price=base_price + change,
                    change=change,
                    change_pct=change_pct,
                    volume=1000000 + (hash(symbol) % 9000000),
                    market_cap=base_price * 1000000,
                    pe_ratio=15 + (hash(symbol) % 20),
                    dividend_yield=2 + (hash(symbol) % 5),
                    timestamp=datetime.now(),
                    data_source="mock",
                )

            return market_data

        except Exception as e:
            logger.error(f"Error getting mock data: {e}")
            return {}

    def get_market_summary(self) -> Dict[str, Any]:
        """Get overall market summary"""
        try:
            # Get major indices data
            major_indices = [
                "^GSPC",
                "^DJI",
                "^IXIC",
                "^RUT",
            ]  # S&P 500, Dow, NASDAQ, Russell 2000

            indices_data = self.get_real_time_data(major_indices)

            # Calculate market breadth
            advancing = 0
            declining = 0

            for data in indices_data.values():
                if data.change > 0:
                    advancing += 1
                elif data.change < 0:
                    declining += 1

            return {
                "major_indices": {
                    symbol: asdict(data) for symbol, data in indices_data.items()
                },
                "market_breadth": {
                    "advancing": advancing,
                    "declining": declining,
                    "unchanged": len(indices_data) - advancing - declining,
                },
                "market_status": {
                    "is_open": self.is_market_open(),
                    "last_updated": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"Error getting market summary: {e}")
            return {}

    def clear_cache(self) -> None:
        """Clear all cached data"""
        try:
            self.market_data_cache.clear()
            self.historical_data_cache.clear()
            logger.info("Market data cache cleared")

        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    def export_market_data(self, symbols: List[str], filename: str = None) -> str:
        """Export market data to CSV"""
        try:
            if filename is None:
                filename = f"market_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            filepath = self.data_dir / filename

            # Get market data
            market_data = self.get_real_time_data(symbols)

            # Prepare for export
            export_data = []
            for symbol, data in market_data.items():
                export_data.append(asdict(data))

            # Convert to DataFrame and export
            df = pd.DataFrame(export_data)
            df.to_csv(filepath, index=False)

            logger.info(f"Market data exported to {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error exporting market data: {e}")
            return ""


# Example usage and testing
if __name__ == "__main__":
    # Create market data service
    mds = MarketDataService()

    # Test real-time data
    symbols = ["AAPL", "MSFT", "GOOGL"]
    real_time_data = mds.get_real_time_data(symbols)

    print("Real-time Market Data:")
    for symbol, data in real_time_data.items():
        print(f"{symbol}: ${data.price:.2f} ({data.change_pct:+.2f}%)")

    # Test historical data
    hist_data = mds.get_historical_data("AAPL", period="1mo")
    if hist_data:
        print(f"\nAAPL Historical Data: {len(hist_data.data)} records")

    # Test market sentiment
    sentiment = mds.get_market_sentiment("AAPL")
    if sentiment:
        print(f"\nAAPL Sentiment: RSI={sentiment.rsi:.2f}, MACD={sentiment.macd:.4f}")

    # Test portfolio market data
    portfolio_data = mds.get_portfolio_market_data(symbols)
    print(
        f"\nPortfolio Market Data: {len(portfolio_data.get('real_time_data', {}))} symbols"
    )

    # Test market summary
    market_summary = mds.get_market_summary()
    print(f"\nMarket Summary: {len(market_summary.get('major_indices', {}))} indices")
