from __future__ import annotations
from typing import Any, Dict, List

from .models import DataSourceType, DataType, DataPriority


class DataSourceMapper:
    """Maps existing scattered data sources to unified system."""

    def __init__(self) -> None:
        self.source_mappings = {
            "market_data_service": {
                "sources": [
                    {
                        "name": "YFinance Market Data",
                        "type": DataSourceType.API,
                        "data_type": DataType.MARKET,
                        "location": "src/services/financial/market_data_service.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "market_data_service",
                        "metadata": {
                            "provider": "yfinance",
                            "cache_duration": 300,
                            "market_hours": "09:30-16:00 EST",
                        },
                    },
                    {
                        "name": "Mock Market Data",
                        "type": DataSourceType.MOCK,
                        "data_type": DataType.MARKET,
                        "location": "src/services/financial/market_data_service.py",
                        "priority": DataPriority.LOW,
                        "original_service": "market_data_service",
                        "metadata": {
                            "provider": "mock",
                            "purpose": "testing",
                        },
                    },
                ]
            },
            "sentiment_data_analyzer": {
                "sources": [
                    {
                        "name": "Analyst Ratings Sentiment",
                        "type": DataSourceType.API,
                        "data_type": DataType.SENTIMENT,
                        "location": "src/services/financial/sentiment/data_analyzer.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "sentiment_data_analyzer",
                        "metadata": {
                            "analysis_method": "rating_based",
                            "confidence_threshold": 0.7,
                        },
                    },
                    {
                        "name": "Options Flow Sentiment",
                        "type": DataSourceType.API,
                        "data_type": DataType.OPTIONS,
                        "location": "src/services/financial/sentiment/data_analyzer.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "sentiment_data_analyzer",
                        "metadata": {
                            "analysis_method": "volume_based",
                            "pcr_threshold": 1.0,
                        },
                    },
                    {
                        "name": "Insider Trading Sentiment",
                        "type": DataSourceType.API,
                        "data_type": DataType.INSIDER_TRADING,
                        "location": "src/services/financial/sentiment/data_analyzer.py",
                        "priority": DataPriority.CRITICAL,
                        "original_service": "sentiment_data_analyzer",
                        "metadata": {
                            "analysis_method": "activity_based",
                            "trade_size_threshold": 100000,
                        },
                    },
                ]
            },
            "data_manager": {
                "sources": [
                    {
                        "name": "Unified Data Manager",
                        "type": DataSourceType.DATABASE,
                        "data_type": DataType.SYSTEM,
                        "location": "src/core/managers/data_manager.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "data_manager",
                        "metadata": {
                            "consolidation_level": "high",
                            "duplication_eliminated": "80%",
                        },
                    }
                ]
            },
        }

    def get_all_source_mappings(self) -> List[Dict[str, Any]]:
        """Get all source mappings for migration."""
        all_sources: List[Dict[str, Any]] = []
        for mapping_data in self.source_mappings.values():
            all_sources.extend(mapping_data["sources"])
        return all_sources

    def get_service_mappings(self, service_name: str) -> List[Dict[str, Any]]:
        """Get mappings for a specific service."""
        return self.source_mappings.get(service_name, {}).get("sources", [])

    def validate_mapping(self, mapping: Dict[str, Any]) -> bool:
        """Validate a source mapping."""
        required_fields = ["name", "type", "data_type", "location", "original_service"]
        return all(field in mapping for field in required_fields)
