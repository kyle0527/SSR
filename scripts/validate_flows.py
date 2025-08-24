import json, sys, pathlib

def main():
    repo = pathlib.Path(".")
    p = repo / "impl" / "flows" / "scan_and_report.yaml"
    if not p.exists():
        print("scan_and_report.yaml not found", file=sys.stderr)
        sys.exit(1)
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "flow should be an object"
    assert "targets" in data and isinstance(data["targets"], list) and data["targets"], "flow.targets must be a non-empty list"
    print("validate_flows: OK")

if __name__ == "__main__":
    main()