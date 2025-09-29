#!/usr/bin/env python3
"""
Project Scanner Connector
=========================

Integration with project scanner results.
V2 Compliance: ≤400 lines, focused scanner integration.
"""

import logging
from typing import Any

from ..ingest import Ingestor

logger = logging.getLogger(__name__)


def ingest_scan(result: dict[str, Any], project: str, agent_id: str = "Agent-2"):
    """
    Ingest project scanner results into the swarm brain.

    Args:
        result: Scanner result dictionary
        project: Project identifier
        agent_id: Agent performing the scan

    Example result structure:
    {
      "compliance": {"v2_pass": 97.6, "violations": [{"file":"x.py","rule":"len>300"}]},
      "refactoring": [{"pattern":"split-mod","files":["x.py"]}],
      "summary": "V2 97.6%, 8 violations",
      "files_analyzed": 603,
      "total_lines": 125000
    }
    """
    try:
        ingestor = Ingestor()

        # Extract key information
        compliance_data = result.get("compliance", {})
        v2_pass_rate = compliance_data.get("v2_pass", 0.0)
        violations = compliance_data.get("violations", [])

        refactoring_suggestions = result.get("refactoring", [])
        files_analyzed = result.get("files_analyzed", 0)
        total_lines = result.get("total_lines", 0)

        # Create context for the action
        context = {
            "v2_pass_rate": v2_pass_rate,
            "violations_count": len(violations),
            "files_analyzed": files_analyzed,
            "total_lines": total_lines,
            "refactoring_suggestions": len(refactoring_suggestions),
            "violations": violations[:10],  # Limit to first 10 violations
            "refactoring_patterns": [r.get("pattern", "") for r in refactoring_suggestions[:5]],
        }

        # Determine outcome based on compliance
        if v2_pass_rate >= 95.0:
            outcome = "success"
        elif v2_pass_rate >= 80.0:
            outcome = "partial"
        else:
            outcome = "failure"

        # Record the scanner action
        doc_id = ingestor.action(
            title="Project Scanner Analysis",
            tool="project_scanner",
            outcome=outcome,
            context=context,
            project=project,
            agent_id=agent_id,
            tags=["scanner", "compliance", "analysis", "v2"],
            summary=result.get(
                "summary", f"Analyzed {files_analyzed} files, {v2_pass_rate:.1f}% V2 compliant"
            ),
        )

        # Record refactoring protocols if any
        if refactoring_suggestions:
            refactor_protocols = []
            for refactor in refactoring_suggestions:
                pattern = refactor.get("pattern", "")
                files = refactor.get("files", [])
                if pattern and files:
                    refactor_protocols.append(f"{pattern}: {', '.join(files[:3])}")

            if refactor_protocols:
                ingestor.protocol(
                    title="Refactoring Strategy",
                    steps=refactor_protocols,
                    effectiveness=0.0,  # Will be updated based on results
                    improvements={"source": "scanner", "violations_addressed": len(violations)},
                    project=project,
                    agent_id=agent_id,
                    tags=["protocol", "refactor", "scanner"],
                    summary=f"Generated {len(refactor_protocols)} refactoring strategies",
                )

        # Record tool usage pattern
        ingestor.tool(
            title="Project Scanner Usage",
            usage_pattern=f"Analyzed {files_analyzed} files for V2 compliance",
            success_rate=1.0 if outcome == "success" else 0.5,
            failure_modes=["high_violation_rate"] if outcome == "failure" else [],
            optimizations=["batch_processing", "parallel_analysis"],
            project=project,
            agent_id=agent_id,
            tags=["tool", "scanner", "usage"],
            summary=f"Scanner used to analyze {files_analyzed} files",
        )

        logger.info(f"Successfully ingested scanner results for {project}")
        return doc_id

    except Exception as e:
        logger.error(f"Failed to ingest scanner results: {e}")
        raise


def ingest_compliance_fix(
    file_path: str,
    fix_type: str,
    before_lines: int,
    after_lines: int,
    project: str,
    agent_id: str = "Agent-2",
):
    """
    Ingest a compliance fix action.

    Args:
        file_path: Path to the fixed file
        fix_type: Type of fix applied
        before_lines: Lines before fix
        after_lines: Lines after fix
        project: Project identifier
        agent_id: Agent performing the fix
    """
    try:
        ingestor = Ingestor()

        context = {
            "file_path": file_path,
            "fix_type": fix_type,
            "before_lines": before_lines,
            "after_lines": after_lines,
            "lines_reduced": before_lines - after_lines,
            "reduction_percentage": ((before_lines - after_lines) / before_lines * 100)
            if before_lines > 0
            else 0,
        }

        outcome = "success" if after_lines <= 400 else "partial"

        ingestor.action(
            title=f"V2 Compliance Fix: {fix_type}",
            tool="compliance_fixer",
            outcome=outcome,
            context=context,
            project=project,
            agent_id=agent_id,
            tags=["compliance", "refactor", "v2", "fix"],
            summary=f"Applied {fix_type} fix to {file_path}, reduced from {before_lines} to {after_lines} lines",
        )

        logger.info(f"Recorded compliance fix for {file_path}")

    except Exception as e:
        logger.error(f"Failed to ingest compliance fix: {e}")
        raise
