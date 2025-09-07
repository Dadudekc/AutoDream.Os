"""
Results Management Package - Phase-2 V2 Compliance Refactoring
=============================================================

Specialized result processing components for better SRP compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from .base_results_manager import BaseResultsManager
from .validation_results_processor import ValidationResultsProcessor
from .analysis_results_processor import AnalysisResultsProcessor
from .integration_results_processor import IntegrationResultsProcessor
from .performance_results_processor import PerformanceResultsProcessor
from .general_results_processor import GeneralResultsProcessor
from .results_archive_manager import ResultsArchiveManager

__all__ = [
    "BaseResultsManager",
    "ValidationResultsProcessor",
    "AnalysisResultsProcessor", 
    "IntegrationResultsProcessor",
    "PerformanceResultsProcessor",
    "GeneralResultsProcessor",
    "ResultsArchiveManager",
]
