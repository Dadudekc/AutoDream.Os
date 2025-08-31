from src.core.unified_data_source_consolidation import (
    UnifiedDataSourceManager,
    DataValidator,
    DataSourceMigrator,
    DataSource,
    DataSourceType,
    DataType,
    DataPriority,
)


def _create_source(idx: str, enabled: bool = True) -> DataSource:
    """Helper to create a DataSource instance"""
    return DataSource(
        id=f"source-{idx}",
        name=f"Source {idx}",
        type=DataSourceType.API,
        data_type=DataType.MARKET,
        location=f"/tmp/source{idx}.json",
        priority=DataPriority.HIGH,
        enabled=enabled,
        metadata={"provider": "test"},
        validation_rules={},
        access_patterns=[],
        original_service="test_service",
        migration_status="pending",
    )


def test_imports():
    from src.core.unified_data_source_consolidation import (
        UnifiedDataSourceManager,
        DataValidator,
        DataSourceMigrator,
        DataSource,
        DataSourceType,
        DataType,
        DataPriority,
    )


def test_unified_manager_and_ssot():
    manager = UnifiedDataSourceManager()
    src1 = _create_source("1")
    src2 = _create_source("2")
    target = _create_source("target")

    assert manager.add_source(src1)
    assert manager.add_source(src2)
    assert manager.add_source(target)
    assert len(manager.list_sources()) == 3

    assert manager.consolidate_sources(target, ["source-1", "source-2"])
    report = manager.generate_report()
    # After consolidation, source-1 and source-2 should be disabled (SSOT enforced)
    disabled_sources = [s for s in manager.list_sources() if not s.enabled]
    assert len(disabled_sources) == 2
    assert report.total_sources == 3


def test_data_validator():
    validator = DataValidator()
    valid_data = {"id": "1", "name": "Example", "type": "test"}
    assert validator.validate_data(valid_data)["valid"]
    invalid_data = {"id": "1"}
    assert not validator.validate_data(invalid_data)["valid"]


def test_data_source_migrator(tmp_path):
    migrator = DataSourceMigrator()
    source = _create_source("src")
    target = _create_source("tgt")
    data = []
    success = migrator.migrate_data(source, target, data)
    assert isinstance(success, bool)
    validation = migrator.validate_migration(source, target, 10, 10)
    assert validation["success"]
