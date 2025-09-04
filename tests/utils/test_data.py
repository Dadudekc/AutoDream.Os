"""
Test Data Utilities - V2 Compliant Test Data Generation
Shared test data and utilities for comprehensive test coverage
V2 COMPLIANCE: Under 300-line limit, modular design, comprehensive utilities

@version 1.0.0 - V2 COMPLIANCE TEST DATA UTILITIES
@license MIT
"""

from datetime import datetime, timedelta


@dataclass
class PerformanceTestData:
    """Performance test data structure"""
    test_id: str
    agent_id: str
    operation: str
    start_time: datetime
    end_time: datetime
    duration_ms: float
    success: bool
    metadata: Dict[str, Any]


@dataclass
class CoordinationTestData:
    """Coordination test data structure"""
    coordination_id: str
    agents: List[str]
    operation: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    metadata: Dict[str, Any]


def get_performance_test_data(count: int = 10) -> List[PerformanceTestData]:
    """Generate sample performance test data"""
    data = []
    base_time = datetime.now() - timedelta(hours=1)

    for i in range(count):
        start_time = base_time + timedelta(minutes=i * 6)
        duration = 50 + (i * 10)  # Increasing duration
        end_time = start_time + timedelta(milliseconds=duration)

        data.append(PerformanceTestData(
            test_id=f"perf_test_{i}",
            agent_id=f"Agent-{(i % 8) + 1}",
            operation=f"test_operation_{i % 5}",
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration,
            success=i % 10 != 0,  # 90% success rate
            metadata={
                "cpu_usage": 20 + (i * 2),
                "memory_usage": 100 + (i * 5),
                "network_calls": i % 20
            }
        ))

    return data


def get_coordination_test_data(count: int = 5) -> List[CoordinationTestData]:
    """Generate sample coordination test data"""
    data = []
    base_time = datetime.now() - timedelta(hours=2)

    operations = ["pattern_elimination", "system_deployment", "validation_check", "consolidation"]

    for i in range(count):
        start_time = base_time + timedelta(minutes=i * 15)
        end_time = start_time + timedelta(minutes=5 + (i * 2)) if i < count - 1 else None

        agents = [f"Agent-{j+1}" for j in range((i % 3) + 2)]  # 2-4 agents

        data.append(CoordinationTestData(
            coordination_id=f"coord_{i}",
            agents=agents,
            operation=operations[i % len(operations)],
            start_time=start_time,
            end_time=end_time,
            status="completed" if end_time else "in_progress",
            metadata={
                "priority": "high" if i % 3 == 0 else "medium",
                "complexity": i % 5,
                "patterns_processed": 10 + (i * 5)
            }
        ))

    return data


def get_sample_agent_ids() -> List[str]:
    """Get list of sample agent IDs"""
    return [f"Agent-{i}" for i in range(1, 9)]


def get_sample_operations() -> List[str]:
    """Get list of sample operations"""
    return [
        "pattern_elimination",
        "system_deployment",
        "validation_check",
        "consolidation",
        "coordination",
        "integration",
        "optimization"
    ]


def generate_unique_id(prefix: str = "test") -> str:
    """Generate unique test ID"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def get_timestamp_range(hours: int = 24) -> tuple[datetime, datetime]:
    """Get timestamp range for testing"""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    return start_time, end_time


# Export for test imports
__all__ = [
    'PerformanceTestData',
    'CoordinationTestData',
    'get_performance_test_data',
    'get_coordination_test_data',
    'get_sample_agent_ids',
    'get_sample_operations',
    'generate_unique_id',
    'get_timestamp_range'
]
