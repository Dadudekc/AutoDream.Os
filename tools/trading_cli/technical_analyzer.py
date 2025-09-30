#!/usr/bin/env python3
"""
Technical Analysis CLI Tool
===========================

Advanced technical analysis for better trading predictions.
Refactored into modular components for V2 compliance.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

# Import all components from refactored modules
from .technical_analyzer_core import TechnicalAnalyzer
from .technical_analyzer_main import main
from .technical_analyzer_utils import (
    calculate_bollinger_bands,
    calculate_ema,
    calculate_macd,
    calculate_rsi,
    calculate_sma,
    calculate_stochastic,
    calculate_technical_indicators,
    generate_technical_signals,
)

# Re-export main classes for backward compatibility
__all__ = [
    # Main analyzer
    "TechnicalAnalyzer",
    # Utility functions
    "calculate_sma",
    "calculate_ema",
    "calculate_rsi",
    "calculate_macd",
    "calculate_bollinger_bands",
    "calculate_stochastic",
    "calculate_technical_indicators",
    "generate_technical_signals",
    # CLI
    "main",
]


# For direct execution
if __name__ == "__main__":
    main()
