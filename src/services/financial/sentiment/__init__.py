"""
Sentiment Analysis Package

This package provides modular sentiment analysis functionality extracted from
the MarketSentimentService to improve maintainability and follow SRP principles.
"""

from .text_analyzer import TextAnalyzer
from .data_analyzer import DataAnalyzer
from .aggregator import SentimentAggregator
from .data_manager import SentimentDataManager

__all__ = [
    "TextAnalyzer",
    "DataAnalyzer", 
    "SentimentAggregator",
    "SentimentDataManager"
]


