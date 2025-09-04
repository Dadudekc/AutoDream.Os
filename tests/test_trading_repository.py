sys.path.append(get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), '..'))
"""
Trading Repository Unit Tests - V2 Compliant Test Suite
Comprehensive test coverage for trading data access operations
REFACTORED: Complete test suite with mocking and edge cases
V2 COMPLIANCE: >85% coverage, clear test names, comprehensive assertions

@author Agent-7 - Web Development Specialist (adapted for Trading Robot)
@version 1.0.0 - V2 COMPLIANCE UNIT TESTS
@license MIT
"""


    TradingRepositoryInterface,
    InMemoryTradingRepository,
    Trade,
    Position,
    create_trading_repository
)


@pytest.fixture
def mock_logger():
    """Mock logger fixture"""
    return MagicMock(spec=UnifiedLoggingSystem)


@pytest.fixture
def trading_repo(mock_logger):
    """Trading repository fixture"""
    repo = InMemoryTradingRepository()
    repo.logger = mock_logger
    return repo


@pytest.fixture
def sample_trade():
    """Sample trade fixture"""
    return Trade(
        id="trade_123",
        symbol="AAPL",
        side="buy",
        quantity=100.0,
        price=150.0,
        timestamp=datetime(2024, 1, 1, 10, 0, 0),
        status="executed",
        order_type="market"
    )


@pytest.fixture
def sample_position():
    """Sample position fixture"""
    return Position(
        symbol="AAPL",
        quantity=100.0,
        average_price=150.0,
        current_price=155.0,
        pnl=500.0,
        timestamp=datetime(2024, 1, 1, 10, 0, 0)
    )


class TestInMemoryTradingRepository:
    """Test suite for InMemoryTradingRepository"""

    def test_initialization(self, trading_repo, mock_logger):
        """Test repository initialization"""
        assert trading_repo.trades == {}
        assert trading_repo.positions == {}
        assert trading_repo.logger == mock_logger

    @pytest.mark.asyncio
    async def test_save_trade_success(self, trading_repo, sample_trade, mock_logger):
        """Test successful trade saving"""
        # Mock logger calls
        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.save_trade(sample_trade)

        assert result is True
        assert sample_trade.id in trading_repo.trades
        assert trading_repo.trades[sample_trade.id] == sample_trade

        # Verify logging calls
        mock_logger.log_operation_start.assert_called_with(
            "save_trade", {"trade_id": sample_trade.id, "symbol": sample_trade.symbol}
        )
        mock_logger.log_operation_complete.assert_called_with(
            "save_trade", {"trade_id": sample_trade.id}
        )

    @pytest.mark.asyncio
    async def test_get_trade_success(self, trading_repo, sample_trade, mock_logger):
        """Test successful trade retrieval"""
        await trading_repo.save_trade(sample_trade)

        # Mock logger calls
        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_trade(sample_trade.id)

        assert result == sample_trade

        # Verify logging calls
        mock_logger.log_operation_start.assert_called_with(
            "get_trade", {"trade_id": sample_trade.id}
        )
        mock_logger.log_operation_complete.assert_called_with(
            "get_trade", {"found": True}
        )

    @pytest.mark.asyncio
    async def test_get_trade_not_found(self, trading_repo, mock_logger):
        """Test trade retrieval for non-existent trade"""
        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_trade("non_existent")

        assert result is None

        mock_logger.log_operation_complete.assert_called_with(
            "get_trade", {"found": False}
        )

    @pytest.mark.asyncio
    async def test_get_trades_by_symbol(self, trading_repo, mock_logger):
        """Test getting trades by symbol"""
        # Create multiple trades
        trade1 = Trade("t1", "AAPL", "buy", 100, 150, datetime.now(), "executed", "market")
        trade2 = Trade("t2", "AAPL", "sell", 50, 160, datetime.now(), "executed", "market")
        trade3 = Trade("t3", "GOOGL", "buy", 10, 2800, datetime.now(), "executed", "market")

        await trading_repo.save_trade(trade1)
        await trading_repo.save_trade(trade2)
        await trading_repo.save_trade(trade3)

        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_trades_by_symbol("AAPL")

        assert len(result) == 2
        assert all(trade.symbol == "AAPL" for trade in result)
        # Should be sorted by timestamp descending
        assert result[0].timestamp >= result[1].timestamp

        mock_logger.log_operation_complete.assert_called_with(
            "get_trades_by_symbol", {"count": 2}
        )

    @pytest.mark.asyncio
    async def test_get_all_trades(self, trading_repo, mock_logger):
        """Test getting all trades"""
        # Create multiple trades
        for i in range(5):
            trade = Trade(f"t{i}", f"SYM{i}", "buy", 10, 100,
                         datetime(2024, 1, 1, 10, i), "executed", "market")
            await trading_repo.save_trade(trade)

        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_all_trades()

        assert len(result) == 5
        # Should be sorted by timestamp descending
        for i in range(len(result) - 1):
            assert result[i].timestamp >= result[i + 1].timestamp

        mock_logger.log_operation_complete.assert_called_with(
            "get_all_trades", {"count": 5}
        )

    @pytest.mark.asyncio
    async def test_update_trade_status_success(self, trading_repo, sample_trade, mock_logger):
        """Test successful trade status update"""
        await trading_repo.save_trade(sample_trade)

        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.update_trade_status(sample_trade.id, "cancelled")

        assert result is True
        assert trading_repo.trades[sample_trade.id].status == "cancelled"

        mock_logger.log_operation_complete.assert_called_with(
            "update_trade_status", {"success": True}
        )

    @pytest.mark.asyncio
    async def test_update_trade_status_not_found(self, trading_repo, mock_logger):
        """Test trade status update for non-existent trade"""
        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.update_trade_status("non_existent", "cancelled")

        assert result is False

        mock_logger.log_operation_complete.assert_called_with(
            "update_trade_status", {"success": False, "reason": "trade_not_found"}
        )

    @pytest.mark.asyncio
    async def test_save_position_success(self, trading_repo, sample_position, mock_logger):
        """Test successful position saving"""
        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.save_position(sample_position)

        assert result is True
        assert sample_position.symbol in trading_repo.positions
        assert trading_repo.positions[sample_position.symbol] == sample_position

        mock_logger.log_operation_complete.assert_called_with(
            "save_position", {"success": True}
        )

    @pytest.mark.asyncio
    async def test_get_position_success(self, trading_repo, sample_position, mock_logger):
        """Test successful position retrieval"""
        await trading_repo.save_position(sample_position)

        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_position(sample_position.symbol)

        assert result == sample_position

        mock_logger.log_operation_complete.assert_called_with(
            "get_position", {"found": True}
        )

    @pytest.mark.asyncio
    async def test_get_position_not_found(self, trading_repo, mock_logger):
        """Test position retrieval for non-existent symbol"""
        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_position("NON_EXISTENT")

        assert result is None

        mock_logger.log_operation_complete.assert_called_with(
            "get_position", {"found": False}
        )

    @pytest.mark.asyncio
    async def test_get_all_positions(self, trading_repo, mock_logger):
        """Test getting all positions"""
        # Create multiple positions
        positions = [
            Position("AAPL", 100, 150, 155, 500, datetime.now()),
            Position("GOOGL", 10, 2800, 2850, 500, datetime.now()),
        ]

        for pos in positions:
            await trading_repo.save_position(pos)

        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.get_all_positions()

        assert len(result) == 2
        assert all(get_unified_validator().validate_type(pos, Position) for pos in result)

        mock_logger.log_operation_complete.assert_called_with(
            "get_all_positions", {"count": 2}
        )

    @pytest.mark.asyncio
    async def test_delete_position_success(self, trading_repo, sample_position, mock_logger):
        """Test successful position deletion"""
        await trading_repo.save_position(sample_position)

        mock_logger.log_operation_start = MagicMock()
        mock_logger.log_operation_complete = MagicMock()

        result = await trading_repo.delete_position(sample_position.symbol)

        assert result is True
        assert sample_position.symbol not in trading_repo.positions

        mock_logger.log_operation_complete.assert_called_with(
            "delete_position", {"success": True}
        )


class TestCreateTradingRepository:
    """Test suite for create_trading_repository factory function"""

    def test_create_trading_repository(self):
        """Test factory function creates correct instance"""
        repo = create_trading_repository()

        assert get_unified_validator().validate_type(repo, TradingRepositoryInterface)
        assert get_unified_validator().validate_type(repo, InMemoryTradingRepository)


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

