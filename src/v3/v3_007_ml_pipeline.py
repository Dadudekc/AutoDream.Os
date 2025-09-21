#!/usr/bin/env python3
"""
V3-007: ML Pipeline Setup Implementation
=======================================

Complete implementation of V3-007 ML Pipeline Setup for the Dream.OS V3 system.
Provides comprehensive machine learning capabilities for agent operations.

Features:
- TensorFlow/PyTorch integration
- Model training and deployment
- Data preprocessing pipelines
- Model versioning and management
- Performance monitoring
- Automated retraining

Usage:
    python src/v3/v3_007_ml_pipeline.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the main coordinator
from .ml_pipeline_coordinator import MLPipelineCoordinator, main

# Re-export for backward compatibility
V3_007_MLPipeline = MLPipelineCoordinator

if __name__ == "__main__":
    sys.exit(main())





