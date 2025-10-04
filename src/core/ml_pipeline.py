"""
Unified ML Pipeline - V2 Compliant Import Wrapper
==================================================

Backward compatibility wrapper for the refactored unified ML pipeline.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

from .ml_pipeline_config import DeploymentConfig

# Import all components from refactored modules
from .ml_pipeline_core import UnifiedMLPipeline, create_unified_ml_pipeline
from .ml_pipeline_models import (
    ModelConfig,
    ModelType,
    PipelineMetrics,
    PipelineStatus,
    TrainingData,
)

# from .ml_pipeline_utils import (  # Module not found - commented out
#     ModelExporter,
#     ModelInfoManager,
#     ModelValidator,
#     create_sample_model,
#     create_sample_training_data,
#     run_pipeline_demo,
# )

# Re-export main components for backward compatibility
__all__ = [
    "UnifiedMLPipeline",
    "ModelConfig",
    "TrainingData",
    "PipelineMetrics",
    "DeploymentConfig",
    "PipelineStatus",
    "ModelType",
    "ModelValidator",
    "ModelExporter",
    "ModelInfoManager",
    "create_unified_ml_pipeline",
    "create_sample_model",
    "create_sample_training_data",
    "run_pipeline_demo",
]


if __name__ == "__main__":
    # Run pipeline demonstration
    run_pipeline_demo()
