"""
Tool Registry
=============

Central registry for all Agent Toolbelt tools with dynamic import and caching.

V2 Compliance: <160 lines
Author: Agent-7 - Repository Cloning Specialist
"""

import importlib
import json
import logging
from pathlib import Path
from typing import Type

from .adapters.base_adapter import IToolAdapter
from .adapters.error_types import ToolNotFoundError

logger = logging.getLogger(__name__)


# Static tool registry mapping tool names to adapter classes
TOOL_REGISTRY: dict[str, tuple[str, str]] = {
    # Vector DB tools (module_path, class_name)
    "vector.context": ("tools_v2.categories.vector_tools", "TaskContextTool"),
    "vector.search": ("tools_v2.categories.vector_tools", "VectorSearchTool"),
    "vector.index": ("tools_v2.categories.vector_tools", "IndexWorkTool"),
    
    # Messaging tools
    "msg.send": ("tools_v2.categories.messaging_tools", "SendMessageTool"),
    "msg.broadcast": ("tools_v2.categories.messaging_tools", "BroadcastTool"),
    "msg.inbox": ("tools_v2.categories.messaging_tools", "InboxCheckTool"),
    
    # Analysis tools
    "analysis.scan": ("tools_v2.categories.analysis_tools", "ProjectScanTool"),
    "analysis.complexity": ("tools_v2.categories.analysis_tools", "ComplexityTool"),
    "analysis.duplicates": ("tools_v2.categories.analysis_tools", "DuplicationTool"),
    
    # V2 compliance tools
    "v2.check": ("tools_v2.categories.v2_tools", "V2CheckTool"),
    "v2.report": ("tools_v2.categories.v2_tools", "V2ReportTool"),
    
    # Agent operations
    "agent.status": ("tools_v2.categories.agent_ops_tools", "AgentStatusTool"),
    "agent.claim": ("tools_v2.categories.agent_ops_tools", "ClaimTaskTool"),
    
    # Testing tools
    "test.coverage": ("tools_v2.categories.testing_tools", "CoverageReportTool"),
    "test.mutation": ("tools_v2.categories.testing_tools", "MutationGateTool"),
    
    # Compliance tracking
    "comp.history": ("tools_v2.categories.compliance_tools", "ComplianceHistoryTool"),
    "comp.check": ("tools_v2.categories.compliance_tools", "PolicyCheckTool"),
    
    # Infrastructure tools (Agent-3 additions)
    "infra.orchestrator_scan": ("tools_v2.categories.infrastructure_tools", "OrchestratorScanTool"),
    "infra.file_lines": ("tools_v2.categories.infrastructure_tools", "FileLineCounterTool"),
    "infra.extract_planner": ("tools_v2.categories.infrastructure_tools", "ModuleExtractorPlannerTool"),
    "infra.roi_calc": ("tools_v2.categories.infrastructure_tools", "ROICalculatorTool"),
    
    # Discord tools (Agent-3 additions)
    "discord.health": ("tools_v2.categories.discord_tools", "DiscordBotHealthTool"),
    "discord.start": ("tools_v2.categories.discord_tools", "DiscordBotStartTool"),
    "discord.test": ("tools_v2.categories.discord_tools", "DiscordTestMessageTool"),
    
    # Onboarding
    "onboard.soft": ("tools_v2.categories.onboarding_tools", "SoftOnboardTool"),
    "onboard.hard": ("tools_v2.categories.onboarding_tools", "HardOnboardTool"),
    
    # Documentation
    "docs.search": ("tools_v2.categories.docs_tools", "DocsSearchTool"),
    "docs.export": ("tools_v2.categories.docs_tools", "DocsExportTool"),
    
    # Health monitoring
    "health.ping": ("tools_v2.categories.health_tools", "HealthPingTool"),
    "health.snapshot": ("tools_v2.categories.health_tools", "SnapshotTool"),
    
    # Memory Safety & Production Tools (NEW - Session 2025-10-13 Agent-5)
    "mem.leaks": ("tools_v2.categories.memory_safety_adapters", "MemoryLeakDetectorTool"),
    "mem.verify": ("tools_v2.categories.memory_safety_adapters", "FileVerificationTool"),
    "mem.scan": ("tools_v2.categories.memory_safety_adapters", "UnboundedScanTool"),
    "mem.imports": ("tools_v2.categories.memory_safety_adapters", "ImportValidatorTool"),
    "mem.handles": ("tools_v2.categories.memory_safety_adapters", "FileHandleCheckTool"),
    
    # 🧠 INTELLIGENT MISSION ADVISOR - THE MASTERPIECE (Agent-5)
    "advisor.recommend": ("tools_v2.categories.intelligent_mission_advisor_adapter", "MissionAdvisorTool"),
    "advisor.validate": ("tools_v2.categories.intelligent_mission_advisor_adapter", "OrderValidatorTool"),
    "advisor.swarm": ("tools_v2.categories.intelligent_mission_advisor_adapter", "SwarmAnalyzerTool"),
    "advisor.guide": ("tools_v2.categories.intelligent_mission_advisor_adapter", "RealtimeGuidanceTool"),
    
    # Message-Task integration (NEW - Session 2025-10-13)
    "msgtask.ingest": ("tools_v2.categories.message_task_tools", "MessageIngestTool"),
    "msgtask.parse": ("tools_v2.categories.message_task_tools", "TaskParserTool"),
    "msgtask.fingerprint": ("tools_v2.categories.message_task_tools", "TaskFingerprintTool"),
    
    # Session management tools (NEW - Agent-7 from thread learning)
    "session.cleanup": ("tools_v2.categories.session_tools", "SessionCleanupTool"),
    "session.passdown": ("tools_v2.categories.session_tools", "PassdownTool"),
    "agent.points": ("tools_v2.categories.session_tools", "PointsCalculatorTool"),
    
    # Workflow tools (NEW - Agent-7 from thread learning)
    "msg.cleanup": ("tools_v2.categories.workflow_tools", "InboxCleanupTool"),
    "mission.claim": ("tools_v2.categories.workflow_tools", "MissionClaimTool"),
    "workflow.roi": ("tools_v2.categories.workflow_tools", "ROICalculatorTool"),
    
    # MASTERPIECE: Real-time swarm consciousness (NEW - Agent-7)
    "swarm.pulse": ("tools_v2.categories.swarm_consciousness", "SwarmPulseTool"),
    
    # Democratic debate system (NEW - Agent-7, built from docs)
    "debate.start": ("tools_v2.categories.debate_tools", "DebateStartTool"),
    "debate.vote": ("tools_v2.categories.debate_tools", "DebateVoteTool"),
    "debate.status": ("tools_v2.categories.debate_tools", "DebateStatusTool"),
    "debate.notify": ("tools_v2.categories.debate_tools", "DebateNotifyTool"),
    
    # OSS contributions (NEW - Session 2025-10-13)
    "oss.clone": ("tools_v2.categories.oss_tools", "OSSCloneTool"),
    "oss.issues": ("tools_v2.categories.oss_tools", "OSSFetchIssuesTool"),
    "oss.import": ("tools_v2.categories.oss_tools", "OSSImportIssuesTool"),
    "oss.portfolio": ("tools_v2.categories.oss_tools", "OSSPortfolioTool"),
    "oss.status": ("tools_v2.categories.oss_tools", "OSSStatusTool"),
    
    # Swarm brain & notes (NEW - Session 2025-10-13)
    "brain.note": ("tools_v2.categories.swarm_brain_tools", "TakeNoteTool"),
    "brain.share": ("tools_v2.categories.swarm_brain_tools", "ShareLearningTool"),
    "brain.search": ("tools_v2.categories.swarm_brain_tools", "SearchKnowledgeTool"),
    "brain.session": ("tools_v2.categories.swarm_brain_tools", "LogSessionTool"),
    "brain.get": ("tools_v2.categories.swarm_brain_tools", "GetAgentNotesTool"),
    
    # Observability (NEW - Session 2025-10-13)
    "obs.metrics": ("tools_v2.categories.observability_tools", "MetricsSnapshotTool"),
    "obs.get": ("tools_v2.categories.observability_tools", "MetricsTool"),
    "obs.health": ("tools_v2.categories.observability_tools", "SystemHealthTool"),
    "obs.slo": ("tools_v2.categories.observability_tools", "SLOCheckTool"),
    
    # Validation (NEW - Session 2025-10-13)
    "val.smoke": ("tools_v2.categories.validation_tools", "SmokeTestTool"),
    "val.flags": ("tools_v2.categories.validation_tools", "FeatureFlagTool"),
    "val.rollback": ("tools_v2.categories.validation_tools", "RollbackTool"),
    "val.report": ("tools_v2.categories.validation_tools", "ValidationReportTool"),
    
    # Captain Operations (NEW - Session 2025-10-13 Critical Tools)
    "captain.status_check": ("tools_v2.categories.captain_tools", "StatusCheckTool"),
    "captain.git_verify": ("tools_v2.categories.captain_tools", "GitVerifyTool"),
    "captain.calc_points": ("tools_v2.categories.captain_tools", "PointsCalculatorTool"),
    "captain.assign_mission": ("tools_v2.categories.captain_tools", "MissionAssignTool"),
    "captain.deliver_gas": ("tools_v2.categories.captain_tools", "GasDeliveryTool"),
    "captain.update_leaderboard": ("tools_v2.categories.captain_tools", "LeaderboardUpdateTool"),
    "captain.verify_work": ("tools_v2.categories.captain_tools", "WorkVerifyTool"),
    "captain.cycle_report": ("tools_v2.categories.captain_tools", "CycleReportTool"),
    "captain.markov_optimize": ("tools_v2.categories.captain_tools", "MarkovOptimizerTool"),
    "captain.integrity_check": ("tools_v2.categories.captain_tools", "IntegrityCheckTool"),
    
    # Integration Tools (NEW - Session 2025-10-14 Agent-1)
    "integration.find-ssot-violations": ("tools_v2.categories.integration_tools", "FindSSOTViolationsAdapter"),
    "integration.find-duplicates": ("tools_v2.categories.integration_tools", "FindDuplicateFunctionalityAdapter"),
    "integration.find-opportunities": ("tools_v2.categories.integration_tools", "FindIntegrationOpportunitiesAdapter"),
    "integration.check-imports": ("tools_v2.categories.integration_tools", "CheckImportDependenciesAdapter"),
    
    # Coordination Tools (NEW - Session 2025-10-14 Agent-1 - Pattern #5)
    "coord.find-expert": ("tools_v2.categories.coordination_tools", "FindDomainExpertAdapter"),
    "coord.request-review": ("tools_v2.categories.coordination_tools", "RequestExpertReviewAdapter"),
    "coord.check-patterns": ("tools_v2.categories.coordination_tools", "CheckCoordinationPatternsAdapter"),
    
    # Config Tools (NEW - Session 2025-10-14 Agent-1 - Config SSOT)
    "config.validate-ssot": ("tools_v2.categories.config_tools", "ValidateConfigSSOTAdapter"),
    "config.list-sources": ("tools_v2.categories.config_tools", "ListConfigSourcesAdapter"),
    "config.check-imports": ("tools_v2.categories.config_tools", "CheckConfigImportsAdapter"),
    # Refactoring Tools (NEW - Session 2025-10-14 Agent-1 Lean Excellence Mission)
    "refactor.check_file_size": ("tools_v2.categories.refactoring_tools", "FileSizeCheckTool"),
    "refactor.auto_extract": ("tools_v2.categories.refactoring_tools", "AutoExtractTool"),
    "refactor.lint_fix": ("tools_v2.categories.refactoring_tools", "LintFixTool"),
    # Test Generation Tools (NEW - Session 2025-10-14 Agent-1 Testing Pyramid Mission)
    "test.pyramid_check": ("tools_v2.categories.test_generation_tools", "TestPyramidAnalyzerTool"),
    "test.generate_template": ("tools_v2.categories.test_generation_tools", "TestFileGeneratorTool"),
    "test.coverage_pyramid_report": (
        "tools_v2.categories.test_generation_tools",
        "CoveragePyramidReportTool",
    ),
    # Import Fix Tools (NEW - Session 2025-10-14 Agent-1 Refactoring Support)
    "refactor.validate_imports": ("tools_v2.categories.import_fix_tools", "ImportValidatorTool"),
    "refactor.extract_module": ("tools_v2.categories.import_fix_tools", "ModuleExtractorTool"),
    "refactor.quick_line_count": ("tools_v2.categories.import_fix_tools", "QuickLineCountTool"),
}


class ToolRegistry:
    """Central registry for tool resolution and caching."""
    
    def __init__(self):
        """Initialize tool registry with caching."""
        self._cache: dict[str, Type[IToolAdapter]] = {}
        self.logger = logging.getLogger(__name__)
    
    def resolve(self, tool_name: str) -> Type[IToolAdapter]:
        """
        Resolve tool name to adapter class with caching.
        
        Args:
            tool_name: Tool name (e.g., "vector.context")
            
        Returns:
            Tool adapter class
            
        Raises:
            ToolNotFoundError: If tool is not registered
        """
        # Check cache first
        if tool_name in self._cache:
            return self._cache[tool_name]
        
        # Look up in registry
        if tool_name not in TOOL_REGISTRY:
            available = ", ".join(TOOL_REGISTRY.keys())
            raise ToolNotFoundError(
                f"Tool '{tool_name}' not found. Available: {available}",
                tool_name=tool_name
            )
        
        module_path, class_name = TOOL_REGISTRY[tool_name]
        
        try:
            # Dynamic import
            module = importlib.import_module(module_path)
            adapter_class = getattr(module, class_name)
            
            # Validate adapter implements interface
            if not issubclass(adapter_class, IToolAdapter):
                raise ToolNotFoundError(
                    f"Tool '{tool_name}' adapter does not implement IToolAdapter",
                    tool_name=tool_name
                )
            
            # Cache and return
            self._cache[tool_name] = adapter_class
            self.logger.debug(f"Resolved and cached tool: {tool_name}")
            return adapter_class
            
        except (ImportError, AttributeError) as e:
            raise ToolNotFoundError(
                f"Failed to import tool '{tool_name}': {e}",
                tool_name=tool_name
            )
    
    def list_tools(self) -> list[str]:
        """
        List all available tools.
        
        Returns:
            List of tool names
        """
        return sorted(TOOL_REGISTRY.keys())
    
    def list_by_category(self) -> dict[str, list[str]]:
        """
        List tools grouped by category.
        
        Returns:
            Dictionary mapping category to tool names
        """
        categories: dict[str, list[str]] = {}
        
        for tool_name in TOOL_REGISTRY.keys():
            category = tool_name.split('.')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(tool_name)
        
        return categories
    
    def export_lock(self, output_path: str = "tools_v2/tool_registry.lock.json") -> None:
        """
        Export registry to JSON lock file for versioning.
        
        Args:
            output_path: Path to output JSON file
        """
        lock_data = {
            "version": "2.0.0",
            "tools": TOOL_REGISTRY,
            "count": len(TOOL_REGISTRY)
        }
        
        Path(output_path).write_text(json.dumps(lock_data, indent=2))
        self.logger.info(f"Exported tool registry to {output_path}")


# Singleton instance
_registry_instance: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    """
    Get singleton tool registry instance.
    
    Returns:
        Tool registry instance
    """
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ToolRegistry()
    return _registry_instance

