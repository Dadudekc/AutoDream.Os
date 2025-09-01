# 🚀 Agent Cellphone V2 — Messaging System Flags Guide (Authoritative Reference)

> **Scope:** CLI interface for `src/services/messaging_cli` (23 flags).  
> **Audience:** Operators, Captain Agent-4, Background Processors.  
> **Contract:** Zero-message-loss, deterministic ordering (priority → FIFO), cross-platform locks.

---

## 0) TL;DR (90s)

- Choose **who**: `--agent Agent-7` **or** `--bulk` (mutually exclusive).
- Choose **what**: `--message "..."` (required for standard sends).
- Choose **how fast**: `--priority urgent` **or** `--high-priority` (override).
- Choose **how to deliver**: `--mode pyautogui | inbox`.
- Queue ops: `--queue-stats`, `--process-queue`, `--start-queue-processor`, `--stop-queue-processor`.

---

## 1) Synopsis

```bash
python -m src.services.messaging_cli [RECIPIENT] [CONTENT] [PROPS] [MODE] [UTILS] [QUEUE] [ONBOARDING] [TASKS]
```

* **RECIPIENT**: `--agent <NAME>` | `--bulk`
* **CONTENT**: `--message/-m <TEXT>` | `--sender/-s <NAME>`
* **PROPS**: `--type/-t <text|broadcast|onboarding>` | `--priority/-p <regular|urgent>` | `--high-priority`
* **MODE**: `--mode <pyautogui|inbox>` | `--no-paste` | `--new-tab-method <ctrl_t|ctrl_n>`
* **UTILS**: `--list-agents` | `--coordinates` | `--history` | `--check-status`
* **QUEUE**: `--queue-stats` | `--process-queue` | `--start-queue-processor` | `--stop-queue-processor`
* **ONBOARDING**: `--onboarding` | `--onboard` (requires `--agent`) | `--onboarding-style <friendly|professional>`
* **TASKS**: `--get-next-task` (requires `--agent`) | `--wrapup` (bulk-only)

---

## 2) Flag Catalogue (23 Flags)

### 2.1 Message Content

| Flag        | Short | Type | Default           | Notes                       |
| ----------- | ----- | ---- | ----------------- | --------------------------- |
| `--message` | `-m`  | str  | (none)            | Required for standard sends |
| `--sender`  | `-s`  | str  | `Captain Agent-4` | Who authored the message    |

### 2.2 Recipient Selection

| Flag      | Short | Type | Default | Notes             |
| --------- | ----- | ---- | ------- | ----------------- |
| `--agent` | `-a`  | str  | (none)  | Target one agent  |
| `--bulk`  | —     | bool | false   | Target all agents |

### 2.3 Message Properties

| Flag              | Short | Type | Default   | Notes                                     |           |              |
| ----------------- | ----- | ---- | --------- | ----------------------------------------- | --------- | ------------ |
| `--type`          | `-t`  | enum | `text`    | \`text                                    | broadcast | onboarding\` |
| `--priority`      | `-p`  | enum | `regular` | \`regular                                 | urgent\`  |              |
| `--high-priority` | —     | bool | false     | Force `urgent` regardless of `--priority` |           |              |

### 2.4 Delivery Mode

| Flag               | Short | Type | Default     | Notes                        |                            |
| ------------------ | ----- | ---- | ----------- | ---------------------------- | -------------------------- |
| `--mode`           | —     | enum | `pyautogui` | \`pyautogui                  | inbox\`                    |
| `--no-paste`       | —     | bool | false       | Only when `--mode pyautogui` |                            |
| `--new-tab-method` | —     | enum | `ctrl_t`    | \`ctrl\_t                    | ctrl\_n\` (pyautogui only) |

### 2.5 Utility / Info

| Flag             | Type | Notes                      |
| ---------------- | ---- | -------------------------- |
| `--list-agents`  | bool | Roster                     |
| `--coordinates`  | bool | PyAutoGUI XY map           |
| `--history`      | bool | Delivery audit             |
| `--check-status` | bool | Agent and contracts health |

### 2.6 Queue Management

| Flag                      | Type | Notes                               |
| ------------------------- | ---- | ----------------------------------- |
| `--queue-stats`           | bool | Pending/processing/delivered/failed |
| `--process-queue`         | bool | One batch now                       |
| `--start-queue-processor` | bool | Continuous background               |
| `--stop-queue-processor`  | bool | Stop background loop                |

### 2.7 Onboarding

| Flag                 | Type | Notes                             |                                          |
| -------------------- | ---- | --------------------------------- | ---------------------------------------- |
| `--onboarding`       | bool | All agents (bulk)                 |                                          |
| `--onboard`          | bool | Single agent (requires `--agent`) |                                          |
| `--onboarding-style` | enum | \`friendly                        | professional\` (affects onboarding only) |

### 2.8 Contract / Task

| Flag              | Type | Notes                                   |
| ----------------- | ---- | --------------------------------------- |
| `--get-next-task` | bool | Requires `--agent`                      |
| `--wrapup`        | bool | Bulk closure (conflicts with `--agent`) |

**Total:** 23 flags.

---

## 3) Precedence, Dependencies, Conflicts

### 3.1 Mutual Exclusions

* `--agent` **XOR** `--bulk`
* `--onboarding` **XOR** `--agent`
* `--wrapup` **XOR** `--agent`

### 3.2 Dependencies

* `--get-next-task` ➜ **requires** `--agent`
* `--onboard` ➜ **requires** `--agent`
* `--no-paste` ➜ **valid only if** `--mode pyautogui`
* `--new-tab-method` ➜ **valid only if** `--mode pyautogui`

### 3.3 Priority Rules

* `--high-priority` **overrides** `--priority` to `urgent` globally.
* Queue ordering: **priority\_score desc → created\_at asc** (FIFO within same priority).

---

## 4) Exit Codes & Operator Feedback

| Code | Meaning                   | Action                                       |
| ---- | ------------------------- | -------------------------------------------- |
| `0`  | Success                   | —                                            |
| `2`  | Invalid flags/combination | Show remediation hint                        |
| `3`  | Dependency missing        | Print required companion flag                |
| `4`  | Mode mismatch             | Remove pyautogui-only flags or switch mode   |
| `7`  | Lock timeout              | Message queued; advise queue status          |
| `8`  | Queue full                | Reject with remediation (process or enlarge) |
| `9`  | Internal error            | Inspect logs with correlation ID             |

**Standard Error Format (JSON line):**

```json
{"level":"error","code":2,"msg":"Cannot combine --agent with --bulk","hint":"Use either --agent <NAME> OR --bulk","corr":"ab12-..."}
```

---

## 5) Config & Environment

**Precedence (high → low):** CLI flags → ENV → config file → defaults

* **ENV:**

  * `AC_MODE=pyautogui|inbox`
  * `AC_SENDER="Captain Agent-4"`
  * `AC_NEW_TAB_METHOD=ctrl_t|ctrl_n`
* **Config (YAML):** `config/messaging.yml`

```yaml
defaults:
  sender: "Captain Agent-4"
  mode: "pyautogui"
  new_tab_method: "ctrl_t"
  priority: "regular"
  paste: true
```

---

## 6) Validation Matrix (Fast Reference)

| Scenario                  | Valid? | Why                | Correction                                   |
| ------------------------- | ------ | ------------------ | -------------------------------------------- |
| `--agent A --bulk`        | ❌      | Mutual exclusion   | Choose one                                   |
| `--get-next-task`         | ❌      | Missing dependency | Add `--agent A`                              |
| `--mode inbox --no-paste` | ⚠️     | Ignored flag       | Remove `--no-paste` or switch to `pyautogui` |
| `--onboarding --agent A`  | ❌      | Bulk-only          | Use `--onboard --agent A`                    |
| `--wrapup --agent A`      | ❌      | Bulk-only          | Drop `--agent`                               |

---

## 7) Golden Recipes (Copy-Paste)

### 7.1 Single Agent, Urgent

```bash
python -m src.services.messaging_cli \
  --agent Agent-7 -m "Hotfix now" --high-priority --type text --mode inbox
```

### 7.2 System Broadcast (Professional Onboarding)

```bash
python -m src.services.messaging_cli \
  --onboarding --onboarding-style professional
```

### 7.3 Bulk Ops with GUI Isolation (New Window)

```bash
python -m src.services.messaging_cli \
  --bulk -m "Deploy @ 14:00 UTC" --type broadcast \
  --mode pyautogui --new-tab-method ctrl_n
```

### 7.4 Queue Operations (Continuous)

```bash
python -m src.services.messaging_cli --queue-stats
python -m src.services.messaging_cli --start-queue-processor
# ...later
python -m src.services.messaging_cli --stop-queue-processor
```

### 7.5 Contract Pull

```bash
python -m src.services.messaging_cli --agent Agent-7 --get-next-task
```

---

## 8) Output Contracts

### 8.1 `--queue-stats` (JSON)

```json
{
  "pending": 5,
  "processing": 2,
  "delivered": 123,
  "failed": 1,
  "oldest_pending": "2025-09-01T10:30:00",
  "newest_pending": "2025-09-01T11:15:00",
  "corr": "b4e1-..."
}
```

### 8.2 `--check-status` (Table/JSON)

* Per-agent `status.json` merged; includes last heartbeat, contract count, last error, version.

---

## 9) Bash/Zsh Autocomplete (Optional)

```bash
# _messaging_cli
_messaging_cli() {
  local -a opts
  opts=(
    --message -m --sender -s
    --agent -a --bulk
    --type -t --priority -p --high-priority
    --mode --no-paste --new-tab-method
    --list-agents --coordinates --history --check-status
    --queue-stats --process-queue --start-queue-processor --stop-queue-processor
    --onboarding --onboard --onboarding-style
    --get-next-task --wrapup
  )
  COMPREPLY=( $(compgen -W "${opts[*]}" -- "${COMP_WORDS[COMP_CWORD]}") )
}
complete -F _messaging_cli messaging_cli
```

---

## 10) Operator Playbook (Do/Don't)

**Do**

* Use `--high-priority` sparingly (true emergencies).
* Prefer `--mode inbox` on unstable GUI hosts.
* Run exactly one background processor per node.

**Don't**

* Mix `--agent` with bulk flags (`--bulk|--onboarding|--wrapup`).
* Pass pyautogui-only flags when `--mode inbox`.
* Spam `urgent` for routine ops (devalues priority heap).

---

## 11) Troubleshooting (First Response)

| Symptom                        | Likely Cause    | Fast Fix                               |
| ------------------------------ | --------------- | -------------------------------------- |
| Message "sent" but not visible | GUI focus lost  | Switch to `--mode inbox`               |
| Long delays                    | Lock contention | Check `--queue-stats`, start processor |
| Duplicate delivery             | Processor race  | Ensure single processor / verify locks |
| CLI rejected                   | Flag conflict   | Re-run with `--help`, see §3 matrix    |

---

## 12) FAQ

* **Q:** Does `--high-priority` change message type?
  **A:** No. It only overrides urgency, not category.

* **Q:** Is ordering guaranteed globally?
  **A:** Deterministic per target inbox (priority → FIFO). Global order is not defined across all agents.

* **Q:** What if queue is full?
  **A:** Exit `8`. Increase capacity or drain with `--process-queue` / background processor.

---

**Version:** 2.0 • **Maintainer:** Captain Agent-4 • **Contract:** Zero-loss, deterministic per-inbox ordering
