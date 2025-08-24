import os, json, time, hashlib, pathlib
from .stop_policy import StopPolicy
from .guards import filter_findings
from .errors import ContractViolation, StopSignal
from ..scanner.engine import scan as scan_engine
from ..ui.reports import write_report

def _read_json_yaml_as_json(path: str) -> dict:
    # Accept JSON content even if file suffix is .yaml
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read().strip()
    return json.loads(txt or "{}")

def _load_flow(repo_root: str) -> dict:
    p = os.path.join(repo_root, "impl", "flows", "scan_and_report.yaml")
    if os.path.exists(p):
        return _read_json_yaml_as_json(p)
    return {"version": "v1", "targets": []}

def _load_toggles(repo_root: str) -> dict:
    # Try JSON first (optional), fall back to defaults
    p_json = os.path.join(repo_root, "config", "toggles.json")
    if os.path.exists(p_json):
        with open(p_json, "r", encoding="utf-8") as f:
            return json.load(f)
    # Fallback defaults (no external YAML deps)
    return {
        "STOP_POLICY": {
            "max_consecutive_errors": 3,
            "max_runtime_seconds": 900,
            "per_target_timeout_seconds": 60,
            "fail_fast": True,
            "max_drop_ratio": 0.5,
        },
        "GUARDS": {
            "required_fields": ["id","target_id","rule_id","severity","confidence","location","scanner","ts"],
            "accepted_severity": ["low","medium","high","critical"],
            "min_confidence": 0.6,
            "usefulness": {"min_usefulness_score": 0.5, "weights": {"severity":0.5,"confidence":0.3,"evidence_quality":0.2}}
        }
    }

def _run_id():
    t = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    return f"{t}_{hashlib.sha1(str(time.time()).encode()).hexdigest()[:6]}"

def run(repo_root: str | None = None):
    repo_root = repo_root or os.getcwd()
    flow = _load_flow(repo_root)
    toggles = _load_toggles(repo_root)
    policy = StopPolicy(**toggles.get("STOP_POLICY", {}))
    targets = flow.get("targets") or [{"target_id": "demo", "address": "https://example.com"}]

    run_id = _run_id()
    run_dir = os.path.join(repo_root, "artifacts", run_id)
    os.makedirs(os.path.join(run_dir, "validation"), exist_ok=True)
    os.makedirs(os.path.join(run_dir, "diagnostics"), exist_ok=True)

    kept_all, dropped_all = [], []
    for t in targets:
        try:
            raw = scan_engine(t, flow, toggles, timeout=policy.per_target_timeout_seconds)
            kept, dropped = filter_findings(raw, toggles.get("GUARDS", {}))
            kept_all.extend(kept); dropped_all.extend(dropped)
            policy.on_batch_result(len(kept), len(dropped))
            stop, reason = policy.should_stop()
            if stop:
                with open(os.path.join(run_dir, "diagnostics", "last_error.json"), "w", encoding="utf-8") as f:
                    json.dump({"reason": reason, "target": t}, f, indent=2)
                raise StopSignal(reason)
            policy.on_success()
        except Exception as e:
            policy.on_error()
            with open(os.path.join(run_dir, "diagnostics", "last_error.json"), "w", encoding="utf-8") as f:
                json.dump({"error": str(e), "target": t}, f, indent=2)
            if toggles.get("STOP_POLICY", {}).get("fail_fast", True):
                break

    # Write findings
    with open(os.path.join(run_dir, "findings.json"), "w", encoding="utf-8") as f:
        json.dump(kept_all, f, ensure_ascii=False, indent=2)

    # Write policy + run meta + manifest
    policy_json = {
        "kept": len(kept_all), "dropped": len(dropped_all),
        "max_runtime_seconds": policy.max_runtime_seconds,
        "max_consecutive_errors": policy.max_consecutive_errors,
        "max_drop_ratio": policy.max_drop_ratio
    }
    with open(os.path.join(run_dir, "policy.json"), "w", encoding="utf-8") as f:
        json.dump(policy_json, f, indent=2)

    meta = {
        "run_id": run_id,
        "flow_version": flow.get("version", "v1"),
        "start_ts": None,
        "end_ts": None,
        "exit_code": 0
    }
    with open(os.path.join(run_dir, "run.meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    # Report
    rep = write_report(run_dir, run_id, kept_all, dropped_all, meta)

    # Manifest
    manifest = {
        "run_id": run_id,
        "files": []
    }
    for fn in ["findings.json", "report.json", "report.md", "policy.json", "run.meta.json"]:
        p = os.path.join(run_dir, fn)
        if os.path.exists(p):
            manifest["files"].append({"path": fn, "sha256": hashlib.sha256(open(p,"rb").read()).hexdigest(), "bytes": os.path.getsize(p)})
    with open(os.path.join(run_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return {"run_dir": run_dir, "kept": len(kept_all), "dropped": len(dropped_all)}

if __name__ == "__main__":
    out = run()
    print(json.dumps(out, indent=2))