"""Orchestrator for auth integration tests using modular components."""
from datetime import datetime
from .auth_integration_tester_config import AuthTesterConfig
from .auth_integration_tester_validation import validate_environment
from .auth_integration_tester_core import run_core_tests
from .auth_integration_tester_reporting import IntegrationReport


class AuthIntegrationTester:
    """High level orchestrator that wires validation, core tests and reporting."""

    def __init__(self, config: AuthTesterConfig | None = None):
        self.config = config or AuthTesterConfig()

    def run(self) -> IntegrationReport:
        ok, message = validate_environment()
        if not ok:
            raise RuntimeError(message)

        start = datetime.now()
        results = run_core_tests(self.config)
        end = datetime.now()
        report = IntegrationReport(started=start, ended=end, results=results)

        if self.config.save_report_path:
            report.to_json(self.config.save_report_path)
        return report


def main() -> None:
    tester = AuthIntegrationTester()
    report = tester.run()
    print(f"Auth integration tests completed: {report.summary}")


if __name__ == "__main__":
    main()
