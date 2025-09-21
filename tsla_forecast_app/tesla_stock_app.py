#!/usr/bin/env python3
"""
Tesla Stock Forecast App - PyQt5 Desktop Application
===================================================

Fast desktop application for Tesla stock forecasting with PyQt5.
Simple, fast, and effective for rapid prototyping.

Author: Agent-1 (Backend API & Data Integration)
License: MIT
"""

import sys
import json
import random
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QTabWidget, QTableWidget, QTableWidgetItem,
                             QProgressBar, QGroupBox, QGridLayout, QFrame)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class StockDataWorker(QThread):
    """Worker thread for fetching stock data."""
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
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

class TeslaStockApp(QMainWindow):
    """Main Tesla Stock Forecast Application."""
    
    def __init__(self):
        super().__init__()
        self.stock_data = {}
        self.historical_data = []
        self.init_ui()
        self.start_data_worker()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Tesla Stock Forecast App - PyQt5")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QPushButton {
                background-color: #00ff88;
                color: #000000;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc6a;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #00ff88;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTableWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                gridline-color: #444444;
                border: 1px solid #444444;
            }
            QHeaderView::section {
                background-color: #00ff88;
                color: #000000;
                padding: 4px;
                border: none;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        self.create_header(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_chart_tab()
        self.create_forecast_tab()
        self.create_technical_tab()
        
        # Create status bar
        self.statusBar().showMessage("Tesla Stock Forecast App - Ready")
    
    def create_header(self, layout):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #00ff88;
                color: #000000;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("🚀 Tesla Stock Forecast App")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000;")
        header_layout.addWidget(title_label)
        
        # Status
        self.status_label = QLabel("Loading...")
        self.status_label.setStyleSheet("font-size: 14px; color: #000000;")
        header_layout.addWidget(self.status_label)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header_frame)
    
    def create_dashboard_tab(self):
        """Create the dashboard tab."""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Current price section
        price_group = QGroupBox("Current Stock Price")
        price_layout = QGridLayout(price_group)
        
        self.price_label = QLabel("$0.00")
        self.price_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #00ff88;")
        price_layout.addWidget(QLabel("Price:"), 0, 0)
        price_layout.addWidget(self.price_label, 0, 1)
        
        self.change_label = QLabel("$0.00 (0.00%)")
        self.change_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        price_layout.addWidget(QLabel("Change:"), 1, 0)
        price_layout.addWidget(self.change_label, 1, 1)
        
        self.volume_label = QLabel("0")
        self.volume_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        price_layout.addWidget(QLabel("Volume:"), 2, 0)
        price_layout.addWidget(self.volume_label, 2, 1)
        
        self.market_cap_label = QLabel("$0")
        self.market_cap_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        price_layout.addWidget(QLabel("Market Cap:"), 3, 0)
        price_layout.addWidget(self.market_cap_label, 3, 1)
        
        layout.addWidget(price_group)
        
        # Company info section
        company_group = QGroupBox("Company Information")
        company_layout = QVBoxLayout(company_group)
        
        self.company_text = QTextEdit()
        self.company_text.setMaximumHeight(150)
        self.company_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444;")
        company_layout.addWidget(self.company_text)
        
        layout.addWidget(company_group)
        
        self.tab_widget.addTab(dashboard_widget, "📊 Dashboard")
    
    def create_chart_tab(self):
        """Create the chart tab."""
        chart_widget = QWidget()
        layout = QVBoxLayout(chart_widget)
        
        # Chart controls
        controls_layout = QHBoxLayout()
        
        self.chart_type_btn = QPushButton("📈 Line Chart")
        self.chart_type_btn.clicked.connect(self.toggle_chart_type)
        controls_layout.addWidget(self.chart_type_btn)
        
        self.time_range_btn = QPushButton("📅 30 Days")
        self.time_range_btn.clicked.connect(self.toggle_time_range)
        controls_layout.addWidget(self.time_range_btn)
        
        layout.addLayout(controls_layout)
        
        # Chart display
        self.chart_text = QTextEdit()
        self.chart_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;")
        layout.addWidget(self.chart_text)
        
        self.tab_widget.addTab(chart_widget, "📈 Charts")
    
    def create_forecast_tab(self):
        """Create the forecast tab."""
        forecast_widget = QWidget()
        layout = QVBoxLayout(forecast_widget)
        
        # Forecast section
        forecast_group = QGroupBox("Price Forecast")
        forecast_layout = QGridLayout(forecast_group)
        
        self.forecast_1d_label = QLabel("$0.00")
        self.forecast_1d_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        forecast_layout.addWidget(QLabel("1 Day:"), 0, 0)
        forecast_layout.addWidget(self.forecast_1d_label, 0, 1)
        
        self.forecast_7d_label = QLabel("$0.00")
        self.forecast_7d_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        forecast_layout.addWidget(QLabel("7 Days:"), 1, 0)
        forecast_layout.addWidget(self.forecast_7d_label, 1, 1)
        
        self.forecast_30d_label = QLabel("$0.00")
        self.forecast_30d_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        forecast_layout.addWidget(QLabel("30 Days:"), 2, 0)
        forecast_layout.addWidget(self.forecast_30d_label, 2, 1)
        
        self.confidence_label = QLabel("0%")
        self.confidence_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        forecast_layout.addWidget(QLabel("Confidence:"), 3, 0)
        forecast_layout.addWidget(self.confidence_label, 3, 1)
        
        layout.addWidget(forecast_group)
        
        # Forecast table
        self.forecast_table = QTableWidget(10, 3)
        self.forecast_table.setHorizontalHeaderLabels(["Date", "Price", "Confidence"])
        self.forecast_table.setStyleSheet("QTableWidget { background-color: #2a2a2a; color: #ffffff; }")
        layout.addWidget(self.forecast_table)
        
        self.tab_widget.addTab(forecast_widget, "🔮 Forecast")
    
    def create_technical_tab(self):
        """Create the technical analysis tab."""
        technical_widget = QWidget()
        layout = QVBoxLayout(technical_widget)
        
        # Technical indicators
        tech_group = QGroupBox("Technical Indicators")
        tech_layout = QGridLayout(tech_group)
        
        self.rsi_label = QLabel("0.0")
        self.rsi_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        tech_layout.addWidget(QLabel("RSI:"), 0, 0)
        tech_layout.addWidget(self.rsi_label, 0, 1)
        
        self.macd_label = QLabel("0.0")
        self.macd_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        tech_layout.addWidget(QLabel("MACD:"), 1, 0)
        tech_layout.addWidget(self.macd_label, 1, 1)
        
        self.bb_upper_label = QLabel("$0.00")
        self.bb_upper_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        tech_layout.addWidget(QLabel("Bollinger Upper:"), 2, 0)
        tech_layout.addWidget(self.bb_upper_label, 2, 1)
        
        self.bb_lower_label = QLabel("$0.00")
        self.bb_lower_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        tech_layout.addWidget(QLabel("Bollinger Lower:"), 3, 0)
        tech_layout.addWidget(self.bb_lower_label, 3, 1)
        
        layout.addWidget(tech_group)
        
        # Analysis text
        self.analysis_text = QTextEdit()
        self.analysis_text.setMaximumHeight(200)
        self.analysis_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444;")
        layout.addWidget(self.analysis_text)
        
        self.tab_widget.addTab(technical_widget, "📊 Technical")
    
    def start_data_worker(self):
        """Start the data worker thread."""
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()
    
    def update_stock_data(self, data):
        """Update the stock data display."""
        self.stock_data = data
        
        # Update dashboard
        self.price_label.setText(f"${data['current_price']}")
        
        change_text = f"${data['change']} ({data['change_percent']}%)"
        if data['change'] >= 0:
            self.change_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        else:
            self.change_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        self.change_label.setText(change_text)
        
        self.volume_label.setText(f"{data['volume']:,}")
        self.market_cap_label.setText(f"${data['market_cap']:,}")
        
        # Update company info
        company_info = f"""
Tesla, Inc. (TSLA)
Sector: Consumer Discretionary
Industry: Auto Manufacturers
Website: https://www.tesla.com

Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, 
and energy generation and storage systems in the United States, China, and internationally.

Last Updated: {data['timestamp']}
        """
        self.company_text.setText(company_info)
        
        # Update forecast
        self.update_forecast_data(data)
        
        # Update technical analysis
        self.update_technical_data()
        
        # Update chart
        self.update_chart_display()
        
        # Update status
        source = data.get('source', 'Unknown')
        self.status_label.setText(f"Updated: {datetime.now().strftime('%H:%M:%S')} | Source: {source}")
        self.statusBar().showMessage(f"Tesla Stock: ${data['current_price']} ({data['change_percent']:+.2f}%) | {source}")
    
    def update_forecast_data(self, data):
        """Update forecast data."""
        current_price = data['current_price']
        
        # Generate mock forecasts
        forecast_1d = current_price * (1 + random.uniform(-0.02, 0.02))
        forecast_7d = current_price * (1 + random.uniform(-0.05, 0.05))
        forecast_30d = current_price * (1 + random.uniform(-0.10, 0.10))
        confidence = random.uniform(0.6, 0.8)
        
        self.forecast_1d_label.setText(f"${forecast_1d:.2f}")
        self.forecast_7d_label.setText(f"${forecast_7d:.2f}")
        self.forecast_30d_label.setText(f"${forecast_30d:.2f}")
        self.confidence_label.setText(f"{confidence:.1%}")
        
        # Update forecast table
        self.forecast_table.setRowCount(10)
        for i in range(10):
            date = (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')
            price = current_price * (1 + random.uniform(-0.01, 0.01) * (i+1))
            conf = max(0.5, confidence - (i * 0.02))
            
            self.forecast_table.setItem(i, 0, QTableWidgetItem(date))
            self.forecast_table.setItem(i, 1, QTableWidgetItem(f"${price:.2f}"))
            self.forecast_table.setItem(i, 2, QTableWidgetItem(f"{conf:.1%}"))
    
    def update_technical_data(self):
        """Update technical analysis data."""
        rsi = random.uniform(30, 70)
        macd = random.uniform(-2, 3)
        bb_upper = self.stock_data['current_price'] * 1.05
        bb_lower = self.stock_data['current_price'] * 0.95
        
        self.rsi_label.setText(f"{rsi:.1f}")
        self.macd_label.setText(f"{macd:.2f}")
        self.bb_upper_label.setText(f"${bb_upper:.2f}")
        self.bb_lower_label.setText(f"${bb_lower:.2f}")
        
        # Update analysis text
        analysis = f"""
Technical Analysis Summary:
• RSI: {rsi:.1f} ({'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral'})
• MACD: {macd:.2f} ({'Bullish' if macd > 0 else 'Bearish'})
• Bollinger Bands: Current price is {'above' if self.stock_data['current_price'] > bb_upper else 'below' if self.stock_data['current_price'] < bb_lower else 'within'} the bands
• Trend: {'Uptrend' if self.stock_data['change'] > 0 else 'Downtrend'}

Recommendation: {'BUY' if rsi < 30 and macd > 0 else 'SELL' if rsi > 70 and macd < 0 else 'HOLD'}
        """
        self.analysis_text.setText(analysis)
    
    def update_chart_display(self):
        """Update the chart display."""
        if not self.stock_data:
            return
        
        # Generate mock historical data
        data_points = []
        base_price = self.stock_data['current_price']
        
        for i in range(30, 0, -1):
            date = datetime.now() - timedelta(days=i)
            price = base_price * (1 + random.uniform(-0.05, 0.05))
            data_points.append((date.strftime('%m/%d'), price))
            base_price = price
        
        # Create ASCII chart
        chart_text = "Tesla Stock Price Chart (30 Days)\n"
        chart_text += "=" * 50 + "\n\n"
        
        for date, price in data_points:
            bar_length = int((price / max(p[1] for p in data_points)) * 40)
            chart_text += f"{date}: ${price:.2f} {'█' * bar_length}\n"
        
        chart_text += f"\nCurrent Price: ${self.stock_data['current_price']:.2f}\n"
        chart_text += f"Change: ${self.stock_data['change']:.2f} ({self.stock_data['change_percent']:+.2f}%)\n"
        
        self.chart_text.setText(chart_text)
    
    def toggle_chart_type(self):
        """Toggle chart type."""
        current_text = self.chart_type_btn.text()
        if "Line" in current_text:
            self.chart_type_btn.setText("📊 Bar Chart")
        else:
            self.chart_type_btn.setText("📈 Line Chart")
        self.update_chart_display()
    
    def toggle_time_range(self):
        """Toggle time range."""
        current_text = self.time_range_btn.text()
        if "30 Days" in current_text:
            self.time_range_btn.setText("📅 7 Days")
        elif "7 Days" in current_text:
            self.time_range_btn.setText("📅 90 Days")
        else:
            self.time_range_btn.setText("📅 30 Days")
        self.update_chart_display()
    
    def refresh_data(self):
        """Refresh stock data."""
        self.status_label.setText("Refreshing...")
        self.data_worker.stop()
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()
    
    def closeEvent(self, event):
        """Handle application close."""
        if hasattr(self, 'data_worker'):
            self.data_worker.stop()
        event.accept()

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Tesla Stock Forecast App")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = TeslaStockApp()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
