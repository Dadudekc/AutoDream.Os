#!/usr/bin/env python3
"""
V3-001: Cloud Infrastructure Models
==================================

Data models for cloud infrastructure configuration.
"""

from dataclasses import dataclass
from enum import Enum


class InfrastructureComponent(Enum):
    """Infrastructure components for V3-001."""

    VPC = "vpc"
    EKS = "eks"
    RDS = "rds"
    REDIS = "redis"
    SECURITY = "security"
    KUBERNETES = "kubernetes"
    MONITORING = "monitoring"
    LOGGING = "logging"


@dataclass
class InfrastructureConfig:
    """Configuration for cloud infrastructure."""

    project_name: str = "dream-os-v3"
    environment: str = "production"
    region: str = "us-west-2"
    availability_zones: list[str] = None
    vpc_cidr: str = "10.0.0.0/16"
    public_subnet_cidrs: list[str] = None
    private_subnet_cidrs: list[str] = None
    database_subnet_cidrs: list[str] = None
    eks_cluster_version: str = "1.28"
    eks_node_group_instance_types: list[str] = None
    rds_instance_class: str = "db.t3.medium"
    rds_engine_version: str = "15.4"
    redis_node_type: str = "cache.t3.micro"
    enable_monitoring: bool = True
    enable_logging: bool = True

    def __post_init__(self):
        """Set default values after initialization."""
        if self.availability_zones is None:
            self.availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]

        if self.public_subnet_cidrs is None:
            self.public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

        if self.private_subnet_cidrs is None:
            self.private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]

        if self.database_subnet_cidrs is None:
            self.database_subnet_cidrs = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

        if self.eks_node_group_instance_types is None:
            self.eks_node_group_instance_types = ["t3.medium", "t3.large"]
