import time

from src.core.scaling import (
    ResourceMonitor,
    ScalingDecider,
    ScalingExecutor,
    ScalingConfig,
    ScalingMetrics,
    ScalingStatus,
    LoadDistributor,
    ScalingStrategy,
)
from src.core.managers.scaling_manager import ScalingManager


class DummyScalingManager(ScalingManager):
    def _on_initialize_resources(self) -> bool:  # pragma: no cover - minimal stub
        return True

    def _on_cleanup_resources(self) -> None:  # pragma: no cover - minimal stub
        pass

    def _on_start(self) -> bool:  # pragma: no cover - minimal stub
        return True

    def _on_stop(self) -> None:  # pragma: no cover - minimal stub
        pass

    def _on_recovery_attempt(self) -> bool:  # pragma: no cover - minimal stub
        return False

    def _on_heartbeat(self) -> None:  # pragma: no cover - minimal stub
        pass


def test_resource_monitor_tracks_metrics():
    monitor = ResourceMonitor()
    m1 = monitor.collect(1, 50.0, 60.0)
    m2 = monitor.collect(1, 70.0, 80.0)
    assert monitor.latest() == m2
    assert len(monitor.history) == 2
    assert monitor.history[0] == m1


def test_scaling_decider_actions():
    config = ScalingConfig(target_cpu_utilization=70.0, target_memory_utilization=80.0)
    decider = ScalingDecider()
    high = ScalingMetrics(1, 1, 90.0, 90.0, 0, 0, 0, time.time())
    low = ScalingMetrics(1, 1, 20.0, 20.0, 0, 0, 0, time.time())
    mid = ScalingMetrics(1, 1, 60.0, 60.0, 0, 0, 0, time.time())
    assert decider.decide(high, config).action == "scale_up"
    assert decider.decide(low, config).action == "scale_down"
    assert decider.decide(mid, config).action == "maintain"


def test_scaling_executor_updates_instances():
    executor = ScalingExecutor()
    config = ScalingConfig(min_instances=1, max_instances=3)
    instances, status = executor.execute("scale_up", 1, config)
    assert instances == 2 and status == ScalingStatus.SCALING_UP
    instances, status = executor.execute("scale_down", instances, config)
    assert instances == 1 and status == ScalingStatus.SCALING_DOWN
    instances, status = executor.execute("optimize", instances, config)
    assert instances == 1 and status == ScalingStatus.OPTIMIZING


def test_load_distributor_round_robin():
    distributor = LoadDistributor()
    instances = ["i1", "i2", "i3"]
    request = {}
    results = [
        distributor.distribute(request, ScalingStrategy.ROUND_ROBIN, instances)
        for _ in range(3)
    ]
    assert results == ["i1", "i2", "i3"]
