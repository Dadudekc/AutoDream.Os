#!/usr/bin/env python3
"""Testing System Eliminator."""

import shutil
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

from .output_formatter import OutputFormatter


class EliminationTarget(Enum):
    OLD_TEST_RUNNERS="old_test_runners"
    DUPLICATE_FRAMEWORKS="duplicate_frameworks"
    SCATTERED_UTILITIES="scattered_utilities"
    REDUNDANT_CONFIGS="redundant_configs"
    OBSOLETE_SCRIPTS="obsolete_scripts"


@dataclass
class EliminationTargetInfo:
    path: Path
    type: EliminationTarget
    size_bytes: int
    reason: str
    replacement: str
    safe_to_remove: bool=True


@dataclass
class EliminationPlan:
    targets: List[EliminationTargetInfo]
    total_size_bytes: int
    estimated_reduction: float
    replacement_files: List[str]
    archive_directory: Path


class TestingSystemEliminator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.output_formatter = OutputFormatter()
        self.elimination_targets={
            EliminationTarget.OLD_TEST_RUNNERS:["src/run_tests.py","src/run_all_tests.py","src/run_tdd_tests.py","src/test_runner.py","src/test_suite.py"],
            EliminationTarget.DUPLICATE_FRAMEWORKS:["src/testing/","src/core/testing/testing_framework/","src/core/testing/testing_cli.py"],
            EliminationTarget.SCATTERED_UTILITIES:["src/testing_utils.py","src/test_helpers.py","src/testing_common.py"],
            EliminationTarget.REDUNDANT_CONFIGS:["pytest.ini",".pytestrc","setup.cfg","tox.ini"],
            EliminationTarget.OBSOLETE_SCRIPTS:["scripts/setup_tests.py","scripts/run_tests.sh","scripts/test_environment.py"],
        }
        self.replacement_files=[
            "src/core/testing/unified_testing_framework.py",
            "src/core/testing/test_suite_consolidator.py",
            "src/core/testing/testing_system_eliminator.py",
            "src/unified_test_runner.py",
        ]

    def scan_for_elimination_targets(self) -> List[EliminationTargetInfo]:
        self.output_formatter.print_info("Scanning for elimination targets...")
        targets: List[EliminationTargetInfo] = []
        for target_type, paths in self.elimination_targets.items():
            for path_str in paths:
                path = self.project_root / path_str
                if path.exists():
                    info = self._analyze_elimination_target(path, target_type)
                    if info:
                        targets.append(info)
        targets.extend(self._scan_for_additional_targets())
        self.output_formatter.print_info(f"Found {len(targets)} elimination targets")
        return targets

    def _analyze_elimination_target(
        self, path: Path, target_type: EliminationTarget
    ) -> Optional[EliminationTargetInfo]:
        try:
            size = path.stat().st_size if path.is_file() else self._calculate_directory_size(path)
            return EliminationTargetInfo(
                path=path,
                type=target_type,
                size_bytes=size,
                reason=self._get_elimination_reason(path, target_type),
                replacement=self._get_replacement_file(path, target_type),
                safe_to_remove=self._is_safe_to_remove(path),
            )
        except Exception as e:  # pragma: no cover - logging only
            self.output_formatter.print_warning(
                f"Failed to analyze {path}: {e}"
            )
            return None

    def _scan_for_additional_targets(self) -> List[EliminationTargetInfo]:
        extra: List[EliminationTargetInfo] = []
        src_dir = self.project_root / "src"
        if src_dir.exists():
            for f in src_dir.rglob("*test*.py"):
                if f not in map(Path, self.replacement_files) and self._is_scattered_testing_file(f):
                    extra.append(EliminationTargetInfo(path=f,type=EliminationTarget.SCATTERED_UTILITIES,size_bytes=f.stat().st_size,reason="Scattered testing utility",replacement="src/core/testing/unified_testing_framework.py",safe_to_remove=self._is_safe_to_remove(f)))
        for f in self.project_root.glob("*test*.py"):
            if f not in map(Path, self.replacement_files):
                extra.append(EliminationTargetInfo(path=f,type=EliminationTarget.SCATTERED_UTILITIES,size_bytes=f.stat().st_size,reason="Test file in root directory",replacement="src/core/testing/unified_testing_framework.py",safe_to_remove=self._is_safe_to_remove(f)))
        return extra

    def _is_scattered_testing_file(self, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding="utf-8").lower()
        except Exception:
            return False
        name = file_path.name.lower()
        patterns = ["unittest","pytest","test_","testing","assert","testcase","testrunner","testsuite"]
        return any(p in name or p in content for p in patterns)

    def _calculate_directory_size(self, directory: Path) -> int:
        return sum(f.stat().st_size for f in directory.rglob("*") if f.is_file())

    def _get_elimination_reason(
        self, path: Path, target_type: EliminationTarget
    ) -> str:
        reasons={
            EliminationTarget.OLD_TEST_RUNNERS:"Replaced by unified_test_runner.py",
            EliminationTarget.DUPLICATE_FRAMEWORKS:"Replaced by unified_testing_framework.py",
            EliminationTarget.SCATTERED_UTILITIES:"Replaced by unified testing framework",
            EliminationTarget.REDUNDANT_CONFIGS:"Replaced by unified configuration management",
            EliminationTarget.OBSOLETE_SCRIPTS:"Replaced by automated infrastructure management",
        }
        return reasons.get(target_type,"Consolidated into unified framework")

    def _get_replacement_file(
        self, path: Path, target_type: EliminationTarget
    ) -> str:
        replacements={
            EliminationTarget.OLD_TEST_RUNNERS:"src/unified_test_runner.py",
            EliminationTarget.DUPLICATE_FRAMEWORKS:"src/core/testing/unified_testing_framework.py",
            EliminationTarget.SCATTERED_UTILITIES:"src/core/testing/unified_testing_framework.py",
            EliminationTarget.REDUNDANT_CONFIGS:"src/core/testing/testing_infrastructure_manager.py",
            EliminationTarget.OBSOLETE_SCRIPTS:"src/core/testing/testing_infrastructure_manager.py",
        }
        return replacements.get(target_type,"src/core/testing/unified_testing_framework.py")

    def _is_safe_to_remove(self, path: Path) -> bool:
        path_str=str(path)
        if path_str in self.replacement_files or "unified_testing" in path_str or "testing_system_eliminator" in path_str:
            return False
        return True

    def create_elimination_plan(
        self, targets: List[EliminationTargetInfo]
    ) -> EliminationPlan:
        self.output_formatter.print_info("Creating elimination plan...")
        safe = [t for t in targets if t.safe_to_remove]
        total_size = sum(t.size_bytes for t in safe)
        project_size = self._calculate_project_size()
        reduction = (total_size / project_size * 100) if project_size else 0
        archive = self.project_root / "testing_archive"
        return EliminationPlan(
            targets=safe,
            total_size_bytes=total_size,
            estimated_reduction=reduction,
            replacement_files=self.replacement_files,
            archive_directory=archive,
        )

    def _calculate_project_size(self) -> int:
        return sum(f.stat().st_size for f in self.project_root.rglob("*") if f.is_file())

    def execute_elimination(self, plan: EliminationPlan) -> bool:
        self.output_formatter.print_info("Executing elimination plan...")
        try:
            plan.archive_directory.mkdir(exist_ok=True)
            for t in plan.targets:
                if not self._eliminate_target(t, plan.archive_directory):
                    self.output_formatter.print_warning(f"Failed to eliminate {t.path}")
            self._create_elimination_report(plan)
            self._update_project_structure()
            self.output_formatter.print_success("Elimination completed successfully!")
            return True
        except Exception as e:
            self.output_formatter.print_error(f"Elimination failed: {e}")
            return False

    def _eliminate_target(
        self, target: EliminationTargetInfo, archive_dir: Path
    ) -> bool:
        try:
            archive_path=archive_dir/target.path.name
            if archive_path.exists():
                ts=int(time.time())
                archive_path=archive_dir/(f"{target.path.stem}_{ts}{target.path.suffix}" if target.path.is_file() else f"{target.path.name}_{ts}")
            shutil.move(str(target.path),str(archive_path))
            self.output_formatter.print_info(f"Archived {target.type.value}: {target.path} -> {archive_path}")
            return True
        except Exception as e:
            self.output_formatter.print_error(f"Failed to eliminate {target.path}: {e}")
            return False

    def _create_elimination_report(self, plan: EliminationPlan) -> None:
        report=(
            f"# Testing System Elimination Report - TASK 3H\n"
            f"Total Targets: {len(plan.targets)}\n"
            f"Total Size: {plan.total_size_bytes:,} bytes\n"
            f"Estimated Reduction: {plan.estimated_reduction:.1f}%\n"
            f"Archive: {plan.archive_directory}\n\n"
            "## Eliminated Targets\n"
        )
        for t in plan.targets:
            report+=f"- {t.type.value}: {t.path.name} ({t.size_bytes:,} bytes) {t.reason}\n"
        report+="\n## Replacement Files\n"
        for f in plan.replacement_files:
            report+=f"- {f}\n"
        report_file=plan.archive_directory/"ELIMINATION_REPORT.md"
        report_file.write_text(report)
        self.output_formatter.print_success(f"Created elimination report: {report_file}")

    def _update_project_structure(self) -> None:
        try:
            testing_dir=self.project_root/"src"/"core"/"testing"
            testing_dir.mkdir(parents=True,exist_ok=True)
            (testing_dir/"__init__.py").write_text('"""Unified Testing Framework"""\n')
            readme=("# Unified Testing Framework\n""Run tests with: python -m src.core.testing.unified_testing_framework\n")
            (testing_dir/"README.md").write_text(readme)
            self.output_formatter.print_success("Updated project structure")
        except Exception as e:
            self.output_formatter.print_error(f"Failed to update project structure: {e}")

    def generate_elimination_report(self) -> str:
        if not hasattr(self, "elimination_results"):
            return "No elimination results available"
        content=(
            "🚀 TESTING SYSTEM ELIMINATION REPORT - TASK 3H\n"
            f"Targets Eliminated: {len(self.elimination_results.get('targets', []))}\n"
            f"Total Size Eliminated: {self.elimination_results.get('total_size', 0):,} bytes\n"
            f"Estimated Reduction: {self.elimination_results.get('reduction', 0):.1f}%\n"
            "REPLACEMENT FILES:\n"
        )
        for f in self.replacement_files:
            content+=f"✅ {f}\n"
        return content


def main() -> int:
    project_root = Path(__file__).parent.parent.parent.parent
    eliminator = TestingSystemEliminator(project_root)
    try:
        targets = eliminator.scan_for_elimination_targets()
        print(f"Scan complete: {len(targets)} targets found")
        plan = eliminator.create_elimination_plan(targets)
        print(
            f"Elimination plan created: {plan.estimated_reduction:.1f}% reduction estimated"
        )
        success = eliminator.execute_elimination(plan)
        if success:
            print("✅ Testing system elimination completed successfully!")
            return 0
        print("❌ Testing system elimination failed!")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Elimination interrupted by user")
        return 130
    except Exception as e:
        print(f"❌ Elimination error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

