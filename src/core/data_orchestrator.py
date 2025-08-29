from __future__ import annotations
from typing import Any, Dict, List

from .data_sources.db_adapter import DatabaseAdapter
from .data_sources.mapper import DataSourceMapper
from .data_sources.models import DataSource, DataType
from .data_transform.validation import DataValidationEngine


class DataOrchestrator:
    """Coordinates data adapters and transformers."""

    def __init__(self, db_path: str) -> None:
        self.db = DatabaseAdapter(db_path)
        self.mapper = DataSourceMapper()
        self.validator = DataValidationEngine()

    def register_data_source(self, source: DataSource) -> bool:
        return self.db.add_source(source)

    def list_data_sources(self) -> List[DataSource]:
        return self.db.list_sources()

    def remove_data_source(self, source_id: str) -> bool:
        return self.db.remove_source(source_id)

    def validate_data(self, data: Any, data_type: DataType) -> Dict[str, Any]:
        return self.validator.validate_data(data, data_type)

    def get_consolidation_status(self) -> Dict[str, Any]:
        sources = self.list_data_sources()
        return {"total_sources": len(sources)}
