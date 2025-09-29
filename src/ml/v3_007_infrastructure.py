#!/usr/bin/env python3
"""
V3-007: ML Infrastructure Setup
===============================

ML infrastructure setup component for V3-007 implementation.
V2 Compliant: ≤400 lines, single responsibility, KISS principle.
"""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class MLInfrastructureSetup:
    """ML infrastructure setup component."""
    
    def __init__(self, ml_system: Any):
        """Initialize infrastructure setup."""
        self.ml_system = ml_system
        logger.info("🏗️ ML Infrastructure Setup initialized")
    
    def setup_infrastructure(self) -> bool:
        """Setup the ML infrastructure and directories."""
        try:
            # ML infrastructure is already set up in MLPipelineSystem.__init__
            # Verify directories exist
            required_dirs = [
                "src/ml",
                "src/ml/models",
                "src/ml/data",
                "src/ml/logs"
            ]
            
            for dir_path in required_dirs:
                if not Path(dir_path).exists():
                    logger.error(f"❌ ML directory not found: {dir_path}")
                    return False
            
            logger.info("✅ ML infrastructure setup completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup ML infrastructure: {e}")
            return False

