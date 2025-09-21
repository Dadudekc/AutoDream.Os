#!/usr/bin/env python3
"""
V3-001: Cloud Infrastructure Networking
=====================================

Networking components for cloud infrastructure.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .cloud_infrastructure_models import InfrastructureConfig

logger = logging.getLogger(__name__)


class CloudInfrastructureNetworking:
    """Networking components for cloud infrastructure."""
    
    def __init__(self, config: InfrastructureConfig):
        """Initialize networking components."""
        self.config = config
    
    def create_vpc_config(self) -> Dict[str, Any]:
        """Create VPC configuration."""
        try:
            logger.info("Creating VPC configuration...")
            
            vpc_config = {
                "name": f"{self.config.project_name}-vpc",
                "cidr_block": self.config.vpc_cidr,
                "enable_dns_hostnames": True,
                "enable_dns_support": True,
                "tags": {
                    "Name": f"{self.config.project_name}-vpc",
                    "Environment": self.config.environment,
                    "Project": self.config.project_name
                }
            }
            
            # Add availability zones
            vpc_config["availability_zones"] = self.config.availability_zones
            
            # Add subnets
            vpc_config["public_subnets"] = []
            vpc_config["private_subnets"] = []
            vpc_config["database_subnets"] = []
            
            for i, az in enumerate(self.config.availability_zones):
                # Public subnet
                public_subnet = {
                    "name": f"{self.config.project_name}-public-{az}",
                    "cidr_block": self.config.public_subnet_cidrs[i],
                    "availability_zone": az,
                    "map_public_ip_on_launch": True,
                    "tags": {
                        "Name": f"{self.config.project_name}-public-{az}",
                        "Type": "public",
                        "Environment": self.config.environment
                    }
                }
                vpc_config["public_subnets"].append(public_subnet)
                
                # Private subnet
                private_subnet = {
                    "name": f"{self.config.project_name}-private-{az}",
                    "cidr_block": self.config.private_subnet_cidrs[i],
                    "availability_zone": az,
                    "map_public_ip_on_launch": False,
                    "tags": {
                        "Name": f"{self.config.project_name}-private-{az}",
                        "Type": "private",
                        "Environment": self.config.environment
                    }
                }
                vpc_config["private_subnets"].append(private_subnet)
                
                # Database subnet
                database_subnet = {
                    "name": f"{self.config.project_name}-database-{az}",
                    "cidr_block": self.config.database_subnet_cidrs[i],
                    "availability_zone": az,
                    "map_public_ip_on_launch": False,
                    "tags": {
                        "Name": f"{self.config.project_name}-database-{az}",
                        "Type": "database",
                        "Environment": self.config.environment
                    }
                }
                vpc_config["database_subnets"].append(database_subnet)
            
            # Add internet gateway
            vpc_config["internet_gateway"] = {
                "name": f"{self.config.project_name}-igw",
                "tags": {
                    "Name": f"{self.config.project_name}-igw",
                    "Environment": self.config.environment
                }
            }
            
            # Add NAT gateways
            vpc_config["nat_gateways"] = []
            for i, az in enumerate(self.config.availability_zones):
                nat_gateway = {
                    "name": f"{self.config.project_name}-nat-{az}",
                    "subnet": f"{self.config.project_name}-public-{az}",
                    "tags": {
                        "Name": f"{self.config.project_name}-nat-{az}",
                        "Environment": self.config.environment
                    }
                }
                vpc_config["nat_gateways"].append(nat_gateway)
            
            logger.info("VPC configuration created successfully")
            return vpc_config
            
        except Exception as e:
            logger.error(f"Error creating VPC configuration: {e}")
            return {}
    
    def create_eks_config(self) -> Dict[str, Any]:
        """Create EKS cluster configuration."""
        try:
            logger.info("Creating EKS configuration...")
            
            eks_config = {
                "cluster_name": f"{self.config.project_name}-eks",
                "version": self.config.eks_cluster_version,
                "role_arn": f"arn:aws:iam::ACCOUNT_ID:role/{self.config.project_name}-eks-role",
                "subnet_ids": [
                    f"{self.config.project_name}-private-{az}" 
                    for az in self.config.availability_zones
                ],
                "security_group_ids": [
                    f"{self.config.project_name}-eks-cluster-sg"
                ],
                "endpoint_config": {
                    "private_access": True,
                    "public_access": True,
                    "public_access_cidrs": ["0.0.0.0/0"]
                },
                "logging": {
                    "enable_types": ["api", "audit", "authenticator", "controllerManager", "scheduler"]
                },
                "addons": [
                    {
                        "name": "vpc-cni",
                        "version": "latest"
                    },
                    {
                        "name": "coredns",
                        "version": "latest"
                    },
                    {
                        "name": "kube-proxy",
                        "version": "latest"
                    }
                ],
                "node_groups": []
            }
            
            # Add node groups
            for i, instance_type in enumerate(self.config.eks_node_group_instance_types):
                node_group = {
                    "name": f"{self.config.project_name}-node-group-{i+1}",
                    "instance_types": [instance_type],
                    "capacity_type": "ON_DEMAND",
                    "scaling_config": {
                        "desired_size": 2,
                        "max_size": 10,
                        "min_size": 1
                    },
                    "subnet_ids": [
                        f"{self.config.project_name}-private-{az}" 
                        for az in self.config.availability_zones
                    ],
                    "tags": {
                        "Name": f"{self.config.project_name}-node-group-{i+1}",
                        "Environment": self.config.environment
                    }
                }
                eks_config["node_groups"].append(node_group)
            
            logger.info("EKS configuration created successfully")
            return eks_config
            
        except Exception as e:
            logger.error(f"Error creating EKS configuration: {e}")
            return {}



