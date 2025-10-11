"""
Trading Dashboard Routes - V2 Compliant
========================================

FastAPI route definitions for trading dashboard.
Extracted from dashboard.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

import asyncio

from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from loguru import logger


def setup_dashboard_routes(dashboard):
    """Setup all dashboard routes."""

    @dashboard.app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Main dashboard page."""
        return dashboard.templates.TemplateResponse("dashboard.html", {"request": request})

    @dashboard.app.get("/api/status")
    async def get_status():
        """Get current trading status."""
        return await dashboard.get_status()

    @dashboard.app.get("/api/portfolio")
    async def get_portfolio():
        """Get portfolio information."""
        try:
            positions = await dashboard.trading_engine.get_positions()
            account_info = await dashboard.trading_engine.get_account_info()

            return {
                "positions": positions,
                "account": account_info,
                "total_positions": len(positions),
            }
        except Exception as e:
            logger.error(f"Error getting portfolio: {e}")
            return {"error": str(e)}

    @dashboard.app.get("/api/market_data/{symbol}")
    async def get_market_data(symbol: str, timeframe: str = "1Min", limit: int = 100):
        """Get market data for a symbol."""
        try:
            data = await dashboard.trading_engine.get_market_data(symbol, timeframe, limit)
            return {"symbol": symbol, "timeframe": timeframe, "data": data}
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return {"error": str(e)}

    @dashboard.app.post("/api/trade/{symbol}/{side}")
    async def execute_trade(symbol: str, side: str, quantity: int = 1):
        """Execute a trade."""
        try:
            order = await dashboard.trading_engine.place_order(symbol, quantity, side)
            return {"status": "success", "order": order}
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return {"status": "error", "message": str(e)}

    @dashboard.app.get("/api/stop_trading")
    async def stop_trading():
        """Emergency stop trading."""
        try:
            await dashboard.trading_engine.stop()
            return {"status": "success", "message": "Trading stopped"}
        except Exception as e:
            logger.error(f"Error stopping trading: {e}")
            return {"status": "error", "message": str(e)}

    @dashboard.app.websocket("/ws/updates")
    async def websocket_updates(websocket: WebSocket):
        """WebSocket endpoint for real-time updates."""
        await websocket.accept()
        dashboard.connected_clients.append(websocket)

        try:
            while True:
                await asyncio.sleep(5)
                try:
                    status = await dashboard.get_status()
                    await websocket.send_json(status)
                except Exception as e:
                    logger.error(f"Error sending update: {e}")

        except WebSocketDisconnect:
            if websocket in dashboard.connected_clients:
                dashboard.connected_clients.remove(websocket)
