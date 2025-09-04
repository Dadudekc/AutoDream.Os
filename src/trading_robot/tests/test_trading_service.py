"""
Trading Service Unit Tests - V2 Compliant Test Suite
Comprehensive test coverage for trading business logic operations
REFACTORED: Complete test suite with dependency injection mocking
V2 COMPLIANCE: >85% coverage, clear test names, comprehensive assertions

@author Agent-7 - Web Development Specialist (adapted for Trading Robot)
@version 1.0.0 - V2 COMPLIANCE UNIT TESTS
@license MIT
"""




@pytest.fixture
def mock_repository():
    """Mock repository fixture"""
    repo = AsyncMock()
    return repo


@pytest.fixture
def mock_logger():
    """Mock logger fixture"""
    return MagicMock(spec=UnifiedLoggingSystem)


@pytest.fixture
def trading_service(mock_repository, mock_logger):
    """Trading service fixture"""
    service = TradingService(mock_repository)
    service.logger = mock_logger
    return service


class TestTradingService:
    """Test suite for TradingService"""

    def test_initialization(self, trading_service, mock_repository):
        """Test service initialization"""
        assert trading_service.repository == mock_repository
        assert get_unified_validator().validate_hasattr(trading_service, 'logger')

    @pytest.mark.asyncio
    async def test_execute_trade_success(self, trading_service, mock_repository, mock_logger):
        """Test successful trade execution"""
        # Mock repository save_trade
        mock_repository.save_trade.return_value = True
        mock_repository.get_position.return_value = None
        mock_repository.save_position.return_value = True

        # Mock logger calls
        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        trade_id = await trading_service.execute_trade(
            "AAPL", "buy", 100.0, 150.0, "market"
        )

        assert trade_id is not None
        assert get_unified_validator().validate_type(trade_id, str)

        # Verify repository calls
        mock_repository.save_trade.assert_called_once()
        saved_trade = mock_repository.save_trade.call_args[0][0]
        assert saved_trade.symbol == "AAPL"
        assert saved_trade.side == "buy"
        assert saved_trade.quantity == 100.0
        assert saved_trade.price == 150.0

        # Verify position creation
        mock_repository.save_position.assert_called_once()

        # Verify logging
        mock_logger.get_unified_logger().log_operation_start(operation)_start.assert_called_with(
            "execute_trade", {
                "symbol": "AAPL", "side": "buy", "quantity": 100.0, "price": 150.0
            }
        )
        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called()

    @pytest.mark.asyncio
    async def test_execute_trade_validation_failure(self, trading_service, mock_logger):
        """Test trade execution with validation failure"""
        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        # Test invalid side
        result = await trading_service.execute_trade("AAPL", "invalid", 100, 150)
        assert result is None

        # Test negative quantity
        result = await trading_service.execute_trade("AAPL", "buy", -100, 150)
        assert result is None

        # Test zero price
        result = await trading_service.execute_trade("AAPL", "buy", 100, 0)
        assert result is None

        # Verify error logging
        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "execute_trade", {"success": False, "reason": "validation_failed"}
        )

    @pytest.mark.asyncio
    async def test_execute_trade_repository_failure(self, trading_service, mock_repository, mock_logger):
        """Test trade execution with repository failure"""
        mock_repository.save_trade.return_value = False
        mock_logger.log_error = MagicMock()

        result = await trading_service.execute_trade("AAPL", "buy", 100, 150)

        assert result is None
        mock_logger.log_error.assert_called()

    @pytest.mark.asyncio
    async def test_get_trade_history_all(self, trading_service, mock_repository, mock_logger):
        """Test getting all trade history"""
        mock_trades = [
            Trade("t1", "AAPL", "buy", 100, 150, datetime.now(), "executed", "market"),
            Trade("t2", "GOOGL", "sell", 50, 2800, datetime.now(), "executed", "market")
        ]
        mock_repository.get_all_trades.return_value = mock_trades

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.get_trade_history()

        assert result == mock_trades
        mock_repository.get_all_trades.assert_called_once_with(100)

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "get_trade_history", {"count": 2, "symbol": None}
        )

    @pytest.mark.asyncio
    async def test_get_trade_history_by_symbol(self, trading_service, mock_repository, mock_logger):
        """Test getting trade history for specific symbol"""
        mock_trades = [
            Trade("t1", "AAPL", "buy", 100, 150, datetime.now(), "executed", "market"),
            Trade("t2", "AAPL", "sell", 50, 160, datetime.now(), "executed", "market")
        ]
        mock_repository.get_trades_by_symbol.return_value = mock_trades

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.get_trade_history("AAPL", 50)

        assert result == mock_trades
        mock_repository.get_trades_by_symbol.assert_called_once_with("AAPL", 50)

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "get_trade_history", {"count": 2, "symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_get_positions(self, trading_service, mock_repository, mock_logger):
        """Test getting all positions"""
        mock_positions = [
            Position("AAPL", 100, 150, 155, 500, datetime.now()),
            Position("GOOGL", 10, 2800, 2850, 500, datetime.now())
        ]
        mock_repository.get_all_positions.return_value = mock_positions

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.get_positions()

        assert result == mock_positions
        mock_repository.get_all_positions.assert_called_once()

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "get_positions", {"count": 2}
        )

    @pytest.mark.asyncio
    async def test_get_position(self, trading_service, mock_repository, mock_logger):
        """Test getting position for specific symbol"""
        mock_position = Position("AAPL", 100, 150, 155, 500, datetime.now())
        mock_repository.get_position.return_value = mock_position

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.get_position("AAPL")

        assert result == mock_position
        mock_repository.get_position.assert_called_once_with("AAPL")

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "get_position", {"symbol": "AAPL", "found": True}
        )

    @pytest.mark.asyncio
    async def test_calculate_portfolio_pnl(self, trading_service, mock_repository, mock_logger):
        """Test portfolio P&L calculation"""
        mock_positions = [
            Position("AAPL", 100, 150, 160, 1000, datetime.now()),  # +$1000 P&L
            Position("GOOGL", 10, 2800, 2700, -1000, datetime.now())  # -$1000 P&L
        ]
        mock_repository.get_all_positions.return_value = mock_positions

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.calculate_portfolio_pnl()

        assert result["total_pnl"] == 0  # 1000 + (-1000)
        assert result["total_value"] == 100 * 160 + 10 * 2700  # 16000 + 27000 = 43000
        assert result["positions_count"] == 2
        assert "timestamp" in result

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called()

    @pytest.mark.asyncio
    async def test_cancel_trade_success(self, trading_service, mock_repository, mock_logger):
        """Test successful trade cancellation"""
        mock_trade = Trade("t1", "AAPL", "buy", 100, 150,
                          datetime.now(), "pending", "limit")
        mock_repository.get_trade.return_value = mock_trade
        mock_repository.update_trade_status.return_value = True

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.cancel_trade("t1")

        assert result is True
        mock_repository.update_trade_status.assert_called_once_with("t1", "cancelled")

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "cancel_trade", {"success": True}
        )

    @pytest.mark.asyncio
    async def test_cancel_trade_not_found(self, trading_service, mock_repository, mock_logger):
        """Test canceling non-existent trade"""
        mock_repository.get_trade.return_value = None

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.cancel_trade("non_existent")

        assert result is False

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "cancel_trade", {"success": False, "reason": "trade_not_found"}
        )

    @pytest.mark.asyncio
    async def test_cancel_executed_trade(self, trading_service, mock_repository, mock_logger):
        """Test canceling already executed trade"""
        mock_trade = Trade("t1", "AAPL", "buy", 100, 150,
                          datetime.now(), "executed", "market")
        mock_repository.get_trade.return_value = mock_trade

        mock_logger.get_unified_logger().log_operation_start(operation)_start = MagicMock()
        mock_logger.get_unified_logger().log_operation_start(operation)_complete = MagicMock()

        result = await trading_service.cancel_trade("t1")

        assert result is False

        mock_logger.get_unified_logger().log_operation_start(operation)_complete.assert_called_with(
            "cancel_trade", {"success": False, "reason": "trade_not_pending"}
        )

    @pytest.mark.asyncio
    async def test_position_update_buy_new_position(self, trading_service, mock_repository):
        """Test position update when buying with no existing position"""
        mock_repository.get_position.return_value = None
        mock_repository.save_position.return_value = True
        mock_repository.save_trade.return_value = True

        await trading_service.execute_trade("AAPL", "buy", 100, 150)

        # Verify position creation
        mock_repository.save_position.assert_called_once()
        saved_position = mock_repository.save_position.call_args[0][0]

        assert saved_position.symbol == "AAPL"
        assert saved_position.quantity == 100
        assert saved_position.average_price == 150
        assert saved_position.current_price == 150
        assert saved_position.pnl == 0

    @pytest.mark.asyncio
    async def test_position_update_buy_existing_position(self, trading_service, mock_repository):
        """Test position update when buying with existing position"""
        existing_position = Position("AAPL", 100, 150, 155, 500, datetime.now())
        mock_repository.get_position.return_value = existing_position
        mock_repository.save_position.return_value = True
        mock_repository.save_trade.return_value = True

        await trading_service.execute_trade("AAPL", "buy", 50, 160)

        # Verify position update
        mock_repository.save_position.assert_called_once()
        saved_position = mock_repository.save_position.call_args[0][0]

        # New quantity: 100 + 50 = 150
        # New average price: ((100 * 150) + (50 * 160)) / 150 = 153.33...
        assert saved_position.symbol == "AAPL"
        assert saved_position.quantity == 150
        assert saved_position.current_price == 160
        assert saved_position.pnl > 0  # Should have positive P&L

    @pytest.mark.asyncio
    async def test_position_update_sell_partial(self, trading_service, mock_repository):
        """Test position update when selling partial position"""
        existing_position = Position("AAPL", 100, 150, 160, 1000, datetime.now())
        mock_repository.get_position.return_value = existing_position
        mock_repository.save_position.return_value = True
        mock_repository.save_trade.return_value = True

        await trading_service.execute_trade("AAPL", "sell", 30, 165)

        # Verify partial position update
        mock_repository.save_position.assert_called_once()
        saved_position = mock_repository.save_position.call_args[0][0]

        assert saved_position.symbol == "AAPL"
        assert saved_position.quantity == 70  # 100 - 30
        assert saved_position.current_price == 165
        # P&L should be updated with realized profit from sale

    @pytest.mark.asyncio
    async def test_position_update_sell_complete(self, trading_service, mock_repository):
        """Test position update when selling complete position"""
        existing_position = Position("AAPL", 50, 150, 160, 500, datetime.now())
        mock_repository.get_position.return_value = existing_position
        mock_repository.save_trade.return_value = True
        mock_repository.delete_position.return_value = True

        await trading_service.execute_trade("AAPL", "sell", 50, 165)

        # Verify position deletion (complete sell)
        mock_repository.delete_position.assert_called_once_with("AAPL")
        # Should not save a new position
        mock_repository.save_position.assert_not_called()


class TestCreateTradingService:
    """Test suite for create_trading_service factory function"""

    def test_create_trading_service_without_repo(self):
        """Test factory function creates service with default repository"""
        service = create_trading_service()

        assert get_unified_validator().validate_type(service, TradingService)
        assert service.repository is not None

    def test_create_trading_service_with_repo(self, mock_repository):
        """Test factory function creates service with provided repository"""
        service = create_trading_service(mock_repository)

        assert get_unified_validator().validate_type(service, TradingService)
        assert service.repository == mock_repository


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

