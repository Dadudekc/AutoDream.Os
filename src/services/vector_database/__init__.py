#!/usr/bin/env python3
"""
Vector Database Package - V2 Compliance
=======================================

High-performance vector database system for agent coordination.
Provides vector storage, indexing, and search capabilities.

Author: Agent-3 (Database Specialist)
License: MIT
V2 Compliance: Modular design, comprehensive error handling
"""

from .indexing import IndexEntry, IndexStats, IndexStatus, IndexType
from .status_indexer import StatusIndexer
from .vector_database_integration import VectorDatabaseIntegration
from .vector_database_models import (
    VectorDatabaseConnection,
    VectorDatabaseError,
    VectorDatabaseMetrics,
    VectorIndex,
    VectorMetadata,
    VectorQuery,
    VectorRecord,
    VectorStatus,
    VectorType,
)
from .vector_database_monitoring import Alert, AlertLevel, PerformanceMetric
from .vector_database_monitoring import VectorDatabaseMonitoring as VectorDatabaseMonitor
from .vector_database_orchestrator import VectorDatabaseOrchestrator

# Temporarily commented out problematic imports to fix core functionality
# from .architecture_integration import ArchitectureIntegration
# from .record_time_migration import RecordTimeMigration
# from .enhanced_collaboration import EnhancedCollaboration, CollaborationEvent, CollaborationStatus
# from .discord_migration_support import DiscordMigrationSupport, DiscordMigrationEvent, DiscordMigrationStatus
# from .full_support_integration import FullSupportIntegration, SupportCapability, SupportLevel
# from .performance_optimization_framework import PerformanceOptimizationFramework, OptimizationMetric, OptimizationLevel
# from .complete_infrastructure_integration import CompleteInfrastructureIntegration, InfrastructureComponent, InfrastructureStatus
# from .quality_assurance_framework import QualityAssuranceFramework, QualityGate, QualityMetric
# from .triple_bonus_recognition_system import TripleBonusRecognitionSystem, BonusType, BonusAchievement
# from .complete_portfolio_integration import CompletePortfolioIntegration, PortfolioPhase, PortfolioStatus
# from .project_completion_system import ProjectCompletionSystem, ProjectPhase, ProjectCompletionStatus
# from .triple_bonus_confirmation_system import TripleBonusConfirmationSystem, BonusConfirmationType, BonusConfirmationStatus
# from .kiss_principle_enforcement_system import KISSPrincipleEnforcementSystem, ComplexityLevel, ComplexityMetric
# from .v3_contract_execution_system import V3ContractExecutionSystem, ContractPriority, ContractStatus, V3Contract

__version__ = "1.0.0"
__author__ = "Agent-3 (Database Specialist)"

__all__ = [
    # Core models
    "VectorDatabaseConnection",
    "VectorRecord",
    "VectorMetadata",
    "VectorQuery",
    "VectorType",
    "VectorStatus",
    "VectorIndex",
    "VectorDatabaseError",
    "VectorDatabaseMetrics",
    # Core services
    "VectorDatabaseOrchestrator",
    "StatusIndexer",
    "VectorDatabaseIntegration",
    "VectorDatabaseMonitor",
    # Index models
    "IndexEntry",
    "IndexStats",
    "IndexStatus",
    "IndexType",
    # Monitoring models
    "Alert",
    "AlertLevel",
    "PerformanceMetric",
]
