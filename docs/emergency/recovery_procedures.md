# Recovery Procedures

Recovery procedures execute automated actions to restore normal operation after an emergency is detected.

## Capabilities
- Executes recovery actions based on emergency type
- Validates each step before completion
- Supports rollback operations when recovery fails
- Handles multiple concurrent recovery workflows

## Usage
The procedures are defined in `RecoveryExecutor` and driven by the `ProtocolManager`.
