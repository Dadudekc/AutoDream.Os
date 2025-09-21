#!/usr/bin/env python3
"""
V3-001: Cloud Infrastructure Data Services
=========================================

Data services configuration for cloud infrastructure.
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


class CloudInfrastructureData:
    """Data services configuration for cloud infrastructure."""
    
    def __init__(self, config: InfrastructureConfig):
        """Initialize data services."""
        self.config = config
    
    def create_rds_config(self) -> Dict[str, Any]:
        """Create RDS database configuration."""
        try:
            logger.info("Creating RDS configuration...")
            
            rds_config = {
                "identifier": f"{self.config.project_name}-rds",
                "engine": "postgres",
                "engine_version": self.config.rds_engine_version,
                "instance_class": self.config.rds_instance_class,
                "allocated_storage": 100,
                "max_allocated_storage": 1000,
                "storage_type": "gp3",
                "storage_encrypted": True,
                "multi_az": True,
                "publicly_accessible": False,
                "backup_retention_period": 7,
                "backup_window": "03:00-04:00",
                "maintenance_window": "sun:04:00-sun:05:00",
                "auto_minor_version_upgrade": True,
                "deletion_protection": True,
                "performance_insights_enabled": True,
                "monitoring_interval": 60,
                "monitoring_role_arn": f"arn:aws:iam::ACCOUNT_ID:role/{self.config.project_name}-rds-monitoring-role",
                "db_subnet_group_name": f"{self.config.project_name}-db-subnet-group",
                "vpc_security_group_ids": [
                    f"{self.config.project_name}-rds-sg"
                ],
                "parameter_group_name": f"{self.config.project_name}-postgres-params",
                "option_group_name": f"{self.config.project_name}-postgres-options",
                "tags": {
                    "Name": f"{self.config.project_name}-rds",
                    "Environment": self.config.environment,
                    "Project": self.config.project_name
                }
            }
            
            # Add database subnet group
            rds_config["db_subnet_group"] = {
                "name": f"{self.config.project_name}-db-subnet-group",
                "subnet_ids": [
                    f"{self.config.project_name}-database-{az}" 
                    for az in self.config.availability_zones
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-db-subnet-group",
                    "Environment": self.config.environment
                }
            }
            
            # Add parameter group
            rds_config["parameter_group"] = {
                "name": f"{self.config.project_name}-postgres-params",
                "family": "postgres15",
                "description": f"Parameter group for {self.config.project_name}",
                "parameters": [
                    {
                        "name": "shared_preload_libraries",
                        "value": "pg_stat_statements"
                    },
                    {
                        "name": "log_statement",
                        "value": "all"
                    },
                    {
                        "name": "log_min_duration_statement",
                        "value": "1000"
                    }
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-postgres-params",
                    "Environment": self.config.environment
                }
            }
            
            logger.info("RDS configuration created successfully")
            return rds_config
            
        except Exception as e:
            logger.error(f"Error creating RDS configuration: {e}")
            return {}
    
    def create_redis_config(self) -> Dict[str, Any]:
        """Create Redis cache configuration."""
        try:
            logger.info("Creating Redis configuration...")
            
            redis_config = {
                "cluster_id": f"{self.config.project_name}-redis",
                "node_type": self.config.redis_node_type,
                "num_cache_nodes": 2,
                "engine_version": "7.0",
                "port": 6379,
                "parameter_group_name": f"{self.config.project_name}-redis-params",
                "subnet_group_name": f"{self.config.project_name}-redis-subnet-group",
                "security_group_ids": [
                    f"{self.config.project_name}-redis-sg"
                ],
                "snapshot_retention_limit": 5,
                "snapshot_window": "03:00-05:00",
                "maintenance_window": "sun:05:00-sun:07:00",
                "auto_minor_version_upgrade": True,
                "at_rest_encryption_enabled": True,
                "transit_encryption_enabled": True,
                "auth_token": "REPLACE_WITH_SECURE_TOKEN",
                "tags": {
                    "Name": f"{self.config.project_name}-redis",
                    "Environment": self.config.environment,
                    "Project": self.config.project_name
                }
            }
            
            # Add subnet group
            redis_config["subnet_group"] = {
                "name": f"{self.config.project_name}-redis-subnet-group",
                "description": f"Subnet group for {self.config.project_name} Redis",
                "subnet_ids": [
                    f"{self.config.project_name}-private-{az}" 
                    for az in self.config.availability_zones
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-redis-subnet-group",
                    "Environment": self.config.environment
                }
            }
            
            # Add parameter group
            redis_config["parameter_group"] = {
                "name": f"{self.config.project_name}-redis-params",
                "family": "redis7.x",
                "description": f"Parameter group for {self.config.project_name} Redis",
                "parameters": [
                    {
                        "name": "maxmemory-policy",
                        "value": "allkeys-lru"
                    },
                    {
                        "name": "timeout",
                        "value": "300"
                    }
                ],
                "tags": {
                    "Name": f"{self.config.project_name}-redis-params",
                    "Environment": self.config.environment
                }
            }
            
            logger.info("Redis configuration created successfully")
            return redis_config
            
        except Exception as e:
            logger.error(f"Error creating Redis configuration: {e}")
            return {}



