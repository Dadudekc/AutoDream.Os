# Onboarding Guide

## Regular Onboarding

### Usage

```bash
python -m src.services.messaging_cli --onboarding
python -m src.services.messaging_cli --onboard --agent Agent-1
```

## Onboarding Modes (Roles)

Assign quality roles to agents during hard onboarding:

```bash
# Full suite, round-robin roles across agents
python -m src.services.messaging_cli --hard-onboarding --mode quality-suite --yes

# Focus on a single doctrine
python -m src.services.messaging_cli --hard-onboarding --mode solid --yes

# Explicit mapping
python -m src.services.messaging_cli --hard-onboarding --mode quality-suite \
  --assign-roles "Agent-1:SOLID,Agent-2:SSOT,Agent-3:DRY" --yes

# UI delivery with role-tailored messages
python -m src.services.messaging_cli --hard-onboarding --ui --mode quality-suite --yes
```

**Roles**

* **SOLID Sentinel** — enforces SOLID across code structure.
* **SSOT Warden** — guards single-source-of-truth and anti-duplication of facts.
* **DRY Hunter** — eliminates duplicate logic via consolidation.
* **KISS Guard** — reduces complexity and size, favors clarity.
* **TDD Architect** — drives red/green/refactor and coverage thresholds.

## TDD Proof Ledger

Emit a test-run proof artifact:

```bash
python -m src.services.messaging_cli --hard-onboarding --mode quality-suite --proof --yes
```

Writes JSON to `runtime/quality/proofs/tdd/proof-<UTCSTAMP>.json`:

```json
{
  "schema": "tdd_proof/v1",
  "timestamp_utc": "20250906-000000",
  "git_commit": "abc123...",
  "mode": "quality-suite",
  "roles": {"Agent-1":"SOLID", "...":"..."},
  "pytest_available": true,
  "pytest_exit_code": 0,
  "tests": {"passed": 42, "failed": 0, "errors": 0, "skipped": 3},
  "duration_sec": 2.317
}
```

If `pytest` is unavailable, the artifact still records `pytest_available: false` with notes.

## Hard Onboarding (Safe, Reversible)

Run a full reset + forced re-onboarding across agents. **High risk** — creates backups and prompts for confirmation.

### Usage

```bash
python -m src.services.messaging_cli --hard-onboarding
python -m src.services.messaging_cli --hard-onboarding --yes
python -m src.services.messaging_cli --hard-onboarding --dry-run
python -m src.services.messaging_cli --hard-onboarding --agents Agent-1,Agent-2 --yes
python -m src.services.messaging_cli --hard-onboarding --timeout 45 --yes
```

### Output (example)

```
🚨 HARD ONBOARDING SEQUENCE INITIATED 🚨
🔄 Resetting all agent statuses...
🗑️ Clearing previous onboardings...
⚡ Sending force onboarding to all agents...
✅ Agent-1: Hard onboarding successful
❌ Agent-2: Hard onboarding failed
📊 Hard onboarding complete: 1/2 agents successfully onboarded
🔒 System synchronized and compliant
```

### Safety Features

* **Creates backup** to `runtime/backups/hard_onboarding/<UTCSTAMP>/`
* **Confirmation prompt** before proceeding (unless `--yes` specified)
* **`--dry-run` mode** performs no writes
* **Rollback capability** if all agents fail
* **Exit codes**: `0=all ok`, `2=partial`, `1=abort/failure`

### Technical Implementation

The hard onboarding sequence includes:

1. **Mouse Navigation**: Click onboarding coordinates
2. **New Tab Creation**: Press Ctrl+N for new tab/window
3. **Position Validation**: Verify mouse at correct coordinates
4. **Auto-correction**: Navigate and retry if position invalid
5. **Message Delivery**: Paste onboarding message and send

### Error Handling

* PyAutoGUI availability check
* Coordinate validation
* Mouse position verification
* Timeout handling
* Rollback on catastrophic failure

### Warning

Hard onboarding is a **high-risk operation** that resets agent states. Always use `--dry-run` first and ensure backups are created. Only use when necessary for system recovery or initial setup.
