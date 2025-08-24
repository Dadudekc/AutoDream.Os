from typing import Dict, List


class TestReporter:
    """Generate summaries of test execution results."""

    def summarize(self, results: List[Dict[str, int]]) -> Dict[str, int]:
        summary = {
            "total_runs": len(results),
            "successful_runs": sum(1 for r in results if r.get("return_code", 1) == 0),
            "failed_runs": sum(1 for r in results if r.get("return_code", 1) != 0),
            "total_tests": sum(r.get("total", 0) for r in results),
            "passed": sum(r.get("passed", 0) for r in results),
            "failed": sum(r.get("failed", 0) for r in results),
        }
        return summary
