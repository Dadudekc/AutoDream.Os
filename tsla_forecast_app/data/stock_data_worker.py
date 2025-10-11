#!/usr/bin/env python3
"""
Stock Data Worker - V2 Compliant
===============================

Worker thread for fetching stock data following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Backend API & Data Integration)
License: MIT
"""

import os
import random
import requests
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class StockDataWorker(QThread):
    """Worker thread for fetching stock data."""
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
        """Initialize stock data worker."""
        super().__init__()
        self.running = True
        self.api_keys = self._load_api_keys()
    
    def _load_api_keys(self):
        """Load API keys from environment variables."""
        keys = {
            'polygon': os.getenv('POLYGONIO_API_KEY'),
            'alpha_vantage': os.getenv('ALPHAVANTAGE_API_KEY'),
            'nasdaq': os.getenv('NASDAQ_API_KEY'),
            'fred': os.getenv('FRED_API_KEY'),
            'finnhub': os.getenv('FINNHUB_API_KEY')
        }
        
        # Debug: Print which keys are loaded
        print("🔑 API Keys Status:")
        for name, key in keys.items():
            status = "✅ Found" if key else "❌ Missing"
            print(f"   {name}: {status}")
        
        return keys
    
    def run(self):
        """Main worker loop."""
        while self.running:
            try:
                # Try to get real data from multiple APIs
                data = self.get_real_stock_data()
                if data:
                    self.data_updated.emit(data)
                else:
                    # Fall back to mock data
                    data = self.get_mock_stock_data()
                    self.data_updated.emit(data)
            except Exception as e:
                print(f"Error fetching data: {e}")
                data = self.get_mock_stock_data()
                self.data_updated.emit(data)
            
            self.msleep(10000)  # Update every 10 seconds (API rate limits)
    
    def get_real_stock_data(self):
        """Try to get real stock data from multiple APIs."""
        print("🔍 Attempting to fetch real stock data...")
        
        # Try Alpha Vantage first (most reliable)
        if self.api_keys['alpha_vantage']:
            print("📡 Trying Alpha Vantage API...")
            data = self._get_alpha_vantage_data()
            if data:
                print("✅ Alpha Vantage data received!")
                return data
            else:
                print("❌ Alpha Vantage failed")
        
        # Try Polygon.io
        if self.api_keys['polygon']:
            print("📡 Trying Polygon.io API...")
            data = self._get_polygon_data()
            if data:
                print("✅ Polygon.io data received!")
                return data
            else:
                print("❌ Polygon.io failed")
        
        # Try Finnhub
        if self.api_keys['finnhub']:
            print("📡 Trying Finnhub API...")
            data = self._get_finnhub_data()
            if data:
                print("✅ Finnhub data received!")
                return data
            else:
                print("❌ Finnhub failed")
        
        # Try local Flask API as fallback
        try:
            print("📡 Trying local Flask API...")
            response = requests.get('http://localhost:5000/api/stock/current', timeout=2)
            if response.status_code == 200:
                print("✅ Local Flask data received!")
                return response.json()
        except Exception as e:
            print(f"❌ Local Flask failed: {e}")
        
        print("⚠️ All APIs failed, using mock data")
        return None
    
    def _get_alpha_vantage_data(self):
        """Get data from Alpha Vantage API."""
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'TSLA',
                'apikey': self.api_keys['alpha_vantage']
            }
            print(f"   📡 Alpha Vantage URL: {url}")
            print(f"   🔑 Using API key: {self.api_keys['alpha_vantage'][:8]}...")
            
            response = requests.get(url, params=params, timeout=10)
            print(f"   📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   📋 Response data keys: {list(data.keys())}")
                
                # Check for API error messages
                if 'Error Message' in data:
                    print(f"   ❌ API Error: {data['Error Message']}")
                    return None
                if 'Note' in data:
                    print(f"   ⚠️ API Note: {data['Note']}")
                    return None
                
                quote = data.get('Global Quote', {})
                if quote and quote.get('05. price'):
                    current_price = float(quote.get('05. price', 0))
                    previous_close = float(quote.get('08. previous close', current_price))
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close > 0 else 0
                    
                    print(f"   ✅ Price: ${current_price}, Change: {change_percent:.2f}%")
                    
                    return {
                        "symbol": "TSLA",
                        "current_price": round(current_price, 2),
                        "previous_close": round(previous_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "volume": int(quote.get('06. volume', 0)),
                        "market_cap": 0,  # Not provided by Alpha Vantage
                        "timestamp": datetime.now().isoformat(),
                        "source": "Alpha Vantage"
                    }
                else:
                    print("   ❌ No valid quote data in response")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Alpha Vantage API error: {e}")
        return None
    
    def _get_polygon_data(self):
        """Get data from Polygon.io API."""
        try:
            url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/TSLA"
            params = {'apikey': self.api_keys['polygon']}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                ticker_data = data.get('ticker', {})
                if ticker_data:
                    current_price = ticker_data.get('day', {}).get('c', 0)  # Close price
                    previous_close = ticker_data.get('prevDay', {}).get('c', current_price)
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close > 0 else 0
                    
                    return {
                        "symbol": "TSLA",
                        "current_price": round(current_price, 2),
                        "previous_close": round(previous_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "volume": ticker_data.get('day', {}).get('v', 0),
                        "market_cap": ticker_data.get('market_cap', 0),
                        "timestamp": datetime.now().isoformat(),
                        "source": "Polygon.io"
                    }
        except Exception as e:
            print(f"Polygon.io API error: {e}")
        return None
    
    def _get_finnhub_data(self):
        """Get data from Finnhub API."""
        try:
            url = f"https://finnhub.io/api/v1/quote"
            params = {
                'symbol': 'TSLA',
                'token': self.api_keys['finnhub']
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('c'):  # Current price exists
                    current_price = data.get('c', 0)
                    previous_close = data.get('pc', current_price)
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close > 0 else 0
                    
                    return {
                        "symbol": "TSLA",
                        "current_price": round(current_price, 2),
                        "previous_close": round(previous_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "volume": 0,  # Not provided by Finnhub quote endpoint
                        "market_cap": 0,  # Not provided by Finnhub quote endpoint
                        "timestamp": datetime.now().isoformat(),
                        "source": "Finnhub"
                    }
        except Exception as e:
            print(f"Finnhub API error: {e}")
        return None
    
    def get_mock_stock_data(self):
        """Generate mock stock data."""
        base_price = 275.0
        change = random.uniform(-5, 5)
        current_price = base_price + change
        
        return {
            "symbol": "TSLA",
            "current_price": round(current_price, 2),
            "previous_close": round(base_price, 2),
            "change": round(change, 2),
            "change_percent": round((change / base_price) * 100, 2),
            "volume": random.randint(50000000, 100000000),
            "market_cap": random.randint(800000000000, 900000000000),
            "timestamp": datetime.now().isoformat(),
            "source": "Mock Data (No API keys found)"
        }
    
    def stop(self):
        """Stop the worker thread."""
        self.running = False
        self.wait()  # Wait for thread to finish