"""
Data Replication System - V2 Compliant Main Interface
V3-003: Data Replication System

V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import asyncio
import logging

from .data_replication_core import DataReplicationCore
from .data_replication_models import (
    ConflictResolutionStrategy,
    ReplicationConfig,
    ReplicationMetrics,
    ReplicationStatus,
    SyncResult,
)

logger = logging.getLogger(__name__)


class DataReplicationSystem:
    """Main data replication system interface."""

    def __init__(self, config: ReplicationConfig):
        self.config = config
        self.core = DataReplicationCore(config)
        self._running = False

    async def start_replication(self) -> None:
        """Start continuous replication."""
        self._running = True
        logger.info("Starting data replication system")

        while self._running:
            try:
                result = await self.core.sync_data()
                if result.success:
                    logger.info(f"Sync completed: {result.records_processed} records")
                else:
                    logger.error(f"Sync failed: {result.errors}")

                # Wait for next sync interval
                await asyncio.sleep(self.config.sync_interval)

            except Exception as e:
                logger.error(f"Replication error: {e}")
                await asyncio.sleep(60)  # Wait before retry

    def stop_replication(self) -> None:
        """Stop replication."""
        self._running = False
        logger.info("Stopping data replication system")

    async def sync_once(self) -> SyncResult:
        """Perform a single synchronization."""
        return await self.core.sync_data()

    def get_status(self) -> ReplicationStatus:
        """Get current replication status."""
        return self.core.metrics.status

    def get_metrics(self) -> ReplicationMetrics:
        """Get replication metrics."""
        return self.core.get_metrics()

    def pause(self) -> None:
        """Pause replication."""
        self.core.pause_replication()

    def resume(self) -> None:
        """Resume replication."""
        self.core.resume_replication()


def create_replication_config(
    source_db: str,
    target_db: str,
    tables: list[str],
    strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.LAST_WRITE_WINS,
    batch_size: int = 1000,
    sync_interval: int = 60,
) -> ReplicationConfig:
    """Create replication configuration."""
    return ReplicationConfig(
        source_db=source_db,
        target_db=target_db,
        tables=tables,
        strategy=strategy,
        batch_size=batch_size,
        sync_interval=sync_interval,
    )


def create_replication_system(config: ReplicationConfig) -> DataReplicationSystem:
    """Create data replication system."""
    return DataReplicationSystem(config)


async def run_replication_demo() -> None:
    """Run replication system demonstration."""
    # Demo configuration
    config = create_replication_config(
        source_db="postgresql://localhost/source_db",
        target_db="postgresql://localhost/target_db",
        tables=["users", "orders", "products"],
        strategy=ConflictResolutionStrategy.LAST_WRITE_WINS,
        sync_interval=30,
    )

    # Create and start replication system
    replication_system = create_replication_system(config)

    try:
        # Run single sync for demo
        result = await replication_system.sync_once()
        print(f"Demo sync result: {result}")

        # Show metrics
        metrics = replication_system.get_metrics()
        print(f"Metrics: {metrics}")

    except Exception as e:
        print(f"Demo failed: {e}")


def main():
    """CLI entry point for data replication system."""
    import argparse

    parser = argparse.ArgumentParser(description="Data Replication System")
    parser.add_argument("--source", required=True, help="Source database URL")
    parser.add_argument("--target", required=True, help="Target database URL")
    parser.add_argument("--tables", nargs="+", required=True, help="Tables to replicate")
    parser.add_argument(
        "--strategy",
        choices=["last_write_wins", "first_write_wins", "manual"],
        default="last_write_wins",
        help="Conflict resolution strategy",
    )
    parser.add_argument("--interval", type=int, default=60, help="Sync interval in seconds")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")

    args = parser.parse_args()

    if args.demo:
        asyncio.run(run_replication_demo())
        return

    # Create configuration
    strategy_map = {
        "last_write_wins": ConflictResolutionStrategy.LAST_WRITE_WINS,
        "first_write_wins": ConflictResolutionStrategy.FIRST_WRITE_WINS,
        "manual": ConflictResolutionStrategy.MANUAL_RESOLUTION,
    }

    config = create_replication_config(
        source_db=args.source,
        target_db=args.target,
        tables=args.tables,
        strategy=strategy_map[args.strategy],
        sync_interval=args.interval,
    )

    # Create and run replication system
    replication_system = create_replication_system(config)

    try:
        asyncio.run(replication_system.start_replication())
    except KeyboardInterrupt:
        print("Stopping replication system...")
        replication_system.stop_replication()


if __name__ == "__main__":
    main()
