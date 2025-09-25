#!/usr/bin/env python3
"""
V2 Trading Robot Demo
====================

Demonstration of V2-compliant trading robot frontend
Shows all modular components working together
V2 Compliant: ≤200 lines, focused demo application
"""

import sys
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont

# Import V2 compliant components
try:
    from modules.v2_trading_interface import V2TradingInterface
    from modules.ui.trading_dashboard import TradingDashboard
    from modules.ui.chart_widget import ChartWidget
    from modules.ui.mobile_responsive import MobileTradingCard
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all V2 UI components are properly installed.")
    sys.exit(1)


class MockDataProvider(QThread):
    """Mock data provider for demo purposes"""
    
    data_updated = pyqtSignal(dict)
    chart_data_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.base_price = 200.0
        
    def run(self):
        """Generate mock trading data"""
        while self.running:
            # Generate mock price data
            price_change = random.uniform(-2, 2)
            self.base_price += price_change
            
            # Ensure price stays reasonable
            self.base_price = max(150, min(300, self.base_price))
            
            # Create trading data
            trading_data = {
                'price': round(self.base_price, 2),
                'change': round(price_change, 2),
                'change_percent': round((price_change / (self.base_price - price_change)) * 100, 2),
                'volume': random.randint(1000000, 5000000),
                'market_cap': round(self.base_price * 3.2, 2),  # Approximate Tesla market cap
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'source': 'Mock Data Provider'
            }
            
            # Emit data update
            self.data_updated.emit(trading_data)
            
            # Generate chart data
            chart_data = self.generate_chart_data()
            self.chart_data_updated.emit(chart_data)
            
            # Wait before next update
            self.msleep(2000)  # 2 second updates
    
    def generate_chart_data(self):
        """Generate mock chart data"""
        chart_data = []
        current_price = self.base_price
        
        for i in range(20):  # 20 data points
            price_change = random.uniform(-1, 1)
            current_price += price_change
            
            chart_data.append({
                'price': round(current_price, 2),
                'open': round(current_price - price_change, 2),
                'high': round(current_price + abs(price_change), 2),
                'low': round(current_price - abs(price_change), 2),
                'volume': random.randint(500000, 2000000),
                'timestamp': (datetime.now() - timedelta(minutes=20-i)).strftime("%H:%M")
            })
        
        return chart_data
    
    def stop(self):
        """Stop data generation"""
        self.running = False


class V2TradingRobotDemo:
    """V2 Trading Robot Demo Application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.interface = V2TradingInterface()
        self.data_provider = MockDataProvider()
        self.setup_connections()
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect data provider signals
        self.data_provider.data_updated.connect(self.interface.update_trading_data)
        self.data_provider.chart_data_updated.connect(self.interface.update_chart_data)
        
        # Connect trading action signals
        self.interface.trading_action.connect(self.handle_trading_action)
        
    def handle_trading_action(self, action: str, data: dict):
        """Handle trading actions"""
        price = data.get('price', 0)
        
        if action == "buy":
            self.show_message(f"🟢 BUY Order: Tesla at ${price:.2f}")
        elif action == "sell":
            self.show_message(f"🔴 SELL Order: Tesla at ${price:.2f}")
        elif action == "hold":
            self.show_message(f"⏸️ HOLD Position: Tesla at ${price:.2f}")
    
    def show_message(self, message: str):
        """Show trading action message"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Trading Action")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
    
    def run(self):
        """Run the demo application"""
        print("🚀 Starting V2 Trading Robot Demo...")
        print("📊 Features:")
        print("  • V2-compliant modular UI components (≤200 lines each)")
        print("  • Professional dark theme trading interface")
        print("  • Real-time chart visualization")
        print("  • Mobile-responsive design")
        print("  • Mock data provider for demonstration")
        
        # Start data provider
        self.data_provider.start()
        
        # Show interface
        self.interface.show()
        
        # Run application
        try:
            return self.app.exec_()
        finally:
            # Cleanup
            self.data_provider.stop()
            self.data_provider.wait()


def main():
    """Main demo function"""
    demo = V2TradingRobotDemo()
    return demo.run()


if __name__ == "__main__":
    sys.exit(main())
