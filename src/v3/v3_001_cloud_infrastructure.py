#!/usr/bin/env python3
"""
V3-001: Cloud Infrastructure Setup Implementation
===============================================

Complete implementation of V3-001 Cloud Infrastructure Setup for the Dream.OS V3 system.
Provides comprehensive cloud infrastructure capabilities for agent operations.

Features:
- AWS VPC and networking
- EKS cluster configuration
- RDS database setup
- Redis cache configuration
- Security groups and IAM roles
- Kubernetes deployment
- Terraform automation
- Validation tools

Usage:
    python src/v3/v3_001_cloud_infrastructure.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the main coordinator
from .cloud_infrastructure_coordinator import CloudInfrastructureCoordinator, main

# Re-export for backward compatibility
V3001CloudInfrastructure = CloudInfrastructureCoordinator

if __name__ == "__main__":
    sys.exit(main())





