#!/usr/bin/env python3
"""
V3-004: Distributed Tracing Implementation
=========================================

Complete implementation of V3-004 Distributed Tracing for the Dream.OS V3 system.
Provides comprehensive distributed tracing capabilities for agent operations.

Features:
- Jaeger backend integration
- Agent operation tracing
- FSM state tracking
- Messaging observability
- Performance monitoring
- Error correlation
- Trace visualization

Usage:
    python src/v3/v3_004_distributed_tracing.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the main coordinator
from .tracing_coordinator import TracingCoordinator, main

# Re-export for backward compatibility
V3_004_DistributedTracing = TracingCoordinator

if __name__ == "__main__":
    sys.exit(main())
