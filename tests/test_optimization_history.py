"""Tests for shared optimization history behavior."""

import types
import sys
from enum import Enum
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.modules.setdefault("src", types.ModuleType("src"))
sys.modules.setdefault("src.core", types.ModuleType("src.core"))

ic_pkg = types.ModuleType("src.core.integration_coordinators")
ic_pkg.__path__ = [str(ROOT / "src/core/integration_coordinators")]
sys.modules["src.core.integration_coordinators"] = ic_pkg

ui_pkg = types.ModuleType("src.core.integration_coordinators.unified_integration")
ui_pkg.__path__ = [str(ROOT / "src/core/integration_coordinators/unified_integration")]
sys.modules["src.core.integration_coordinators.unified_integration"] = ui_pkg

opt_pkg = types.ModuleType(
    "src.core.integration_coordinators.unified_integration.optimizers"
)
opt_pkg.__path__ = [str(ROOT / "src/core/integration_coordinators/unified_integration/optimizers")]
sys.modules[
    "src.core.integration_coordinators.unified_integration.optimizers"
] = opt_pkg

models_module = types.ModuleType(
    "src.core.integration_coordinators.unified_integration.models"
)

class IntegrationType(Enum):
    API = "api"


class OptimizationLevel(Enum):
    BASIC = "basic"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


class IntegrationMetrics:
    """Stub for integration metrics."""


class OptimizationConfig:
    """Stub for optimization config."""

    def __init__(self, integration_type: IntegrationType, optimization_level: OptimizationLevel):
        self.integration_type = integration_type
        self.optimization_level = optimization_level


class PerformanceReport:
    """Stub for performance report."""


class OptimizationRecommendation(dict):
    """Stub for optimization recommendation."""


class IntegrationModels:
    """Stub for model factory."""

    @staticmethod
    def create_optimization_recommendation(**kwargs):
        return kwargs


models_module.IntegrationType = IntegrationType
models_module.OptimizationLevel = OptimizationLevel
models_module.IntegrationMetrics = IntegrationMetrics
models_module.OptimizationConfig = OptimizationConfig
models_module.PerformanceReport = PerformanceReport
models_module.OptimizationRecommendation = OptimizationRecommendation
models_module.IntegrationModels = IntegrationModels

sys.modules["src.core.integration_coordinators.unified_integration.models"] = models_module

from src.core.integration_coordinators.unified_integration.optimizers.optimizer import IntegrationOptimizer
from src.core.integration_coordinators.unified_integration.optimizers.maximum_optimizer import MaximumOptimizer


def test_shared_history_recording() -> None:
    integration_optimizer = IntegrationOptimizer()
    maximum_optimizer = MaximumOptimizer()

    improvements = [{'key': 'value'}]
    integration_optimizer._record_optimization(IntegrationType.API, improvements, 5.0)
    maximum_optimizer._record_optimization(IntegrationType.API, improvements, 5.0)

    integration_history = integration_optimizer.get_optimization_history()
    maximum_history = maximum_optimizer.get_optimization_history()

    assert integration_history[0]['improvements_count'] == 1
    assert 'optimization_level' not in integration_history[0]

    assert maximum_history[0]['improvements_count'] == 1
    assert maximum_history[0]['optimization_level'] == 'maximum'
