import json, os, collections

def summarize(findings):
    by_rule = collections.Counter(f["rule_id"] for f in findings)
    top = [{"rule_id": r, "count": c, "severity": "unknown"} for r,c in by_rule.most_common(5)]
    return {
        "targets_scanned": len(set(f["target_id"] for f in findings)) if findings else 0,
        "findings_total": len(findings),
        "top_risks": top,
        "recommendations": [
            "Review TLS configuration and disable legacy cipher suites.",
            "Add missing security headers (CSP, HSTS) where applicable."
        ]
    }

def write_report(run_dir, run_id, kept, dropped, metadata):
    os.makedirs(run_dir, exist_ok=True)
    rep = {"run_id": run_id, **summarize(kept)}
    rep["dropped_count"] = len(dropped)
    rep["drop_reasons_topK"] = []
    # Write JSON
    with open(os.path.join(run_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    # Write MD (minimal)
    with open(os.path.join(run_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write(f"# Security Suite Report\n\nRun: {run_id}\n\n")
        f.write(f"Findings total: {rep['findings_total']}\n\nTop risks:\n")
        for t in rep["top_risks"]:
            f.write(f"- {t['rule_id']} × {t['count']}\n")
    return rep