import json

from src.utils.test_components import (
    CoverageReporter,
    ResultAggregator,
    SubprocessHandler,
    RunOrchestrator,
)


def test_test_orchestrator_integration(tmp_path):
    cov_file = tmp_path / "coverage.json"
    cov_file.write_text(json.dumps({"totals": {"percent_covered": 66.0}}))

    orchestrator = RunOrchestrator(
        SubprocessHandler(),
        ResultAggregator(),
        CoverageReporter(cov_file),
    )

    commands = [
        ["python", "-c", "print('one')"],
        ["python", "-c", "print('two')"],
    ]
    result = orchestrator.run_commands(commands)

    assert result["summary"]["total"] == 2
    assert result["summary"]["successes"] == 2
    assert result["coverage"] == 66.0
