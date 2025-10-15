# Lean Excellence Framework Implementation Plan

## Objectives

- Establish `STANDARDS.md` at repo root as single source of truth for code quality and process rules.
- Provide durable, minimal templates for compact and full cycle reports and onboarding.
- Simplify and centralize reporting standards in `STANDARDS.md` and reference it from core docs.
- Patch service and messaging code to use new lean templates by default.
- Update README with link to new standards and enforce soft file-size cap in CI.

## Proposed Changes

1. **STANDARDS.md** (repo root)
   - Create file with code quality and process rules (≤500 preferred, ≤600 soft cap; single mission summary; compact/full cycle formats; base points only).

2. **Messaging Templates** (`templates/messaging/`)
   - Add `compact_cycle.md`, `full_cycle.md`, `onboarding_min.md` per provided drafts.

3. **docs/CYCLE_TIMELINE.md**
   - Patch usage guidelines header to reference `STANDARDS.md` and compact/full policy.

4. **soft_onboarding_service.py**
   - Replace `SESSION_CLEANUP_MESSAGE` with compact cycle template; add `ONBOARDING_MIN_TEMPLATE`.

5. **messaging_pyautogui.py**
   - Replace verbose C2A formatter with compact `format_c2a_message` requiring minimal fields.

6. **README.md**
   - Under "Quality Standards" section, add link to `STANDARDS.md`.

7. **Tests & CI**
   - Add unit tests for compact formatter (happy path, missing fields)
   - Update pre-commit or CI config to warn/error if any file >600 lines.

## Implementation Todos

### To-dos

- [ ] Create `STANDARDS.md` at repo root with Lean Excellence standards
- [ ] Create messaging templates directory `templates/messaging/` and add `compact_cycle.md`, `full_cycle.md`, `onboarding_min.md`
- [ ] Patch `docs/CYCLE_TIMELINE.md` header to reference `STANDARDS.md` and enforce compact/full policy
- [ ] Patch `src/services/soft_onboarding_service.py` to use new compact `SESSION_CLEANUP_MESSAGE` and add `ONBOARDING_MIN_TEMPLATE`
- [ ] Patch `src/services/messaging_pyautogui.py` to implement the lean compact C2A formatter
- [ ] Update `README.md` to add link to `STANDARDS.md` under Quality Standards
- [ ] Add unit tests for the new `format_c2a_message` (happy path and missing fields)
- [ ] Update pre-commit or CI config to enforce soft file-size cap (≤600 lines)
- [ ] Agent-4 to announce adoption of Lean Excellence Framework swarm-wide

