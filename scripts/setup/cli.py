"""Command line entrypoint for the setup workflow."""

import argparse

from . import (
    env_config,
    dependency_install,
    frontend_tooling,
    backend_api,
    testing_setup,
)


def main(argv=None):
    """Run setup steps in sequence.

    Args:
        argv (list[str] | None): Optional CLI arguments for testing.

    Returns:
        list[dict]: List of step result dictionaries.
    """
    parser = argparse.ArgumentParser(description="AutoDream OS setup")
    parser.add_argument(
        "--step",
        choices=["env", "deps", "frontend", "backend", "tests", "all"],
        default="all",
        help="Run a specific step or all steps",
    )
    args = parser.parse_args(argv)

    results = []
    if args.step in ("env", "all"):
        results.append(env_config.setup_environment())
    if args.step in ("deps", "all"):
        results.append(dependency_install.install_dependencies())
    if args.step in ("frontend", "all"):
        results.append(frontend_tooling.setup_frontend())
    if args.step in ("backend", "all"):
        results.append(backend_api.setup_backend())
    if args.step in ("tests", "all"):
        results.append(testing_setup.setup_testing())

    return results


if __name__ == "__main__":
    main()
