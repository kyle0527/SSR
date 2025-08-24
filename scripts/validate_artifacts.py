import json, sys, pathlib

REQUIRED_FINDING_FIELDS = {"id","target_id","rule_id","severity","confidence","location","scanner","ts"}
REQUIRED_REPORT_FIELDS = {"run_id","targets_scanned","findings_total","top_risks","recommendations"}
REQUIRED_RUNMETA_FIELDS = {"run_id","flow_version","start_ts","end_ts","exit_code"}

def _load(p): 
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def validate_findings(p):
    arr = _load(p)
    assert isinstance(arr, list), "findings.json should be a list"
    for i,f in enumerate(arr[:50]):
        missing = REQUIRED_FINDING_FIELDS - set(f)
        assert not missing, f"finding[{i}] missing: {missing}"

def validate_report(p):
    obj = _load(p)
    missing = REQUIRED_REPORT_FIELDS - set(obj)
    assert not missing, f"report.json missing: {missing}"

def validate_runmeta(p):
    obj = _load(p)
    missing = REQUIRED_RUNMETA_FIELDS - set(obj)
    assert not missing, f"run.meta.json missing: {missing}"

if __name__ == "__main__":
    run_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not run_dir:
        print("usage: python scripts/validate_artifacts.py artifacts/<run_id>", file=sys.stderr); sys.exit(1)
    validate_findings(run_dir / "findings.json")
    validate_report(run_dir / "report.json")
    validate_runmeta(run_dir / "run.meta.json")
    print("artifacts validation: OK")