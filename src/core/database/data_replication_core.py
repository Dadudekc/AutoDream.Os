"""
Data Replication System Core - V2 Compliant
V3-003: Data Replication System Core

V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import logging
from datetime import UTC, datetime
from typing import Any

import asyncpg

from .data_replication_models import (
    ConflictRecord,
    ConflictResolutionStrategy,
    ReplicationConfig,
    ReplicationMetrics,
    ReplicationStatus,
    SyncResult,
)

logger = logging.getLogger(__name__)


class DataReplicationCore:
    """Core data replication functionality."""

    def __init__(self, config: ReplicationConfig):
        self.config = config
        self.metrics = ReplicationMetrics(
            records_synced=0,
            conflicts_resolved=0,
            sync_duration=0.0,
            last_sync_time=datetime.now(UTC),
            status=ReplicationStatus.ACTIVE,
        )

    async def sync_data(self) -> SyncResult:
        """Synchronize data between source and target databases."""
        start_time = datetime.now(UTC)
        errors = []
        records_processed = 0
        conflicts_found = 0

        try:
            self.metrics.status = ReplicationStatus.SYNCING

            # Connect to databases
            source_conn = await asyncpg.connect(self.config.source_db)
            target_conn = await asyncpg.connect(self.config.target_db)

            try:
                for table in self.config.tables:
                    table_result = await self._sync_table(source_conn, target_conn, table)
                    records_processed += table_result["records"]
                    conflicts_found += table_result["conflicts"]

            finally:
                await source_conn.close()
                await target_conn.close()

            self.metrics.status = ReplicationStatus.ACTIVE

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            errors.append(str(e))
            self.metrics.status = ReplicationStatus.FAILED
            self.metrics.error_count += 1

        duration = (datetime.now(UTC) - start_time).total_seconds()
        self.metrics.sync_duration = duration
        self.metrics.last_sync_time = datetime.now(UTC)
        self.metrics.records_synced += records_processed

        return SyncResult(
            success=len(errors) == 0,
            records_processed=records_processed,
            conflicts_found=conflicts_found,
            errors=errors,
            duration=duration,
        )

    async def _sync_table(
        self, source_conn: asyncpg.Connection, target_conn: asyncpg.Connection, table: str
    ) -> dict[str, int]:
        """Synchronize a single table."""
        records = 0
        conflicts = 0

        try:
            # Get source data
            source_data = await source_conn.fetch(f"SELECT * FROM {table}")

            for row in source_data:
                record_dict = dict(row)

                # Check for conflicts
                conflict = await self._check_conflict(target_conn, table, record_dict)
                if conflict:
                    conflicts += 1
                    await self._resolve_conflict(target_conn, table, conflict)
                else:
                    await self._upsert_record(target_conn, table, record_dict)

                records += 1

        except Exception as e:
            logger.error(f"Table sync failed for {table}: {e}")
            raise

        return {"records": records, "conflicts": conflicts}

    async def _check_conflict(
        self, target_conn: asyncpg.Connection, table: str, record: dict[str, Any]
    ) -> ConflictRecord | None:
        """Check for data conflicts."""
        try:
            # Simple conflict detection based on primary key
            primary_key = record.get("id")
            if not primary_key:
                return None

            existing = await target_conn.fetchrow(
                f"SELECT * FROM {table} WHERE id = $1", primary_key
            )

            if existing:
                existing_dict = dict(existing)
                if existing_dict != record:
                    return ConflictRecord(
                        record_id=str(primary_key),
                        table_name=table,
                        source_data=record,
                        target_data=existing_dict,
                        conflict_type="data_mismatch",
                        timestamp=datetime.now(UTC),
                    )

        except Exception as e:
            logger.error(f"Conflict check failed: {e}")

        return None

    async def _resolve_conflict(
        self, target_conn: asyncpg.Connection, table: str, conflict: ConflictRecord
    ) -> None:
        """Resolve data conflicts."""
        try:
            if self.config.strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
                await self._upsert_record(target_conn, table, conflict.source_data)
            elif self.config.strategy == ConflictResolutionStrategy.FIRST_WRITE_WINS:
                # Keep existing data (do nothing)
                pass
            elif self.config.strategy == ConflictResolutionStrategy.MANUAL_RESOLUTION:
                # Log conflict for manual resolution
                logger.warning(f"Manual resolution required for {conflict.record_id}")
                return

            self.metrics.conflicts_resolved += 1

        except Exception as e:
            logger.error(f"Conflict resolution failed: {e}")
            raise

    async def _upsert_record(
        self, target_conn: asyncpg.Connection, table: str, record: dict[str, Any]
    ) -> None:
        """Upsert a record into the target table."""
        try:
            columns = list(record.keys())
            values = list(record.values())
            placeholders = [f"${i+1}" for i in range(len(values))]

            # Build upsert query
            update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns])

            query = f"""
                INSERT INTO {table} ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                ON CONFLICT (id) DO UPDATE SET {update_clause}
            """

            await target_conn.execute(query, *values)

        except Exception as e:
            logger.error(f"Upsert failed: {e}")
            raise

    def get_metrics(self) -> ReplicationMetrics:
        """Get current replication metrics."""
        return self.metrics

    def pause_replication(self) -> None:
        """Pause replication."""
        self.metrics.status = ReplicationStatus.PAUSED

    def resume_replication(self) -> None:
        """Resume replication."""
        self.metrics.status = ReplicationStatus.ACTIVE

    def reset_metrics(self) -> None:
        """Reset replication metrics."""
        self.metrics = ReplicationMetrics(
            records_synced=0,
            conflicts_resolved=0,
            sync_duration=0.0,
            last_sync_time=datetime.now(UTC),
            status=self.metrics.status,
        )
