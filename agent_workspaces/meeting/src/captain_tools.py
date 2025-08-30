import logging
from dataclasses import dataclass

# Shared logging configuration for captain scripts
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - CAPTAIN AGENT-3 - %(levelname)s - %(message)s'
)

logger = logging.getLogger("captain_tools")


@dataclass
class OptimizationResult:
    """Result of optimization operation."""
    success: bool
    performance_improvement: float
    optimization_type: str
    implementation_time: float
    system_impact: str
    innovation_score: float


@dataclass
class SystemMetrics:
    """Comprehensive system performance metrics."""
    cpu_usage: float
    memory_usage: float
    disk_io: float
    network_throughput: float
    process_count: int
    system_load: float
    optimization_potential: float


@dataclass
class WorkflowMetrics:
    """Comprehensive workflow performance metrics."""
    current_momentum: float
    efficiency_score: float
    productivity_rate: float
    workflow_velocity: float
    acceleration_potential: float
    innovation_readiness: float


@dataclass
class AccelerationResult:
    """Result of workflow acceleration operation."""
    success: bool
    momentum_increase: float
    acceleration_type: str
    implementation_time: float
    workflow_impact: str
    innovation_score: float


@dataclass
class InnovationMetrics:
    """Comprehensive innovation readiness metrics."""
    gateway_readiness: float
    transition_protocols: float
    innovation_capacity: float
    system_adaptability: float
    captain_leadership: float
    innovation_activation_potential: float


@dataclass
class GatewayResult:
    """Result of gateway activation operation."""
    success: bool
    activation_level: float
    activation_type: str
    implementation_time: float
    system_impact: str
    innovation_score: float
