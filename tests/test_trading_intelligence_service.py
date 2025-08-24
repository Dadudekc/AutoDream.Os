import pandas as pd

from src.services.financial.trading_intelligence_service import (
    TradingIntelligenceService,
)
from src.services.financial.trading_intelligence import StrategyType, SignalType


def test_momentum_strategy_buy() -> None:
    service = TradingIntelligenceService()
    data = pd.DataFrame({"Close": [100, 110], "Volume": [1000, 1100]})
    signal = service.run_strategy(StrategyType.MOMENTUM, "XYZ", data)
    assert signal is not None
    assert signal.signal_type == SignalType.BUY


def test_mean_reversion_strategy_sell() -> None:
    service = TradingIntelligenceService()
    data = pd.DataFrame({"Close": [100, 120], "Volume": [1000, 1100]})
    signal = service.run_strategy(StrategyType.MEAN_REVERSION, "XYZ", data)
    assert signal is not None
    assert signal.signal_type == SignalType.SELL
