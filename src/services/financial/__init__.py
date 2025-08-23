"""Financial Services Module - simplified for testing.

This package exposes financial service components. During testing we avoid
importing heavy dependencies so that modules with optional third-party
requirements (e.g. `yfinance`) don't fail on import. Individual services
should be imported directly as needed.
"""

__version__ = "1.0.0"
__author__ = "Business Intelligence Agent"
__status__ = "ACTIVE"

# Intentionally leave __all__ empty to prevent eager imports that may rely on
# unavailable external packages. Consumers can import the required services
# explicitly, e.g. ``from src.services.financial.trading_intelligence_v2 import
# TradingIntelligenceService``.
__all__: list[str] = []

