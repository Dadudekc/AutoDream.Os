#!/usr/bin/env python3
"""
Stock Data Worker
=================

Worker thread for fetching Tesla stock data from multiple APIs
V2 Compliant: ≤400 lines, focused data fetching logic
"""

import os
import random
import requests
from datetime import datetime, timedelta
from PyQt5.QtCore import QThread, pyqtSignal


class StockDataWorker(QThread):
    """Worker thread for fetching stock data"""

    data_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.running = True
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self):
        """Load API keys from environment variables"""
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
        """Main worker loop"""
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
        """Try to get real stock data from multiple APIs"""
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

        print("❌ All real data sources failed, using mock data")
        return None

    def _get_alpha_vantage_data(self):
        """Get data from Alpha Vantage API"""
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': 'TSLA',
                'interval': '1min',
                'apikey': self.api_keys['alpha_vantage']
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'Time Series (1min)' in data:
                    return self._parse_alpha_vantage_data(data)
        except Exception as e:
            print(f"Alpha Vantage error: {e}")
        return None

    def _get_polygon_data(self):
        """Get data from Polygon.io API"""
        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/TSLA/prev"
            params = {'apikey': self.api_keys['polygon']}

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    return self._parse_polygon_data(data)
        except Exception as e:
            print(f"Polygon.io error: {e}")
        return None

    def _get_finnhub_data(self):
        """Get data from Finnhub API"""
        try:
            url = f"https://finnhub.io/api/v1/quote"
            params = {
                'symbol': 'TSLA',
                'token': self.api_keys['finnhub']
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'c' in data:  # Current price
                    return self._parse_finnhub_data(data)
        except Exception as e:
            print(f"Finnhub error: {e}")
        return None

    def _parse_alpha_vantage_data(self, data):
        """Parse Alpha Vantage data"""
        try:
            time_series = data['Time Series (1min)']
            latest_time = max(time_series.keys())
            latest_data = time_series[latest_time]

            return {
                'symbol': 'TSLA',
                'price': float(latest_data['4. close']),
                'change': float(latest_data['4. close']) - float(latest_data['1. open']),
                'change_percent': ((float(latest_data['4. close']) - float(latest_data['1. open'])) / float(latest_data['1. open'])) * 100,
                'volume': int(latest_data['5. volume']),
                'timestamp': latest_time,
                'source': 'Alpha Vantage'
            }
        except Exception as e:
            print(f"Alpha Vantage parsing error: {e}")
            return None

    def _parse_polygon_data(self, data):
        """Parse Polygon.io data"""
        try:
            result = data['results'][0]
            return {
                'symbol': 'TSLA',
                'price': result['c'],  # Close price
                'change': result['c'] - result['o'],  # Close - Open
                'change_percent': ((result['c'] - result['o']) / result['o']) * 100,
                'volume': result['v'],
                'timestamp': datetime.fromtimestamp(result['t'] / 1000).isoformat(),
                'source': 'Polygon.io'
            }
        except Exception as e:
            print(f"Polygon.io parsing error: {e}")
            return None

    def _parse_finnhub_data(self, data):
        """Parse Finnhub data"""
        try:
            return {
                'symbol': 'TSLA',
                'price': data['c'],  # Current price
                'change': data['d'],  # Change
                'change_percent': data['dp'],  # Change percent
                'volume': data.get('volume', 0),
                'timestamp': datetime.now().isoformat(),
                'source': 'Finnhub'
            }
        except Exception as e:
            print(f"Finnhub parsing error: {e}")
            return None

    def get_mock_stock_data(self):
        """Generate mock stock data for testing"""
        base_price = 200.0
        change = random.uniform(-10, 10)
        new_price = base_price + change
        change_percent = (change / base_price) * 100

        return {
            'symbol': 'TSLA',
            'price': round(new_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': random.randint(1000000, 50000000),
            'timestamp': datetime.now().isoformat(),
            'source': 'Mock Data'
        }

    def stop(self):
        """Stop the worker thread"""
        self.running = False
        self.quit()
        self.wait()