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

from .vector_database_models import (
    VectorDatabaseConnection,
    VectorRecord,
    VectorMetadata,
    VectorQuery,
    VectorType,
    VectorStatus,
    VectorIndex,
    VectorDatabaseError,
    VectorDatabaseMetrics
)

from .vector_database_orchestrator import VectorDatabaseOrchestrator
from .status_indexer import StatusIndexer, IndexEntry, IndexStats, IndexStatus, IndexType
from .vector_database_integration import VectorDatabaseIntegration
from .vector_database_monitoring import VectorDatabaseMonitor, Alert, AlertLevel, PerformanceMetric
from .architecture_integration import ArchitectureIntegration
from .record_time_migration import RecordTimeMigration
from .enhanced_collaboration import EnhancedCollaboration, CollaborationEvent, CollaborationStatus
from .discord_migration_support import DiscordMigrationSupport, DiscordMigrationEvent, DiscordMigrationStatus
from .full_support_integration import FullSupportIntegration, SupportCapability, SupportLevel
from .performance_optimization_framework import PerformanceOptimizationFramework, OptimizationMetric, OptimizationLevel
from .complete_infrastructure_integration import CompleteInfrastructureIntegration, InfrastructureComponent, InfrastructureStatus
from .quality_assurance_framework import QualityAssuranceFramework, QualityGate, QualityMetric
from .triple_bonus_recognition_system import TripleBonusRecognitionSystem, BonusType, BonusAchievement
from .complete_portfolio_integration import CompletePortfolioIntegration, PortfolioPhase, PortfolioStatus
from .project_completion_system import ProjectCompletionSystem, ProjectPhase, ProjectCompletionStatus
from .triple_bonus_confirmation_system import TripleBonusConfirmationSystem, BonusConfirmationType, BonusConfirmationStatus
from .kiss_principle_enforcement_system import KISSPrincipleEnforcementSystem, ComplexityLevel, ComplexityMetric
from .v3_contract_execution_system import V3ContractExecutionSystem, ContractPriority, ContractStatus, V3Contract

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
    "ArchitectureIntegration",
    "RecordTimeMigration",
    "EnhancedCollaboration",
    "DiscordMigrationSupport",
    "FullSupportIntegration",
    "PerformanceOptimizationFramework",
    "CompleteInfrastructureIntegration",
    "QualityAssuranceFramework",
    "TripleBonusRecognitionSystem",
    "CompletePortfolioIntegration",
    "ProjectCompletionSystem",
    "TripleBonusConfirmationSystem",
    "KISSPrincipleEnforcementSystem",
    "V3ContractExecutionSystem",
    
    # Index models
    "IndexEntry",
    "IndexStats", 
    "IndexStatus",
    "IndexType",
    
    # Monitoring models
    "Alert",
    "AlertLevel",
    "PerformanceMetric",
    
    # Collaboration models
    "CollaborationEvent",
    "CollaborationStatus",
    
    # Discord migration models
    "DiscordMigrationEvent",
    "DiscordMigrationStatus",
    
    # Full support models
    "SupportCapability",
    "SupportLevel",
    
    # Performance optimization models
    "OptimizationMetric",
    "OptimizationLevel",
    
    # Complete infrastructure models
    "InfrastructureComponent",
    "InfrastructureStatus",
    
    # Quality assurance models
    "QualityGate",
    "QualityMetric",
    
    # Triple bonus recognition models
    "BonusType",
    "BonusAchievement",
    
    # Complete portfolio integration models
    "PortfolioPhase",
    "PortfolioStatus",
    
    # Project completion system models
    "ProjectPhase",
    "ProjectCompletionStatus",
    
    # Triple bonus confirmation system models
    "BonusConfirmationType",
    "BonusConfirmationStatus",
    
    # KISS principle enforcement system models
    "ComplexityLevel",
    "ComplexityMetric",
    
    # V3 contract execution system models
    "ContractPriority",
    "ContractStatus",
    "V3Contract"
]
