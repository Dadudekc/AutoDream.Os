#!/usr/bin/env python3
"""
Comprehensive coverage analysis and testing pipeline.
Usage:
  python tools/coverage/run_coverage_analysis.py --discover --analyze --report
"""
import argparse
import subprocess
import sys
import pathlib
from typing import List, Dict, Optional


class CoveragePipeline:
    """Comprehensive coverage analysis pipeline."""
    
    def __init__(self):
        """Initialize coverage pipeline."""
        self.thresholds = {
            "global_line_coverage_min": 85,
            "changed_code_line_coverage_min": 95,
            "branch_coverage_min": 70,
            "mutation_score_target": 60
        }
    
    def run_command(self, cmd: List[str], description: str) -> bool:
        """Run a command and return success status."""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ {description} completed")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed")
            print(f"   Error: {e.stderr}")
            return False
    
    def discover_gaps(self) -> bool:
        """Discover coverage gaps and generate reports."""
        print("\n🔍 DISCOVERY PHASE")
        print("=" * 50)
        
        commands = [
            (["pytest", "-q", "--maxfail=1"], "Running quick test check"),
            (["coverage", "run", "-m", "pytest", "-q"], "Running tests with coverage"),
            (["coverage", "html", "-d", ".coverage_html"], "Generating HTML coverage report"),
            (["coverage", "xml", "-o", "coverage.xml"], "Generating XML coverage report"),
            (["coverage", "report", "--show-missing"], "Generating coverage report")
        ]
        
        success = True
        for cmd, desc in commands:
            if not self.run_command(cmd, desc):
                success = False
        
        # Run changed file report
        changed_file_cmd = [
            "python", "tools/coverage/changed_file_report.py",
            "--base", "HEAD~1",
            "--min", str(self.thresholds["changed_code_line_coverage_min"])
        ]
        
        if not self.run_command(changed_file_cmd, "Checking changed file coverage"):
            success = False
        
        return success
    
    def analyze_gaps(self) -> bool:
        """Analyze coverage gaps and identify priorities."""
        print("\n📊 ANALYSIS PHASE")
        print("=" * 50)
        
        gap_analyzer_cmd = [
            "python", "tools/coverage/gap_analyzer.py",
            "--top", "10",
            "--min-coverage", "70",
            "--suggest"
        ]
        
        return self.run_command(gap_analyzer_cmd, "Analyzing coverage gaps")
    
    def run_mutation_tests(self) -> bool:
        """Run mutation tests (optional)."""
        print("\n🧬 MUTATION TESTING PHASE")
        print("=" * 50)
        
        mutation_cmd = [
            "python", "tools/coverage/mutation_gate.py",
            "--min", str(self.thresholds["mutation_score_target"]),
            "--defer-on-failure"
        ]
        
        return self.run_command(mutation_cmd, "Running mutation tests")
    
    def verify_thresholds(self) -> bool:
        """Verify coverage thresholds are met."""
        print("\n✅ VERIFICATION PHASE")
        print("=" * 50)
        
        commands = [
            (["coverage", "erase"], "Clearing previous coverage data"),
            (["coverage", "run", "-m", "pytest", "-q"], "Running final coverage test"),
            (["coverage", "report", f"--fail-under={self.thresholds['global_line_coverage_min']}"], 
             "Verifying global coverage threshold"),
            (["python", "tools/coverage/changed_file_report.py", 
              "--base", "HEAD~1", "--strict", 
              "--min", str(self.thresholds["changed_code_line_coverage_min"])], 
             "Verifying changed file coverage threshold")
        ]
        
        success = True
        for cmd, desc in commands:
            if not self.run_command(cmd, desc):
                success = False
        
        return success
    
    def generate_report(self) -> bool:
        """Generate comprehensive coverage report."""
        print("\n📋 REPORTING PHASE")
        print("=" * 50)
        
        try:
            # Get coverage summary
            result = subprocess.run(
                ["coverage", "report"], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                print("📊 Coverage Summary:")
                print(result.stdout)
                
                # Extract total coverage
                lines = result.stdout.split('\n')
                total_line = next((line for line in lines if 'TOTAL' in line), None)
                if total_line:
                    print(f"\n🎯 Total Coverage: {total_line.strip()}")
                
                return True
            else:
                print(f"❌ Failed to generate coverage report: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return False
    
    def print_summary(self, results: Dict[str, bool]) -> None:
        """Print pipeline execution summary."""
        print("\n" + "=" * 60)
        print("📋 COVERAGE PIPELINE SUMMARY")
        print("=" * 60)
        
        for phase, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{phase:<20} {status}")
        
        overall_success = all(results.values())
        print(f"\n🎯 Overall Status: {'✅ SUCCESS' if overall_success else '❌ FAILURE'}")
        
        if overall_success:
            print("\n🚀 Coverage pipeline completed successfully!")
            print("   - All thresholds met")
            print("   - Reports generated")
            print("   - Ready for CI/CD")
        else:
            print("\n⚠️  Coverage pipeline completed with issues")
            print("   - Review failed phases")
            print("   - Add missing tests")
            print("   - Re-run pipeline")


def main() -> int:
    """Main function for coverage pipeline."""
    ap = argparse.ArgumentParser(description="Comprehensive coverage analysis pipeline")
    ap.add_argument("--discover", action="store_true", help="Run discovery phase")
    ap.add_argument("--analyze", action="store_true", help="Run analysis phase")
    ap.add_argument("--mutate", action="store_true", help="Run mutation testing")
    ap.add_argument("--verify", action="store_true", help="Run verification phase")
    ap.add_argument("--report", action="store_true", help="Generate final report")
    ap.add_argument("--all", action="store_true", help="Run all phases")
    args = ap.parse_args()
    
    # If no specific phases selected, run all
    if not any([args.discover, args.analyze, args.mutate, args.verify, args.report]):
        args.all = True
    
    pipeline = CoveragePipeline()
    results = {}
    
    print("🚀 Starting Coverage Analysis Pipeline")
    print("=" * 60)
    
    # Run selected phases
    if args.all or args.discover:
        results["Discovery"] = pipeline.discover_gaps()
    
    if args.all or args.analyze:
        results["Analysis"] = pipeline.analyze_gaps()
    
    if args.all or args.mutate:
        results["Mutation Testing"] = pipeline.run_mutation_tests()
    
    if args.all or args.verify:
        results["Verification"] = pipeline.verify_thresholds()
    
    if args.all or args.report:
        results["Reporting"] = pipeline.generate_report()
    
    # Print summary
    pipeline.print_summary(results)
    
    # Return exit code
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())



