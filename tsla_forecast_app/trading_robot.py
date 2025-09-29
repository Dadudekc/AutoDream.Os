#!/usr/bin/env python3
"""
Tesla Trading Robot - Advanced Trading System
============================================

A powerful trading robot for Tesla stock with:
- Real-time market data
- Technical analysis indicators
- Automated trading strategies
- Risk management
- Portfolio tracking
- Backtesting capabilities

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import sys
from datetime import datetime

import numpy as np
from dotenv import load_dotenv
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Load environment variables
load_dotenv()


class TradingStrategy:
    """Base class for trading strategies."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.enabled = False
        self.positions = []
        self.performance = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_profit": 0.0,
            "win_rate": 0.0,
        }

    def analyze(self, data):
        """Analyze market data and return trading signals."""
        return {"action": "HOLD", "confidence": 0.0, "reason": "No signal"}

    def execute_trade(self, action, price, quantity):
        """Execute a trade."""
        trade = {
            "timestamp": datetime.now(),
            "action": action,
            "price": price,
            "quantity": quantity,
            "strategy": self.name,
        }
        self.positions.append(trade)
        self.performance["total_trades"] += 1
        return trade


class MovingAverageStrategy(TradingStrategy):
    """Moving Average Crossover Strategy."""

    def __init__(self):
        super().__init__("Moving Average Crossover", "Buy when short MA crosses above long MA")
        self.short_period = 10
        self.long_period = 30
        self.price_history = []

    def analyze(self, data):
        """Analyze using moving average crossover."""
        current_price = data["current_price"]
        self.price_history.append(current_price)

        # Keep only last 50 prices
        if len(self.price_history) > 50:
            self.price_history = self.price_history[-50:]

        if len(self.price_history) < self.long_period:
            return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient data"}

        # Calculate moving averages
        short_ma = np.mean(self.price_history[-self.short_period :])
        long_ma = np.mean(self.price_history[-self.long_period :])
        prev_short_ma = np.mean(self.price_history[-self.short_period - 1 : -1])
        prev_long_ma = np.mean(self.price_history[-self.long_period - 1 : -1])

        # Check for crossover
        if prev_short_ma <= prev_long_ma and short_ma > long_ma:
            return {
                "action": "BUY",
                "confidence": 0.8,
                "reason": f"Golden Cross: MA{self.short_period} > MA{self.long_period}",
            }
        elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
            return {
                "action": "SELL",
                "confidence": 0.8,
                "reason": f"Death Cross: MA{self.short_period} < MA{self.long_period}",
            }

        return {
            "action": "HOLD",
            "confidence": 0.5,
            "reason": f"MA{self.short_period}={short_ma:.2f}, MA{self.long_period}={long_ma:.2f}",
        }


class RSIMeanReversionStrategy(TradingStrategy):
    """RSI Mean Reversion Strategy."""

    def __init__(self):
        super().__init__("RSI Mean Reversion", "Buy when RSI < 30, Sell when RSI > 70")
        self.price_history = []
        self.rsi_period = 14

    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return 50

        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def analyze(self, data):
        """Analyze using RSI mean reversion."""
        current_price = data["current_price"]
        self.price_history.append(current_price)

        if len(self.price_history) < self.rsi_period + 1:
            return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient data for RSI"}

        rsi = self.calculate_rsi(self.price_history, self.rsi_period)

        if rsi < 30:
            return {"action": "BUY", "confidence": 0.9, "reason": f"RSI oversold: {rsi:.1f}"}
        elif rsi > 70:
            return {"action": "SELL", "confidence": 0.9, "reason": f"RSI overbought: {rsi:.1f}"}

        return {"action": "HOLD", "confidence": 0.5, "reason": f"RSI neutral: {rsi:.1f}"}


class BollingerBandsStrategy(TradingStrategy):
    """Bollinger Bands Strategy."""

    def __init__(self):
        super().__init__(
            "Bollinger Bands",
            "Buy when price touches lower band, Sell when price touches upper band",
        )
        self.price_history = []
        self.bb_period = 20
        self.bb_std = 2

    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return None, None, None

        sma = np.mean(prices[-period:])
        std = np.std(prices[-period:])

        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)

        return upper_band, sma, lower_band

    def analyze(self, data):
        """Analyze using Bollinger Bands."""
        current_price = data["current_price"]
        self.price_history.append(current_price)

        if len(self.price_history) < self.bb_period:
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "reason": "Insufficient data for Bollinger Bands",
            }

        upper, middle, lower = self.calculate_bollinger_bands(
            self.price_history, self.bb_period, self.bb_std
        )

        if current_price <= lower:
            return {
                "action": "BUY",
                "confidence": 0.85,
                "reason": f"Price at lower band: ${current_price:.2f} <= ${lower:.2f}",
            }
        elif current_price >= upper:
            return {
                "action": "SELL",
                "confidence": 0.85,
                "reason": f"Price at upper band: ${current_price:.2f} >= ${upper:.2f}",
            }

        return {
            "action": "HOLD",
            "confidence": 0.5,
            "reason": f"Price within bands: ${lower:.2f} < ${current_price:.2f} < ${upper:.2f}",
        }


class TradingRobot(QMainWindow):
    """Main Trading Robot Application."""

    def __init__(self):
        super().__init__()
        self.stock_data = {}
        self.portfolio = {
            "cash": 100000.0,  # Starting cash
            "shares": 0,
            "total_value": 100000.0,
            "trades": [],
            "daily_pnl": 0.0,
            "total_pnl": 0.0,
        }
        self.strategies = {
            "ma_crossover": MovingAverageStrategy(),
            "rsi_mean_reversion": RSIMeanReversionStrategy(),
            "bollinger_bands": BollingerBandsStrategy(),
        }
        self.active_strategies = []
        self.trading_enabled = False
        self.risk_management = {
            "max_position_size": 0.1,  # 10% of portfolio
            "stop_loss_pct": 0.05,  # 5% stop loss
            "take_profit_pct": 0.10,  # 10% take profit
            "max_daily_loss": 0.02,  # 2% max daily loss
        }
        self.init_ui()
        self.start_data_worker()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Tesla Trading Robot - Advanced Trading System")
        self.setGeometry(100, 100, 1400, 900)

        # Set dark theme
        self.setStyleSheet(
            """
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
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
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
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444444;
                padding: 4px;
                border-radius: 4px;
            }
            QCheckBox {
                color: #ffffff;
            }
            QComboBox {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444444;
                padding: 4px;
                border-radius: 4px;
            }
        """
        )

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
        self.create_strategies_tab()
        self.create_portfolio_tab()
        self.create_trading_tab()
        self.create_risk_tab()
        self.create_backtest_tab()

        # Create status bar
        self.statusBar().showMessage("Trading Robot - Ready")

    def create_header(self, layout):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setStyleSheet(
            """
            QFrame {
                background-color: #00ff88;
                color: #000000;
                border-radius: 8px;
                padding: 10px;
            }
        """
        )
        header_layout = QHBoxLayout(header_frame)

        # Title
        title_label = QLabel("🤖 Tesla Trading Robot")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000;")
        header_layout.addWidget(title_label)

        # Status
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("font-size: 14px; color: #000000;")
        header_layout.addWidget(self.status_label)

        # Trading toggle
        self.trading_toggle = QPushButton("🔴 STOP TRADING")
        self.trading_toggle.clicked.connect(self.toggle_trading)
        self.trading_toggle.setStyleSheet(
            """
            QPushButton {
                background-color: #ff4444;
                color: #ffffff;
                font-weight: bold;
                padding: 10px 20px;
            }
        """
        )
        header_layout.addWidget(self.trading_toggle)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)

        layout.addWidget(header_frame)

    def create_dashboard_tab(self):
        """Create the dashboard tab."""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)

        # Market data section
        market_group = QGroupBox("Market Data")
        market_layout = QGridLayout(market_group)

        self.price_label = QLabel("$0.00")
        self.price_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #00ff88;")
        market_layout.addWidget(QLabel("Price:"), 0, 0)
        market_layout.addWidget(self.price_label, 0, 1)

        self.change_label = QLabel("$0.00 (0.00%)")
        self.change_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        market_layout.addWidget(QLabel("Change:"), 1, 0)
        market_layout.addWidget(self.change_label, 1, 1)

        self.volume_label = QLabel("0")
        self.volume_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        market_layout.addWidget(QLabel("Volume:"), 2, 0)
        market_layout.addWidget(self.volume_label, 2, 1)

        layout.addWidget(market_group)

        # Portfolio summary
        portfolio_group = QGroupBox("Portfolio Summary")
        portfolio_layout = QGridLayout(portfolio_group)

        self.cash_label = QLabel("$100,000.00")
        self.cash_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        portfolio_layout.addWidget(QLabel("Cash:"), 0, 0)
        portfolio_layout.addWidget(self.cash_label, 0, 1)

        self.shares_label = QLabel("0")
        self.shares_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        portfolio_layout.addWidget(QLabel("Shares:"), 1, 0)
        portfolio_layout.addWidget(self.shares_label, 1, 1)

        self.total_value_label = QLabel("$100,000.00")
        self.total_value_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        portfolio_layout.addWidget(QLabel("Total Value:"), 2, 0)
        portfolio_layout.addWidget(self.total_value_label, 2, 1)

        self.pnl_label = QLabel("$0.00 (0.00%)")
        self.pnl_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        portfolio_layout.addWidget(QLabel("P&L:"), 3, 0)
        portfolio_layout.addWidget(self.pnl_label, 3, 1)

        layout.addWidget(portfolio_group)

        # Trading signals
        signals_group = QGroupBox("Trading Signals")
        signals_layout = QVBoxLayout(signals_group)

        self.signals_text = QTextEdit()
        self.signals_text.setMaximumHeight(200)
        self.signals_text.setStyleSheet(
            "background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;"
        )
        signals_layout.addWidget(self.signals_text)

        layout.addWidget(signals_group)

        self.tab_widget.addTab(dashboard_widget, "📊 Dashboard")

    def create_strategies_tab(self):
        """Create the strategies tab."""
        strategies_widget = QWidget()
        layout = QVBoxLayout(strategies_widget)

        # Strategy controls
        controls_group = QGroupBox("Strategy Controls")
        controls_layout = QGridLayout(controls_group)

        # Moving Average Strategy
        self.ma_enabled = QCheckBox("Enable Moving Average Crossover")
        self.ma_enabled.toggled.connect(self.toggle_strategy)
        controls_layout.addWidget(self.ma_enabled, 0, 0)

        self.ma_short = QSpinBox()
        self.ma_short.setRange(5, 50)
        self.ma_short.setValue(10)
        self.ma_short.valueChanged.connect(self.update_strategy_params)
        controls_layout.addWidget(QLabel("Short Period:"), 1, 0)
        controls_layout.addWidget(self.ma_short, 1, 1)

        self.ma_long = QSpinBox()
        self.ma_long.setRange(10, 100)
        self.ma_long.setValue(30)
        self.ma_long.valueChanged.connect(self.update_strategy_params)
        controls_layout.addWidget(QLabel("Long Period:"), 2, 0)
        controls_layout.addWidget(self.ma_long, 2, 1)

        # RSI Strategy
        self.rsi_enabled = QCheckBox("Enable RSI Mean Reversion")
        self.rsi_enabled.toggled.connect(self.toggle_strategy)
        controls_layout.addWidget(self.rsi_enabled, 3, 0)

        self.rsi_period = QSpinBox()
        self.rsi_period.setRange(5, 30)
        self.rsi_period.setValue(14)
        self.rsi_period.valueChanged.connect(self.update_strategy_params)
        controls_layout.addWidget(QLabel("RSI Period:"), 4, 0)
        controls_layout.addWidget(self.rsi_period, 4, 1)

        # Bollinger Bands Strategy
        self.bb_enabled = QCheckBox("Enable Bollinger Bands")
        self.bb_enabled.toggled.connect(self.toggle_strategy)
        controls_layout.addWidget(self.bb_enabled, 5, 0)

        self.bb_period = QSpinBox()
        self.bb_period.setRange(10, 50)
        self.bb_period.setValue(20)
        self.bb_period.valueChanged.connect(self.update_strategy_params)
        controls_layout.addWidget(QLabel("BB Period:"), 6, 0)
        controls_layout.addWidget(self.bb_period, 6, 1)

        layout.addWidget(controls_group)

        # Strategy performance
        performance_group = QGroupBox("Strategy Performance")
        performance_layout = QVBoxLayout(performance_group)

        self.performance_table = QTableWidget(3, 5)
        self.performance_table.setHorizontalHeaderLabels(
            ["Strategy", "Trades", "Win Rate", "Profit", "Status"]
        )
        self.performance_table.setStyleSheet(
            "QTableWidget { background-color: #2a2a2a; color: #ffffff; }"
        )
        performance_layout.addWidget(self.performance_table)

        layout.addWidget(performance_group)

        self.tab_widget.addTab(strategies_widget, "🎯 Strategies")

    def create_portfolio_tab(self):
        """Create the portfolio tab."""
        portfolio_widget = QWidget()
        layout = QVBoxLayout(portfolio_widget)

        # Portfolio details
        details_group = QGroupBox("Portfolio Details")
        details_layout = QVBoxLayout(details_group)

        self.portfolio_table = QTableWidget(0, 6)
        self.portfolio_table.setHorizontalHeaderLabels(
            ["Time", "Action", "Price", "Quantity", "Value", "Strategy"]
        )
        self.portfolio_table.setStyleSheet(
            "QTableWidget { background-color: #2a2a2a; color: #ffffff; }"
        )
        details_layout.addWidget(self.portfolio_table)

        layout.addWidget(details_group)

        # Performance chart (placeholder)
        chart_group = QGroupBox("Performance Chart")
        chart_layout = QVBoxLayout(chart_group)

        self.chart_text = QTextEdit()
        self.chart_text.setStyleSheet(
            "background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;"
        )
        chart_layout.addWidget(self.chart_text)

        layout.addWidget(chart_group)

        self.tab_widget.addTab(portfolio_widget, "💼 Portfolio")

    def create_trading_tab(self):
        """Create the trading tab."""
        trading_widget = QWidget()
        layout = QVBoxLayout(trading_widget)

        # Manual trading
        manual_group = QGroupBox("Manual Trading")
        manual_layout = QGridLayout(manual_group)

        self.buy_btn = QPushButton("🟢 BUY")
        self.buy_btn.clicked.connect(self.manual_buy)
        self.buy_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #00ff88;
                color: #000000;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
            }
        """
        )
        manual_layout.addWidget(self.buy_btn, 0, 0)

        self.sell_btn = QPushButton("🔴 SELL")
        self.sell_btn.clicked.connect(self.manual_sell)
        self.sell_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #ff4444;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
            }
        """
        )
        manual_layout.addWidget(self.sell_btn, 0, 1)

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)
        self.quantity_input.setValue(10)
        manual_layout.addWidget(QLabel("Quantity:"), 1, 0)
        manual_layout.addWidget(self.quantity_input, 1, 1)

        layout.addWidget(manual_group)

        # Trading log
        log_group = QGroupBox("Trading Log")
        log_layout = QVBoxLayout(log_group)

        self.trading_log = QTextEdit()
        self.trading_log.setStyleSheet(
            "background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;"
        )
        log_layout.addWidget(self.trading_log)

        layout.addWidget(log_group)

        self.tab_widget.addTab(trading_widget, "⚡ Trading")

    def create_risk_tab(self):
        """Create the risk management tab."""
        risk_widget = QWidget()
        layout = QVBoxLayout(risk_widget)

        # Risk parameters
        risk_group = QGroupBox("Risk Parameters")
        risk_layout = QGridLayout(risk_group)

        self.max_position = QDoubleSpinBox()
        self.max_position.setRange(0.01, 1.0)
        self.max_position.setValue(0.1)
        self.max_position.setDecimals(2)
        self.max_position.valueChanged.connect(self.update_risk_params)
        risk_layout.addWidget(QLabel("Max Position Size:"), 0, 0)
        risk_layout.addWidget(self.max_position, 0, 1)

        self.stop_loss = QDoubleSpinBox()
        self.stop_loss.setRange(0.01, 0.50)
        self.stop_loss.setValue(0.05)
        self.stop_loss.setDecimals(2)
        self.stop_loss.valueChanged.connect(self.update_risk_params)
        risk_layout.addWidget(QLabel("Stop Loss %:"), 1, 0)
        risk_layout.addWidget(self.stop_loss, 1, 1)

        self.take_profit = QDoubleSpinBox()
        self.take_profit.setRange(0.01, 1.0)
        self.take_profit.setValue(0.10)
        self.take_profit.setDecimals(2)
        self.take_profit.valueChanged.connect(self.update_risk_params)
        risk_layout.addWidget(QLabel("Take Profit %:"), 2, 0)
        risk_layout.addWidget(self.take_profit, 2, 1)

        self.max_daily_loss = QDoubleSpinBox()
        self.max_daily_loss.setRange(0.01, 0.20)
        self.max_daily_loss.setValue(0.02)
        self.max_daily_loss.setDecimals(2)
        self.max_daily_loss.valueChanged.connect(self.update_risk_params)
        risk_layout.addWidget(QLabel("Max Daily Loss %:"), 3, 0)
        risk_layout.addWidget(self.max_daily_loss, 3, 1)

        layout.addWidget(risk_group)

        # Risk monitoring
        monitor_group = QGroupBox("Risk Monitoring")
        monitor_layout = QVBoxLayout(monitor_group)

        self.risk_text = QTextEdit()
        self.risk_text.setMaximumHeight(200)
        self.risk_text.setStyleSheet(
            "background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;"
        )
        monitor_layout.addWidget(self.risk_text)

        layout.addWidget(monitor_group)

        self.tab_widget.addTab(risk_widget, "🛡️ Risk")

    def create_backtest_tab(self):
        """Create the backtesting tab."""
        backtest_widget = QWidget()
        layout = QVBoxLayout(backtest_widget)

        # Backtest controls
        controls_group = QGroupBox("Backtest Controls")
        controls_layout = QGridLayout(controls_group)

        self.backtest_start = QLineEdit()
        self.backtest_start.setText("2024-01-01")
        controls_layout.addWidget(QLabel("Start Date:"), 0, 0)
        controls_layout.addWidget(self.backtest_start, 0, 1)

        self.backtest_end = QLineEdit()
        self.backtest_end.setText("2024-12-31")
        controls_layout.addWidget(QLabel("End Date:"), 1, 0)
        controls_layout.addWidget(self.backtest_end, 1, 1)

        self.backtest_btn = QPushButton("🚀 Run Backtest")
        self.backtest_btn.clicked.connect(self.run_backtest)
        controls_layout.addWidget(self.backtest_btn, 2, 0, 1, 2)

        layout.addWidget(controls_group)

        # Backtest results
        results_group = QGroupBox("Backtest Results")
        results_layout = QVBoxLayout(results_group)

        self.backtest_results = QTextEdit()
        self.backtest_results.setStyleSheet(
            "background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;"
        )
        results_layout.addWidget(self.backtest_results)

        layout.addWidget(results_group)

        self.tab_widget.addTab(backtest_widget, "📈 Backtest")

    def start_data_worker(self):
        """Start the data worker thread."""
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()

    def update_stock_data(self, data):
        """Update stock data and run trading strategies."""
        self.stock_data = data

        # Update UI
        self.price_label.setText(f"${data['current_price']}")

        change_text = f"${data['change']} ({data['change_percent']}%)"
        if data["change"] >= 0:
            self.change_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        else:
            self.change_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        self.change_label.setText(change_text)

        self.volume_label.setText(f"{data['volume']:,}")

        # Update portfolio
        self.update_portfolio_display()

        # Run trading strategies
        if self.trading_enabled:
            self.run_trading_strategies(data)

        # Update status
        source = data.get("source", "Unknown")
        self.status_label.setText(f"Updated: {datetime.now().strftime('%H:%M:%S')} | {source}")
        self.statusBar().showMessage(
            f"Tesla: ${data['current_price']} ({data['change_percent']:+.2f}%) | Trading: {'ON' if self.trading_enabled else 'OFF'}"
        )

    def run_trading_strategies(self, data):
        """Run all active trading strategies."""
        signals = []

        for strategy_name, strategy in self.strategies.items():
            if strategy.enabled:
                signal = strategy.analyze(data)
                signals.append(
                    f"{strategy.name}: {signal['action']} (Confidence: {signal['confidence']:.1f}) - {signal['reason']}"
                )

                # Execute trades based on signals
                if signal["action"] in ["BUY", "SELL"] and signal["confidence"] > 0.7:
                    self.execute_strategy_trade(strategy, signal, data)

        # Update signals display
        self.signals_text.setText("\n".join(signals))

    def execute_strategy_trade(self, strategy, signal, data):
        """Execute a trade based on strategy signal."""
        current_price = data["current_price"]

        # Calculate position size based on risk management
        max_position_value = (
            self.portfolio["total_value"] * self.risk_management["max_position_size"]
        )
        quantity = int(max_position_value / current_price)

        if quantity > 0:
            if signal["action"] == "BUY" and self.portfolio["cash"] >= current_price * quantity:
                # Execute buy
                trade = strategy.execute_trade("BUY", current_price, quantity)
                self.portfolio["cash"] -= current_price * quantity
                self.portfolio["shares"] += quantity
                self.portfolio["trades"].append(trade)

                self.log_trade(
                    f"🤖 {strategy.name}: BOUGHT {quantity} shares at ${current_price:.2f}"
                )

            elif signal["action"] == "SELL" and self.portfolio["shares"] >= quantity:
                # Execute sell
                trade = strategy.execute_trade("SELL", current_price, quantity)
                self.portfolio["cash"] += current_price * quantity
                self.portfolio["shares"] -= quantity
                self.portfolio["trades"].append(trade)

                self.log_trade(f"🤖 {strategy.name}: SOLD {quantity} shares at ${current_price:.2f}")

    def update_portfolio_display(self):
        """Update portfolio display."""
        if self.stock_data:
            current_price = self.stock_data["current_price"]
            self.portfolio["total_value"] = self.portfolio["cash"] + (
                self.portfolio["shares"] * current_price
            )

            self.cash_label.setText(f"${self.portfolio['cash']:,.2f}")
            self.shares_label.setText(f"{self.portfolio['shares']}")
            self.total_value_label.setText(f"${self.portfolio['total_value']:,.2f}")

            # Calculate P&L
            initial_value = 100000.0
            pnl = self.portfolio["total_value"] - initial_value
            pnl_pct = (pnl / initial_value) * 100

            self.portfolio["total_pnl"] = pnl

            if pnl >= 0:
                self.pnl_label.setStyleSheet("font-size: 18px; color: #00ff88;")
            else:
                self.pnl_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")

            self.pnl_label.setText(f"${pnl:,.2f} ({pnl_pct:+.2f}%)")

    def toggle_trading(self):
        """Toggle trading on/off."""
        self.trading_enabled = not self.trading_enabled

        if self.trading_enabled:
            self.trading_toggle.setText("🟢 TRADING ON")
            self.trading_toggle.setStyleSheet(
                """
                QPushButton {
                    background-color: #00ff88;
                    color: #000000;
                    font-weight: bold;
                    padding: 10px 20px;
                }
            """
            )
            self.log_trade("🤖 Trading ENABLED")
        else:
            self.trading_toggle.setText("🔴 STOP TRADING")
            self.trading_toggle.setStyleSheet(
                """
                QPushButton {
                    background-color: #ff4444;
                    color: #ffffff;
                    font-weight: bold;
                    padding: 10px 20px;
                }
            """
            )
            self.log_trade("🤖 Trading DISABLED")

    def toggle_strategy(self):
        """Toggle strategy on/off."""
        sender = self.sender()

        if sender == self.ma_enabled:
            self.strategies["ma_crossover"].enabled = sender.isChecked()
        elif sender == self.rsi_enabled:
            self.strategies["rsi_mean_reversion"].enabled = sender.isChecked()
        elif sender == self.bb_enabled:
            self.strategies["bollinger_bands"].enabled = sender.isChecked()

        self.update_strategy_performance()

    def update_strategy_params(self):
        """Update strategy parameters."""
        self.strategies["ma_crossover"].short_period = self.ma_short.value()
        self.strategies["ma_crossover"].long_period = self.ma_long.value()
        self.strategies["rsi_mean_reversion"].rsi_period = self.rsi_period.value()
        self.strategies["bollinger_bands"].bb_period = self.bb_period.value()

    def update_risk_params(self):
        """Update risk management parameters."""
        self.risk_management["max_position_size"] = self.max_position.value()
        self.risk_management["stop_loss_pct"] = self.stop_loss.value()
        self.risk_management["take_profit_pct"] = self.take_profit.value()
        self.risk_management["max_daily_loss"] = self.max_daily_loss.value()

    def manual_buy(self):
        """Execute manual buy order."""
        if self.stock_data:
            quantity = self.quantity_input.value()
            current_price = self.stock_data["current_price"]
            total_cost = current_price * quantity

            if self.portfolio["cash"] >= total_cost:
                self.portfolio["cash"] -= total_cost
                self.portfolio["shares"] += quantity

                trade = {
                    "timestamp": datetime.now(),
                    "action": "BUY",
                    "price": current_price,
                    "quantity": quantity,
                    "strategy": "Manual",
                }
                self.portfolio["trades"].append(trade)

                self.log_trade(f"👤 MANUAL: BOUGHT {quantity} shares at ${current_price:.2f}")
                self.update_portfolio_display()
            else:
                self.log_trade(
                    f"❌ INSUFFICIENT CASH: Need ${total_cost:.2f}, have ${self.portfolio['cash']:.2f}"
                )

    def manual_sell(self):
        """Execute manual sell order."""
        if self.stock_data:
            quantity = self.quantity_input.value()
            current_price = self.stock_data["current_price"]

            if self.portfolio["shares"] >= quantity:
                self.portfolio["cash"] += current_price * quantity
                self.portfolio["shares"] -= quantity

                trade = {
                    "timestamp": datetime.now(),
                    "action": "SELL",
                    "price": current_price,
                    "quantity": quantity,
                    "strategy": "Manual",
                }
                self.portfolio["trades"].append(trade)

                self.log_trade(f"👤 MANUAL: SOLD {quantity} shares at ${current_price:.2f}")
                self.update_portfolio_display()
            else:
                self.log_trade(
                    f"❌ INSUFFICIENT SHARES: Need {quantity}, have {self.portfolio['shares']}"
                )

    def log_trade(self, message):
        """Log a trade message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.trading_log.append(log_message)

        # Keep only last 100 messages
        if self.trading_log.document().blockCount() > 100:
            cursor = self.trading_log.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.Down, cursor.KeepAnchor, 1)
            cursor.removeSelectedText()

    def update_strategy_performance(self):
        """Update strategy performance display."""
        self.performance_table.setRowCount(len(self.strategies))

        for i, (name, strategy) in enumerate(self.strategies.items()):
            self.performance_table.setItem(i, 0, QTableWidgetItem(strategy.name))
            self.performance_table.setItem(
                i, 1, QTableWidgetItem(str(strategy.performance["total_trades"]))
            )
            self.performance_table.setItem(
                i, 2, QTableWidgetItem(f"{strategy.performance['win_rate']:.1f}%")
            )
            self.performance_table.setItem(
                i, 3, QTableWidgetItem(f"${strategy.performance['total_profit']:.2f}")
            )
            self.performance_table.setItem(
                i, 4, QTableWidgetItem("🟢 Active" if strategy.enabled else "🔴 Inactive")
            )

    def run_backtest(self):
        """Run backtest simulation."""
        self.backtest_results.setText(
            "🚀 Running backtest...\n\nThis feature will be implemented in the next version.\n\nBacktesting will include:\n- Historical data analysis\n- Strategy performance metrics\n- Risk-adjusted returns\n- Drawdown analysis\n- Sharpe ratio calculation"
        )

    def refresh_data(self):
        """Refresh stock data."""
        self.status_label.setText("Refreshing...")
        if hasattr(self, "data_worker"):
            self.data_worker.stop()
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()

    def closeEvent(self, event):
        """Handle application close."""
        if hasattr(self, "data_worker"):
            self.data_worker.stop()
        event.accept()


# Import the StockDataWorker from the original app
from tesla_stock_app import StockDataWorker


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Tesla Trading Robot")
    app.setApplicationVersion("1.0.0")

    # Create and show main window
    window = TradingRobot()
    window.show()

    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
