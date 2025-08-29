from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

from ..data_sources.models import DataSource, DataPriority


class DataSourceMigrationFramework:
    """Framework for migrating existing scattered data sources."""

    def __init__(self, consolidation_system: Any) -> None:
        self.consolidation_system = consolidation_system
        self.migration_log = []
        self.migration_status: Dict[str, Any] = {}

    def migrate_service(self, service_name: str) -> Dict[str, Any]:
        result = {
            "service": service_name,
            "status": "pending",
            "sources_migrated": 0,
            "errors": [],
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None,
        }
        try:
            mappings = self.consolidation_system.mapper.get_service_mappings(service_name)
            if not mappings:
                result["errors"].append(f"No mappings found for service: {service_name}")
                result["status"] = "failed"
                return result
            for mapping in mappings:
                if self.consolidation_system.mapper.validate_mapping(mapping):
                    try:
                        self._migrate_source(mapping)
                        result["sources_migrated"] += 1
                    except Exception as exc:  # pragma: no cover - defensive
                        result["errors"].append(f"Failed to migrate source {mapping['name']}: {exc}")
                else:
                    result["errors"].append(f"Invalid mapping for source: {mapping.get('name', 'Unknown')}")
            result["status"] = "completed" if not result["errors"] else "completed_with_errors"
        except Exception as exc:  # pragma: no cover - defensive
            result["status"] = "failed"
            result["errors"].append(f"Migration failed: {exc}")
        result["end_time"] = datetime.now(timezone.utc).isoformat()
        self.migration_log.append(result)
        self.migration_status[service_name] = result
        return result

    def _migrate_source(self, mapping: Dict[str, Any]) -> None:
        source = DataSource(
            id=str(uuid.uuid4()),
            name=mapping["name"],
            type=mapping["type"],
            data_type=mapping["data_type"],
            location=mapping["location"],
            priority=mapping.get("priority", DataPriority.NORMAL),
            metadata=mapping.get("metadata", {}),
            original_service=mapping["original_service"],
            migration_status="migrated",
        )
        self.consolidation_system.register_data_source(source)

    def get_migration_status(self) -> Dict[str, Any]:
        total_services = len(self.migration_status)
        completed_services = sum(
            1
            for status in self.migration_status.values()
            if status["status"] in ["completed", "completed_with_errors"]
        )
        return {
            "total_services": total_services,
            "completed_services": completed_services,
            "pending_services": total_services - completed_services,
            "migration_log": self.migration_log,
            "service_status": self.migration_status,
        }

    def rollback_migration(self, service_name: str) -> bool:
        if service_name not in self.migration_status:
            return False
        try:
            sources_to_remove = [
                source.id
                for source in self.consolidation_system.list_data_sources()
                if source.original_service == service_name
            ]
            for source_id in sources_to_remove:
                self.consolidation_system.remove_data_source(source_id)
            self.migration_status[service_name]["status"] = "rolled_back"
            self.migration_status[service_name]["rollback_time"] = datetime.now(timezone.utc).isoformat()
            return True
        except Exception:  # pragma: no cover - defensive
            return False
