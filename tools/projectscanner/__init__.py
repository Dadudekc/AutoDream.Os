"""
Enhanced Project Scanner Package
================================

Advanced project scanning and analysis tools with enhanced language analysis,
intelligent caching, agent categorization, and swarm intelligence features.

Components:
- enhanced_scanner: Main enhanced scanner with advanced features
- enhanced_analyzer: Advanced language analysis with tree-sitter support
- analyzers: Language-specific analyzers (legacy)
- workers: Multi-threaded processing workers
- reporters: Report generation and export (legacy)

Enhanced Features:
- Tree-sitter AST parsing for Python, Rust, JavaScript, TypeScript
- Advanced route detection for Flask, FastAPI, Express.js
- Agent categorization and maturity assessment
- Intelligent caching with file movement detection
- V2 compliance monitoring
- Automatic __init__.py generation
- Swarm intelligence analysis

Usage:
    from tools.projectscanner import EnhancedProjectScanner
    scanner = EnhancedProjectScanner(project_root=".")
    scanner.scan_project()
"""

from .enhanced_scanner import EnhancedProjectScanner
from .enhanced_analyzer import EnhancedLanguageAnalyzer, EnhancedCachingSystem, EnhancedReportGenerator
from .analyzers import LanguageAnalyzer
from .workers import BotWorker, MultibotManager, FileProcessor
from .reporters import ReportGenerator, ModularReportGenerator

# Legacy imports for backward compatibility
try:
    from .core import ProjectScanner
except ImportError:
    ProjectScanner = None

__all__ = [
    "EnhancedProjectScanner",
    "EnhancedLanguageAnalyzer", 
    "EnhancedCachingSystem",
    "EnhancedReportGenerator",
    "ProjectScanner",  # Legacy
    "LanguageAnalyzer",
    "BotWorker",
    "MultibotManager", 
    "FileProcessor",
    "ReportGenerator",
    "ModularReportGenerator"
]

__version__ = "3.0.0"
__author__ = "V2_SWARM Agent-8 (SSOT & System Integration Specialist)"
__description__ = "Enhanced V2 Compliant Project Scanner Package with Swarm Intelligence and Vector Database Integration"


