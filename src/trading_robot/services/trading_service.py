"""
Trading Service - V2 Compliant Service Layer Implementation
Business logic layer for trading operations with dependency injection
REFACTORED: Clean architecture with separation of concerns
V2 COMPLIANCE: Under 300-line limit, comprehensive error handling, modular design

@author Agent-7 - Web Development Specialist (adapted for Trading Robot)
@version 1.0.0 - V2 COMPLIANCE SERVICE LAYER
@license MIT
"""

import uuid
from datetime import datetime
from typing import Any

from ...core.unified_logging_system import UnifiedLoggingSystem
from ...core.unified_utilities import get_unified_validator
from ..repositories.trading_repository import (
    Position,
    Trade,
    TradingRepositoryInterface,
    create_trading_repository,
)


class TradingService:
    """Service layer for trading business logic."""

    def __init__(self, repository: TradingRepositoryInterface | None = None):
        """Initialize with dependency injection."""
        self.repository = repository or create_trading_repository()
        self.logger = UnifiedLoggingSystem("TradingService")

    async def execute_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        order_type: str = "market",
    ) -> str | None:
        """Execute a trade and return trade ID."""
        try:
            self.logger.get_unified_logger().log_operation_start(
                "execute_trade",
                {"symbol": symbol, "side": side, "quantity": quantity, "price": price},
            )

            # Validate inputs
            if not self._validate_trade_inputs(symbol, side, quantity, price):
                self.logger.get_unified_logger().log_operation_complete(
                    "execute_trade", {"success": False, "reason": "validation_failed"}
                )
                return None

            # Create trade object
            trade_id = str(uuid.uuid4())
            trade = Trade(
                id=trade_id,
                symbol=symbol.upper(),
                side=side.lower(),
                quantity=quantity,
                price=price,
                timestamp=datetime.now(),
                status="executed",
                order_type=order_type,
            )

            # Save trade
            success = await self.repository.save_trade(trade)
            if success:
                # Update position
                await self._update_position_from_trade(trade)
                self.logger.get_unified_logger().log_operation_complete(
                    "execute_trade", {"success": True, "trade_id": trade_id}
                )
                return trade_id
            else:
                self.logger.get_unified_logger().log_operation_complete(
                    "execute_trade", {"success": False, "reason": "save_failed"}
                )
                return None

        except Exception as e:
            self.logger.log_error(
                "execute_trade",
                str(e),
                {"symbol": symbol, "side": side, "quantity": quantity},
            )
            return None

    async def get_trade_history(self, symbol: str | None = None, limit: int = 100) -> list[Trade]:
        """Get trade history, optionally filtered by symbol."""
        try:
            self.logger.get_unified_logger().log_operation_start(
                "get_trade_history", {"symbol": symbol, "limit": limit}
            )

            if symbol:
                trades = await self.repository.get_trades_by_symbol(symbol, limit)
            else:
                trades = await self.repository.get_all_trades(limit)

            self.logger.get_unified_logger().log_operation_complete(
                "get_trade_history", {"count": len(trades), "symbol": symbol}
            )
            return trades

        except Exception as e:
            self.logger.log_error("get_trade_history", str(e), {"symbol": symbol})
            return []

    async def get_positions(self) -> list[Position]:
        """Get all current positions."""
        try:
            self.logger.get_unified_logger().log_operation_start("get_positions")
            positions = await self.repository.get_all_positions()
            self.logger.get_unified_logger().log_operation_complete(
                "get_positions", {"count": len(positions)}
            )
            return positions
        except Exception as e:
            self.logger.log_error("get_positions", str(e))
            return []

    async def get_position(self, symbol: str) -> Position | None:
        """Get position for specific symbol."""
        try:
            self.logger.get_unified_logger().log_operation_start("get_position", {"symbol": symbol})
            position = await self.repository.get_position(symbol.upper())
            self.logger.get_unified_logger().log_operation_complete(
                "get_position", {"symbol": symbol, "found": position is not None}
            )
            return position
        except Exception as e:
            self.logger.log_error("get_position", str(e), {"symbol": symbol})
            return None

    async def calculate_portfolio_pnl(self) -> dict[str, Any]:
        """Calculate portfolio P&L."""
        try:
            self.logger.get_unified_logger().log_operation_start("calculate_portfolio_pnl")

            positions = await self.get_positions()
            total_pnl = sum(pos.pnl for pos in positions)
            total_value = sum(pos.quantity * pos.current_price for pos in positions)

            result = {
                "total_pnl": total_pnl,
                "total_value": total_value,
                "positions_count": len(positions),
                "timestamp": datetime.now(),
            }

            self.logger.get_unified_logger().log_operation_complete(
                "calculate_portfolio_pnl",
                {"total_pnl": total_pnl, "positions_count": len(positions)},
            )
            return result

        except Exception as e:
            self.logger.log_error("calculate_portfolio_pnl", str(e))
            return {"error": str(e), "timestamp": datetime.now()}

    async def cancel_trade(self, trade_id: str) -> bool:
        """Cancel a pending trade."""
        try:
            self.logger.get_unified_logger().log_operation_start(
                "cancel_trade", {"trade_id": trade_id}
            )

            # Get current trade
            trade = await self.repository.get_trade(trade_id)
            if not get_unified_validator().validate_required(trade):
                self.logger.get_unified_logger().log_operation_complete(
                    "cancel_trade", {"success": False, "reason": "trade_not_found"}
                )
                return False

            if trade.status != "pending":
                self.logger.get_unified_logger().log_operation_complete(
                    "cancel_trade", {"success": False, "reason": "trade_not_pending"}
                )
                return False

            # Update status
            success = await self.repository.update_trade_status(trade_id, "cancelled")
            self.logger.get_unified_logger().log_operation_complete(
                "cancel_trade", {"success": success}
            )
            return success

        except Exception as e:
            self.logger.log_error("cancel_trade", str(e), {"trade_id": trade_id})
            return False

    def _validate_trade_inputs(self, symbol: str, side: str, quantity: float, price: float) -> bool:
        """Validate trade input parameters."""
        if not symbol or not get_unified_validator().validate_type(symbol, str):
            return False
        if side not in ["buy", "sell"]:
            return False
        if not get_unified_validator().validate_type(quantity, (int, float)) or quantity <= 0:
            return False
        if not get_unified_validator().validate_type(price, (int, float)) or price <= 0:
            return False
        return True

    async def _update_position_from_trade(self, trade: Trade) -> None:
        """Update position based on executed trade."""
        try:
            symbol = trade.symbol
            current_position = await self.repository.get_position(symbol)

            if trade.side == "buy":
                if current_position:
                    # Update existing position
                    total_quantity = current_position.quantity + trade.quantity
                    total_cost = (current_position.quantity * current_position.average_price) + (
                        trade.quantity * trade.price
                    )
                    new_avg_price = total_cost / total_quantity

                    updated_position = Position(
                        symbol=symbol,
                        quantity=total_quantity,
                        average_price=new_avg_price,
                        current_price=trade.price,
                        pnl=(trade.price - new_avg_price) * total_quantity,
                        timestamp=datetime.now(),
                    )
                else:
                    # Create new position
                    updated_position = Position(
                        symbol=symbol,
                        quantity=trade.quantity,
                        average_price=trade.price,
                        current_price=trade.price,
                        pnl=0.0,
                        timestamp=datetime.now(),
                    )
            else:  # sell
                if current_position:
                    # Reduce position
                    new_quantity = current_position.quantity - trade.quantity
                    if new_quantity > 0:
                        # Partial sell
                        pnl = (trade.price - current_position.average_price) * trade.quantity
                        updated_position = Position(
                            symbol=symbol,
                            quantity=new_quantity,
                            average_price=current_position.average_price,
                            current_price=trade.price,
                            pnl=current_position.pnl + pnl,
                            timestamp=datetime.now(),
                        )
                    else:
                        # Complete sell
                        pnl = (
                            trade.price - current_position.average_price
                        ) * current_position.quantity
                        # Position will be deleted
                        await self.repository.delete_position(symbol)
                        return
                else:
                    # Short selling (not implemented in this basic version)
                    return

            await self.repository.save_position(updated_position)

        except Exception as e:
            self.logger.log_error(
                "_update_position_from_trade",
                str(e),
                {"symbol": trade.symbol, "side": trade.side},
            )


# Factory function for dependency injection
def create_trading_service(
    repository: TradingRepositoryInterface | None = None,
) -> TradingService:
    """Factory function to create trading service with optional repository injection."""
    return TradingService(repository)


# Export for DI
__all__ = ["TradingService", "create_trading_service"]
