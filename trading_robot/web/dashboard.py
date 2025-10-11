"""
Trading Robot Web Dashboard - V2 Compliant
===========================================

Web dashboard for trading robot monitoring.
Refactored for V2 compliance by Agent-3.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 refactor)
"""

import asyncio
from datetime import datetime
from typing import Any

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.templating import Jinja2Templates
from loguru import logger

from config.settings import config

from .dashboard_routes import setup_dashboard_routes


class TradingDashboard:
    """Web dashboard for trading robot monitoring."""

    def __init__(self, trading_engine):
        """Initialize dashboard."""
        self.trading_engine = trading_engine
        self.app = FastAPI(title="Trading Robot Dashboard")
        self.templates = Jinja2Templates(directory="web/templates")
        self.connected_clients: list[WebSocket] = []
        self.is_running = False

        # Setup routes using extracted module
        setup_dashboard_routes(self)

    async def start(self):
        """Start the dashboard server."""
        try:
            self.is_running = True
            logger.info(f"🌐 Starting dashboard on http://localhost:{config.web_port}")

            config_obj = uvicorn.Config(
                self.app, host=config.web_host, port=config.web_port, log_level="info"
            )
            server = uvicorn.Server(config_obj)
            asyncio.create_task(server.serve())

        except Exception as e:
            logger.error(f"❌ Failed to start dashboard: {e}")
            raise

    async def stop(self):
        """Stop the dashboard server."""
        try:
            self.is_running = False

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
        """Broadcast update to all connected clients."""
        disconnected_clients = []

        for client in self.connected_clients:
            try:
                await client.send_json(data)
            except Exception:
                disconnected_clients.append(client)

        for client in disconnected_clients:
            if client in self.connected_clients:
                self.connected_clients.remove(client)

    async def get_status(self) -> dict[str, Any]:
        """Get current trading status."""
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
