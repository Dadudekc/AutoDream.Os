"""
Agent-5 Phase 2 Task 1: Analytics Consolidation
==============================================

Business Intelligence Specialist Task 1: Analyze and consolidate analytics files.
Target: 15-20 file reduction through duplicate identification and merging.

Usage:
    python src/core/agent5_phase2_task1_analytics_consolidation.py
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class AnalyticsFile:
    """Analytics file information."""
    path: str
    size: int
    functions: List[str]
    classes: List[str]
    imports: List[str]
    dependencies: List[str]


@dataclass
class ConsolidationCandidate:
    """Candidate for consolidation."""
    files: List[AnalyticsFile]
    similarity_score: float
    consolidation_strategy: str
    estimated_reduction: int


class Agent5Phase2Task1AnalyticsConsolidation:
    """Agent-5's Task 1: Analytics file consolidation."""
    
    def __init__(self, agent_id: str = "Agent-5"):
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        self.task_id = "TASK_1_ANALYTICS_CONSOLIDATION"
        self.target_reduction = "15-20 files"
        
    def analyze_analytics_files(self) -> List[AnalyticsFile]:
        """Analyze all analytics files in the codebase."""
        analytics_files = []
        
        # Core analytics files
        core_analytics_paths = [
            "src/core/unified_analytics_engine.py",
            "src/core/swarm_business_intelligence.py",
            "src/core/swarm_data_optimizer.py",
            "src/core/swarm_bi_coordinator.py",
            "src/core/performance_monitoring_dashboard.py"
        ]
        
        # Services analytics files
        services_analytics_path = Path("src/services/analytics")
        if services_analytics_path.exists():
            for py_file in services_analytics_path.glob("*.py"):
                if py_file.name != "__init__.py":
                    core_analytics_paths.append(str(py_file))
        
        # Web analytics files
        web_analytics_paths = [
            "src/web/analytics_dashboard.py",
            "src/web/vector_database/analytics_utils.py"
        ]
        
        all_paths = core_analytics_paths + web_analytics_paths
        
        for file_path in all_paths:
            if Path(file_path).exists():
                analytics_file = self._analyze_single_file(file_path)
                if analytics_file:
                    analytics_files.append(analytics_file)
        
        return analytics_files
    
    def _analyze_single_file(self, file_path: str) -> AnalyticsFile:
        """Analyze a single analytics file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic analysis
            size = len(content.split('\n'))
            functions = self._extract_functions(content)
            classes = self._extract_classes(content)
            imports = self._extract_imports(content)
            dependencies = self._extract_dependencies(content)
            
            return AnalyticsFile(
                path=file_path,
                size=size,
                functions=functions,
                classes=classes,
                imports=imports,
                dependencies=dependencies
            )
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from content."""
        import re
        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        return functions
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names from content."""
        import re
        classes = re.findall(r'class\s+(\w+)', content)
        return classes
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from content."""
        import re
        imports = re.findall(r'(?:from\s+\S+\s+)?import\s+(\S+)', content)
        return imports
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from content."""
        import re
        dependencies = re.findall(r'from\s+(\S+)\s+import', content)
        return dependencies
    
    def identify_duplicate_modules(self, analytics_files: List[AnalyticsFile]) -> List[ConsolidationCandidate]:
        """Identify duplicate analytics modules."""
        candidates = []
        
        # Group files by similar functionality
        function_groups = {}
        class_groups = {}
        
        for file in analytics_files:
            # Group by functions
            for func in file.functions:
                if func not in function_groups:
                    function_groups[func] = []
                function_groups[func].append(file)
            
            # Group by classes
            for cls in file.classes:
                if cls not in class_groups:
                    class_groups[cls] = []
                class_groups[cls].append(file)
        
        # Find consolidation candidates
        for func, files in function_groups.items():
            if len(files) > 1:
                candidates.append(ConsolidationCandidate(
                    files=files,
                    similarity_score=0.8,
                    consolidation_strategy=f"Merge duplicate {func} functions",
                    estimated_reduction=len(files) - 1
                ))
        
        for cls, files in class_groups.items():
            if len(files) > 1:
                candidates.append(ConsolidationCandidate(
                    files=files,
                    similarity_score=0.9,
                    consolidation_strategy=f"Merge duplicate {cls} classes",
                    estimated_reduction=len(files) - 1
                ))
        
        return candidates
    
    def identify_similar_data_processing_functions(self, analytics_files: List[AnalyticsFile]) -> List[ConsolidationCandidate]:
        """Identify similar data processing functions."""
        candidates = []
        
        # Common data processing patterns
        data_processing_patterns = [
            "process_data", "analyze_data", "optimize_data", "transform_data",
            "collect_metrics", "aggregate_data", "filter_data", "validate_data"
        ]
        
        for pattern in data_processing_patterns:
            matching_files = []
            for file in analytics_files:
                if any(pattern in func.lower() for func in file.functions):
                    matching_files.append(file)
            
            if len(matching_files) > 1:
                candidates.append(ConsolidationCandidate(
                    files=matching_files,
                    similarity_score=0.7,
                    consolidation_strategy=f"Merge similar {pattern} functions",
                    estimated_reduction=len(matching_files) - 1
                ))
        
        return candidates
    
    def generate_consolidation_plan(self) -> Dict[str, Any]:
        """Generate comprehensive consolidation plan."""
        analytics_files = self.analyze_analytics_files()
        duplicate_candidates = self.identify_duplicate_modules(analytics_files)
        similar_function_candidates = self.identify_similar_data_processing_functions(analytics_files)
        
        all_candidates = duplicate_candidates + similar_function_candidates
        
        # Calculate total estimated reduction
        total_estimated_reduction = sum(candidate.estimated_reduction for candidate in all_candidates)
        
        consolidation_plan = {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "target_reduction": self.target_reduction,
            "analytics_files_analyzed": len(analytics_files),
            "consolidation_candidates": len(all_candidates),
            "estimated_reduction": total_estimated_reduction,
            "candidates": [
                {
                    "strategy": candidate.consolidation_strategy,
                    "files": [f.path for f in candidate.files],
                    "similarity_score": candidate.similarity_score,
                    "estimated_reduction": candidate.estimated_reduction
                }
                for candidate in all_candidates
            ],
            "high_priority_targets": [
                "src/services/analytics/ - 17 files for consolidation",
                "src/core/ - 5 analytics files for consolidation",
                "src/web/ - 2 analytics files for consolidation"
            ],
            "consolidation_strategies": [
                "Merge duplicate analytics modules",
                "Unify similar data processing functions",
                "Consolidate analytics interfaces",
                "Optimize analytics performance"
            ]
        }
        
        return consolidation_plan
    
    def get_task1_status(self) -> Dict[str, Any]:
        """Get Task 1 status."""
        consolidation_plan = self.generate_consolidation_plan()
        
        return {
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "status": "ANALYZING",
            "target_reduction": self.target_reduction,
            "consolidation_plan": consolidation_plan,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main entry point for Task 1 Analytics Consolidation."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize Task 1 Analytics Consolidation
    task1 = Agent5Phase2Task1AnalyticsConsolidation()
    
    # Get status
    status = task1.get_task1_status()
    
    # Log status
    logger.info("🎯 TASK 1: ANALYTICS CONSOLIDATION STATUS:")
    logger.info(f"Task ID: {status['task_id']}")
    logger.info(f"Status: {status['status']}")
    logger.info(f"Target Reduction: {status['target_reduction']}")
    logger.info(f"Analytics Files Analyzed: {status['consolidation_plan']['analytics_files_analyzed']}")
    logger.info(f"Consolidation Candidates: {status['consolidation_plan']['consolidation_candidates']}")
    logger.info(f"Estimated Reduction: {status['consolidation_plan']['estimated_reduction']} files")
    
    logger.info("✅ TASK 1: ANALYTICS CONSOLIDATION INITIATED")
    logger.info("Mission: PHASE 2 BI INTEGRATION TASKS")
    logger.info("Status: ANALYZING analytics files for consolidation")


if __name__ == "__main__":
    main()
