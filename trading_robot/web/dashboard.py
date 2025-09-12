"""
Trading Robot Web Dashboard
"""

import asyncio
from datetime import datetime
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from config.settings import config


class TradingDashboard:
    """Web dashboard for trading robot monitoring"""

    def __init__(self, trading_engine):
        self.trading_engine = trading_engine
        self.app = FastAPI(title="Trading Robot Dashboard")
        self.templates = Jinja2Templates(directory="web/templates")
        self.connected_clients: list[WebSocket] = []
        self.is_running = False

        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard page"""
            return self.templates.TemplateResponse("dashboard.html", {"request": request})

        @self.app.get("/api/status")
        async def get_status():
            """Get current trading status"""
            try:
                account_info = await self.trading_engine.get_account_info()
                positions = await self.trading_engine.get_positions()
                portfolio_value = await self.trading_engine.get_portfolio_value()

                return {
                    "timestamp": datetime.now().isoformat(),
                    "market_open": self.trading_engine.is_market_open(),
                    "portfolio_value": portfolio_value,
                    "cash_balance": account_info.get("cash", 0),
                    "positions": positions,
                    "total_positions": len(positions),
                }
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                return {"error": str(e)}

        @self.app.get("/api/portfolio")
        async def get_portfolio():
            """Get portfolio information"""
            try:
                positions = await self.trading_engine.get_positions()
                account_info = await self.trading_engine.get_account_info()

                return {
                    "positions": positions,
                    "account": account_info,
                    "total_positions": len(positions),
                }
            except Exception as e:
                logger.error(f"Error getting portfolio: {e}")
                return {"error": str(e)}

        @self.app.get("/api/market_data/{symbol}")
        async def get_market_data(symbol: str, timeframe: str = "1Min", limit: int = 100):
            """Get market data for a symbol"""
            try:
                data = await self.trading_engine.get_market_data(symbol, timeframe, limit)
                return {"symbol": symbol, "timeframe": timeframe, "data": data}
            except Exception as e:
                logger.error(f"Error getting market data: {e}")
                return {"error": str(e)}

        @self.app.post("/api/trade/{symbol}/{side}")
        async def execute_trade(symbol: str, side: str, quantity: int = 1):
            """Execute a trade"""
            try:
                # Validate trade
                # In production, add proper validation
                order = await self.trading_engine.place_order(symbol, quantity, side)
                return {"status": "success", "order": order}
            except Exception as e:
                logger.error(f"Error executing trade: {e}")
                return {"status": "error", "message": str(e)}

        @self.app.websocket("/ws/updates")
        async def websocket_updates(websocket: WebSocket):
            """WebSocket endpoint for real-time updates"""
            await websocket.accept()
            self.connected_clients.append(websocket)

            try:
                while True:
                    # Send periodic updates
                    await asyncio.sleep(5)  # Update every 5 seconds

                    try:
                        status = await self.get_status()
                        await websocket.send_json(status)
                    except Exception as e:
                        logger.error(f"Error sending websocket update: {e}")

            except WebSocketDisconnect:
                if websocket in self.connected_clients:
                    self.connected_clients.remove(websocket)

        @self.app.get("/api/stop_trading")
        async def stop_trading():
            """Emergency stop trading"""
            try:
                await self.trading_engine.stop()
                return {"status": "success", "message": "Trading stopped"}
            except Exception as e:
                logger.error(f"Error stopping trading: {e}")
                return {"status": "error", "message": str(e)}

    async def start(self):
        """Start the dashboard server"""
        try:
            self.is_running = True
            logger.info(f"🌐 Starting dashboard on http://localhost:{config.web_port}")

            # Start server in background
            config_obj = uvicorn.Config(
                self.app, host=config.web_host, port=config.web_port, log_level="info"
            )
            server = uvicorn.Server(config_obj)

            # Run server in background task
            asyncio.create_task(server.serve())

        except Exception as e:
            logger.error(f"❌ Failed to start dashboard: {e}")
            raise

    async def stop(self):
        """Stop the dashboard server"""
        try:
            self.is_running = False

            # Close all WebSocket connections
            for client in self.connected_clients:
                try:
                    await client.close()
                except Exception:
                    pass

            self.connected_clients.clear()
            logger.info("🌐 Dashboard stopped")

        except Exception as e:
            logger.error(f"❌ Error stopping dashboard: {e}")

    async def broadcast_update(self, data: dict[str, Any]):
        """Broadcast update to all connected clients"""
        disconnected_clients = []

        for client in self.connected_clients:
            try:
                await client.send_json(data)
            except Exception:
                disconnected_clients.append(client)

        # Remove disconnected clients
        for client in disconnected_clients:
            if client in self.connected_clients:
                self.connected_clients.remove(client)

    async def get_status(self) -> dict[str, Any]:
        """Get current trading status"""
        try:
            account_info = await self.trading_engine.get_account_info()
            positions = await self.trading_engine.get_positions()
            portfolio_value = await self.trading_engine.get_portfolio_value()

            return {
                "timestamp": datetime.now().isoformat(),
                "market_open": self.trading_engine.is_market_open(),
                "portfolio_value": portfolio_value,
                "cash_balance": account_info.get("cash", 0),
                "positions": positions,
                "total_positions": len(positions),
            }
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {"error": str(e)}


# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Robot Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-value { font-size: 2em; font-weight: bold; color: #2c3e50; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
        .positions-table { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
        .status-open { background-color: #27ae60; }
        .status-closed { background-color: #e74c3c; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #2980b9; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Alpaca Trading Robot Dashboard</h1>
            <div>
                <span class="status-indicator" id="marketStatus"></span>
                <span id="marketStatusText">Loading...</span>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="portfolioValue">$0.00</div>
                <div class="stat-label">Portfolio Value</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="cashBalance">$0.00</div>
                <div class="stat-label">Cash Balance</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalPositions">0</div>
                <div class="stat-label">Total Positions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="lastUpdate">--:--:--</div>
                <div class="stat-label">Last Update</div>
            </div>
        </div>

        <div class="positions-table">
            <h2>📊 Current Positions</h2>
            <table id="positionsTable">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Quantity</th>
                        <th>Avg Price</th>
                        <th>Current Price</th>
                        <th>Market Value</th>
                        <th>Unrealized P&L</th>
                        <th>P&L %</th>
                    </tr>
                </thead>
                <tbody id="positionsBody">
                    <tr>
                        <td colspan="7">Loading positions...</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="stat-card" style="margin-top: 20px;">
            <h3>🎛️ Controls</h3>
            <button class="btn" onclick="refreshData()">🔄 Refresh</button>
            <button class="btn btn-danger" onclick="stopTrading()">🛑 Stop Trading</button>
        </div>
    </div>

    <script>
        let websocket;
        let reconnectInterval;

        function connectWebSocket() {
            websocket = new WebSocket('ws://localhost:8000/ws/updates');

            websocket.onopen = function(event) {
                console.log('WebSocket connected');
                clearInterval(reconnectInterval);
            };

            websocket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };

            websocket.onclose = function(event) {
                console.log('WebSocket disconnected');
                reconnectInterval = setInterval(connectWebSocket, 5000);
            };

            websocket.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        }

        function updateDashboard(data) {
            if (data.error) {
                console.error('Dashboard update error:', data.error);
                return;
            }

            // Update status
            document.getElementById('marketStatus').className = data.market_open ?
                'status-indicator status-open' : 'status-indicator status-closed';
            document.getElementById('marketStatusText').textContent =
                data.market_open ? 'Market Open' : 'Market Closed';

            // Update stats
            document.getElementById('portfolioValue').textContent =
                new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
                    .format(data.portfolio_value);
            document.getElementById('cashBalance').textContent =
                new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
                    .format(data.cash_balance);
            document.getElementById('totalPositions').textContent = data.total_positions;
            document.getElementById('lastUpdate').textContent =
                new Date(data.timestamp).toLocaleTimeString();

            // Update positions table
            const tbody = document.getElementById('positionsBody');
            tbody.innerHTML = '';

            if (data.positions && data.positions.length > 0) {
                data.positions.forEach(position => {
                    const row = tbody.insertRow();
                    row.insertCell(0).textContent = position.symbol;
                    row.insertCell(1).textContent = position.qty;
                    row.insertCell(2).textContent = parseFloat(position.avg_entry_price).toFixed(2);
                    row.insertCell(3).textContent = parseFloat(position.current_price).toFixed(2);
                    row.insertCell(4).textContent = parseFloat(position.market_value).toFixed(2);
                    row.insertCell(5).textContent = parseFloat(position.unrealized_pl).toFixed(2);
                    row.insertCell(6).textContent = parseFloat(position.unrealized_plpc).toFixed(2) + '%';
                });
            } else {
                const row = tbody.insertRow();
                row.insertCell(0).textContent = 'No positions';
                row.insertCell(0).colSpan = 7;
            }
        }

        async function refreshData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error refreshing data:', error);
            }
        }

        async function stopTrading() {
            if (confirm('Are you sure you want to stop all trading?')) {
                try {
                    const response = await fetch('/api/stop_trading', { method: 'GET' });
                    const result = await response.json();
                    alert(result.message);
                } catch (error) {
                    console.error('Error stopping trading:', error);
                    alert('Error stopping trading');
                }
            }
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            connectWebSocket();
            refreshData();
        });
    </script>
</body>
</html>
"""


# Create templates directory and dashboard template
def create_templates():
    """Create template files"""
    import os

    # Create templates directory
    os.makedirs("trading_robot/web/templates", exist_ok=True)

    # Create dashboard template
    with open("trading_robot/web/templates/dashboard.html", "w") as f:
        f.write(DASHBOARD_HTML)

    logger.info("📄 Dashboard templates created")


# Create templates when module is imported
create_templates()
