"""
Agent-5 Phase 2 Task 2: Performance Monitoring Integration
========================================================

Business Intelligence Specialist Task 2: Integrate performance monitoring systems.
Target: 10-15 file reduction through monitoring utilities consolidation.

Usage:
    python src/core/agent5_phase2_task2_performance_monitoring.py
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class MonitoringFile:
    """Performance monitoring file information."""
    path: str
    size: int
    monitoring_functions: List[str]
    dashboard_components: List[str]
    metrics_collected: List[str]
    monitoring_type: str


@dataclass
class MonitoringConsolidationCandidate:
    """Candidate for monitoring consolidation."""
    files: List[MonitoringFile]
    consolidation_type: str
    similarity_score: float
    estimated_reduction: int
    consolidation_strategy: str


class Agent5Phase2Task2PerformanceMonitoring:
    """Agent-5's Task 2: Performance monitoring integration."""
    
    def __init__(self, agent_id: str = "Agent-5"):
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        self.task_id = "TASK_2_PERFORMANCE_MONITORING"
        self.target_reduction = "10-15 files"
        
    def analyze_monitoring_files(self) -> List[MonitoringFile]:
        """Analyze all performance monitoring files in the codebase."""
        monitoring_files = []
        
        # Core monitoring files
        core_monitoring_paths = [
            "src/core/performance_monitoring_dashboard.py",
            "src/core/swarm_performance_monitor.py",
            "src/core/progress_monitoring_dashboard.py",
            "src/core/performance/performance_orchestrator.py",
            "src/core/performance/performance_metrics_collector.py"
        ]
        
        # Web monitoring files
        web_monitoring_paths = [
            "src/web/simple_monitoring_dashboard.py",
            "src/web/messaging_performance_dashboard.py",
            "src/web/analytics_dashboard.py",
            "src/web/swarm_monitoring_core.py",
            "src/web/swarm_monitoring_ui.py"
        ]
        
        # Services monitoring files
        services_monitoring_paths = [
            "src/services/analytics/performance_dashboard.py",
            "src/services/analytics/analytics_performance_optimizer.py",
            "src/services/analytics/bi_dashboard_service.py"
        ]
        
        # Infrastructure monitoring files
        infrastructure_monitoring_paths = [
            "src/infrastructure/monitoring/infrastructure_monitoring_integration.py",
            "src/infrastructure/monitoring/components/performance_metrics.py",
            "src/infrastructure/monitoring/components/monitoring_components.py"
        ]
        
        all_paths = (core_monitoring_paths + web_monitoring_paths + 
                    services_monitoring_paths + infrastructure_monitoring_paths)
        
        for file_path in all_paths:
            if Path(file_path).exists():
                monitoring_file = self._analyze_monitoring_file(file_path)
                if monitoring_file:
                    monitoring_files.append(monitoring_file)
        
        return monitoring_files
    
    def _analyze_monitoring_file(self, file_path: str) -> MonitoringFile:
        """Analyze a single monitoring file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic analysis
            size = len(content.split('\n'))
            monitoring_functions = self._extract_monitoring_functions(content)
            dashboard_components = self._extract_dashboard_components(content)
            metrics_collected = self._extract_metrics_collected(content)
            monitoring_type = self._determine_monitoring_type(file_path, content)
            
            return MonitoringFile(
                path=file_path,
                size=size,
                monitoring_functions=monitoring_functions,
                dashboard_components=dashboard_components,
                metrics_collected=metrics_collected,
                monitoring_type=monitoring_type
            )
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def _extract_monitoring_functions(self, content: str) -> List[str]:
        """Extract monitoring function names from content."""
        import re
        monitoring_patterns = [
            r'def\s+(monitor_\w+)\s*\(',
            r'def\s+(collect_\w+)\s*\(',
            r'def\s+(track_\w+)\s*\(',
            r'def\s+(measure_\w+)\s*\(',
            r'def\s+(analyze_\w+)\s*\(',
            r'def\s+(report_\w+)\s*\('
        ]
        
        functions = []
        for pattern in monitoring_patterns:
            matches = re.findall(pattern, content)
            functions.extend(matches)
        
        return functions
    
    def _extract_dashboard_components(self, content: str) -> List[str]:
        """Extract dashboard component names from content."""
        import re
        dashboard_patterns = [
            r'class\s+(\w*[Dd]ashboard\w*)\s*:',
            r'class\s+(\w*[Mm]onitor\w*)\s*:',
            r'class\s+(\w*[Mm]etrics\w*)\s*:',
            r'def\s+(render_\w+)\s*\(',
            r'def\s+(display_\w+)\s*\(',
            r'def\s+(show_\w+)\s*\('
        ]
        
        components = []
        for pattern in dashboard_patterns:
            matches = re.findall(pattern, content)
            components.extend(matches)
        
        return components
    
    def _extract_metrics_collected(self, content: str) -> List[str]:
        """Extract metrics collected from content."""
        import re
        metrics_patterns = [
            r'(\w*[Mm]etrics?\w*)',
            r'(\w*[Pp]erformance\w*)',
            r'(\w*[Ss]tats?\w*)',
            r'(\w*[Dd]ata\w*)',
            r'(\w*[Ii]nfo\w*)'
        ]
        
        metrics = []
        for pattern in metrics_patterns:
            matches = re.findall(pattern, content)
            metrics.extend(matches)
        
        # Remove duplicates and filter
        unique_metrics = list(set(metrics))
        return [m for m in unique_metrics if len(m) > 3]
    
    def _determine_monitoring_type(self, file_path: str, content: str) -> str:
        """Determine the type of monitoring based on file path and content."""
        if 'performance' in file_path.lower():
            return 'performance'
        elif 'dashboard' in file_path.lower():
            return 'dashboard'
        elif 'metrics' in file_path.lower():
            return 'metrics'
        elif 'swarm' in file_path.lower():
            return 'swarm'
        elif 'analytics' in file_path.lower():
            return 'analytics'
        else:
            return 'general'
    
    def identify_monitoring_utilities_consolidation(self, monitoring_files: List[MonitoringFile]) -> List[MonitoringConsolidationCandidate]:
        """Identify monitoring utilities consolidation opportunities."""
        candidates = []
        
        # Group by monitoring type
        type_groups = {}
        for file in monitoring_files:
            if file.monitoring_type not in type_groups:
                type_groups[file.monitoring_type] = []
            type_groups[file.monitoring_type].append(file)
        
        # Create consolidation candidates for each type
        for monitoring_type, files in type_groups.items():
            if len(files) > 1:
                candidates.append(MonitoringConsolidationCandidate(
                    files=files,
                    consolidation_type=f"{monitoring_type}_monitoring",
                    similarity_score=0.8,
                    estimated_reduction=len(files) - 1,
                    consolidation_strategy=f"Merge {monitoring_type} monitoring utilities"
                ))
        
        return candidates
    
    def identify_dashboard_components_consolidation(self, monitoring_files: List[MonitoringFile]) -> List[MonitoringConsolidationCandidate]:
        """Identify dashboard components consolidation opportunities."""
        candidates = []
        
        # Group by dashboard components
        component_groups = {}
        for file in monitoring_files:
            for component in file.dashboard_components:
                if component not in component_groups:
                    component_groups[component] = []
                component_groups[component].append(file)
        
        # Create consolidation candidates for duplicate components
        for component, files in component_groups.items():
            if len(files) > 1:
                candidates.append(MonitoringConsolidationCandidate(
                    files=files,
                    consolidation_type=f"dashboard_{component}",
                    similarity_score=0.9,
                    estimated_reduction=len(files) - 1,
                    consolidation_strategy=f"Merge duplicate {component} dashboard components"
                ))
        
        return candidates
    
    def identify_metrics_collection_consolidation(self, monitoring_files: List[MonitoringFile]) -> List[MonitoringConsolidationCandidate]:
        """Identify metrics collection consolidation opportunities."""
        candidates = []
        
        # Group by similar metrics
        metrics_groups = {}
        for file in monitoring_files:
            for metric in file.metrics_collected:
                if metric not in metrics_groups:
                    metrics_groups[metric] = []
                metrics_groups[metric].append(file)
        
        # Create consolidation candidates for duplicate metrics
        for metric, files in metrics_groups.items():
            if len(files) > 1:
                candidates.append(MonitoringConsolidationCandidate(
                    files=files,
                    consolidation_type=f"metrics_{metric}",
                    similarity_score=0.7,
                    estimated_reduction=len(files) - 1,
                    consolidation_strategy=f"Merge duplicate {metric} metrics collection"
                ))
        
        return candidates
    
    def generate_monitoring_consolidation_plan(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring consolidation plan."""
        monitoring_files = self.analyze_monitoring_files()
        utilities_candidates = self.identify_monitoring_utilities_consolidation(monitoring_files)
        dashboard_candidates = self.identify_dashboard_components_consolidation(monitoring_files)
        metrics_candidates = self.identify_metrics_collection_consolidation(monitoring_files)
        
        all_candidates = utilities_candidates + dashboard_candidates + metrics_candidates
        
        # Calculate total estimated reduction
        total_estimated_reduction = sum(candidate.estimated_reduction for candidate in all_candidates)
        
        consolidation_plan = {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "target_reduction": self.target_reduction,
            "monitoring_files_analyzed": len(monitoring_files),
            "consolidation_candidates": len(all_candidates),
            "estimated_reduction": total_estimated_reduction,
            "candidates": [
                {
                    "type": candidate.consolidation_type,
                    "strategy": candidate.consolidation_strategy,
                    "files": [f.path for f in candidate.files],
                    "similarity_score": candidate.similarity_score,
                    "estimated_reduction": candidate.estimated_reduction
                }
                for candidate in all_candidates
            ],
            "high_priority_targets": [
                "src/core/performance/ - 5 performance monitoring files",
                "src/web/ - 5 monitoring dashboard files",
                "src/services/analytics/ - 3 analytics monitoring files",
                "src/infrastructure/monitoring/ - 3 infrastructure monitoring files"
            ],
            "consolidation_strategies": [
                "Merge monitoring utilities by type",
                "Consolidate dashboard components",
                "Unify metrics collection systems",
                "Optimize monitoring performance"
            ]
        }
        
        return consolidation_plan
    
    def get_task2_status(self) -> Dict[str, Any]:
        """Get Task 2 status."""
        consolidation_plan = self.generate_monitoring_consolidation_plan()
        
        return {
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "status": "ANALYZING",
            "target_reduction": self.target_reduction,
            "consolidation_plan": consolidation_plan,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main entry point for Task 2 Performance Monitoring Integration."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize Task 2 Performance Monitoring Integration
    task2 = Agent5Phase2Task2PerformanceMonitoring()
    
    # Get status
    status = task2.get_task2_status()
    
    # Log status
    logger.info("🎯 TASK 2: PERFORMANCE MONITORING INTEGRATION STATUS:")
    logger.info(f"Task ID: {status['task_id']}")
    logger.info(f"Status: {status['status']}")
    logger.info(f"Target Reduction: {status['target_reduction']}")
    logger.info(f"Monitoring Files Analyzed: {status['consolidation_plan']['monitoring_files_analyzed']}")
    logger.info(f"Consolidation Candidates: {status['consolidation_plan']['consolidation_candidates']}")
    logger.info(f"Estimated Reduction: {status['consolidation_plan']['estimated_reduction']} files")
    
    logger.info("✅ TASK 2: PERFORMANCE MONITORING INTEGRATION INITIATED")
    logger.info("Mission: PHASE 2 BI INTEGRATION TASKS")
    logger.info("Status: ANALYZING performance monitoring files for consolidation")


if __name__ == "__main__":
    main()
