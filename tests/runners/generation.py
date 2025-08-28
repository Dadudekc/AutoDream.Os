"""Utilities for test discovery and command construction."""
from pathlib import Path
from typing import List, Optional


def discover_tests(
    tests_dir: Path,
    repo_root: Path,
    test_type: Optional[str] = None,
    pattern: str = "test_*.py",
) -> List[Path]:
    """Discover test files based on type and pattern."""
    if not tests_dir.exists():
        print(f"❌ Test directory not found: {tests_dir}")
        return []

    test_files: List[Path] = []
    if test_type:
        type_dir = tests_dir / test_type
        if type_dir.exists():
            test_files.extend(type_dir.rglob(pattern))
        else:
            print(f"⚠️ Test type directory not found: {type_dir}")
    else:
        test_files.extend(tests_dir.rglob(pattern))
        test_files.extend(repo_root.glob(pattern))

    return sorted(set(test_files))


def build_pytest_command(
    test_paths: List[Path],
    results_dir: Path,
    coverage: bool = True,
    parallel: bool = False,
    verbose: bool = True,
    markers: Optional[List[str]] = None,
) -> List[str]:
    """Construct a pytest command for the provided test paths."""
    cmd = ["python", "-m", "pytest"]
    for test_path in test_paths:
        cmd.append(str(test_path))
    if verbose:
        cmd.append("-v")
    if coverage:
        cmd.extend(
            [
                "--cov=src",
                "--cov-report=html",
                "--cov-report=term-missing",
                "--cov-report=json",
            ]
        )
    if parallel:
        cmd.extend(["-n", "auto"])
    if markers:
        for marker in markers:
            cmd.extend(["-m", marker])
    cmd.extend(
        [
            "--tb=short",
            "--strict-markers",
            "--disable-warnings",
            f"--html={results_dir}/report.html",
            "--self-contained-html",
        ]
    )
    return cmd
