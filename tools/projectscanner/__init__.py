"""
Project Scanner Package
======================

Modular project scanning and analysis tools for the Agent Cellphone V2 project.

Components:
- core: Core scanning functionality
- analyzers: Language-specific analyzers
- workers: Multi-threaded processing workers
- reporters: Report generation and export
- cli: Command-line interface

Usage:
    from tools.projectscanner import ProjectScanner
    scanner = ProjectScanner(project_root=".")
    scanner.scan_project()
"""

from .core import ProjectScanner
from .analyzers import LanguageAnalyzer
from .workers import BotWorker, MultibotManager, FileProcessor
from .reporters import ReportGenerator, ModularReportGenerator
from .cli import main

__all__ = [
    "ProjectScanner",
    "LanguageAnalyzer",
    "BotWorker",
    "MultibotManager", 
    "FileProcessor",
    "ReportGenerator",
    "ModularReportGenerator",
    "main"
]

__version__ = "2.0.0"
__author__ = "V2_SWARM Agent-4 (Captain)"
__description__ = "V2 Compliant Project Scanner Package"


