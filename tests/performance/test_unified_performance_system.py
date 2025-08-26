"""Unit tests for the consolidated UnifiedPerformanceSystem."""

from src.core.unified_performance_system import UnifiedPerformanceSystem


def test_start_stop_and_report():
    system = UnifiedPerformanceSystem()
    assert system.start_system()

    result = system.run_benchmark("cpu", duration=0)
    assert result.success

    report = system.generate_report()
    assert isinstance(report, dict)

    status = system.get_system_status()
    assert "system_status" in status

    assert system.stop_system()
