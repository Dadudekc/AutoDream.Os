#!/usr/bin/env python3
"""
Week 1 Day 1: Duplicate Analysis & Planning
==========================================

Analyze 11 duplicate groups identified in dependency analysis and create detailed elimination strategy.
"""

import datetime
import json
from collections import Counter
from pathlib import Path


def load_dependency_analysis():
    """Load the dependency analysis results from the backup."""
    backup_dir = find_backup_directory()
    if not backup_dir:
        return None

    analysis_file = backup_dir / "dependency_analysis" / "dependency_analysis_report.json"
    if analysis_file.exists():
        with open(analysis_file) as f:
            return json.load(f)

    return None


def find_backup_directory():
    """Find the most recent web infrastructure backup directory."""
    backup_base = Path("backups")
    if not backup_base.exists():
        return None

    backup_dirs = [
        d for d in backup_base.iterdir() if d.is_dir() and "web_infrastructure" in d.name
    ]
    if not backup_dirs:
        return None

    # Sort by timestamp (newest first)
    backup_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return backup_dirs[0]


def analyze_duplicate_groups(duplicates):
    """Analyze duplicate groups and create elimination strategy."""
    print(f"📊 Analyzing {len(duplicates)} duplicate groups...")

    analysis = {
        "total_files": sum(group["count"] for group in duplicates),
        "total_size_kb": sum(group["size_kb"] * group["count"] for group in duplicates),
        "groups": [],
        "elimination_strategy": {},
        "risk_assessment": {},
        "priority_order": [],
    }

    for i, group in enumerate(duplicates):
        group_id = f"duplicate_group_{i+1}"
        size_kb = group["size_kb"]
        file_count = group["count"]
        files = group["files"]

        # Extract file names for analysis
        file_names = []
        directories = set()

        for file_path in files:
            # Convert Windows path to relative path and extract filename
            path_parts = file_path.replace("\\", "/").split("/")
            filename = path_parts[-1]
            file_names.append(filename)

            # Extract directory structure
            if "static/js/" in file_path:
                dir_part = file_path.split("static/js/")[1]
                if "/" in dir_part:
                    directories.add(dir_part.split("/")[0])
                else:
                    directories.add("root")

        # Analyze filename patterns
        name_patterns = Counter()
        for name in file_names:
            # Extract meaningful parts of filename
            parts = name.replace(".js", "").replace("-", "_").split("_")
            if len(parts) > 1:
                pattern = "_".join(parts[:2])  # First two parts as pattern
                name_patterns[pattern] += 1

        # Categorize duplicate types
        duplicate_type = "unknown"
        if any("dashboard" in name.lower() for name in file_names):
            duplicate_type = "dashboard_modules"
        elif any("service" in name.lower() or "module" in name.lower() for name in file_names):
            duplicate_type = "service_modules"
        elif any("utilit" in name.lower() for name in file_names):
            duplicate_type = "utility_functions"
        elif any("validation" in name.lower() for name in file_names):
            duplicate_type = "validation_modules"

        group_analysis = {
            "group_id": group_id,
            "file_count": file_count,
            "size_kb": size_kb,
            "total_size_kb": size_kb * file_count,
            "file_names": file_names[:10],  # First 10 for brevity
            "directories": list(directories),
            "name_patterns": dict(name_patterns.most_common(5)),
            "duplicate_type": duplicate_type,
            "files": files,
        }

        analysis["groups"].append(group_analysis)

    # Create elimination strategy
    analysis["elimination_strategy"] = create_elimination_strategy(analysis["groups"])

    # Risk assessment
    analysis["risk_assessment"] = assess_elimination_risks(analysis["groups"])

    # Priority order for elimination
    analysis["priority_order"] = determine_elimination_priority(analysis["groups"])

    return analysis


def create_elimination_strategy(groups):
    """Create detailed elimination strategy for each duplicate group."""
    strategy = {
        "phases": {
            "phase_1_critical": [],  # Obvious duplicates, backup files
            "phase_2_safe": [],  # Utility functions, simple modules
            "phase_3_complex": [],  # Interdependent modules, core functionality
            "phase_4_review": [],  # Requires detailed analysis
        },
        "consolidation_approach": {},
        "backup_strategy": "enterprise_backup_verified",
        "rollback_procedures": "3_click_restore_available",
    }

    for group in groups:
        group_id = group["group_id"]

        # Phase 1: Critical (obvious duplicates, backups)
        if any(
            "backup" in name.lower() or "original" in name.lower() for name in group["file_names"]
        ):
            strategy["phases"]["phase_1_critical"].append(
                {
                    "group_id": group_id,
                    "reason": "backup_files_detected",
                    "files_to_remove": [
                        f
                        for f in group["files"]
                        if "backup" in f.lower() or "original" in f.lower()
                    ],
                    "keep_file": next(
                        (
                            f
                            for f in group["files"]
                            if "backup" not in f.lower() and "original" not in f.lower()
                        ),
                        group["files"][0],
                    ),
                }
            )

        # Phase 2: Safe (utility functions, simple modules)
        elif (
            group["duplicate_type"] in ["utility_functions", "validation_modules"]
            and group["file_count"] <= 10
        ):
            strategy["phases"]["phase_2_safe"].append(
                {
                    "group_id": group_id,
                    "reason": "simple_utilities",
                    "consolidation_method": "merge_into_core_utility",
                    "estimated_effort": "2-4_hours",
                    "risk_level": "low",
                }
            )

        # Phase 3: Complex (dashboard modules, service modules)
        elif (
            group["duplicate_type"] in ["dashboard_modules", "service_modules"]
            or group["file_count"] > 15
        ):
            strategy["phases"]["phase_3_complex"].append(
                {
                    "group_id": group_id,
                    "reason": "complex_interdependencies",
                    "consolidation_method": "detailed_analysis_required",
                    "estimated_effort": "8-12_hours",
                    "risk_level": "medium",
                }
            )

        # Phase 4: Review (requires detailed analysis)
        else:
            strategy["phases"]["phase_4_review"].append(
                {
                    "group_id": group_id,
                    "reason": "requires_detailed_review",
                    "consolidation_method": "functional_analysis_needed",
                    "estimated_effort": "4-6_hours",
                    "risk_level": "medium",
                }
            )

    return strategy


def assess_elimination_risks(groups):
    """Assess risks associated with duplicate elimination."""
    risk_assessment = {
        "overall_risk_level": "medium",
        "critical_risks": [],
        "mitigation_strategies": [],
        "backup_validation_required": True,
        "testing_requirements": [],
    }

    # Analyze each group for risks
    for group in groups:
        group_id = group["group_id"]

        # High risk: Core dashboard functionality
        if group["duplicate_type"] == "dashboard_modules":
            risk_assessment["critical_risks"].append(
                {
                    "group_id": group_id,
                    "risk_type": "core_functionality_impact",
                    "description": f'Dashboard modules ({group["file_count"]} files) may affect UI/UX',
                    "mitigation": "functional_testing_required",
                }
            )

        # Medium risk: Service modules
        elif group["duplicate_type"] == "service_modules":
            risk_assessment["critical_risks"].append(
                {
                    "group_id": group_id,
                    "risk_type": "service_integration_impact",
                    "description": f'Service modules ({group["file_count"]} files) may affect backend integration',
                    "mitigation": "api_testing_required",
                }
            )

        # Low risk: Utilities and validation
        elif group["duplicate_type"] in ["utility_functions", "validation_modules"]:
            risk_assessment["mitigation_strategies"].append(
                {
                    "group_id": group_id,
                    "strategy": "incremental_replacement",
                    "description": f'Safe consolidation of {group["file_count"]} utility files',
                }
            )

    # Overall risk assessment
    critical_count = len(
        [
            r
            for r in risk_assessment["critical_risks"]
            if r["risk_type"] in ["core_functionality_impact"]
        ]
    )
    if critical_count > 3:
        risk_assessment["overall_risk_level"] = "high"
    elif critical_count > 1:
        risk_assessment["overall_risk_level"] = "medium"
    else:
        risk_assessment["overall_risk_level"] = "low"

    # Testing requirements
    risk_assessment["testing_requirements"] = [
        "unit_tests_for_modified_modules",
        "integration_tests_for_service_changes",
        "ui_functionality_tests_for_dashboard_changes",
        "performance_regression_tests",
        "cross_browser_compatibility_tests",
    ]

    return risk_assessment


def determine_elimination_priority(groups):
    """Determine priority order for duplicate elimination."""
    priority_groups = {
        "high_priority": [],  # Obvious wins, low risk
        "medium_priority": [],  # Requires analysis, moderate risk
        "low_priority": [],  # Complex, high risk
        "review_required": [],  # Needs detailed investigation
    }

    for group in groups:
        group_id = group["group_id"]
        file_count = group["file_count"]
        duplicate_type = group["duplicate_type"]

        # High priority: Many small utility files, low risk
        if file_count > 20 and duplicate_type in ["utility_functions", "validation_modules"]:
            priority_groups["high_priority"].append(
                {
                    "group_id": group_id,
                    "reason": "high_count_utilities",
                    "impact": f"{file_count} utility files consolidation",
                    "estimated_savings": file_count * group["size_kb"],
                }
            )

        # High priority: Obvious backup files
        elif any("backup" in name.lower() for name in group["file_names"]):
            priority_groups["high_priority"].append(
                {
                    "group_id": group_id,
                    "reason": "backup_files_elimination",
                    "impact": "obvious_duplicates_removal",
                    "estimated_savings": file_count * group["size_kb"],
                }
            )

        # Medium priority: Service modules with moderate count
        elif duplicate_type == "service_modules" and 5 <= file_count <= 15:
            priority_groups["medium_priority"].append(
                {
                    "group_id": group_id,
                    "reason": "service_consolidation",
                    "impact": f"{file_count} service modules optimization",
                    "estimated_savings": file_count * group["size_kb"],
                }
            )

        # Low priority: Core dashboard functionality
        elif duplicate_type == "dashboard_modules":
            priority_groups["low_priority"].append(
                {
                    "group_id": group_id,
                    "reason": "core_dashboard_risk",
                    "impact": f"{file_count} dashboard modules (high risk)",
                    "estimated_savings": file_count * group["size_kb"],
                }
            )

        # Review required: Unclear categorization
        else:
            priority_groups["review_required"].append(
                {
                    "group_id": group_id,
                    "reason": "detailed_analysis_needed",
                    "impact": f"{file_count} files require investigation",
                    "estimated_savings": file_count * group["size_kb"],
                }
            )

    return priority_groups


def generate_day_1_report(analysis):
    """Generate comprehensive Day 1 analysis report."""
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "phase": "Week 1 Day 1: Duplicate Analysis & Planning",
        "analysis_summary": {
            "total_duplicate_groups": len(analysis["groups"]),
            "total_duplicate_files": analysis["total_files"],
            "total_size_kb": analysis["total_size_kb"],
            "estimated_reduction_percentage": round((analysis["total_files"] / 170) * 100, 1),
        },
        "elimination_strategy": analysis["elimination_strategy"],
        "risk_assessment": analysis["risk_assessment"],
        "priority_recommendations": analysis["priority_order"],
        "day_1_deliverables": {
            "completed": [
                "duplicate_groups_analysis",
                "elimination_strategy_development",
                "risk_assessment_completed",
                "priority_order_established",
            ],
            "next_steps": [
                "cross_agent_strategy_review",
                "implementation_plan_finalization",
                "phase_1_elimination_preparation",
            ],
        },
        "week_1_projection": {
            "target_reduction": "20-25%",
            "current_potential": f"{analysis['analysis_summary']['estimated_reduction_percentage']}%",
            "recommended_approach": "prioritize_high_impact_groups",
            "timeline": {
                "day_1": "analysis_complete",
                "day_2": "safe_elimination_50%",
                "day_3": "structure_optimization_70%",
            },
        },
    }

    return report


def perform_day_1_analysis():
    """Main function to perform Day 1 duplicate analysis."""
    print("🚀 WEEK 1 DAY 1: Duplicate Analysis & Planning")
    print("=" * 50)

    # Load dependency analysis
    dependency_data = load_dependency_analysis()
    if not dependency_data:
        print("❌ Could not load dependency analysis data")
        return None

    # Extract duplicate utilities
    duplicates = dependency_data.get("consolidation_opportunities", {}).get(
        "duplicate_utilities", []
    )
    if not duplicates:
        print("❌ No duplicate utilities found in analysis")
        return None

    print(f"📊 Found {len(duplicates)} duplicate groups to analyze")

    # Perform comprehensive analysis
    analysis = analyze_duplicate_groups(duplicates)

    # Add analysis summary to analysis dict
    analysis["analysis_summary"] = {
        "total_duplicate_groups": len(analysis["groups"]),
        "total_duplicate_files": analysis["total_files"],
        "total_size_kb": analysis["total_size_kb"],
        "estimated_reduction_percentage": round((analysis["total_files"] / 170) * 100, 1),
    }

    # Generate Day 1 report
    report = generate_day_1_report(analysis)

    # Save analysis results
    backup_dir = find_backup_directory()
    day1_dir = backup_dir / "week_1_day_1_analysis"
    day1_dir.mkdir(exist_ok=True)

    # Save detailed analysis
    analysis_file = day1_dir / "duplicate_analysis_detailed.json"
    with open(analysis_file, "w") as f:
        json.dump(analysis, f, indent=2)

    # Save Day 1 report
    report_file = day1_dir / "day_1_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print("\n🎯 DUPLICATE ANALYSIS SUMMARY:")
    print(f"   Groups Analyzed: {len(analysis['groups'])}")
    print(f"   Total Files: {analysis['total_files']}")
    print(f"   Total Size: {analysis['total_size_kb']} KB")
    print(
        f"   Estimated Reduction: {report['analysis_summary']['estimated_reduction_percentage']}%"
    )

    print("\n📋 ELIMINATION STRATEGY:")
    strategy = analysis["elimination_strategy"]
    for phase, groups in strategy["phases"].items():
        if groups:
            print(f"   {phase.replace('_', ' ').title()}: {len(groups)} groups")

    print("\n⚠️  RISK ASSESSMENT:")
    risk = analysis["risk_assessment"]
    print(f"   Overall Risk Level: {risk['overall_risk_level'].upper()}")
    print(f"   Critical Risks: {len(risk['critical_risks'])}")
    print(f"   Mitigation Strategies: {len(risk['mitigation_strategies'])}")

    print("\n🎯 PRIORITY RECOMMENDATIONS:")
    priority = analysis["priority_order"]
    for level, groups in priority.items():
        if groups:
            print(f"   {level.replace('_', ' ').title()}: {len(groups)} groups")

    print("\n✅ DAY 1 DELIVERABLES COMPLETED!")
    print(f"📁 Analysis saved: {day1_dir}")

    return analysis


if __name__ == "__main__":
    analysis = perform_day_1_analysis()
    if analysis:
        print("\n🎉 Duplicate analysis completed successfully!")
        print("🎯 Ready to proceed with cross-agent strategy review and implementation planning!")
    else:
        print("\n❌ Duplicate analysis failed - check dependency data")
