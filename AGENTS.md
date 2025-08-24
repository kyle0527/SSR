# AGENTS.md — Security Suite Agent Contract

## Commands to run every cycle
- pytest -q
- python scripts/validate_flows.py
- python scripts/validate_agents_doc.py
- (optional) python scripts/validate_artifacts.py artifacts/<run_id>

## Acceptance gates (all required)
1) Golden path passes (orchestrator demo run succeeds).
2) Flow/schema: impl/flows/scan_and_report.yaml (JSON content) is valid.
3) Docs parity (agents/doc validator passes).

## Cross-task state (required)
- Before edits, READ `.codex/state.json` and `.codex/handoff.json` if present.
- After completing a task, WRITE:
  - `.codex/handoff.json` with {task_id, summary, decisions, risks, next_steps}
  - Append `.codex/state.json` with {task_id, files_touched[], tests[], status}