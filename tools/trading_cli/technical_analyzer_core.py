#!/usr/bin/env python3
"""
Technical Analyzer Core
======================

Core technical analysis functionality for trading predictions.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import os
from typing import Any

import requests


class TechnicalAnalyzer:
    """Advanced technical analysis tool"""

    def __init__(self):
        """Initialize technical analyzer"""
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self) -> dict[str, str]:
        """Load API keys from environment"""
        return {
            "alpha_vantage": os.getenv("ALPHAVANTAGE_API_KEY"),
            "polygon": os.getenv("POLYGONIO_API_KEY"),
        }

    def get_historical_data(self, symbol: str = "TSLA", days: int = 30) -> list[dict[str, Any]]:
        """Get historical price data"""
        print(f"[DATA] Fetching historical data for {symbol} ({days} days)...")

        try:
            # Try Alpha Vantage first
            if self.api_keys["alpha_vantage"]:
                data = self._get_alpha_vantage_historical(symbol)
                if data:
                    return data

            # Fallback to mock data
            return self._get_mock_historical_data(symbol, days)

        except Exception as e:
            print(f"[ERROR] Failed to get historical data: {e}")
            return self._get_mock_historical_data(symbol, days)

    def _get_alpha_vantage_historical(self, symbol: str) -> list[dict[str, Any]] | None:
        """Get historical data from Alpha Vantage API"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_keys["alpha_vantage"],
                "outputsize": "compact",
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "Time Series (Daily)" not in data:
                print(f"[WARNING] No data found for {symbol}")
                return None

            time_series = data["Time Series (Daily)"]
            historical_data = []

            for date, values in time_series.items():
                historical_data.append(
                    {
                        "date": date,
                        "open": float(values["1. open"]),
                        "high": float(values["2. high"]),
                        "low": float(values["3. low"]),
                        "close": float(values["4. close"]),
                        "volume": int(values["5. volume"]),
                    }
                )

            # Sort by date (oldest first)
            historical_data.sort(key=lambda x: x["date"])
            return historical_data[-30:]  # Return last 30 days

        except Exception as e:
            print(f"[ERROR] Alpha Vantage API error: {e}")
            return None

    def _get_mock_historical_data(self, symbol: str, days: int) -> list[dict[str, Any]]:
        """Generate mock historical data for testing"""
        print(f"[MOCK] Generating mock data for {symbol} ({days} days)")

        import random
        from datetime import datetime, timedelta

        base_price = 200.0
        historical_data = []

        for i in range(days):
            date = (datetime.now() - timedelta(days=days - i)).strftime("%Y-%m-%d")

            # Generate realistic price movement
            price_change = random.uniform(-0.05, 0.05)  # ±5% daily change
            base_price *= 1 + price_change

            # Generate OHLC data
            open_price = base_price
            high_price = open_price * random.uniform(1.0, 1.03)
            low_price = open_price * random.uniform(0.97, 1.0)
            close_price = random.uniform(low_price, high_price)
            volume = random.randint(1000000, 5000000)

            historical_data.append(
                {
                    "date": date,
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2),
                    "volume": volume,
                }
            )

        return historical_data

    def analyze_technical(self, symbol: str = "TSLA", days: int = 30) -> dict[str, Any]:
        """Perform comprehensive technical analysis"""
        print(f"[ANALYSIS] Starting technical analysis for {symbol}...")

        # Get historical data
        historical_data = self.get_historical_data(symbol, days)
        if not historical_data:
            return {"error": "Failed to get historical data"}

        # Calculate technical indicators
        indicators = self.calculate_technical_indicators(historical_data)

        # Generate trading signals
        signals = self.generate_technical_signals(historical_data, indicators)

        # Compile analysis results
        analysis = {
            "symbol": symbol,
            "analysis_date": historical_data[-1]["date"],
            "current_price": historical_data[-1]["close"],
            "historical_data": historical_data,
            "technical_indicators": indicators,
            "trading_signals": signals,
            "summary": self._generate_analysis_summary(signals, indicators),
        }

        print(f"[ANALYSIS] Technical analysis completed for {symbol}")
        return analysis

    def display_technical_analysis(self, analysis: dict[str, Any]):
        """Display technical analysis results"""
        print("\n" + "=" * 60)
        print(f"TECHNICAL ANALYSIS: {analysis['symbol']}")
        print("=" * 60)
        print(f"Analysis Date: {analysis['analysis_date']}")
        print(f"Current Price: ${analysis['current_price']:.2f}")
        print()

        # Display technical indicators
        indicators = analysis["technical_indicators"]
        print("TECHNICAL INDICATORS:")
        print(f"  SMA (20): ${indicators['sma_20']:.2f}")
        print(f"  EMA (12): ${indicators['ema_12']:.2f}")
        print(f"  RSI (14): {indicators['rsi_14']:.2f}")
        print(f"  MACD: {indicators['macd']['macd']:.4f}")
        print(f"  MACD Signal: {indicators['macd']['signal']:.4f}")
        print(f"  MACD Histogram: {indicators['macd']['histogram']:.4f}")
        print()

        # Display Bollinger Bands
        bb = indicators["bollinger_bands"]
        print("BOLLINGER BANDS:")
        print(f"  Upper Band: ${bb['upper']:.2f}")
        print(f"  Middle Band: ${bb['middle']:.2f}")
        print(f"  Lower Band: ${bb['lower']:.2f}")
        print()

        # Display Stochastic
        stoch = indicators["stochastic"]
        print("STOCHASTIC OSCILLATOR:")
        print(f"  %K: {stoch['k_percent']:.2f}")
        print(f"  %D: {stoch['d_percent']:.2f}")
        print()

        # Display trading signals
        signals = analysis["trading_signals"]
        print("TRADING SIGNALS:")
        print(f"  Overall Signal: {signals['overall_signal']}")
        print(f"  Signal Strength: {signals['signal_strength']}")
        print(f"  Trend Direction: {signals['trend_direction']}")
        print()

        # Display summary
        print("ANALYSIS SUMMARY:")
        print(f"  {analysis['summary']}")
        print("=" * 60)

    def _generate_analysis_summary(
        self, signals: dict[str, Any], indicators: dict[str, Any]
    ) -> str:
        """Generate analysis summary"""
        overall_signal = signals["overall_signal"]
        signal_strength = signals["signal_strength"]
        trend_direction = signals["trend_direction"]

        if overall_signal == "BUY" and signal_strength == "STRONG":
            return f"Strong buy signal detected. {trend_direction} trend confirmed by multiple indicators."
        elif overall_signal == "SELL" and signal_strength == "STRONG":
            return f"Strong sell signal detected. {trend_direction} trend confirmed by multiple indicators."
        elif overall_signal == "BUY":
            return f"Moderate buy signal. {trend_direction} trend with some confirmation."
        elif overall_signal == "SELL":
            return f"Moderate sell signal. {trend_direction} trend with some confirmation."
        else:
            return f"Neutral signal. {trend_direction} trend with mixed indicators."
