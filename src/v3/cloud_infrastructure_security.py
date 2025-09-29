#!/usr/bin/env python3
"""
V3-001: Cloud Infrastructure Security
===================================

Security configuration for cloud infrastructure.
"""

import logging
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .cloud_infrastructure_models import InfrastructureConfig

logger = logging.getLogger(__name__)


class CloudInfrastructureSecurity:
    """Security configuration for cloud infrastructure."""

    def __init__(self, config: InfrastructureConfig):
        """Initialize security components."""
        self.config = config

    def create_security_config(self) -> dict[str, Any]:
        """Create security configuration."""
        try:
            logger.info("Creating security configuration...")

            security_config = {
                "security_groups": [],
                "iam_roles": [],
                "policies": [],
                "certificates": [],
            }

            # EKS Cluster Security Group
            eks_cluster_sg = {
                "name": f"{self.config.project_name}-eks-cluster-sg",
                "description": f"Security group for {self.config.project_name} EKS cluster",
                "vpc_id": f"{self.config.project_name}-vpc",
                "ingress_rules": [
                    {
                        "from_port": 443,
                        "to_port": 443,
                        "protocol": "tcp",
                        "cidr_blocks": ["0.0.0.0/0"],
                        "description": "HTTPS from anywhere",
                    }
                ],
                "egress_rules": [
                    {
                        "from_port": 0,
                        "to_port": 0,
                        "protocol": "-1",
                        "cidr_blocks": ["0.0.0.0/0"],
                        "description": "All outbound traffic",
                    }
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-eks-cluster-sg",
                    "Environment": self.config.environment,
                },
            }
            security_config["security_groups"].append(eks_cluster_sg)

            # EKS Node Group Security Group
            eks_node_sg = {
                "name": f"{self.config.project_name}-eks-node-sg",
                "description": f"Security group for {self.config.project_name} EKS node group",
                "vpc_id": f"{self.config.project_name}-vpc",
                "ingress_rules": [
                    {
                        "from_port": 0,
                        "to_port": 65535,
                        "protocol": "tcp",
                        "source_security_group_id": f"{self.config.project_name}-eks-cluster-sg",
                        "description": "All traffic from EKS cluster",
                    },
                    {
                        "from_port": 22,
                        "to_port": 22,
                        "protocol": "tcp",
                        "cidr_blocks": ["10.0.0.0/16"],
                        "description": "SSH from VPC",
                    },
                ],
                "egress_rules": [
                    {
                        "from_port": 0,
                        "to_port": 0,
                        "protocol": "-1",
                        "cidr_blocks": ["0.0.0.0/0"],
                        "description": "All outbound traffic",
                    }
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-eks-node-sg",
                    "Environment": self.config.environment,
                },
            }
            security_config["security_groups"].append(eks_node_sg)

            # RDS Security Group
            rds_sg = {
                "name": f"{self.config.project_name}-rds-sg",
                "description": f"Security group for {self.config.project_name} RDS",
                "vpc_id": f"{self.config.project_name}-vpc",
                "ingress_rules": [
                    {
                        "from_port": 5432,
                        "to_port": 5432,
                        "protocol": "tcp",
                        "source_security_group_id": f"{self.config.project_name}-eks-node-sg",
                        "description": "PostgreSQL from EKS nodes",
                    }
                ],
                "egress_rules": [],
                "tags": {
                    "Name": f"{self.config.project_name}-rds-sg",
                    "Environment": self.config.environment,
                },
            }
            security_config["security_groups"].append(rds_sg)

            # Redis Security Group
            redis_sg = {
                "name": f"{self.config.project_name}-redis-sg",
                "description": f"Security group for {self.config.project_name} Redis",
                "vpc_id": f"{self.config.project_name}-vpc",
                "ingress_rules": [
                    {
                        "from_port": 6379,
                        "to_port": 6379,
                        "protocol": "tcp",
                        "source_security_group_id": f"{self.config.project_name}-eks-node-sg",
                        "description": "Redis from EKS nodes",
                    }
                ],
                "egress_rules": [],
                "tags": {
                    "Name": f"{self.config.project_name}-redis-sg",
                    "Environment": self.config.environment,
                },
            }
            security_config["security_groups"].append(redis_sg)

            # IAM Roles
            eks_cluster_role = {
                "name": f"{self.config.project_name}-eks-cluster-role",
                "assume_role_policy": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "eks.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                },
                "managed_policy_arns": ["arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"],
                "tags": {
                    "Name": f"{self.config.project_name}-eks-cluster-role",
                    "Environment": self.config.environment,
                },
            }
            security_config["iam_roles"].append(eks_cluster_role)

            eks_node_role = {
                "name": f"{self.config.project_name}-eks-node-role",
                "assume_role_policy": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "ec2.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                },
                "managed_policy_arns": [
                    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
                    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
                    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-eks-node-role",
                    "Environment": self.config.environment,
                },
            }
            security_config["iam_roles"].append(eks_node_role)

            logger.info("Security configuration created successfully")
            return security_config

        except Exception as e:
            logger.error(f"Error creating security configuration: {e}")
            return {}
