#!/usr/bin/env python3
"""
Test All Data Sources Core
===========================

Core logic for testing all available data sources.
"""

import os
from datetime import datetime

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_yahoo_finance():
    """Test Yahoo Finance API"""
    print("🔍 Testing Yahoo Finance API...")
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/TSLA"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            result = data["chart"]["result"][0]
            meta = result["meta"]

            price = meta["regularMarketPrice"]
            change = meta["regularMarketPrice"] - meta.get(
                "previousClose", meta["regularMarketPrice"]
            )
            volume = meta["regularMarketVolume"]

            print(f"✅ Yahoo Finance: ${price:.2f} (${change:.2f}) Vol: {volume:,}")
            return {
                "source": "Yahoo Finance",
                "price": price,
                "change": change,
                "volume": volume,
                "status": "working",
            }
        else:
            print(f"❌ Yahoo Finance: HTTP {response.status_code}")
            return {"source": "Yahoo Finance", "status": "failed"}

    except Exception as e:
        print(f"❌ Yahoo Finance: {e}")
        return {"source": "Yahoo Finance", "status": "error"}


def test_alpha_vantage():
    """Test Alpha Vantage API"""
    print("🔍 Testing Alpha Vantage API...")

    api_key = os.getenv("ALPHAVANTAGE_API_KEY") or os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        print("❌ Alpha Vantage: No API key found in .env")
        return {"source": "Alpha Vantage", "status": "no_api_key"}

    try:
        url = "https://www.alphavantage.co/query"
        params = {"function": "GLOBAL_QUOTE", "symbol": "TSLA", "apikey": api_key}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "Global Quote" in data:
                quote = data["Global Quote"]
                price = float(quote["05. price"])
                change = float(quote["09. change"])
                volume = int(quote["06. volume"])

                print(f"✅ Alpha Vantage: ${price:.2f} (${change:.2f}) Vol: {volume:,}")
                return {
                    "source": "Alpha Vantage",
                    "price": price,
                    "change": change,
                    "volume": volume,
                    "status": "working",
                }
            else:
                print(f"❌ Alpha Vantage: {data.get('Note', 'Unknown error')}")
                return {"source": "Alpha Vantage", "status": "api_error"}
        else:
            print(f"❌ Alpha Vantage: HTTP {response.status_code}")
            return {"source": "Alpha Vantage", "status": "failed"}

    except Exception as e:
        print(f"❌ Alpha Vantage: {e}")
        return {"source": "Alpha Vantage", "status": "error"}


def test_polygon():
    """Test Polygon.io API"""
    print("🔍 Testing Polygon.io API...")

    api_key = os.getenv("POLYGONIO_API_KEY") or os.getenv("POLYGON_API_KEY")

    if not api_key:
        print("❌ Polygon.io: No API key found in .env")
        return {"source": "Polygon.io", "status": "no_api_key"}

    try:
        url = "https://api.polygon.io/v2/aggs/ticker/TSLA/prev"
        params = {"apikey": api_key}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                price = result["c"]  # Close price
                change = result["c"] - result["o"]  # Close - Open
                volume = result["v"]

                print(f"✅ Polygon.io: ${price:.2f} (${change:.2f}) Vol: {volume:,}")
                return {
                    "source": "Polygon.io",
                    "price": price,
                    "change": change,
                    "volume": volume,
                    "status": "working",
                }
            else:
                print(f"❌ Polygon.io: {data.get('message', 'Unknown error')}")
                return {"source": "Polygon.io", "status": "api_error"}
        else:
            print(f"❌ Polygon.io: HTTP {response.status_code}")
            return {"source": "Polygon.io", "status": "failed"}

    except Exception as e:
        print(f"❌ Polygon.io: {e}")
        return {"source": "Polygon.io", "status": "error"}


def test_finnhub():
    """Test Finnhub API"""
    print("🔍 Testing Finnhub API...")

    api_key = os.getenv("FINNHUB_API_KEY")

    if not api_key:
        print("❌ Finnhub: No API key found in .env")
        return {"source": "Finnhub", "status": "no_api_key"}

    try:
        url = "https://finnhub.io/api/v1/quote"
        params = {"symbol": "TSLA", "token": api_key}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "c" in data:  # Current price
                price = data["c"]
                change = data["d"]  # Change
                volume = data.get("volume", 0)

                print(f"✅ Finnhub: ${price:.2f} (${change:.2f}) Vol: {volume:,}")
                return {
                    "source": "Finnhub",
                    "price": price,
                    "change": change,
                    "volume": volume,
                    "status": "working",
                }
            else:
                print(f"❌ Finnhub: {data.get('error', 'Unknown error')}")
                return {"source": "Finnhub", "status": "api_error"}
        else:
            print(f"❌ Finnhub: HTTP {response.status_code}")
            return {"source": "Finnhub", "status": "failed"}

    except Exception as e:
        print(f"❌ Finnhub: {e}")
        return {"source": "Finnhub", "status": "error"}


def test_news_api():
    """Test News API"""
    print("🔍 Testing News API...")

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        print("❌ News API: No API key found in .env")
        return {"source": "News API", "status": "no_api_key"}

    try:
        url = "https://newsapi.org/v2/everything"
        params = {"q": "Tesla OR TSLA", "sortBy": "publishedAt", "apiKey": api_key, "pageSize": 5}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "ok":
                articles = data.get("articles", [])
                print(f"✅ News API: Found {len(articles)} articles")
                return {"source": "News API", "articles_count": len(articles), "status": "working"}
            else:
                print(f"❌ News API: {data.get('message', 'Unknown error')}")
                return {"source": "News API", "status": "api_error"}
        else:
            print(f"❌ News API: HTTP {response.status_code}")
            return {"source": "News API", "status": "failed"}

    except Exception as e:
        print(f"❌ News API: {e}")
        return {"source": "News API", "status": "error"}


def test_alpaca():
    """Test Alpaca API (if configured)"""
    print("🔍 Testing Alpaca API...")

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

    if not api_key or not secret_key:
        print("❌ Alpaca: No API credentials found in .env")
        return {"source": "Alpaca", "status": "no_credentials"}

    try:
        # Test account info
        url = f"{base_url}/v2/account"
        headers = {"APCA-API-KEY-ID": api_key, "APCA-API-SECRET-KEY": secret_key}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            account_id = data.get("id", "Unknown")
            buying_power = data.get("buying_power", "0")

            print(f"✅ Alpaca: Account {account_id}, Buying Power: ${buying_power}")
            return {
                "source": "Alpaca",
                "account_id": account_id,
                "buying_power": buying_power,
                "status": "working",
            }
        else:
            print(f"❌ Alpaca: HTTP {response.status_code}")
            return {"source": "Alpaca", "status": "failed"}

    except Exception as e:
        print(f"❌ Alpaca: {e}")
        return {"source": "Alpaca", "status": "error"}


def check_env_file():
    """Check what's in the .env file"""
    print("🔍 Checking .env file...")

    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file exists")

        with open(env_file) as f:
            lines = f.readlines()

        api_keys = []
        for line in lines:
            if "API_KEY" in line or "SECRET" in line:
                key_name = line.split("=")[0]
                api_keys.append(key_name)

        if api_keys:
            print(f"📋 Found API keys: {', '.join(api_keys)}")
        else:
            print("❌ No API keys found in .env")
    else:
        print("❌ .env file not found")
