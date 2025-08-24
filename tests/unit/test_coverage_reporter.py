import json
from pathlib import Path

from src.utils.test_components import CoverageReporter


def test_coverage_reporter_reads_file(tmp_path):
    data = {"totals": {"percent_covered": 87.5}}
    cov_file = tmp_path / "coverage.json"
    cov_file.write_text(json.dumps(data))
    reporter = CoverageReporter(cov_file)
    assert reporter.report() == 87.5
