# Workspace Maintenance Modules

The workspace maintenance system is divided into three focused
submodules coordinated by a top-level orchestrator:

- `WorkspaceScanner` – recursively gathers all files in a workspace.
- `WorkspaceHealthChecker` – performs lightweight health evaluation
  based on scan results.
- `WorkspaceRemediator` – executes follow-up remediation actions.

`WorkspaceMaintenanceOrchestrator` ties these components together and
provides a single `run()` method that performs scanning, health
checking, and remediation in sequence.

The modules live under `src/workspace_maintenance`.
