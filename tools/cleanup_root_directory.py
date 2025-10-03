#!/usr/bin/env python3
"""
Root Directory Cleanup Script - V2 Compliant
============================================

Automated cleanup of root directory files.
Removes duplicates, temporary files, and organizes remaining files.

Author: Agent-4 (Captain)
License: MIT
"""

import os
import shutil
from pathlib import Path


def cleanup_root_directory():
    """Clean up root directory files."""
    root = Path(".")

    # Files to delete (duplicates, temporary, old reports)
    files_to_delete = [
        # Old analysis files
        "agent_analysis.json",
        "architecture_overview.json",
        "complexity_analysis.json",
        "dependency_analysis.json",
        "file_type_analysis.json",
        "module_analysis.json",
        "project_analysis.json",
        "project_analysis_enhanced.json",
        "project_registry.json",
        # Compliance duplicates
        "compliance_report.json",
        "compliance_summary.json",
        "current_compliance.json",
        "violations.json",
        "current_violations.json",
        "latest_compliance.json",
        "updated_compliance.json",
        "final_compliance.json",
        "final_compliance_check.json",
        # Temporary files
        "all_devlogs_*.json",
        "complete_devlog_*.json",
        "all_python_files.csv",
        "chatgpt_project_context.json",
        "clone_progress_report.json",
        "deployment_manifest.json",
        "import_map.json",
        "refactor_plan.json",
        "refactor_suggestions.json",
        # Status files
        "current_*.txt",
        "current_*.json",
        "remaining_violations.txt",
        "refactoring_status.txt",
        "quality_*.txt",
        "compliance_violations_*.txt",
        "consolidation_quality_check.txt",
        "final_*.txt",
        "cycle_*.json",
        "cycle_*.txt",
        "phase1_*.txt",
        "phase3_*.md",
        # Reports
        "testing_validation_report.json",
        "comprehensive_test_report.json",
        "deployment_dashboard_report.json",
        "lightweight_dashboard_report.json",
        "ide_integration_test_report.md",
        "PORTFOLIO_DEPLOYMENT_SUCCESS_REPORT.md",
        "MISSION_ACCELERATION_DASHBOARD.md",
        "MISSION_STATUS_SYNCHRONIZATION_REPORT.md",
        # Old mission files
        "autonomous_workflow_integration_summary.md",
        "captain_progress_data",
        "CAPTAIN_FINAL_INTEGRATION_PLAN.md",
        "CAPTAIN_MEMORY_LEAK_REMEDIATION_PLAN.md",
        "CAPTAIN_TASK_ASSIGNMENTS.md",
        "CAPTAIN_THEA_*.md",
        # Integration summaries
        "quality_gates_integration_summary.md",
        "workflow_static_analysis_tools_integration_summary.md",
        "specialized_role_cli_tools_integration_summary.md",
        "ONBOARDING_INTEGRATION_ANALYSIS.md",
        # Other temporary files
        "pipeline_status_update.md",
        "integration_*.txt",
        "metric_refresh_results.json",
        "database_content_hashes.json",
        "ssot_*.json",
        "workflow_*.json",
        "database_cleanup_final_report.md",
        "full_project_scan.txt",
        "project_scan.txt",
        # Backup files
        "AGENTS.md.backup",
        "COMPREHENSIVE_FILE_ANALYSIS.md",
        "SYSTEMATIC_FILE_ANALYSIS.md",
        "CORE_FILES_ANALYSIS.md",
        # Old mission reports
        "AGENT_PASSDOWN_CYCLES_1-5.md",
        "AGENT5_COORDINATION_RESPONSE.md",
        "AGENT7_MISSION_COMPLETION_REPORT.md",
        "AGENT8_FILE_REDUCTION_MISSION_REPORT.md",
        "CAPTAIN_COORDINATION_STATUS.md",
        "CAPTAIN_CYCLE_COMPLETION_REPORT.md",
        # Duplicate consolidation checks
        "final_consolidation_check*.txt",
        # Other cleanup
        "response_detector.py",
        "watchdog.py",
        "report.py",
        "get_real_tesla_price.py",
        "switch_agent_mode.py",
        "restart_mcp_servers.ps1",
        "setup_discord_commander.py",
        "simple_discord_bot.py",
        "v2_swarm_deployment_script.py",
        "V3_DIRECTIVES_DEPLOYMENT_SYSTEM.py",
        "V3_SECURITY_CLEANUP_FIXED.py",
        "V3_VALIDATION_REPORT.json",
        "reduce_md_files.py",
        "delete_static_documentation.py",
        "static_documentation_deleter_core.py",
        "complete_onboarding_core.py",
        "combined_export_core.py",
        "cleanup_stale_database_core.py",
        "cleanup_stale_database_records.py",
        "update_captain_cycle_core.py",
        "real_agent_coordination_core.py",
        "real_agent_coordination.py",
        "swarm_orchestrator_core.py",
        "swarm_orchestrator.py",
        "quality_coordination_response.py",
        "check_v2_compliance.py",
        "check_agent5_inbox.py",
        "ingest_all_onboarding_docs.py",
        "ingest_captain_docs.py",
        "ingest_existing_documentation.py",
        # Database files
        "predictions.db",
        "test_predictions.db",
        # Configuration duplicates
        "discord_commander_config.py",
        "discord_commander_core.py",
        "discord_commander_setup_core.py",
        "discord_commander.py",
        "cursor_agent_coords.json",
        # Core files that should be in src/
        "agent_mode_switcher_core.py",
        "captain_cycle_core.py",
        "captain_cycle_improvement_prompt.py",
        "captain_docs_core.py",
        "quality_gates_core.py",
        "quality_gates.py",
        # Documentation that should be in docs/
        "AGENT_DIRECTORY_COMPLETION_PLAN.md",
        "AGENT_DIRECTORY_IMPLEMENTATION_COMPLETE.md",
        "AGENT_ONBOARDING_CONTEXT_PACKAGE.md",
        "AGENT_ONBOARDING_TASK_ASSIGNMENT_COMPLETE.md",
        "AGENT_USABILITY_REPORT.md",
        "AGENTS_OVERVIEW.md",
        "ANTI_AI_SLOP_PROTOCOL.md",
        "ANTI_SLOP_PROTOCOL.md",
        "CUE_SYSTEM_PROTOCOL.md",
        "DATABASE_SYSTEMS.md",
        "DEVELOPMENT_GUIDELINES.md",
        "DEVLOG_ANALYTICS_SYSTEM_README.md",
        "GENERAL_CYCLE.md",
        "IMPORT_REFERENCE.md",
        "MD_FILE_REDUCTION_PLAN.md",
        "NAMING_STANDARDS.md",
        "PROJECT_ANALYSIS_REPORT.md",
        "QUALITY_COMPLIANCE.md",
        "README.md",
        "REPOSITORY_DEPLOYMENT_STRATEGY.md",
        "ROOT_DIRECTORY_CLEANUP_PLAN.md",
        "SECURITY_GUIDELINES.md",
        "STATIC_ANALYSIS_SETUP.md",
        "SWARM_COORDINATION.md",
        "TOOL_INTEGRATION.md",
        "VECTOR_DATABASE_INTEGRATION_GUIDE.md",
        "VECTOR_DATABASE_INTEGRATION_PLAN.md",
        "VECTOR_DATABASE_INTEGRATION_SUMMARY.md",
        "VECTOR_INTEGRATION_STATUS_UPDATE.md",
        "CHANGELOG.md",
        # Integration reports
        "finance_roles_integration_summary.md",
        "quality_focus_team_report.txt",
        "integration_monitoring_update.txt",
        "integration_quality_report.txt",
        # Other files
        "complete_devlog_export_20250921_201707.json",
        "thea_conversations.json",
        "thea_cookies.json",
        "thea_manual_login.py",
        "docker-compose.yml",
        "Dockerfile",
        "Doxyfile",
        "Makefile",
        "pytest.ini",
        "importlinter.ini",
        "requirements-security.txt",
        "requirements-test.txt",
        "requirements-testing.txt",
        "env.example",
        # Directories that should be cleaned up
        "htmlcov",
        "logs",
        "runtime",
        "sqlite_sessions",
        "json_sessions",
        "demo_sessions",
        "standalone_devlogs",
        "documentation_backup",
        "documentation_reports",
        "archaeology_reports",
        "financial_reports",
        "integration_reports",
        "research_reports",
        "security_reports",
        "strategy_reports",
        "risk_reports",
        "efficiency_monitoring",
        "unified_status",
        "content_registry",
        "memory",
        "migration_system",
        "multi_agent_tools",
        "operational_dashboard",
        "swarm_coordination",
        "thea_auth",
        "thea_communication",
        "thea_responses",
        "web_dashboard",
        "web_interface",
        "workflows",
        "frontend",
        "infrastructure",
        "k8s",
        "ml_deployments",
        "ml_models",
        "ml_training",
        "social",
        "templates",
        "vector_database",
        "tsla_forecast_app",
    ]

    deleted_count = 0
    moved_count = 0

    print("🧹 Starting root directory cleanup...")

    # Create necessary directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    os.makedirs("tools", exist_ok=True)

    # Delete files
    for file_pattern in files_to_delete:
        if "*" in file_pattern:
            # Handle wildcard patterns
            import glob

            for file_path in glob.glob(file_pattern):
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                        print(f"  🗑️  Deleted: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        deleted_count += 1
                        print(f"  🗑️  Deleted directory: {file_path}")
        else:
            # Handle specific files
            if os.path.exists(file_pattern):
                if os.path.isfile(file_pattern):
                    os.remove(file_pattern)
                    deleted_count += 1
                    print(f"  🗑️  Deleted: {file_pattern}")
                elif os.path.isdir(file_pattern):
                    shutil.rmtree(file_pattern)
                    deleted_count += 1
                    print(f"  🗑️  Deleted directory: {file_pattern}")

    # Move remaining files to appropriate directories
    files_to_move = {"reports": ["*.json", "*.txt", "*.md"], "docs": ["*.md"], "tools": ["*.py"]}

    for target_dir, patterns in files_to_move.items():
        for pattern in patterns:
            import glob

            for file_path in glob.glob(pattern):
                if (
                    os.path.isfile(file_path)
                    and not file_path.startswith("src/")
                    and not file_path.startswith("docs/")
                    and not file_path.startswith("tools/")
                ):
                    target_path = os.path.join(target_dir, os.path.basename(file_path))
                    if not os.path.exists(target_path):
                        shutil.move(file_path, target_path)
                        moved_count += 1
                        print(f"  📁  Moved: {file_path} -> {target_path}")

    print("\n✅ Cleanup complete!")
    print(f"  🗑️  Deleted: {deleted_count} files/directories")
    print(f"  📁  Moved: {moved_count} files")

    # Count remaining files
    remaining_files = [f for f in os.listdir(".") if os.path.isfile(f)]
    print(f"  📊  Remaining files in root: {len(remaining_files)}")

    return deleted_count, moved_count


if __name__ == "__main__":
    cleanup_root_directory()
