# V2 Compliance Exceptions

This document lists approved exceptions to strict V2 limits for critical system components where comprehensive, cohesive implementations are required for reliability, UX, or operational control.

## Discord Commander System (Approved)
- Approved By: Captain Agent-4
- Date: 2025-10-06
- Scope: `src/services/discord_commander/**`
- Rationale: Critical operator interface and orchestration layer; strict per-file line limits would degrade reliability, discoverability, and UX for interactive Discord views and command registration.
- Guardrails:
  - Maintain readability and modular structure; exceed limits only when cohesion/UX require it.
  - Keep robust logging and clear error handling.
  - Secure env-based token handling; no secrets in repo.
  - Manual run validation remains required; smoke tests added where feasible.
- Review Cadence: Weekly quick review; monthly deep-dive; API-change-triggered review.
- Status: Active
