"""
CLI Command Handlers Module

Extracted command handlers for the testing framework CLI,
following Single Responsibility Principle.
"""

from .run_handler import RunCommandHandler
from .report_handler import ReportCommandHandler
from .status_handler import StatusCommandHandler
from .register_handler import RegisterCommandHandler
from .suite_handler import SuiteCommandHandler
from .results_handler import ResultsCommandHandler

__all__ = [
    'RunCommandHandler',
    'ReportCommandHandler', 
    'StatusCommandHandler',
    'RegisterCommandHandler',
    'SuiteCommandHandler',
    'ResultsCommandHandler'
]

