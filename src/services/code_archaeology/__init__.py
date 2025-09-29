#!/usr/bin/env python3
"""
Code Archaeology Service Package
===============================

Comprehensive historical code analysis and technical debt mapping system.
V2 Compliant: ≤400 lines, focused archaeological functionality.

Author: Agent-2 (Architecture Specialist & Code Archaeologist)
License: MIT
"""

from .core.git_archaeologist import GitArchaeologist
from .core.pattern_discoverer import PatternDiscoverer
from .core.debt_mapper import DebtMapper
from .core.evolution_tracker import EvolutionTracker
from .analyzers.historical_analyzer import HistoricalAnalyzer
from .analyzers.dependency_tracer import DependencyTracer
from .analyzers.dead_code_detector import DeadCodeDetector
from .reporters.archaeological_reporter import ArchaeologicalReporter
from .reporters.debt_reporter import DebtReporter
from .integration.git_integration import GitIntegration

__version__ = "1.0.0"
__author__ = "Agent-2"

# Main service class that agents will use
class CodeArchaeologyService:
    """Main code archaeology service that agents can import and use."""
    
    def __init__(self):
        """Initialize the code archaeology service with all components."""
        self.git_archaeologist = GitArchaeologist()
        self.pattern_discoverer = PatternDiscoverer()
        self.debt_mapper = DebtMapper()
        self.evolution_tracker = EvolutionTracker()
        self.historical_analyzer = HistoricalAnalyzer()
        self.dependency_tracer = DependencyTracer()
        self.dead_code_detector = DeadCodeDetector()
        self.archaeological_reporter = ArchaeologicalReporter()
        self.debt_reporter = DebtReporter()
        self.git_integration = GitIntegration()
    
    def conduct_archaeological_dig(self, target_path: str, analysis_depth: str = "comprehensive") -> dict:
        """Main method that agents will call to conduct archaeological analysis."""
        try:
            # Initialize archaeological dig
            dig_session = self.git_archaeologist.initialize_dig(target_path)
            
            # Analyze historical evolution
            evolution_analysis = self.evolution_tracker.track_evolution(target_path)
            
            # Discover patterns
            pattern_discoveries = self.pattern_discoverer.discover_patterns(target_path)
            
            # Map technical debt
            debt_mapping = self.debt_mapper.map_technical_debt(target_path)
            
            # Trace dependencies
            dependency_analysis = self.dependency_tracer.trace_dependencies(target_path)
            
            # Detect dead code
            dead_code_findings = self.dead_code_detector.detect_dead_code(target_path)
            
            # Generate archaeological report
            archaeological_report = self.archaeological_reporter.generate_report({
                "dig_session": dig_session,
                "evolution_analysis": evolution_analysis,
                "pattern_discoveries": pattern_discoveries,
                "debt_mapping": debt_mapping,
                "dependency_analysis": dependency_analysis,
                "dead_code_findings": dead_code_findings
            })
            
            return {
                "status": "success",
                "archaeological_report": archaeological_report,
                "findings_summary": {
                    "evolution_stages": len(evolution_analysis.get("stages", [])),
                    "patterns_discovered": len(pattern_discoveries.get("patterns", [])),
                    "debt_items_mapped": len(debt_mapping.get("debt_items", [])),
                    "dead_code_fragments": len(dead_code_findings.get("dead_fragments", []))
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Convenience functions for agents
def conduct_code_archaeology(target_path: str, analysis_depth: str = "comprehensive") -> dict:
    """Convenience function for agents to conduct code archaeology."""
    service = CodeArchaeologyService()
    return service.conduct_archaeological_dig(target_path, analysis_depth)

def get_archaeology_tools() -> dict:
    """Return available archaeology tools for agent discovery."""
    return {
        "main_service": "CodeArchaeologyService",
        "core_tools": [
            "GitArchaeologist",
            "PatternDiscoverer", 
            "DebtMapper",
            "EvolutionTracker"
        ],
        "analyzer_tools": [
            "HistoricalAnalyzer",
            "DependencyTracer",
            "DeadCodeDetector"
        ],
        "reporter_tools": [
            "ArchaeologicalReporter",
            "DebtReporter"
        ],
        "integration_tools": [
            "GitIntegration"
        ],
        "convenience_functions": [
            "conduct_code_archaeology",
            "get_archaeology_tools"
        ]
    }
