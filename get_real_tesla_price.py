#!/usr/bin/env python3
"""
Get Real Tesla Stock Price
==========================

Get actual current Tesla stock price from free APIs
"""

from datetime import datetime

import requests


def get_tesla_price_yahoo():
    """Get Tesla price from Yahoo Finance (free, no API key needed)"""
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/TSLA"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()

            # Extract price data
            result = data["chart"]["result"][0]
            meta = result["meta"]
            quote = result["indicators"]["quote"][0]

            current_price = meta["regularMarketPrice"]
            previous_close = meta["previousClose"]
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
            volume = meta["regularMarketVolume"]

            return {
                "symbol": "TSLA",
                "price": current_price,
                "change": change,
                "change_percent": change_percent,
                "volume": volume,
                "timestamp": datetime.now().isoformat(),
                "source": "Yahoo Finance",
            }
    except Exception as e:
        print(f"Yahoo Finance error: {e}")
    return None


def get_tesla_price_alpha_vantage():
    """Get Tesla price from Alpha Vantage (free tier)"""
    try:
        # Using demo API key for testing
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": "TSLA",
            "apikey": "demo",  # Demo key - limited requests
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()

            if "Global Quote" in data:
                quote = data["Global Quote"]
                current_price = float(quote["05. price"])
                change = float(quote["09. change"])
                change_percent = float(quote["10. change percent"].replace("%", ""))
                volume = int(quote["06. volume"])

                return {
                    "symbol": "TSLA",
                    "price": current_price,
                    "change": change,
                    "change_percent": change_percent,
                    "volume": volume,
                    "timestamp": datetime.now().isoformat(),
                    "source": "Alpha Vantage",
                }
    except Exception as e:
        print(f"Alpha Vantage error: {e}")
    return None


def get_tesla_price_finnhub():
    """Get Tesla price from Finnhub (free tier)"""
    try:
        url = "https://finnhub.io/api/v1/quote"
        params = {"symbol": "TSLA", "token": "demo"}  # Demo token - limited requests

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()

            if "c" in data:  # Current price
                current_price = data["c"]
                change = data["d"]  # Change
                change_percent = data["dp"]  # Change percent
                volume = data.get("volume", 0)

                return {
                    "symbol": "TSLA",
                    "price": current_price,
                    "change": change,
                    "change_percent": change_percent,
                    "volume": volume,
                    "timestamp": datetime.now().isoformat(),
                    "source": "Finnhub",
                }
    except Exception as e:
        print(f"Finnhub error: {e}")
    return None


def get_real_tesla_price():
    """Get real Tesla stock price from multiple sources"""
    print("🔍 Getting REAL Tesla Stock Price...")
    print("=" * 50)

    # Try Yahoo Finance first (most reliable, no API key needed)
    print("📡 Trying Yahoo Finance...")
    yahoo_data = get_tesla_price_yahoo()
    if yahoo_data:
        print("✅ Yahoo Finance data received!")
        return yahoo_data

    # Try Alpha Vantage
    print("📡 Trying Alpha Vantage...")
    alpha_data = get_tesla_price_alpha_vantage()
    if alpha_data:
        print("✅ Alpha Vantage data received!")
        return alpha_data

    # Try Finnhub
    print("📡 Trying Finnhub...")
    finnhub_data = get_tesla_price_finnhub()
    if finnhub_data:
        print("✅ Finnhub data received!")
        return finnhub_data

    print("❌ All real data sources failed")
    return None


def main():
    """Main function to get and display real Tesla price"""
    real_data = get_real_tesla_price()

    if real_data:
        print("\n🚀 REAL TESLA STOCK DATA:")
        print("=" * 30)
        print(f"Symbol: {real_data['symbol']}")
        print(f"Current Price: ${real_data['price']:.2f}")
        print(f"Change: ${real_data['change']:.2f}")
        print(f"Change %: {real_data['change_percent']:.2f}%")
        print(f"Volume: {real_data['volume']:,}")
        print(f"Source: {real_data['source']}")
        print(f"Timestamp: {real_data['timestamp']}")

        # Now test the trading prediction system with REAL data
        print("\n🤖 TESTING TRADING PREDICTIONS WITH REAL DATA:")
        print("=" * 50)

        from tsla_forecast_app.modules import TradingFlagEngine

        engine = TradingFlagEngine()

        # Analyze real market data
        analysis = engine.analyze_market_data(real_data)
        print("Market Analysis:")
        print(f"  Trend: {analysis.trend_direction}")
        print(f"  Volatility: {analysis.volatility:.1%}")
        print(f"  Support: ${analysis.support_level:.2f}")
        print(f"  Resistance: ${analysis.resistance_level:.2f}")

        # Generate agent predictions
        print("\nAgent Predictions:")
        flags = engine.generate_all_agent_flags(analysis)
        for i, flag in enumerate(flags, 1):
            print(
                f"  {i}. {flag.agent_id.value}: {flag.flag_type.value.upper()} → ${flag.price_target:.2f} ({flag.confidence:.1%})"
            )

        # Get consensus
        consensus = engine.get_consensus_flag(flags)
        print("\n🎯 FINAL PREDICTION:")
        print(f"  Action: {consensus.flag_type.value.upper()}")
        print(f"  Price Target: ${consensus.price_target:.2f}")
        print(f"  Confidence: {consensus.confidence:.1%}")
        print(f"  Reasoning: {consensus.reasoning}")

    else:
        print("❌ Could not get real Tesla stock data")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- API rate limits")
        print("- Market hours (APIs work better during trading hours)")


if __name__ == "__main__":
    main()
