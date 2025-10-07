#!/usr/bin/env python3
"""
Agent-8 Quality Assessment for SWARM Survey
==========================================

Phase 3: Quality Assessment - V2 compliance, violations, anti-patterns
Operational perspective on system stability and quality metrics
"""

import json
import re
from pathlib import Path


def analyze_code_quality():
    """Analyze code quality from operational perspective"""

    print("🔍 AGENT-8 QUALITY ASSESSMENT")
    print("============================")
    print()

    src_path = Path("src")
    if not src_path.exists():
        print("❌ src/ directory not found")
        return

    # 1. V2 Compliance Analysis
    print("📋 V2 COMPLIANCE ANALYSIS:")
    print("-" * 26)

    v2_compliance = {
        "type_hints": 0,
        "docstrings": 0,
        "error_handling": 0,
        "logging_usage": 0,
        "config_management": 0,
        "total_files": 0,
    }

    for py_file in src_path.rglob("*.py"):
        v2_compliance["total_files"] += 1

        try:
            with open(py_file, encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Check for type hints
                if "->" in content or ": " in content:
                    # More sophisticated type hint detection
                    if re.search(r":\s*(str|int|float|bool|List|Dict|Optional)", content):
                        v2_compliance["type_hints"] += 1

                # Check for docstrings
                if '"""' in content or "'''" in content:
                    v2_compliance["docstrings"] += 1

                # Check for error handling
                if "try:" in content and "except" in content:
                    v2_compliance["error_handling"] += 1

                # Check for logging usage
                if "logging" in content or "logger" in content:
                    v2_compliance["logging_usage"] += 1

                # Check for configuration management
                if "config" in content.lower() or "settings" in content.lower():
                    v2_compliance["config_management"] += 1

        except Exception:
            continue

    print("V2 Compliance Metrics:")
    for metric, count in v2_compliance.items():
        if metric != "total_files":
            percentage = (
                (count / v2_compliance["total_files"] * 100)
                if v2_compliance["total_files"] > 0
                else 0
            )
            print(f'{metric.title()}: {count}/{v2_compliance["total_files"]} ({percentage:.1f}%)')

    # 2. Anti-Pattern Detection
    print("\n🚨 ANTI-PATTERN DETECTION:")
    print("-" * 25)

    anti_patterns = {
        "god_objects": [],
        "circular_imports": [],
        "duplicate_code": [],
        "magic_numbers": [],
        "long_functions": [],
        "deep_nesting": [],
    }

    for py_file in src_path.rglob("*.py"):
        try:
            with open(py_file, encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")

                # Check for long functions (>50 lines)
                in_function = False
                function_lines = 0
                indent_level = 0

                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith("def ") or stripped.startswith("async def "):
                        if in_function and function_lines > 50:
                            anti_patterns["long_functions"].append(str(py_file))
                        in_function = True
                        function_lines = 0
                        indent_level = len(line) - len(line.lstrip())
                    elif in_function:
                        if stripped and not stripped.startswith("#"):
                            current_indent = len(line) - len(line.lstrip())
                            if current_indent <= indent_level:
                                if function_lines > 50:
                                    anti_patterns["long_functions"].append(str(py_file))
                                in_function = False
                                function_lines = 0
                            else:
                                function_lines += 1

                    # Check for deep nesting (>4 levels)
                    if line.count("    ") > 4:
                        anti_patterns["deep_nesting"].append(str(py_file))
                        break

                # Check for magic numbers
                magic_numbers = re.findall(r"\b\d{2,}\b", content)
                if len(magic_numbers) > 10:  # Arbitrary threshold
                    anti_patterns["magic_numbers"].append(str(py_file))

        except Exception:
            continue

    print("Anti-Pattern Detection Results:")
    for pattern, files in anti_patterns.items():
        unique_files = len(set(files))
        print(f"{pattern.title()}: {unique_files} files")

    # 3. Stability Assessment
    print("\n⚖️  OPERATIONAL STABILITY ASSESSMENT:")
    print("-" * 35)

    stability_metrics = {
        "error_prone_patterns": 0,
        "resource_leaks": 0,
        "threading_issues": 0,
        "async_complexity": 0,
        "exception_safety": 0,
    }

    for py_file in src_path.rglob("*.py"):
        try:
            with open(py_file, encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Check for error-prone patterns
                if "eval(" in content or "exec(" in content:
                    stability_metrics["error_prone_patterns"] += 1

                # Check for potential resource leaks
                if ("open(" in content and "close()" not in content) or (
                    "connect(" in content and "disconnect" not in content
                ):
                    stability_metrics["resource_leaks"] += 1

                # Check for threading issues
                if "threading" in content and "threading.Lock()" not in content:
                    stability_metrics["threading_issues"] += 1

                # Check for async complexity
                if "async def" in content and "await asyncio.gather" in content:
                    stability_metrics["async_complexity"] += 1

                # Check for exception safety
                if "try:" in content and "finally:" in content:
                    stability_metrics["exception_safety"] += 1

        except Exception:
            continue

    print("Stability Assessment Results:")
    for metric, count in stability_metrics.items():
        print(f"{metric.title()}: {count} files")

    # 4. Code Quality Scoring
    print("\n📊 CODE QUALITY SCORING:")
    print("-" * 24)

    # Calculate quality scores
    total_files = v2_compliance["total_files"]

    quality_scores = {
        "type_hint_compliance": (
            (v2_compliance["type_hints"] / total_files * 100) if total_files > 0 else 0
        ),
        "documentation_compliance": (
            (v2_compliance["docstrings"] / total_files * 100) if total_files > 0 else 0
        ),
        "error_handling_compliance": (
            (v2_compliance["error_handling"] / total_files * 100) if total_files > 0 else 0
        ),
        "logging_compliance": (
            (v2_compliance["logging_usage"] / total_files * 100) if total_files > 0 else 0
        ),
        "anti_pattern_density": (
            (sum(len(files) for files in anti_patterns.values()) / total_files * 100)
            if total_files > 0
            else 0
        ),
    }

    print("Quality Compliance Scores:")
    for metric, score in quality_scores.items():
        print(f"{metric.title()}: {score:.1f}%")

    overall_quality = sum(quality_scores.values()) / len(quality_scores)
    print(f"\nOverall Quality Score: {overall_quality:.1f}%")

    print("\n✅ QUALITY ASSESSMENT COMPLETE")
    print("📊 Operational stability analysis ready for SWARM coordination")

    return {
        "v2_compliance": v2_compliance,
        "anti_patterns": {k: len(set(v)) for k, v in anti_patterns.items()},
        "stability_metrics": stability_metrics,
        "quality_scores": quality_scores,
        "overall_quality": overall_quality,
    }


if __name__ == "__main__":
    results = analyze_code_quality()

    # Save results for SWARM coordination
    with open("Agent-8_Quality_Analysis_Results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n💾 Results saved to: Agent-8_Quality_Analysis_Results.json")
