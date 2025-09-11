#!/usr/bin/env python3
"""
Onboarding Files Analysis Tool
Analyzes all onboarding-related files and generates ChatGPT context and project analysis.
"""

import ast
import json
import os
import re
from pathlib import Path
from typing import Any


def analyze_python_file(file_path: str) -> dict[str, Any]:
    """Analyze a Python file and extract metadata."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        functions = []
        classes = {}
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes[node.name] = {"methods": methods, "line_count": len(node.body)}
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    module = node.module or ""
                    imports.extend([f"{module}.{alias.name}" for alias in node.names])

        return {
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "line_count": len(content.splitlines()),
            "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path),
        }
    except Exception as e:
        return {
            "language": ".py",
            "functions": [],
            "classes": {},
            "imports": [],
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e),
        }


def analyze_js_file(file_path: str) -> dict[str, Any]:
    """Analyze a JavaScript file and extract metadata."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Simple regex-based analysis for JS
        functions = re.findall(r"function\s+(\w+)\s*\(", content)
        classes = re.findall(r"class\s+(\w+)", content)

        return {
            "language": ".js",
            "functions": functions,
            "classes": {cls: {"methods": []} for cls in classes},
            "line_count": len(content.splitlines()),
            "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path),
        }
    except Exception as e:
        return {
            "language": ".js",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e),
        }


def analyze_md_file(file_path: str) -> dict[str, Any]:
    """Analyze a Markdown file and extract metadata."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Extract headers
        headers = re.findall(r"^#+\s+(.+)$", content, re.MULTILINE)

        return {
            "language": ".md",
            "functions": [],
            "classes": {},
            "headers": headers,
            "line_count": len(content.splitlines()),
            "complexity": len(headers),
            "file_size": os.path.getsize(file_path),
        }
    except Exception as e:
        return {
            "language": ".md",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e),
        }


def analyze_yaml_file(file_path: str) -> dict[str, Any]:
    """Analyze a YAML file and extract metadata."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Simple YAML analysis
        lines = content.splitlines()
        keys = [
            line.split(":")[0].strip() for line in lines if ":" in line and not line.startswith("#")
        ]

        return {
            "language": ".yml",
            "functions": [],
            "classes": {},
            "keys": keys,
            "line_count": len(lines),
            "complexity": len(keys),
            "file_size": os.path.getsize(file_path),
        }
    except Exception as e:
        return {
            "language": ".yml",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e),
        }


def analyze_json_file(file_path: str) -> dict[str, Any]:
    """Analyze a JSON file and extract metadata."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            data = json.loads(content)

        # Analyze JSON structure
        def count_keys(obj, prefix=""):
            keys = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    keys.append(full_key)
                    if isinstance(value, (dict, list)):
                        keys.extend(count_keys(value, full_key))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    keys.extend(count_keys(item, f"{prefix}[{i}]"))
            return keys

        all_keys = count_keys(data)

        return {
            "language": ".json",
            "functions": [],
            "classes": {},
            "keys": all_keys,
            "line_count": len(content.splitlines()),
            "complexity": len(all_keys),
            "file_size": os.path.getsize(file_path),
        }
    except Exception as e:
        return {
            "language": ".json",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e),
        }


def analyze_file(file_path: str) -> dict[str, Any]:
    """Analyze a file based on its extension."""
    ext = Path(file_path).suffix.lower()

    if ext == ".py":
        return analyze_python_file(file_path)
    elif ext == ".js":
        return analyze_js_file(file_path)
    elif ext == ".md":
        return analyze_md_file(file_path)
    elif ext in [".yml", ".yaml"]:
        return analyze_yaml_file(file_path)
    elif ext == ".json":
        return analyze_json_file(file_path)
    else:
        return {
            "language": ext,
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": "Unsupported file type",
        }


def main():
    """Main analysis function."""
    # Onboarding-related files
    onboarding_files = [
        "onboarding_system_audit_report.md",
        "phase_transition_onboarding.py",
        "src/services/handlers/onboarding_handler.py",
        "onboard_survey_agents.py",
        "survey_team_onboarding_sequence.py",
        "src/automation/ui_onboarding.py",
        "specialized_survey_agents_onboarding.json",
        "scripts/agent_onboarding.py",
        "src/services/simple_onboarding.py",
        "fix_agent7_onboarding.py",
        "fix_agent_onboarding.py",
        "re_onboard_agent7.py",
        "simple_agent_onboarding.py",
        "src/services/onboarding_service.py",
        "onboard_agents_xml_debate.py",
        "src/services/architectural_onboarding.py",
        "src/core/managers/core_onboarding_manager.py",
        "src/services/onboarding_message_generator.py",
        "agent_workspaces/Agent-SQA-2/onboarding.json",
        "agent_workspaces/Agent-STM-6/onboarding.json",
        "agent_workspaces/Agent-SRC-1/onboarding.json",
        "agent_workspaces/Agent-SDA-3/onboarding.json",
        "agent_workspaces/Agent-SRA-5/onboarding.json",
        "agent_workspaces/Agent-SRC-4/onboarding.json",
        "src/core/validation/rules/onboarding.yaml",
        "docs/ONBOARDING_GUIDE.md",
        "docs/AGENT_ONBOARDING_GUIDE.md",
        "prompts/agents/onboarding.md",
        "prompts/captain/onboarding.md",
        "archive/onboarding/README_onboarding.md",
        "archive/onboarding/ONBOARDING_SYSTEM_UPDATES.md",
        "archive/onboarding/AGENT_ONBOARDING_COMPLETE_GUIDE.md",
    ]

    # Analyze each file
    analysis_results = {}
    total_files = 0
    total_lines = 0
    total_functions = 0
    total_classes = 0

    for file_path in onboarding_files:
        if os.path.exists(file_path):
            print(f"Analyzing: {file_path}")
            analysis = analyze_file(file_path)
            analysis_results[file_path] = analysis

            total_files += 1
            total_lines += analysis.get("line_count", 0)
            total_functions += len(analysis.get("functions", []))
            total_classes += len(analysis.get("classes", {}))
        else:
            print(f"File not found: {file_path}")

    # Generate project analysis JSON
    project_analysis = {
        "onboarding_files_analysis": analysis_results,
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": sum(
                analysis.get("complexity", 0) for analysis in analysis_results.values()
            )
            / max(total_files, 1),
        },
    }

    # Save project analysis
    with open("onboarding_project_analysis.json", "w", encoding="utf-8") as f:
        json.dump(project_analysis, f, indent=2)

    # Generate ChatGPT context
    chatgpt_context = {
        "project_root": os.getcwd(),
        "analysis_type": "onboarding_files_focused",
        "num_files_analyzed": total_files,
        "analysis_details": analysis_results,
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "file_types": {
                "python": len([f for f in analysis_results.values() if f.get("language") == ".py"]),
                "markdown": len(
                    [f for f in analysis_results.values() if f.get("language") == ".md"]
                ),
                "yaml": len([f for f in analysis_results.values() if f.get("language") == ".yml"]),
                "json": len([f for f in analysis_results.values() if f.get("language") == ".json"]),
                "javascript": len(
                    [f for f in analysis_results.values() if f.get("language") == ".js"]
                ),
            },
        },
    }

    # Save ChatGPT context
    with open("onboarding_chatgpt_context.json", "w", encoding="utf-8") as f:
        json.dump(chatgpt_context, f, indent=2)

    print("\n✅ Analysis complete!")
    print(f"📊 Files analyzed: {total_files}")
    print(f"📝 Total lines: {total_lines}")
    print(f"🔧 Total functions: {total_functions}")
    print(f"🏗️ Total classes: {total_classes}")
    print("📁 Generated files:")
    print("   - onboarding_project_analysis.json")
    print("   - onboarding_chatgpt_context.json")


if __name__ == "__main__":
    main()
