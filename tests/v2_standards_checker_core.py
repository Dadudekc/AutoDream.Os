"""Core routines for running V2 standards checks.

The core module coordinates walking through source directories and
aggregating file level results produced by :mod:`v2_standards_validator`.
"""

from pathlib import Path
from typing import Dict, Any

from v2_standards_config import StandardsConfig, get_category_limit
from v2_standards_validator import validate_file


def _py_files(directory: Path):
    for path in directory.glob("*.py"):
        if path.name == "__init__.py":
            continue
        yield path


def _aggregate(result: Dict[str, Any], file_result: Dict[str, bool]) -> None:
    if all(file_result.values()):
        result["compliant_files"] += 1
    else:
        for key, ok in file_result.items():
            if not ok:
                result[f"{key}_violations"] += 1


def check_category(category_dir: Path, category: str, config: StandardsConfig) -> Dict[str, Any]:
    """Validate all files inside a category directory."""
    res = {
        "files_checked": 0,
        "compliant_files": 0,
        "loc_violations": 0,
        "oop_violations": 0,
        "cli_violations": 0,
        "srp_violations": 0,
    }
    limit = get_category_limit(category, config)
    for py in _py_files(category_dir):
        res["files_checked"] += 1
        file_result = validate_file(py, limit)
        _aggregate(res, file_result)
    return res


def _merge(overall: Dict[str, Any], cat_res: Dict[str, Any]) -> None:
    overall["total_files"] += cat_res["files_checked"]
    overall["compliant_files"] += cat_res["compliant_files"]
    for key in ["loc", "oop", "cli", "srp"]:
        overall[f"{key}_violations"] += cat_res[f"{key}_violations"]


def check_all(config: StandardsConfig) -> Dict[str, Any]:
    results = {
        "total_files": 0,
        "compliant_files": 0,
        "loc_violations": 0,
        "oop_violations": 0,
        "cli_violations": 0,
        "srp_violations": 0,
    }
    for category in config.COMPONENTS:
        category_dir = Path("src") / category
        if category_dir.exists():
            cat_res = check_category(category_dir, category, config)
            _merge(results, cat_res)
    results["overall_compliance"] = (
        results["compliant_files"] / results["total_files"] * 100
        if results["total_files"]
        else 0.0
    )
    return results


def check_single(metric: str, config: StandardsConfig) -> Dict[str, Any]:
    """Run a single metric check (loc, oop, cli, or srp)."""
    results = {
        "total_files": 0,
        "compliant_files": 0,
        "non_compliant_files": 0,
        "violations": [],
    }
    for category in config.COMPONENTS:
        category_dir = Path("src") / category
        if not category_dir.exists():
            continue
        limit = get_category_limit(category, config)
        for py in _py_files(category_dir):
            results["total_files"] += 1
            file_res = validate_file(py, limit)
            ok = file_res[metric]
            if ok:
                results["compliant_files"] += 1
            else:
                results["non_compliant_files"] += 1
                if metric == "loc":
                    results["violations"].append(
                        {
                            "file": str(py),
                            "message": f"exceeds {limit} LOC",
                        }
                    )
    return results
