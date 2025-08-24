## 2) Environment & Tools (v1.1)
- Runtime: Python 3.11+ (stdlib-only unless `requirements.txt` is added).
- **Environment Setup**: If `scripts/env_setup.sh` (Linux/macOS) or `scripts/env_setup.ps1` (Windows) exists, RUN it during environment initialization.
  - Python: install with `pip install -r requirements.txt` if file exists.
  - Node: run `npm ci` if `package-lock.json` exists; else `pnpm i --frozen-lockfile`.
  - Go: `go mod download` if `go.mod` exists.
- **Artifacts**: write to `artifacts/<run_id>/` (findings.json, report.json, policy.json, run.meta.json, manifest.json).

## 3) Network Policy
- **Setup phase**: Internet allowed for dependency installation.
- **Task execution**: Assume **NO internet** unless this environment explicitly enables it.
- If enabled, restrict to allowlist domains only (e.g., `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`, `github.com`).

## 4) Source-of-Truth & Branching
- Never push to `main` directly; open a PR from a feature branch.
- PR must include: validator logs, artifact fingerprints (from `manifest.json`), risks & rollback.

## 6) Cross-Task State
- READ `.codex/state.json` & `.codex/handoff.json` before edits.
- After task, WRITE both with `{task_id, files_touched[], tests[], status}` and `{summary, decisions, risks, next_steps}`.

## 9) Commands to Run Every Task (unchanged)
1) `python scripts/validate_flows.py`
2) `python scripts/validate_agents_doc.py`
3) `python -c "from impl.core.orchestrator import run; import json; print(json.dumps(run('.')))"`  # capture run_dir
4) `python scripts/validate_artifacts.py <run_dir>`
